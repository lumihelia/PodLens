"""Publish ms&e435-class3-economics-ai-supercycle using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "ms&e435-class3-economics-ai-supercycle",
    "report": "reports/ms&e435-class3-economics-ai-supercycle.md",
    "url": "https://youtu.be/4zk-hJ50vmU?si=9d_9Y7wbYavqltYO",
    "kind": "podcast",
    "date": "2026-06-11",
    "title": "AI超量扩张的电网硬壁垒与能源套利 · Chase Lock Miller",
    "tags": ["算力电能", "数据中心", "数字劳动力", "垂直整合", "电网基建"],
    "connections": [
        {"slug": "ms&e435-class4-economics-ai-supercycle", "kind": "resonance", "relation": "同系"},
        {"slug": "cs153-08-jensen-huang-nvidia-compute", "kind": "resonance", "relation": "印证"},
        {"slug": "jane-street-gpus-trading-hiring-dwarkesh", "kind": "resonance", "relation": "同构"},
        {"slug": "dan-loeb-ai-credit-third-point", "kind": "resonance", "relation": "补充"},
    ],
    "en_title": "AI Overexpansion's Hard Grid Barriers and Energy Arbitrage · Chase Lock Miller",
    "en_tags": ["compute energy", "data centers", "digital labor", "vertical integration", "grid infrastructure"],
    "en_connections": [
        {
            "slug": "ms&e435-class4-economics-ai-supercycle",
            "kind": "resonance",
            "relation": "companion session in the same course: both analyze AI infrastructure economics from the inside",
        },
        {
            "slug": "cs153-08-jensen-huang-nvidia-compute",
            "kind": "resonance",
            "relation": "Jensen Huang's compute scaling thesis is the demand-side basis Chase builds his energy-first supply-side strategy upon",
        },
        {
            "slug": "jane-street-gpus-trading-hiring-dwarkesh",
            "kind": "resonance",
            "relation": "both analyze how high-performance compute forces physical infrastructure codesign — from cooling to power delivery to chip architecture",
        },
        {
            "slug": "dan-loeb-ai-credit-third-point",
            "kind": "resonance",
            "relation": "both are finance-world perspectives on the structural economic consequences of the AI compute buildout",
        },
    ],
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
    print(f"  title:   {item['title']}")
    print(f"  tags:    {', '.join(item['tags'])}")
    for c in item["connections"]:
        print(f"  {c['kind']}: -> {c['slug']} ({c['relation']})")
    print("  [bilingual] using Claude translation from en_bodies/")

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
        d = ROOT / "docs" / ("episodes" if lang == "zh" else "en/episodes")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    print(f"zh:   docs/episodes/{entry['slug']}.html")
    print(f"en:   docs/en/episodes/{entry['slug']}.html")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
