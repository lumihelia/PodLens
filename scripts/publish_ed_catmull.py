"""Publish ed-catmull-pixar-business-of-great-things (0621 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "ed-catmull-pixar-business-of-great-things",
    "report": "reports/0621/ed-catmull-pixar-business-of-great-things.md",
    "url": "https://youtu.be/6ffhW9WAUv0?si=4p_nM4iLmgH9E_W9",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "创意组织的管理、动力学与 Steve Jobs · Ed Catmull",
    "tags": ["组织动力学", "智囊团", "创意文化", "决策机制", "认知安全", "领导力"],
    "connections": [
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人解决的是同一个问题的两个版本：如何把组织决策从「谁有权力、谁声音大」中解放出来，变成对事不对人的机制。Tobi 用 Shopify OS（机器可读的配置文件 + SAT 求解器）把资源分配的政治变成可见的后果；Catmull 用 Brain Trust（对等、无决策权、对事不对人）把创意批评从「我是不是被否定了」的自我防卫中剥离出来。两人也共享同一个「差异化/原创性是义务」的论点：Tobi 说复制别人的7分你的顶板就是7分，Catmull 说追求平庸的管理成本更低但长期死亡率更高——攻克难题（如 Ratatouille）才能拉开差距。",
            "this_point": "[43:08]-[44:21] Catmull 说依赖平庸公式制作的廉价平庸片容易预测、成本低，但市场回报和品牌积累都很差；攻克 Ratatouille 这种反直觉的难题，是用高难度拉开和竞争对手的差距。",
            "that_point": "[50:30-01:01:00] Tobi 说「让它不同，即使它更差」（引 Dyson）：复制别人的7分，你的顶板就是7分；从头建造自己的版本哪怕只有6分，你拥有完全掌控权，可以把它迭代到8分。",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "tension",
            "relation": "张力",
            "why": "两人对「使命」在组织中应该扮演什么角色给出了相反的答案。Mackey 把创始人分为布道者（使命驱动，愿意用十几年复利去兑现一个使命）和雇佣兵，并明确站在布道者一边；Catmull 则认为 mission statement 本身是一种危险的简化——它提供「一劳永逸的虚假安全感」，会让组织停止持续发问。两人都在管理「长期坚持」这件事，但 Mackey 靠的是一个被清晰表述、可以反复诵念的使命；Catmull 靠的是刻意不让使命被表述清楚，逼着组织一直处在「我们正在做什么、方向对不对」的提问状态里。",
            "this_point": "[49:24]-[49:57] Catmull 说他们从来没有 mission statement，因为使命宣言是一个答案，而组织应该始终在发问「我们在做什么、方向是否正确」；一旦说「我们回到使命陈述」，发问就停止了。",
            "that_point": "[00:02-01:57] Mackey 把创始人分为布道者型（使命驱动，把公司当作一生的事业，愿意接受十几年的复利）和雇佣兵型（聪明的起步者，厌倦运营，想要退出），并认为这个区分是他整个思维体系的核心。",
        },
    ],
    "en_title": "Managing Creative Organizations, Group Dynamics, and Steve Jobs · Ed Catmull",
    "en_tags": ["organizational dynamics", "the Brain Trust", "creative culture", "decision mechanisms", "psychological safety", "leadership"],
    "en_connections": [
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "Both are solving two versions of the same problem: how to free organizational decisions from 'whoever holds power or speaks loudest' and turn them into mechanisms that judge the work, not the person. Tobi uses Shopify OS (machine-readable configuration files plus a SAT solver) to make the politics of resource allocation visible as consequence; Catmull uses the Brain Trust (peer-level, no decision-making power, criticize the work not the person) to strip creative criticism of the self-protective fear of being personally rejected. Both also share the same 'differentiation/originality is an obligation' argument — Tobi says copying someone else's 7/10 caps you at 7; Catmull says chasing mediocrity is cheaper to manage but has a far higher long-term mortality rate, and only tackling a genuinely hard problem (like Ratatouille) opens a real gap over competitors.",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "tension",
            "relation": "The two give opposite answers to what role 'mission' should play inside an organization. Mackey divides founders into missionaries (mission-driven, willing to compound for a decade or two toward a calling) and mercenaries, and explicitly sides with the missionaries; Catmull argues a mission statement is itself a dangerous simplification — it offers 'a false, one-time sense of safety' that lets an organization stop asking questions. Both are managing the problem of sustaining commitment over the long run, but Mackey relies on a clearly stated mission you can repeat to yourself; Catmull relies on deliberately never letting the mission be stated cleanly, forcing the organization to stay in a permanent state of asking whether it's doing the right thing.",
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
