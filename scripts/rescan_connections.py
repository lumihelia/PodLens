"""Re-scan cross-episode connections for the already-published corpus, so the
new resonance/tension (conflict) detection applies to existing episodes.

Only CONNECTIONS are recomputed and re-translated — bodies/titles/tags are left
untouched (cheap: one find + one connections-translate per episode, no body
re-translation). Episodes are scanned in chronological order, each only against
STRICTLY EARLIER episodes, so a tension is recorded once (the later page shows
it as a back-reference) instead of twice.

    python scripts/rescan_connections.py

Writes docs/ + manifest only. Review, then commit & push.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import find_connections, translate_connections
from podlens.publish import (
    MANIFEST, extract_claims_section, load_site_config, rebuild_from_manifest,
)

EN_BODY = lambda slug: ROOT / ".podlens" / "episodes" / f"{slug}.en.md"


def _log(*a):
    print(*a, file=sys.stderr, flush=True)


def _en(entry: dict) -> dict:
    return (entry.get("i18n", {}) or {}).get("en", {}) or {}


def _en_candidates(this_tags: list[str], priors: list[dict]) -> list[dict]:
    """Prior episodes (English claims) to consider, tag-prefiltered, capped 8."""
    this_set = set(this_tags or [])
    shared = [it for it in priors if this_set & set(_en(it).get("tags", it.get("tags", [])))]
    pool = shared if shared else priors
    pool = sorted(pool, key=lambda it: it["date"], reverse=True)[:8]
    cands = []
    for it in pool:
        p = EN_BODY(it["slug"])
        claims = extract_claims_section(p.read_text(encoding="utf-8")) if p.exists() else ""
        cands.append({
            "slug": it["slug"],
            "title": _en(it).get("title") or it["title"],
            "tags": _en(it).get("tags", it.get("tags", [])),
            "claims": claims,
        })
    return cands


def main() -> int:
    config = load_config()
    if not config.has_api_key:
        raise SystemExit("GEMINI_API_KEY not set (check .env).")
    site = load_site_config()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = manifest["items"]
    # Chronological, stable; each episode is scanned only against earlier ones.
    order = sorted(items, key=lambda it: (it["date"], it["slug"]))

    total_tension = 0
    for idx, ep in enumerate(order):
        slug = ep["slug"]
        priors = order[:idx]
        if not priors:
            _log(f"\n=== {slug} === (earliest — no priors, skip)")
            continue
        enp = EN_BODY(slug)
        if not enp.exists():
            _log(f"\n=== {slug} === (no English body, skip)")
            continue
        _log(f"\n=== {slug} === scanning against {len(priors)} prior episode(s)")
        en_claims = extract_claims_section(enp.read_text(encoding="utf-8"))
        en_title = _en(ep).get("title") or ep["title"]
        cands = _en_candidates(_en(ep).get("tags", ep.get("tags", [])), priors)

        en_conns = find_connections(en_title, en_claims, cands, config, lang="en")
        tensions = [c for c in en_conns if c.get("kind") == "tension"]
        total_tension += len(tensions)
        _log(f"    found {len(en_conns)} connection(s): "
             f"{len(tensions)} tension, {len(en_conns) - len(tensions)} resonance")
        for c in tensions:
            _log(f"      TENSION [{c.get('conflict_type')}] -> {c['slug']}: {c.get('why','')[:90]}")

        zh_conns = translate_connections(en_conns, "zh", config) if en_conns else []

        # Update connections in place on the manifest entry (find it by slug).
        for it in items:
            if it["slug"] == slug:
                it["connections"] = zh_conns
                it.setdefault("i18n", {}).setdefault("en", {})["connections"] = en_conns
                break

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    n = rebuild_from_manifest(site)
    _log(f"\nDone. Rebuilt {n} episode(s). Total tensions found: {total_tension}. "
         "Review docs/, then commit & push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
