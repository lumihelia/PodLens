"""Publish rick-rubin-creative-act-less-is-more using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "rick-rubin-creative-act-less-is-more",
    "report": "reports/rick-rubin-creative-act-less-is-more.md",
    "url": "https://youtu.be/g6MEDOY7tHo?si=aZ4IIwsS_4AkE51D",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "少即是多、听的艺术与创作的天启 · Rick Rubin",
    "tags": ["创作过程", "减法美学", "专注力", "直觉与坚持", "音乐制作"],
    "connections": [
        {
            "slug": "ivanka-trump-authenticity-reinvention",
            "kind": "resonance",
            "relation": "互引",
            "why": "Ivanka Trump 直接引用了 Rubin 的《创造性行为》中的核心框架——「创作者终究只是高度与宇宙调频的人，听得越深，接收越多」——作为她的晨间宁静例程（在迈阿密海边冥想）的思想根基。Rubin 的「设置舞台、等待天启」和她的「创造宁静以便接收」是同一个认知立场的两种表达。",
            "this_point": "[24:36-25:48] Rubin 说创作天启是「从过程中被召唤出来」的，不是被制造的，他只是设置舞台、保持耐心等它来临——这是他工作的核心认知模型。",
            "that_point": "[15:46-15:58] Ivanka 说 Rick Rubin 的书讲到「创作者终究只是高度与宇宙调频的人，听得越深，接收越多」，这是她设计晨间宁静例程的理论依据。",
        },
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构",
            "why": "Rubin 的「创作天启」（大量低效的等待后突然出现的无法预期的好结果）是 Gopnik 高温搜索论的创作实践版本——高温搜索能发现通过有目的性执行永远找不到的解决方案；Rubin 的「设置舞台」就是一种制度化的高温搜索。两者都认为最重要的创造性发现不能被直接执行，只能被设置条件让其自然出现。",
            "this_point": "[24:36-27:05] Rubin 说好音乐来自那个无法预期、无法控制的「奇迹时刻」——不是技术能力的直接结果，而是从等待和尝试的过程中被召唤出来的。",
            "that_point": "[29:44-31:30] Gopnik 说高温搜索（儿童式探索）能找到通过有目的性低温搜索（成人科学家）永远找不到的全局最优解——约束越少、探索越随机，意外发现的质量反而更高。",
        },
    ],
    "en_title": "Less Is More, the Art of Listening, and the Creative Revelation · Rick Rubin",
    "en_tags": ["creative process", "subtraction aesthetic", "deep listening", "intuition and persistence", "music production"],
    "en_connections": [
        {
            "slug": "ivanka-trump-authenticity-reinvention",
            "kind": "resonance",
            "relation": "Ivanka directly quotes Rubin's Creative Act framework — 'the creator is ultimately just highly attuned to what the universe is saying, the deeper you listen the more you hear' — as the theoretical foundation for her morning stillness practice; Rubin's 'set the stage, wait for the revelation' and Ivanka's 'create stillness to receive' are the same cognitive stance expressed differently",
        },
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Rubin's 'creative revelation' (the unrepeatable, uncontrollable moment that appears from long patient waiting) is the creative-practice version of Gopnik's high-temperature search thesis — both argue the most important creative discoveries cannot be directly executed, only set-staged for; Rubin's studio practice is institutionalized high-temperature search",
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
