"""PodLens command-line interface.

Usage:
    python -m podlens transcript.txt
    python -m podlens transcript.txt -o out.md
    python -m podlens transcript.txt --no-profile
    python -m podlens transcript.txt --dry-run
    cat transcript.txt | python -m podlens -
"""

import argparse
import sys
from pathlib import Path

from .config import load_config
from .interpreter import build_prompts, interpret
from .profile import load_profile
from .transcript import clean_transcript, load_transcript
from .youtube import fetch_transcript, is_youtube_url


def _read_input(source: str) -> str:
    """Read transcript from a YouTube URL, file path, stdin (-), or raw text."""
    if source == "-":
        return load_transcript(sys.stdin.read())
    if is_youtube_url(source):
        _eprint("Fetching YouTube captions...")
        return clean_transcript(fetch_transcript(source))
    return load_transcript(source)


def _eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="podlens",
        description=(
            "Transcript-grounded podcast interpretation: faithful "
            "reconstruction, then plain language, then personal mapping."
        ),
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="YouTube URL, transcript file path, '-' for stdin, or raw text. "
             "Optional when using --publish-existing or --rebuild-site.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write the Markdown report to this file instead of stdout.",
    )
    parser.add_argument(
        "--title",
        default="PodLens 解读",
        help="Title for the report (default: 'PodLens 解读').",
    )
    parser.add_argument(
        "--no-profile",
        action="store_true",
        help="Skip the personal-mapping layer even if a profile exists.",
    )
    parser.add_argument(
        "--profile",
        help="Path to a profile file (overrides PODLENS_PROFILE).",
    )
    parser.add_argument(
        "--lang",
        help="Output language: zh or en (overrides PODLENS_OUTPUT_LANG).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and print the prompts without calling the API. "
             "Useful to inspect the pipeline or test without a key.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="After interpreting, publish the PUBLIC layers to the static "
             "site + RSS feed in docs/ (personal layers are never published).",
    )
    parser.add_argument(
        "--publish-existing",
        metavar="REPORT.md",
        help="Publish the public layers of an already-saved report file to the "
             "site, without calling the API. Use with --title.",
    )
    parser.add_argument(
        "--rebuild-site",
        action="store_true",
        help="Regenerate the site index/feeds/sitemap from the existing "
             "manifest (no new episode, no API call).",
    )
    parser.add_argument(
        "--date",
        help="Publication date (YYYY-MM-DD) for the published episode. "
             "Defaults to today.",
    )
    parser.add_argument(
        "--source-url",
        help="Original episode URL (e.g. the YouTube link). When it's a "
             "YouTube video, timestamps in the published page become clickable "
             "deep links into the video. Auto-detected if the input is a "
             "YouTube URL.",
    )
    args = parser.parse_args(argv)

    config = load_config()
    if args.lang:
        config.output_lang = args.lang

    # --- Publish-only modes (no interpretation / no API call) ---
    if args.rebuild_site:
        from .publish import load_site_config, rebuild_from_manifest
        n = rebuild_from_manifest(load_site_config())
        _eprint(f"Rebuilt site from manifest ({n} episode(s)).")
        return 0

    if args.publish_existing:
        from .publish import load_site_config, publish_report
        try:
            report_md = Path(args.publish_existing).read_text(encoding="utf-8")
        except OSError as exc:
            _eprint(f"Error reading report: {exc}")
            return 1
        entry = publish_report(report_md, args.title, load_site_config(),
                               date=args.date, source_url=args.source_url)
        _eprint(f"Published public layers -> docs/episodes/{entry['slug']}.html")
        return 0

    if not args.source:
        parser.error("source is required (unless using --publish-existing or --rebuild-site)")

    try:
        transcript = _read_input(args.source)
    except (OSError, RuntimeError) as exc:
        _eprint(f"Error reading transcript: {exc}")
        return 1

    if not transcript.strip():
        _eprint("Error: the transcript is empty.")
        return 1

    profile_path = args.profile or config.profile_path
    profile = None if args.no_profile else load_profile(profile_path)
    if not args.no_profile and profile is None:
        _eprint(
            f"Note: no profile found at '{profile_path}'. "
            "Producing reconstruction + plain language only "
            "(copy profile.example.md to profile.md to enable personal mapping)."
        )

    if args.dry_run:
        prompts = build_prompts(transcript, profile, config.output_lang)
        for name, text in prompts.items():
            print(f"\n{'=' * 70}\nPROMPT: {name}\n{'=' * 70}\n{text}")
        return 0

    try:
        result = interpret(transcript, profile, config, on_stage=_eprint)
    except RuntimeError as exc:
        _eprint(f"Error: {exc}")
        return 1

    report = result.to_markdown(title=args.title)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        _eprint(f"Done. Report written to {args.output}")
    else:
        print(report)

    if args.publish:
        from .publish import load_site_config, publish_report
        source_url = args.source_url
        if not source_url and is_youtube_url(args.source):
            source_url = args.source
        entry = publish_report(report, args.title, load_site_config(),
                               date=args.date, source_url=source_url,
                               tags=result.tags)
        _eprint(f"Published public layers -> docs/episodes/{entry['slug']}.html")
        if result.tags:
            _eprint(f"Tags: {', '.join(result.tags)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
