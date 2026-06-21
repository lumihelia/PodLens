"""Publish sarah-paine-continental-maritime-powers-geopolitics using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "sarah-paine-continental-maritime-powers-geopolitics",
    "report": "reports/sarah-paine-continental-maritime-powers-geopolitics.md",
    "url": "https://youtu.be/OS1NZLgKM2c?si=3tPDMLU6aQFHX9R1",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "为何普京和习近平无法逃脱地理的宿命 · Sarah Paine",
    "tags": ["地缘政治", "海权与陆权", "帝国史", "大战略", "国际秩序"],
    "connections": [
        {
            "slug": "ms-e435-class3-economics-ai-supercycle",
            "kind": "resonance",
            "relation": "框架补充",
            "why": "Paine 的陆权/海权框架为理解美中 AI 竞争提供了地缘政治底层逻辑：美国的芯片出口管制是海权猎象策略第二条（「封锁敌方贸易」）在技术领域的现代应用；中国的 AI 基础设施自建冲动是陆权自给自足逻辑在计算领域的复现。这不仅是科技竞争，是两种文明秩序在最新权力领域的正面相遇。",
            "this_point": "[37:04-37:58] Paine 的猎象策略第二条：封锁敌方贸易，切断其资源补充，让对手被迫依赖内部日益枯竭的资产——这是美国芯片管制政策的战略逻辑。",
            "that_point": "[ms&e435-class3 · 核心论点] Chase Lock Miller 指出美中 AI 超算力竞争中，美国通过出口管制切断中国获取先进芯片的路径；中国转而构建国内算力生态——这正是陆权自给自足逻辑在 AI 时代的表现。",
        },
    ],
    "en_title": "Why Putin and Xi Can't Escape Geography · Sarah Paine",
    "en_tags": ["geopolitics", "sea power and land power", "imperial history", "grand strategy", "international order"],
    "en_connections": [
        {
            "slug": "ms-e435-class3-economics-ai-supercycle",
            "kind": "resonance",
            "relation": "Paine's maritime/continental framework provides the geopolitical logic underlying US-China AI competition: US chip export controls are the maritime 'don't let the elephant forage' strategy applied to semiconductors; China's domestic AI infrastructure push is continental self-sufficiency logic applied to compute",
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
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:40]}...)")
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
