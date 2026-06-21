"""Publish lewis-spacex-7years-manufacturing-musk using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "lewis-spacex-7years-manufacturing-musk",
    "report": "reports/lewis-spacex-7years-manufacturing-musk.md",
    "url": "https://youtu.be/a93FT2340c0?si=VYbwPUuIeqiwX8vX",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "SpaceX七年口述史：第一原理制造、火箭民主化与马斯克的管理幽灵 · Lewis",
    "tags": ["SpaceX口述史", "第一原理制造", "可口可乐罐对话", "火箭成本革命", "SpaceX Mafia"],
    "connections": [
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "同构",
            "why": "Marc从外部观察者角度描述了Elon的管理方法——直接和工程师沟通，绕过所有层级，和做那件事的人待到问题解决，不喜欢「大灰云」管理层（IBM的12层）。Lewis从内部7年的角度验证并填充了细节：Musk只开三种会议（晚了/做不出来/需要更多钱）；「我接受你的辞职」被平静地说出，而不是大喊大叫；深夜11点后走进特斯拉工厂二班，当场删除看起来不合逻辑的流程；「可口可乐罐对话」是Marc描述的Musk第一原理询问法的最具体案例——Musk没有说「做得不够好」，他说「从第一原理看，你在做的事和可乐罐是一回事，而可乐罐的生产速度是一分钟几千个」。两人描述的是同一个人和同一套方法，从互补的视角。Marc提供的是分析框架，Lewis提供的是具体质感。",
            "this_point": "[01:38:03-01:46:30] 三种会议类型：「我只会因三件事找你：你的东西晚了，你做不出来，你需要更多钱。其他时间，你就是在做对的事。」可口可乐罐对话：团队把高压桶（行业成本的10%，产能满足40次年发射）带到Musk桌上，等待赞美。Musk第一句话：「你见过可乐罐的生产线吗？」他不是在否定成就，他是在指向一个团队还没看到的天花板。[02:56:15-02:57:07] 深夜工厂行走：特斯拉二班（夜11点后）是Musk最喜欢巡查工厂的时间，当场删除看起来低效的流程。这与Marc描述的「Elon直接到工程师那里，和他们待在那里直到问题解决」在结构上完全一致。",
            "that_point": "[01:32:07-01:37:02] Marc描述IBM的「大灰云」（12层管理，每层微小谎言，CEO与现实完全脱节）和Elon的极端对立：「他只和工程师说话。当有问题时，他直接找到负责那个问题的工程师，一起待到解决。我见过他这样做。几乎没有CEO这样做。」Marc还说：「Elon的管理方式是本世纪最重要的新型管理范式之一。」Marc的框架是分析性的，Lewis的描述是经验性的——两者合在一起，可以让你理解这套方法在日常里是什么感觉。",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "早期猎鹰9的迭代逻辑与Dyson的5127个原型哲学在结构上完全相同：把每一次（发射/原型）的数据反馈进下一次，失败是信息，迭代是唯一的学习机制。Lewis说「早期没有两枚猎鹰9是一样的——每次发射都把好的、坏的、对的、错的全部纳入下一枚」，这就是Dyson「拿起来，问怎么改进，改进，放下，重复」的直接对应。两人都相信：（1）你不可能在不接触真实物理世界的情况下学到你需要的知识；（2）失败不是需要避免的事，而是需要系统性利用的数据；（3）拥有第一个版本的控制权，是迭代超越的前提（Dyson的「让它与众不同，哪怕更差」，SpaceX的「退出Falcon 1，做自己的Falcon 9」）。更深的联系：高压桶故事和Dyson的5127次实验有相同的逻辑——不是靠读别人的研究或采购外部方案，而是亲手做到理解材料的边界在哪里。",
            "this_point": "[01:25:30-01:27:05] 「早期猎鹰9，几百次发射里没有两枚是一样的，因为它需要迭代。不是要求每次成功，是要每次都学到不同的东西。」[01:43:24-01:44:40] 高压桶的迭代过程：「经过了很多时间，很多迭代，反复循环，终于做出来了。当然第一件事是……把这个成品带到了Elon的桌上。」团队的迭代逻辑和Dyson的一样：不知道答案在哪里，但通过足够多次的亲手实验，最终到达答案。[02:04:36-02:05:14] 2015-2016年失败后找原因：「耗时数月，只能靠直觉，测试所有可能性，运气也是其中一部分。我们最终靠直觉猜对了。」——这是具身知识的本质：无法通过阅读找到答案，只能通过实践和直觉。",
            "that_point": "[07:19-09:49, 30:31-33:00] Dyson的5127个原型：「每一个失败都让我更接近解决方案。失败比成功更有趣。」迭代方法：拿起来，问怎么改进，改进，放下，重复——直到你拥有了一个没有其他人知道该如何改进的版本。Dyson也明确批评「先读研究再做」的方法：亲手做才能知道材料如何响应、气流如何变化、结构如何失效。这与Lewis描述的SpaceX学习机制（每次发射学一次，通过亲手制造高压桶学会它的物理边界）是同一认识论。",
        },
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "张力",
            "why": "Tobi和Lewis都在描述反管理主义的组织——没有层级官僚，创始人直接参与，高能动性的人执行高密度任务。但他们面对同一个问题（「如何让领导者对公司实际情况保持掌握」）采取了完全相反的架构解决方案。Tobi的解法：Shopify OS——用Python+SAT求解器把整个公司架构写成机器可读的配置文件，让每一个决策和它的后果都完全可见，把政治从资源分配中消除。SpaceX/Musk的解法：根本不建立系统——Musk本人就是系统。他的三种会议类型、深夜工厂巡查、可乐罐问题——这些都是让他直接感知现实的行为，而不是建立一个可以替代这种感知的组织机器。Tobi认为需要建立一个在没有Tobi的情况下也能正确决策的系统；SpaceX的系统只有在Musk在场时才完全运作。这创造了一个关于「创始人依赖」的根本性张力：Tobi在去除Tobi依赖，SpaceX在强化Musk依赖。",
            "this_point": "[01:05:01-01:07:08] SpaceX组织结构的核心特点：每个零件只有一个负责人，同时是工程师、采购员、项目经理。「如果这个人明天被火车撞了，整个公司等他。」「当你加入SpaceX，如果能撑过6个月，恭喜你，你已经是老兵了。」[01:38:03-02:07:30] Musk作为「首席工程师」的自我描述：「严格来说没什么错——他是做最终决策的人，关于整个公司所有设计方向的所有大小事务。」SpaceX的信息流是通过Musk的直接判断来维持质量，而不是通过Shopify OS那样的系统性透明度。",
            "that_point": "Tobi的Shopify OS（本集核心主题之一）：用Python+SAT求解器把整个公司的组织结构（职级、汇报关系、薪酬结构）写成机器可读的配置文件，计算「应然状态」和「当前状态」的差距，找到最小步骤集来消除这个差距。目的是消除政治——当销售负责人申请50个新职位时，系统立刻显示这意味着工程招聘减少多少、哪些产品工作停止——没有人可以在隐藏代价的情况下接受一个请求。这与SpaceX「Musk就是系统」形成了鲜明对比：Shopify正在建立一个可以在没有Tobi的情况下运转的组织机器；SpaceX的质量控制机制高度依赖Musk的个人存在（深夜工厂巡查、三种会议类型、直接询问工程师）。",
        },
    ],
    "en_title": "SpaceX Oral History: First-Principles Manufacturing, the Rocket Cost Revolution, and the Musk Management Ghost · Lewis",
    "en_tags": ["SpaceX oral history", "first-principles manufacturing", "Coke can conversation", "rocket cost revolution", "SpaceX Mafia"],
    "en_connections": [
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "Andreessen describes Elon's management method from the outside: direct contact with engineers, no tolerance for organizational layers, sitting with the engineer responsible for a problem until it's solved. Lewis provides the interior texture: the three-meeting-type rule (late, can't do it, needs more money), the 'I accept your resignation' delivered without raised voice, the midnight factory walks eliminating illogical processes on the spot, the Coke can conversation as a perfect specimen of first-principles questioning. Marc's framework is analytical; Lewis's account is experiential. Together they constitute something close to a complete portrait of the same operating method from opposite vantage points.",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Early Falcon 9 production operated on exactly Dyson's philosophy: no two rockets were alike because every launch fed data into the next one. Failure is information. You cannot learn what you need to know without touching the physical reality. Lewis describes the high-pressure vessel project — months of iteration, testing possibilities, relying on intuition — as the mechanism by which they learned the physical boundaries of what they were building. Dyson's 5,127 prototypes had the same structure: you cannot read your way to the answer, you can only make your way to it. Both also share the conviction that owning the first version is a precondition for iterating past it: Dyson's 'make it different even if it's worse,' SpaceX's decision to retire Falcon 1 rather than cash it out.",
        },
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "Both Lütke and Lewis describe anti-managerialist organizations — no bureaucracy, high talent density, founders in direct contact with the work. But they chose opposite architectural solutions to the same problem: how does a leader maintain accurate information about what's actually happening in the company? Lütke's solution is Shopify OS — a SAT-solver model that makes every decision and its consequences fully legible, eliminating political fog. SpaceX's solution is no system at all: Musk himself is the system. The midnight factory walks, the three-meeting rule, the Coke can first-principles questions are behaviors that maintain direct contact with reality, not mechanisms that replace that contact. The deep tension: Lütke is systematically removing Tobi-dependence from Shopify; SpaceX structurally reinforces Musk-dependence. The company's quality-control mechanism works precisely because Musk is there. What happens when he isn't is an open question.",
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
