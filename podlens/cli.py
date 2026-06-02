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
        help="YouTube URL, transcript file path, '-' for stdin, or raw text.",
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
    args = parser.parse_args(argv)

    config = load_config()
    if args.lang:
        config.output_lang = args.lang

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
