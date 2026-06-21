"""Publish the-curse-of-optionality-tim-ferriss-founder-mindset (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "the-curse-of-optionality-tim-ferriss-founder-mindset",
    "report": "reports/0621副本/the-curse-of-optionality-tim-ferriss-founder-mindset.md",
    "url": "https://youtu.be/6sfpC8qRGFA?si=Wz4BQ7S2a7wzGU6O",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "选择权的诅咒与实验精神 · Tim Ferriss",
    "tags": ["选择权", "风险校准", "恐惧设定", "实验主义", "认知负荷", "决策策略"],
    "connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在用不同的语言描述同一个心理操作：把模糊、灾难化的失败恐惧转化为具体、可量化、可恢复的信息。Ferriss 的「恐惧设定」要求把担忧列成表格——最坏情况是什么、如何预防、如何恢复——一旦量化，大部分所谓的风险就被证明是可逆的。Dyson 用 5127 次原型实践了同一个原则：成功了你只会说「太好了」然后继续，从不深究；失败了你必须问「哪里出错了」，而那个答案往往只有失败才能给你。两人都把「失败」从一种需要被恐惧的灾难，重新定义为一种主动索取的数据来源。",
            "this_point": "[03:57]-[04:45] Ferriss 说恐惧设定的核心是把脑中模糊的灾难化猜想列成具体清单：最坏情况是什么、怎么预防、发生了怎么恢复——量化之后，大部分风险被证明是完全可逆的。",
            "that_point": "[03:58]-[04:19] Dyson 说失败比成功更有趣：成功了你说「太好了」然后继续，不会深究为什么；失败了你必须问「为什么」，那个答案往往只有失败才能给你——这就是为什么 5127 次原型不是苦役，而是一段「hugely enjoyable struggle」。",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "同构",
            "why": "Ferriss 的「选择权的诅咒」（顶尖学生去投行咨询保留选择权，结果被生活方式蠕变锁死，五年后真正走出来创业的人数是零）和 Marc 引用 Burnham 的「管理主义 vs. 布尔乔亚资本主义」框架，描述的其实是同一种社会结构性陷阱的两个版本。管理主义的核心卖点就是「可转移的技能保留了未来所有的选择权」；布尔乔亚资本主义要求你把名字写在门上、承担不可逆的后果。两人都认为，表面上更安全、更灵活的「保留选择权」路径，实际上系统性地阉割了真正改变世界所需要的那种全情投入。",
            "this_point": "[22:27]-[23:29], [24:47]-[25:10] Ferriss 说顶尖商学院学生进入投行或咨询，对外宣称要「保留创业或投资的选择权」，但五年后真正走出来创业的人数是零——因为生活方式蠕变（买跑车、去 Ibiza）已经把他们的风险承受力彻底阉割。",
            "that_point": "Marc 引用 Burnham《马基雅维利主义者》：管理主义（可互换的管理技能，1880-1920年代的制度产物）让管理者可以在任何稳定环境里运营任何公司，但当世界改变、需要做艰难决定时，他们没有内在驱动力——因为他们的承诺从来不是不可逆的。",
        },
    ],
    "en_title": "The Curse of Optionality and the Experimental Mindset · Tim Ferriss",
    "en_tags": ["optionality", "risk calibration", "fear-setting", "experimentalism", "cognitive load", "decision strategy"],
    "en_connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both describe the same psychological maneuver in different languages: converting a vague, catastrophized fear of failure into something concrete, quantifiable, and recoverable. Ferriss's 'fear-setting' requires tabulating your worries — what's the worst case, how do you prevent it, how do you recover — and once quantified, most so-called risk turns out to be reversible. Dyson practiced the identical principle through 5,127 prototypes: when you succeed you just say 'great' and move on, never digging into why; when you fail you have to ask 'what went wrong,' and that answer is often only available through failure. Both redefine failure from a catastrophe to be feared into a source of data to be actively sought.",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "Ferriss's 'curse of optionality' (top students go into banking or consulting to 'preserve optionality,' get locked in by lifestyle creep, and the number who actually leave to found something five years later is zero) and Marc's framework, borrowed from Burnham, of 'managerialism vs. bourgeois capitalism,' describe two versions of the same structural social trap. Managerialism's core pitch is that a transferable skill preserves all your future options; bourgeois capitalism requires putting your name on the door and bearing irreversible consequences. Both argue that the path which looks safer and more flexible on the surface — 'preserving optionality' — systematically castrates the full, all-in commitment actually required to change anything.",
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
