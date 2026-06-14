"""Publish patel-wang-fan-transformer-executive-control as kind=paper (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "patel-wang-fan-transformer-executive-control",
    "report": "reports/patel-wang-fan-transformer-executive-control.md",
    "url": "https://doi.org/10.1101/2025.01.22.634394",
    "kind": "paper",
    "date": "2026-06-14",
    "title": "变换器注意力的执行控制缺陷：Stroop任务揭示LLM不能做什么",
    "tags": ["执行控制缺陷", "Stroop效应", "晶体智力vs流体智力", "注意力网络理论", "语境长度的隐藏天花板"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构/张力",
            "why": "Gopnik的核心论点之一是：儿童的前额叶皮层「欠发育」不是缺陷而是优势——它让孩子对世界保持开放性和探索性（探索-开发权衡）。成年人的前额叶皮层完全成熟后，会更有效地执行已知策略（执行控制），但对新事物的开放性下降。Patel等人的论文发现LLM缺乏执行控制，这与Gopnik的框架形成了有趣的交叉：LLM既不像孩子（孩子在探索模式中可以灵活切换注意力），也不像成年人（成年人有执行控制来压制主导响应）。更精确地说，LLM有「成年人的晶体知识库」但「没有执行控制机制」——这是一种在人类发展中从未同时存在的组合。Gopnik讨论的是智力的发展性问题：你需要学会压制「自动化」响应才能做到执行控制（孩子在6-7岁才开始展现Stroop效应，因为他们还没自动化阅读）。LLM的问题是反向的：自动化先于控制机制，而且控制机制可能根本不会「发展」出来，因为它不在训练目标里。",
            "this_point": "[论文第16-17页] 「Stroop效应在人类中的发展轨迹：6-7岁出现（阅读开始自动化）；9-11岁接近成人水平；保持稳定直到60岁后才因老化重新恶化。LLM有海量晶体知识但流体智力（处理新颖冲突）严重受限。」[论文第17页] 「认知控制和智力的关系研究显示，执行控制与流体智力的相关高于晶体智力——这正好对应LLM的能力特征：通过司法考试（晶体智力）但无法计算字母数量（流体智力）。」",
            "that_point": "[Gopnik集核心论点] 儿童学习的核心机制是「探索-开发」权衡：孩子大量探索（宽泛的先验分布），成年人大量开发（窄的先验分布，快速执行已有策略）。前额叶皮层的成熟=执行控制增强=开发能力增强=探索能力下降。她的反直觉主张：在AI设计中，简单地追求「更像成年人」（更强的执行控制、更快的目标导向行为）可能会失去学习能力的关键部分。LLM现在的问题不是「太像孩子」（开放探索但没有执行控制），而是「两样都没有」的奇怪状态。",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "张力",
            "why": "Foody认为AI正在革命性地改变知识工作：AI可以积累并应用大量晶体知识，这对传统白领工作（律师、程序员、分析师）产生了根本性的替代压力。他的论点的隐含前提是：知识工作主要需要晶体智力（查询、综合、生成已知模式的变体）。Patel等人的论文精确标定了这个假设成立的边界：在任务中存在系统性竞争冲突的地方，这个前提就失效了。「你正在分析一个案例，背景信息不断出现矛盾」「你在代码审查中，表面逻辑和深层意图相互冲突」——这些场景需要执行控制（压制一个明显的模式，坚持更深层的目标），正是LLM的薄弱点。换句话说：Foody说AI改变了知识工作；这篇论文说「有一类知识工作AI改变不了，就是需要在有噪声/冲突的信息流中维持目标的那种」。",
            "this_point": "[论文第17页] 「LLMs excel at tasks requiring crystallized intelligence, such as passing the bar exam to become a lawyer and passing medical licensing exams, they still struggle with simple yet novel letter-counting problem-solving tasks which are supported by fluid intelligence.」[论文摘要] 「Our results suggest that incorporating executive control mechanisms akin to those in biological attention could be crucial for achieving more general reasoning and reliable performance toward artificial general intelligence.」",
            "that_point": "[Foody集核心论点] Mercor的使命是教AI做知识工作：通过人类反馈数据，AI可以学会编写代码、进行法律研究、分析财务报表。他认为这种「知识工作的自动化」会创造一个新的经济层级：人类指导AI，AI执行大多数实现。Foody看到的是AI的效率优势（更快、更廉价地完成知识工作）；Patel等人揭示的是AI的一个系统性弱点（在长序列冲突情境下无法维持目标导向行为）。这两个图景都是对的，但针对的是知识工作的不同维度：结构化信息检索与综合（AI优势），vs. 在噪声/冲突中维持判断（AI弱点）。",
        },
        {
            "slug": "alexei-efros-surface-deep-data-curious-robot",
            "kind": "resonance",
            "relation": "同构",
            "why": "Efros区分了「表面数据」（AI当前学习的那种，基于统计关联）和「深度数据」（因果结构化的、主动探索获得的数据）。他认为AI需要深度数据才能发展出真正的「世界模型」，而不只是模式匹配器。Patel等人的发现是这个区分的实证体现：Claude 3.5在没有prompt的情况下「识别」了Stroop范式（表面模式匹配的极致表现——它认出了任务），但还是给出了错误答案（没有「深度数据」支撑的世界模型，无法在运行中主动压制干扰）。「知道任务 ≠ 能执行任务」的解离就是Efros所说的「表面模式识别」和「真正的因果理解」之间差距的一个具体、可测量的表现。更具体地：执行控制需要的不只是「我知道颜色和词义之间的关系」，而是「我在当前情境中的目标是什么，以及我主动维持这个目标而不被干扰信息偏离的能力」——这正是Efros所说的「好奇心驱动的主动探索」（而不是被动的统计关联学习）所产生的能力。",
            "this_point": "[论文第18-19页] 「In our exploratory trials without explicit prompts, Claude 3.5 Sonnet demonstrated recognition of the Stroop paradigm but still produced incorrect responses despite output with word-color relationship mappings. This behavior demonstrates a dissociation between task understanding and execution capabilities. The models' effective context window for executive control is notably shorter than their general processing capacity.」[论文第16页] 「The inability to resolve cognitive conflicts in the color naming task due to limited executive control appears to be the primary hindering factor in model performance.」",
            "that_point": "[Efros集核心论点] 「表面数据」：互联网上的文本/图像数据，AI从中学到了海量的统计关联。「深度数据」：需要主动与世界交互才能获得的因果数据——比如机器人伸手触碰物体时的触觉/视觉/运动反馈的同步。Efros说当前AI的「苦涩教训」（scaling laws, more data + more compute = better）正在逼近回报递减的上限，因为表面数据的量再多也补不了因果结构的缺口。这篇论文用Stroop任务量化了这个缺口的一个维度：给再多文本训练数据，也产生不了「在冲突中维持目标」的执行控制能力，因为这个能力来自神经网络里一个尚未实现的架构特性，不来自数据量。",
        },
    ],
    "en_title": "Deficient Executive Control in Transformer Attention: The Stroop Test Reveals What LLMs Cannot Do",
    "en_tags": ["deficient executive control", "Stroop effect", "crystallized vs fluid intelligence", "attention network theory", "hidden ceiling on context length"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Gopnik's core argument includes a counterintuitive claim: the underdeveloped prefrontal cortex in children is a feature, not a bug — it keeps them in exploratory mode. Executive control (which this paper shows LLMs lack) is the mature prefrontal cortex function that suppresses automatic responses in favor of goals. LLMs occupy a strange developmental position: they have the crystallized knowledge base of highly educated adults but none of the executive control that normally develops alongside years of embodied cognitive experience. Gopnik's framework also tracks the Stroop effect's developmental trajectory: it emerges at 6–7 when reading automatizes, and matures by 9–11. LLMs have the automaticity without the inhibitory counterpart — an inversion of the developmental sequence that has no human parallel.",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "Foody's thesis is that AI is transforming knowledge work by accumulating and applying crystallized knowledge at scale — legal research, code review, financial analysis. This paper precisely delineates where that thesis holds and where it breaks. The failure mode is specific: tasks requiring sustained conflict resolution — maintaining a goal when the environment is systematically generating distracting, competing information — are exactly what LLMs cannot do reliably as the context grows. 'You're reviewing a contract and the clauses are mutually contradictory.' 'You're debugging code where the obvious fix conflicts with a hidden invariant.' These require executive control. Foody sees the revolution; this paper marks its boundary.",
        },
        {
            "slug": "alexei-efros-surface-deep-data-curious-robot",
            "kind": "resonance",
            "relation": "Efros distinguishes surface data (statistical associations learned from passive observation) from deep data (causally structured data gathered through active exploration). The paper's finding is a precise empirical version of this distinction: Claude 3.5 Sonnet recognizes the Stroop paradigm without a prompt — maximum surface-pattern matching — but still fails at the task. Knowing the pattern is not the same as having the underlying cognitive machinery. Executive control requires not just 'I know the relationship between word meaning and ink color' but 'I can actively maintain my current goal and suppress the dominant competing response.' That is not something statistical pattern learning over text produces. It is what Efros calls the gap between surface and deep data, measured now in percentage points.",
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

    print(f"Publishing: {slug}  [kind=paper]")
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
        d = ROOT / "docs" / ("papers" if lang == "zh" else "en/papers")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    print(f"zh:   docs/papers/{entry['slug']}.html")
    print(f"en:   docs/en/papers/{entry['slug']}.html")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
