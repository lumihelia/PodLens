"""One-off local fix: correct 3 connection slugs that don't match any
published page, so those cross-episode links (and their backrefs) start
rendering. Purely local manifest edit + rebuild, no API calls.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.publish import _load_manifest, _rebuild_site, load_site_config

FIXES = {
    "caa-co-founder-michael-ovitz": "michael-ovitz-caa-frame-of-reference",
    "ms-e435-class3-economics-ai-supercycle": "ms&e435-class3-economics-ai-supercycle",
}


def _patch(connections: list[dict]) -> int:
    n = 0
    for c in connections:
        if c.get("slug") in FIXES:
            c["slug"] = FIXES[c["slug"]]
            n += 1
    return n


def main() -> int:
    site = load_site_config()
    items = _load_manifest()
    slugs = {it["slug"] for it in items}

    for target in FIXES.values():
        if target not in slugs:
            print(f"!! target slug not found in manifest: {target}")
            return 1

    total = 0
    touched = []
    for it in items:
        n = _patch(it.get("connections", []))
        en = (it.get("i18n") or {}).get("en")
        if en:
            n += _patch(en.get("connections", []))
        if n:
            total += n
            touched.append((it["slug"], n))

    _rebuild_site(items, site)

    print(f"Patched {total} connection slug(s) across {len(touched)} item(s):")
    for slug, n in touched:
        print(f"  {slug}: {n} fixed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
