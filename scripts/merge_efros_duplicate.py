"""One-off local fix: remove the duplicate Alexei Efros episode.

alexei-efros-surface-deep-data-curious-robot and alexei-efros-surface-data-deep-data
are the same talk, published twice on 2026-06-14. Keep the more complete one
(surface-data-deep-data: 20 timeline entries, canonical section names, longer
report) and drop the other. Repoint any connections that referenced the
dropped slug. Purely local manifest edit + rebuild, no API calls.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.publish import _load_manifest, _rebuild_site, load_site_config

DROP_SLUG = "alexei-efros-surface-deep-data-curious-robot"
KEEP_SLUG = "alexei-efros-surface-data-deep-data"


def _repoint(connections: list[dict]) -> None:
    for c in connections:
        if c.get("slug") == DROP_SLUG:
            c["slug"] = KEEP_SLUG


def main() -> int:
    site = load_site_config()
    items = _load_manifest()

    before = len(items)
    items = [it for it in items if it["slug"] != DROP_SLUG]
    if len(items) == before:
        print(f"!! {DROP_SLUG} not found in manifest (already removed?)")
        return 1

    repointed = []
    for it in items:
        _repoint(it.get("connections", []))
        en = (it.get("i18n") or {}).get("en")
        if en:
            _repoint(en.get("connections", []))
        if any(c.get("slug") == KEEP_SLUG for c in it.get("connections", [])):
            repointed.append(it["slug"])

    _rebuild_site(items, site)

    print(f"Removed: {DROP_SLUG}")
    print(f"Connections repointed to {KEEP_SLUG} in: {repointed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
