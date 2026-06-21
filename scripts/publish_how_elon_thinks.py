"""Publish how-elon-thinks-algorithm-physics-makers using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "how-elon-thinks-algorithm-physics-makers",
    "report": "reports/how-elon-thinks-algorithm-physics-makers.md",
    "url": "https://youtu.be/CdBcZSau5iA?si=6fvU6uMUB1u-vN60",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "五步算法、物理律法与造物者的使命 · Elon Musk思维解码",
    "tags": ["五步算法", "物理律法", "速度", "垂直整合", "造物者哲学"],
    "connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都把「失败」重新定义为系统设计的信息基础设施，而不是需要规避的事故——但实现路径不同。Dyson的失败系统是线性的、物理化的：5127个原型，每一个都是下一个的前提；Elon的失败系统是概率化的、组织化的：50%截止日期命中率是最优设计，「如果你不能告诉我你以四种方式搞砸了某件事，你不是真正做那件事的人」。Dyson把失败内化为个人迭代节奏；Elon把失败外化为组织设计原则——两者都在说，失败本身是你能积累的最有价值的信息，拒绝失败等于拒绝学习。",
            "this_point": "[22:07-24:36] Elon：「失败本质上无关紧要，除非它是灾难性的。我想对每一个设计决策都制造500次失败，这样当我们扩大规模时我就知道我们有最优雅的版本了。我喜欢选一个我有50%可能实现的截止日期——我们会错过一半，我完全没问题。」",
            "that_point": "[04:05-04:29] Dyson：「失败比成功更有趣，因为失败了你会质疑它——它会引发调查。成功了你只说'太好了'然后继续。」5127个原型是这个原则放大到商业可行性规模的产物：每次失败都是信息密集的调查起点。",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都明确拒绝「利润最大化」作为创业的起点，都把使命的真实性视为长期竞争优势而非软性情感。Elon：「我不从风险调整回报率出发——我找需要发生的事并让它发生。」Mackey：「布道者和雇佣兵不是对错之分，但长期来看信仰的人走得更稳。」更深的共同点：两人都发现了「不以利润为导向的决策」反而产生了更强的竞争优势——Tesla不打广告，把钱全押回产品；Mackey的天然食品网络最终成为信任型并购管道。悖论相同：越不直接追求利润，越持久地产生利润。",
            "this_point": "[00:58-02:20, 01:19:55-01:20:49] Elon：「我不从风险调整回报率出发。我只找需要发生的事并试图让它发生。如果我们不造东西就没有东西——技术进步不是不可避免的，必须有人做真正的工作。」他对Tesla的定义：不是建立盈利的电动车公司，是让尽可能多的人开上电动车。",
            "that_point": "[00:02-01:57] Mackey说布道者和雇佣兵之间没有对错，但真实信仰的人比计算的人走得更远更稳——他的天然食品网络最终成了信任收购管道，整个competitive moat建立在使命一致性上，而不是战略精算上。",
        },
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "同构",
            "why": "书的作者对这本书的终极目标（「生产一百万个Musk」）与Garry Tan对YC和个人AI的使命（「技术民主化，让更多人能建造」）在结构上是同一个主张：找到还没有被广泛接触到的高杠杆能力，然后把它散布给尽可能多的人。同时，Elon和Garry都有来自困难童年的燃料（Elon：父亲当众羞辱，七八岁被父亲在客厅里站立数小时骂「没用」「愚蠢」；Garry：酗酒暴力父亲，七岁的屋子）——两人都「让恶魔拉犁」，但提取方式不同：Garry是主动的、蓄意的（「我可以随时走进那间屋子，取出一杯铀235」），Elon更像是把它烧成推进剂压入永续驱动。",
            "this_point": "[15:23-16:34, 01:22:02-01:23:05] 书的作者：「我希望这本书能生产一百万个Musk——不是复制他的人生，而是找一个别人还没在做的独特的重要问题，并把一生押注于解决它。」Elon的童年：父亲当众羞辱多年；被一群孩子打到住院一周，父亲站在施暴者那边；「想象一下这给一个孩子填满了什么样的燃料。Elon学会了让恶魔拉犁。」",
            "that_point": "[01:26:02-01:26:27, 01:52:14-01:53:20] Garry说「上帝给了你这个大脑……技术就是一种服务彼此的方式」——他的民主化使命来自个人的技术债务感：技术给了我一切，我想让所有人都拥有它。七岁的屋子：他能「随时走进那间屋子」，那个七岁的自己「倒出一杯放射性铀235，我带着那杯走进我的一天」——主动提取创伤能量。",
        },
    ],
    "en_title": "The Five-Step Algorithm, Physics as the Only Law, and the Maker's Mission · Decoding Elon Musk",
    "en_tags": ["five-step algorithm", "physics as law", "speed", "vertical integration", "maker philosophy"],
    "en_connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both redefine failure as designed information infrastructure rather than something to avoid — but through different mechanisms: Dyson's is linear and physical (5,127 sequential prototypes, each the prerequisite for the next); Elon's is probabilistic and organizational (50% deadline hit rate as optimal design, 'if you can't tell me the four ways you f***ed it up, you weren't doing the real work') — Dyson internalizes failure as personal iteration rhythm; Elon externalizes it as organizational architecture; both reach the same conclusion: refusing failure means refusing to learn",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "Both explicitly refuse profit-maximization as the starting point of entrepreneurship, and both discovered that mission-authentic decisions produce stronger long-term competitive advantage than strategic profit-calculation: Elon's Tesla doesn't advertise and pushes all money back into the product; Mackey's natural foods network became a trust-based acquisition pipeline; the same paradox — the less directly you pursue profit, the more durably you generate it",
        },
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "The book author's stated goal ('generate one million Musks') and Garry's YC/personal AI mission ('democratize tools so more people can build') are structurally the same claim: find a high-leverage capability not yet widely accessible, then spread it to as many people as possible; additionally, both Elon and Garry ran difficult-childhood fuel through their engines (Elon: father's public humiliation for hours at age eight, sided with the bullies who hospitalized him; Garry: alcoholic-violent father, the seven-year-old's room) — both made the demons pull the plow, but with opposite extraction mechanisms: Garry's is deliberate and conscious (he 'walks into the room' and pours the plutonium); Elon's runs as continuous combustion, always on",
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
