"""One-off local fix: push the restructured zh/en bodies for the 4 podcast
episodes that had a collapsed "这期讲了什么" section (missing overview
paragraph, sub-sections nested as H3 instead of standalone H2). Bodies were
already rewritten on disk (.podlens/episodes/<slug>.md and .en.md). This just
refreshes the manifest summary and re-renders. No API calls.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.publish import _load_manifest, load_site_config, update_episode

SLUGS = [
    "adam-neumann-wework-flow-community",
    "marc-andreessen-malleable-world-founder-capitalism",
    "pavel-durov-telegram-freedom-resistance",
    "tobi-lutke-companies-as-technology-shopify-os",
]


def _body_path(slug: str, lang: str) -> Path:
    return ROOT / ".podlens" / "episodes" / (f"{slug}.md" if lang == "zh" else f"{slug}.{lang}.md")


def main() -> int:
    site = load_site_config()
    manifest = {it["slug"]: it for it in _load_manifest()}

    for slug in SLUGS:
        entry = manifest[slug]
        en_prior = entry.get("i18n", {}).get("en", {})
        zh_body = _body_path(slug, "zh").read_text(encoding="utf-8")
        en_body = _body_path(slug, "en").read_text(encoding="utf-8")

        en = {
            "title": en_prior.get("title", ""),
            "tags": en_prior.get("tags", []),
            "body": en_body,
            "editor_note": en_prior.get("editor_note", ""),
            "connections": en_prior.get("connections", []),
        }

        updated = update_episode(slug, site, public_md=zh_body, en=en)
        print(f"{slug}: summary -> {updated['summary'][:60]}...")

    print(f"\nDone. {len(SLUGS)} episodes restructured and rebuilt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
