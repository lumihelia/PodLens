"""Publish ivanka-trump-authenticity-reinvention using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "ivanka-trump-authenticity-reinvention",
    "report": "reports/ivanka-trump-authenticity-reinvention.md",
    "url": "https://youtu.be/VhsiMd9ZFNk?si=WaRGKH5RIBF3lq5J",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "自我认知、本真性与人生重建 · Ivanka Trump",
    "tags": ["自我认知", "创业哲学", "使命驱动", "人生重建", "本真性"],
    "connections": [
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "同构",
            "why": "两者都把「知道自己是谁」作为所有其他事情的前提，且都经历了主要的人生轨道中断并选择了不回头的重建。Brooks 的「螺旋型职业」（主动选择每7-12年学习新事物）和 Ivanka 的「不重接旧线」（被迫中断后拒绝回头）是同一个底层命题的两种不同路径——两者都认为打断惯性、从新的自我位置出发，比沿原轨迹继续更有价值。",
            "this_point": "[41:36-42:05] Ivanka 说最聪明的决定是不「重接旧线」——不回家族企业、不重启时装品牌，而是花6个月说不，等待真正从新的自我位置出现的吸引力，然后才开始行动。",
            "that_point": "[46:16-46:34] Brooks 描述螺旋型职业：每7-12年主动设计一个新的迷你职业，驱动力是「我想学下一件大事」而不是升职或薪酬——两者的共同点是把惯性打断视为机会，而不是损失。",
        },
    ],
    "en_title": "Self-Knowledge, Authenticity, and Rebuilding a Life · Ivanka Trump",
    "en_tags": ["self-knowledge", "entrepreneurial philosophy", "mission-driven work", "reinvention", "authenticity"],
    "en_connections": [
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "Both center on self-knowledge as the precondition for everything, and both describe leveraging major life discontinuity rather than fighting it — Brooks's spiral career (actively designing 7-12 year pivots) and Ivanka's 'don't reconnect old wires' (refusing to return after an involuntary break) are two paths to the same insight: momentum break as opportunity, not loss",
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
