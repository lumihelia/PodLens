"""One-off backfill: re-do the already-published episodes as faithful BILINGUAL.

Why this exists: the first episodes were interpreted directly into Chinese under
the old pipeline, and some lost their personal-mapping layer (published before
the local archive fix). Per the agreed rule, we re-do them natively: interpret
each in its OWN (source) language first, archive the FULL report (incl. the
private personal mapping) locally, then translate the public layer and publish
both Chinese and English pages -- keeping each episode's ORIGINAL slug, date,
and source URL so existing links never break.

Run AFTER filling EPISODES below with each episode's subtitle file path:

    python scripts/backfill_bilingual.py            # do all
    python scripts/backfill_bilingual.py jim-al-khalili   # do one (by slug)

Nothing is pushed; it only writes docs/ + reports/. Review, then commit & push.
"""

import sys
from pathlib import Path

# Make the package importable when run as a script.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import build_bilingual, find_connections, interpret
from podlens.profile import load_profile
from podlens.publish import (
    build_candidates,
    extract_claims_section,
    extract_public_markdown,
    load_site_config,
    publish_report,
    slugify,
)
from podlens.transcript import detect_language, load_transcript

# slug -> (subtitle_file_path, date, source_url). Process in date order so
# cross-episode connections build on the already-rebuilt corpus.
EPISODES = [
    {
        "slug": "jim-al-khalili",
        "date": "2026-06-02",
        "source_url": "https://youtu.be/8xp3Bs6nZ-Y",
        "subtitle": "/Users/heloiseqin/Downloads/字幕/01 Quantum entanglement and the illusion of time, in 79 minutes  Jim Al-Khalili Full Interview.vtt",
    },
    {
        "slug": "david-reich",
        "date": "2026-06-03",
        "source_url": "https://www.youtube.com/watch?v=sRKBGVFVYAw",
        "subtitle": "/Users/heloiseqin/Downloads/字幕/04 David Reich – Bronze Age shock, the Neanderthal puzzle, & the sudden spread of farming.vtt",
    },
    {
        "slug": "hakeem-oluseyi",
        "date": "2026-06-03",
        "source_url": "https://youtu.be/pyhB7B3JWts",
        "subtitle": "/Users/heloiseqin/Downloads/字幕/03 The quantum realm, the cosmological realm, and the multiverse, in 69 minutes  Hakeem Oluseyi.vtt",
    },
    {
        "slug": "don-lincoln-lex-fridman-497",
        "date": "2026-06-03",
        "source_url": "https://youtu.be/1M3Vdl6DRkU",
        "subtitle": "/Users/heloiseqin/Downloads/字幕/02 Biggest Mysteries in Physics Antimatter, Dark Energy & ToE - Don Lincoln  Lex Fridman Podcast #497.vtt",
    },
]

REPORTS_DIR = ROOT / "reports"


def _log(*a):
    print(*a, file=sys.stderr, flush=True)


def backfill_one(ep: dict, config, site) -> None:
    slug = ep["slug"]
    sub_path = ep["subtitle"].strip()
    if not sub_path or not Path(sub_path).is_file():
        raise SystemExit(f"[{slug}] subtitle file not set or missing: {sub_path!r}")

    _log(f"\n=== {slug} ===")
    transcript = load_transcript(sub_path)
    if not transcript.strip():
        raise SystemExit(f"[{slug}] transcript is empty after loading {sub_path}")

    source_lang = detect_language(transcript)
    _log(f"source language detected: {source_lang}")

    profile = load_profile(config.profile_path)
    if profile is None:
        _log("WARNING: no profile.md found -> personal mapping will be skipped.")

    # Native-first interpretation (public layers in source lang; private mapping
    # stays in config.output_lang).
    result = interpret(transcript, profile, config, on_stage=_log,
                       public_lang=source_lang)
    report_title = result.title or slug
    report = result.to_markdown(title=report_title)

    # Archive the FULL report (incl. private personal mapping) locally.
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / f"{slug}.md").write_text(report, encoding="utf-8")
    _log(f"archived full report (with personal mapping) -> reports/{slug}.md")

    # Connections against the prior corpus, then translate the public bundle.
    candidates = build_candidates(result.tags, exclude_slug=slug)
    connections = find_connections(
        report_title, extract_claims_section(report), candidates, config,
        lang=source_lang,
    )
    native_public = extract_public_markdown(report, site.private_cutoff)
    _log("translating public layer -> bilingual")
    _, zh_b, en_b = build_bilingual(
        native_public, report_title, result.tags, connections, config
    )

    # Publish keeping the ORIGINAL slug/date/source_url.
    publish_report(
        report, zh_b["title"], site,
        date=ep["date"], slug=slug, source_url=ep["source_url"],
        tags=zh_b["tags"], connections=zh_b["connections"],
        en=en_b, primary_public_md=zh_b["body"],
    )
    _log(f"published bilingual: /episodes/{slug}.html  +  /en/episodes/{slug}.html")
    if connections:
        _log(f"connections: {len(connections)} -> {', '.join(c['slug'] for c in connections)}")


def main(argv: list[str]) -> int:
    config = load_config()
    if not config.has_api_key:
        raise SystemExit("GEMINI_API_KEY not set (check .env).")
    site = load_site_config()

    only = set(argv)
    todo = [e for e in EPISODES if not only or e["slug"] in only]
    if not todo:
        raise SystemExit(f"No matching episodes for: {', '.join(only)}")

    failures = []
    for ep in todo:
        try:
            backfill_one(ep, config, site)
        except Exception as exc:  # keep going; one bad episode shouldn't lose the rest
            failures.append((ep["slug"], str(exc)))
            _log(f"!! {ep['slug']} FAILED: {exc}")

    _log("\nDone. Review docs/ and reports/, then commit & push to go live.")
    if failures:
        _log(f"FAILED ({len(failures)}): " + "; ".join(f"{s}: {e}" for s, e in failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
