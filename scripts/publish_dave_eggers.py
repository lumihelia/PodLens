"""Publish dave-eggers-storytelling-creative-writing (0621 plus batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "dave-eggers-storytelling-creative-writing",
    "report": "reports/0621 plus/dave-eggers-storytelling-creative-writing.md",
    "url": "https://youtu.be/LwoWdKuB8gg?si=d_BXcZmjPRv-gjCy",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "形式突围、触觉记忆与独立创作的防线 · Dave Eggers",
    "tags": ["创意写作", "独立出版", "触觉化设计", "预警审查", "个人叙事"],
    "connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在描述同一种创作现象学：突破性的灵感不能被硬撑出来，只能通过忍受漫长的无聊去「等待」它被召唤出现。Eggers 把自己锁进金门大桥下没有网络、用着1998年破屏幕电脑的旧帆船里，每天经历6到8小时的独处和拖延，往往要等到第6小时之后才会涌现关键的小说突破。Rubin 用钓鱼来比喻同一件事：大多数时间什么都不会发生，无聊、挫败，然后突然「一些东西从虚无中出现」——这个时刻无法被制造，只能靠每天强迫自己出现来换取被召唤的机会。",
            "this_point": "[52:27]-[53:41], [55:43]-[55:59] Eggers 说写作不能靠硬撑，他在没有互联网、用着1998年破屏幕旧电脑的船舱里经历漫长的无聊和日记式拖延，往往在第6小时之后才会涌现出关键的小说突破。",
            "that_point": "[24:36]-[25:48] Rubin 说创作天启是被召唤的，不是被制造的：大多数时间是等待，像钓鱼一样什么都不发生，然后突然「一些东西从过程中被召唤出来」——这不是我们做的，他对这个时刻上瘾，而不是对通向它的过程上瘾。",
        },
        {
            "slug": "ed-catmull-pixar-business-of-great-things",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在批判同一种创造力杀手：用一个看似安全、可重复的死板模板，去替代持续不断的真实探索和发问。Eggers 痛斥学校强加的「五段式作文」把学生的写作直觉系统性地框死在规范化的网格里；Catmull 拒绝给 Pixar 设立 mission statement，理由完全相同——使命宣言提供的是一种「一劳永逸的虚假安全感」，会让组织停止发问「我们正在做什么、方向是否正确」。两人都认为：真正的创造力依赖于持续保持不确定、不被预先框定的状态，而任何看似高效的固定模板，本质上都是在用安全感置换探索本身。",
            "this_point": "[01:41:53]-[01:43:07] Eggers 猛烈批判扼杀创意的「五段式作文」等学校官僚体制规则，认为各种所谓的写作规则本质上框死了学生的想象力，写作应该鼓励自由地越界和去学习未知的事物。",
            "that_point": "[48:45]-[50:13] Catmull 说他们从来没有 mission statement，因为使命宣言是一个答案，而组织应该始终在发问「我们在做什么、方向是否正确」；一旦说「我们回到使命陈述」，发问就停止了。",
        },
    ],
    "en_title": "Breaking Through Form, Tactile Memory, and the Last Line of Defense for Independent Creation · Dave Eggers",
    "en_tags": ["creative writing", "independent publishing", "tactile design", "preemptive censorship", "personal narrative"],
    "en_connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Both describe the same phenomenology of creation: a breakthrough idea cannot be forced — it can only be summoned by enduring long stretches of boredom while waiting for it. Eggers locks himself into an old sailboat under the Golden Gate Bridge, with no internet and a 1998 laptop with a cracked screen, enduring six to eight hours of solitude and procrastination each day, with the key breakthrough for his novel usually only emerging after the sixth hour. Rubin uses fishing as a metaphor for the exact same thing: most of the time nothing happens — boredom, frustration — and then suddenly 'something appears out of nothing.' That moment can't be manufactured; you can only earn the chance of being chosen by forcing yourself to show up every day.",
        },
        {
            "slug": "ed-catmull-pixar-business-of-great-things",
            "kind": "resonance",
            "relation": "Both attack the same killer of creativity: substituting continuous, genuine exploration and questioning with a rigid template that merely looks safe and repeatable. Eggers excoriates the school-imposed 'five-paragraph essay' for systematically locking students' writing instincts into a standardized grid; Catmull refuses to set a mission statement for Pixar for exactly the same reason — a mission statement offers 'a false, one-time sense of safety' that lets an organization stop asking whether it's doing the right thing. Both believe real creativity depends on staying continuously uncertain and unboxed, and that any seemingly efficient fixed template is, at its core, trading away exploration itself for a feeling of safety.",
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
        d = ROOT / "docs" / ("episodes" if lang == "zh" else "en/episodes")
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
