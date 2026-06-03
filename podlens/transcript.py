"""Transcript loading, subtitle parsing, and light cleaning.

We deliberately do NOT over-clean. The goal is to remove obvious noise
(duplicate blank lines, stray markup) while preserving timestamps,
speaker turns, hesitation and emphasis that reveal how the speaker thinks.

Subtitle files (.srt / .vtt) and YouTube captions are normalized into the
shape the rest of the pipeline expects:

    [12:34] some spoken line
    [12:38] the next line
"""

import re
from pathlib import Path

# Matches common timestamp forms: [00:00], (1:23:45), 00:00, 1:23:45
TIMESTAMP_RE = re.compile(r"[\[\(]?\b\d{1,2}:\d{2}(?::\d{2})?\b[\]\)]?")

# A subtitle cue time line, e.g. "00:00:20,000 --> 00:00:24,960" (SRT, comma)
# or "00:00:20.000 --> 00:00:24.960" (VTT, dot). Captures the start time.
_CUE_RE = re.compile(
    r"(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s*-->\s*"
    r"\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3}"
)
# Inline VTT styling/timing tags like <00:00:01.200><c> ... </c>
_TAG_RE = re.compile(r"<[^>]+>")


def load_transcript(source: str) -> str:
    """Load a transcript from a file path, or treat the string as raw text.

    Subtitle files (.srt / .vtt) and subtitle-shaped text are parsed into
    timestamped lines. Anything else is treated as a plain transcript and
    only lightly cleaned.
    """
    if _looks_like_path(source):
        text = Path(source).read_text(encoding="utf-8")
    else:
        text = source

    if _is_subtitle(text):
        return parse_subtitles(text)
    return clean_transcript(text)


def _looks_like_path(source: str) -> bool:
    """Whether `source` points to a readable file.

    A long blob of transcript text passed directly (or via stdin) is not a
    path. `Path.exists()` raises OSError on over-long names rather than
    returning False, so we guard against that and treat any failure as
    "this is raw text, not a file".
    """
    try:
        return Path(source).is_file()
    except OSError:
        return False


def _is_subtitle(text: str) -> bool:
    """Whether the text looks like SRT/VTT (has cue time ranges)."""
    return bool(_CUE_RE.search(text))


def _format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"[{h}:{m:02d}:{s:02d}]"
    return f"[{m:02d}:{s:02d}]"


def _cue_time_to_seconds(stamp: str) -> float:
    # stamp like "00:01:02,500" (SRT) or "01:02.500" (VTT)
    parts = stamp.replace(",", ".").split(":")
    nums = [float(p) for p in parts]
    while len(nums) < 3:
        nums.insert(0, 0.0)
    h, m, s = nums
    return h * 3600 + m * 60 + s


def parse_subtitles(text: str) -> str:
    """Parse SRT/VTT into '[mm:ss] text' lines.

    Multi-line cue text is joined into one line. Inline VTT tags are stripped.
    Rolling-caption duplicates (auto-generated YouTube subs repeat lines as they
    scroll) are de-duplicated so each distinct line appears once, anchored to
    the timestamp where it first appears.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out: list[str] = []
    seen_recent: list[str] = []
    current_start: float | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if current_start is not None and buffer:
            joined = _TAG_RE.sub("", " ".join(buffer))
            joined = re.sub(r"\s+", " ", joined).strip()
            if joined and joined not in seen_recent:
                out.append(f"{_format_timestamp(current_start)} {joined}")
                seen_recent.append(joined)
                if len(seen_recent) > 8:
                    seen_recent.pop(0)
        buffer = []

    for raw in text.split("\n"):
        line = raw.strip()
        cue = _CUE_RE.search(line)
        if cue:
            flush()
            current_start = _cue_time_to_seconds(cue.group(1))
            continue
        if not line:
            flush()
            continue
        if line.upper().startswith(("WEBVTT", "KIND:", "LANGUAGE:")):
            continue
        if line.isdigit():  # SRT cue index
            continue
        buffer.append(line)
    flush()

    return "\n".join(out).strip()


def clean_transcript(text: str) -> str:
    """Light cleaning: normalize whitespace, drop empty repeated lines.

    Preserves timestamps, speaker labels, and meaningful content as-is.
    """
    # Normalize line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing whitespace per line.
    lines = [line.rstrip() for line in text.split("\n")]
    # Collapse 3+ blank lines into a single blank line.
    cleaned: list[str] = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                cleaned.append("")
        else:
            blank_run = 0
            cleaned.append(line)
    return "\n".join(cleaned).strip()


def has_timestamps(text: str) -> bool:
    """Whether the transcript appears to carry timestamps for evidence linking."""
    return bool(TIMESTAMP_RE.search(text))


_CJK_RE = re.compile(r"[一-鿿]")
_LATIN_RE = re.compile(r"[A-Za-z]")


def detect_language(text: str) -> str:
    """Best-effort source-language detection: 'zh' or 'en'.

    Used to interpret each episode in its OWN language first (most faithful),
    then translate to the other. Heuristic: if there is a meaningful amount of
    Chinese relative to Latin letters, call it Chinese; otherwise English.
    Defaults to 'en' (PodLens's typical input is English podcasts).
    """
    sample = text[:6000]
    cjk = len(_CJK_RE.findall(sample))
    latin = len(_LATIN_RE.findall(sample))
    # Substantial CJK, and not overwhelmingly Latin -> Chinese.
    if cjk >= 20 and cjk * 4 >= latin:
        return "zh"
    return "en"
