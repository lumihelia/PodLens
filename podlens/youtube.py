"""YouTube caption fetching via yt-dlp.

Turns a YouTube URL into a timestamped transcript string in the same shape the
rest of the pipeline already expects:

    [12:34] some spoken line
    [12:38] the next line

We shell out to yt-dlp, the actively-maintained downloader, because YouTube now
blocks lighter caption-scraping approaches. yt-dlp downloads only the subtitle
track (never the video), and we parse its WebVTT output.

If YouTube throws bot-checks (HTTP 429 / "Sign in to confirm"), set
PODLENS_COOKIES_FROM_BROWSER (e.g. "chrome", "safari", "firefox") so yt-dlp can
use your logged-in browser cookies. That is the documented fix for IP/bot blocks.

The interpretation core is untouched -- this is just an input adapter. We fetch
captions in their original language (the interpretation translates to the
configured output language anyway).
"""

import glob
import os
import re
import subprocess
import sys
import tempfile

from .transcript import parse_subtitles

# Capture the 11-character video id from the common YouTube URL shapes.
_ID_PATTERNS = [
    re.compile(r"youtu\.be/([0-9A-Za-z_-]{11})"),
    re.compile(r"[?&]v=([0-9A-Za-z_-]{11})"),
    re.compile(r"youtube\.com/embed/([0-9A-Za-z_-]{11})"),
    re.compile(r"youtube\.com/shorts/([0-9A-Za-z_-]{11})"),
    re.compile(r"youtube\.com/live/([0-9A-Za-z_-]{11})"),
]

# Default subtitle language preference. Override with PODLENS_SUB_LANGS.
_DEFAULT_SUB_LANGS = "en.*,en"


def is_youtube_url(source: str) -> bool:
    """Whether `source` is a YouTube URL we can extract a video id from."""
    s = source.strip()
    if "youtube.com" not in s and "youtu.be" not in s:
        return False
    return extract_video_id(s) is not None


def extract_video_id(source: str) -> str | None:
    """Pull the 11-char video id out of a YouTube URL, or None."""
    s = source.strip()
    for pattern in _ID_PATTERNS:
        match = pattern.search(s)
        if match:
            return match.group(1)
    return None


def _build_command(url: str, out_template: str) -> list[str]:
    sub_langs = os.getenv("PODLENS_SUB_LANGS", _DEFAULT_SUB_LANGS).strip()
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--skip-download",
        # YouTube now forces SABR streaming, so video-format resolution can
        # fail; without this flag yt-dlp aborts before writing the subtitles
        # we actually want. We never download media, so missing formats are fine.
        "--ignore-no-formats-error",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", sub_langs,
        "--sub-format", "vtt",
        "--no-playlist",
        "--retries", "5",
        "-o", out_template,
    ]
    cookies_browser = os.getenv("PODLENS_COOKIES_FROM_BROWSER", "").strip()
    if cookies_browser:
        cmd += ["--cookies-from-browser", cookies_browser]
    # Optionally impersonate a real browser's TLS fingerprint to dodge bot
    # blocks. OFF by default because it requires a working curl_cffi backend;
    # if the target is unavailable, yt-dlp aborts. Turn on with
    # PODLENS_IMPERSONATE=chrome only when impersonate targets are available
    # (check: python -m yt_dlp --list-impersonate-targets).
    impersonate = os.getenv("PODLENS_IMPERSONATE", "").strip()
    if impersonate:
        cmd += ["--impersonate", impersonate]
    cmd.append(url)
    return cmd


def fetch_transcript(source: str) -> str:
    """Fetch a YouTube video's captions as a timestamped transcript string."""
    video_id = extract_video_id(source)
    if video_id is None:
        raise RuntimeError(f"Could not find a YouTube video id in: {source}")

    with tempfile.TemporaryDirectory() as tmp:
        out_template = os.path.join(tmp, "%(id)s.%(ext)s")
        cmd = _build_command(source, out_template)
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=180
            )
        except FileNotFoundError:
            raise RuntimeError(
                "yt-dlp is not installed. Run: pip install yt-dlp "
                "(or re-run setup.sh)."
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Fetching captions timed out after 180s.")

        vtt_files = sorted(glob.glob(os.path.join(tmp, "*.vtt")))
        if not vtt_files:
            raise RuntimeError(_diagnose(proc.stderr))

        # Prefer a manual track over an auto-generated one when both exist.
        manual = [f for f in vtt_files if ".auto." not in f and "-auto" not in f]
        chosen = (manual or vtt_files)[0]
        with open(chosen, encoding="utf-8") as fh:
            vtt_text = fh.read()

    transcript = parse_subtitles(vtt_text)
    if not transcript:
        raise RuntimeError("Captions were downloaded but parsed empty.")
    return transcript


def _diagnose(stderr: str) -> str:
    """Turn yt-dlp stderr into a plain-language, actionable error."""
    s = (stderr or "").lower()
    if "429" in s or "too many requests" in s or "sign in to confirm" in s:
        return (
            "YouTube is rate-limiting or bot-checking this network. Fix: set "
            "PODLENS_COOKIES_FROM_BROWSER=chrome (or safari/firefox) to use your "
            "browser's login, then retry. Or wait a while and retry. Or paste "
            "the transcript directly."
        )
    if "no subtitles" in s or "there are no subtitles" in s:
        return (
            "This video has no captions in the requested language. Try setting "
            "PODLENS_SUB_LANGS (e.g. 'zh.*,en.*,.*'), or paste a transcript."
        )
    if (
        "private video" in s
        or "video unavailable" in s
        or "video is unavailable" in s
        or "no longer available" in s
        or "members-only" in s
        or "removed by the user" in s
    ):
        return "This video is private or unavailable, so captions can't be fetched."
    # Fall back to the last meaningful stderr line.
    last = [ln for ln in (stderr or "").splitlines() if ln.strip()]
    tail = last[-1] if last else "unknown error"
    return f"Could not fetch captions via yt-dlp: {tail}"
