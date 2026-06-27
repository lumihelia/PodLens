"""Publish two-arrows-of-pain-meditation-aversion-identification (0624 batch).

Restructured into the standard paper template; corrected author bylines
(Valentina Nicolardi, not "Veronica"; Domenico Scaringi, not "Donatella")
and fixed a faithfulness error in the original draft (which had the
short-term/long-term LKM pain-reduction pattern reversed relative to the
actual abstract: short-term meditators showed reduced pain in FAM and OMM,
long-term meditators only in LKM). Verified against 材料/0624/extracted.

No new outbound connections were added here -- pain-catastrophizing-critical-
review and letting-go-unwell-self-chronic-conditions already point at this
slug, so their backrefs render automatically on this page once published.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "two-arrows-of-pain-meditation-aversion-identification",
    "report": "reports/0624/two-arrows-of-pain-meditation-aversion-identification.md",
    "url": "https://doi.org/10.1007/s12671-021-01797-0",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "疼痛的两支箭：冥想、排斥与认同的疼痛机制 · Valentina Nicolardi et al.",
    "tags": ["两支箭", "佛教心理学", "Granger因果分析", "冥想", "疼痛认同"],
    "connections": [],
    "en_title": "The Two Arrows of Pain: Mechanisms of Pain Related to Meditation and Mental States of Aversion and Identification · Valentina Nicolardi et al.",
    "en_tags": ["two arrows", "Buddhist psychology", "Granger causality", "meditation", "pain identification"],
    "en_connections": [],
}


def main() -> int:
    site = load_site_config()
    item = ITEM
    slug = item["slug"]

    report_path = ROOT / item["report"]
    if not report_path.exists():
        print(f"!! report not found: {report_path}")
        return 1

    en_body_path = EN_BODIES_DIR / f"{slug}.md"
    if not en_body_path.exists():
        print(f"!! en body not found: {en_body_path}")
        return 1

    report_md = report_path.read_text(encoding="utf-8")
    public_md = extract_public_markdown(report_md, site.private_cutoff)
    if not public_md:
        print("!! no public content extracted (check private cutoff heading)")
        return 1

    en_body = en_body_path.read_text(encoding="utf-8")
    en = {
        "title": item["en_title"],
        "tags": item["en_tags"],
        "body": en_body,
        "connections": item["en_connections"],
    }

    print(f"Publishing: {slug}")
    for c in item["connections"]:
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:30]}...)")

    entry = publish_report(
        report_md, item["title"], site,
        date=item["date"], slug=slug,
        source_url=item["url"],
        tags=item["tags"],
        connections=item["connections"],
        en=en,
        primary_public_md=public_md,
        kind=item["kind"],
    )

    leaks = []
    for lang in ("zh", "en"):
        sec = "papers" if item["kind"] == "paper" else "episodes"
        d = ROOT / "docs" / (f"zh/{sec}" if lang == "zh" else sec)
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
