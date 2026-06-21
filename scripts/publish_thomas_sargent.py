"""Publish thomas-sargent-ai-past-present-future (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "thomas-sargent-ai-past-present-future",
    "report": "reports/0621副本/thomas-sargent-ai-past-present-future.md",
    "url": "https://youtu.be/B2m-T3QQiqQ?si=KQd2LE89eI5RbuMl",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "人工智能的演进：统计、经济学与规则推断 · Thomas Sargent",
    "tags": ["结构模型", "规则推断", "认知局限", "科学革命", "信息论", "经济学思维"],
    "connections": [
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人从完全不同的学科——经济学哲学 vs. 认知神经科学实验——独立诊断出了同一个 AI 能力缺口。Sargent 用费曼「观察一盘棋推断整套规则」的隐喻指出：当代大语言模型在「描述模式」（观察棋子怎么走）上极度优秀，但在「推断博弈规则」（结构模型，看不见的因果机制）上依然一头雾水。Patel-Wang-Fan 用 Stroop 任务给出了这个诊断的精确神经科学版本：变换器自注意力机制只实现了人类注意力网络中的「定向网络」（描述、选择信息），完全没有实现「执行控制网络」（在冲突中维持目标、推断并执行规则）。一个是哲学层面的论断，一个是可复现的实验证据，指向同一个架构性缺口。",
            "this_point": "[01:00:52]-[01:01:34] Sargent 说大语言模型在「描述模式」上极度优秀，但在「推断规则」上依然存在根本性缺陷——它们可以提供极佳的描述性输出，但无法像物理学家或计量经济学家那样从现象中逆向提炼出底层的因果博弈结构。",
            "that_point": "Patel-Wang-Fan Discussion: \"A transformer's self-attention mechanism ≈ the orienting network (selecting relevant tokens from the input via weighting). But it does not implement executive control — the ability to actively suppress a dominant response amid competing information.\"",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在论证同一件事：当两个理论或作品在「客观指标」上表现接近时，人类最终选择相信的那一个，往往是由美学直觉而非纯粹的数据拟合度决定的——而且做到「更少」往往需要更深的理解，不是偷懒。哥白尼提出日心说时，他 36 个参数的模型对行星轨道的预测精度其实低于托勒密 250 个参数的地心说模型，但科学家们因为日心说的简洁优美而选择相信它更接近真理。Rubin 用同样的逻辑解释为什么他在 LL Cool J 第一张专辑上不署名「制作人」而署名「减少者」：叠加的元素越多，每个元素的个性权重就越小；做到少需要先看清什么是核心、什么是噪音，然后有勇气只留下核心。",
            "this_point": "[26:15]-[26:30], [27:59]-[28:22] Sargent 说哥白尼 36 参数的日心说模型，预测精度其实远低于托勒密 250 参数的地心说模型；但科学家们因为日心说模型的简洁与优美，选择相信它更接近真理。",
            "that_point": "[00:20]-[01:30] Rubin 说少即是多，但做到少需要做更多：叠加的东西越多，每个元素的权重越小，个性就越弱；精简不是减法，是让必要之物的本质显现出来——这就是为什么做到「少」需要更多工作，你必须先理解什么是核心、什么是噪音，再有勇气只留下核心。",
        },
    ],
    "en_title": "The Evolution of Artificial Intelligence: Statistics, Economics, and Rule Inference · Thomas Sargent",
    "en_tags": ["structural models", "rule inference", "cognitive limitations", "scientific revolution", "information theory", "economic thinking"],
    "en_connections": [
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "Working from entirely different disciplines — the philosophy of economics versus a cognitive neuroscience experiment — the two independently diagnose the same gap in AI capability. Sargent, using Feynman's metaphor of 'inferring the entire rule set by watching a single chess game,' argues that contemporary LLMs are extremely good at 'describing patterns' (watching how the pieces move) but remain hopelessly lost at 'inferring the rules of the game' (a structural model, the invisible causal mechanism). Patel-Wang-Fan gives the precise neuroscience version of the same diagnosis using the Stroop task: a transformer's self-attention mechanism implements only the 'orienting network' of human attention (describing and selecting information), with no implementation at all of the 'executive control network' (sustaining a goal amid conflict, inferring and enforcing a rule). One is a philosophical argument, the other reproducible experimental evidence — both pointing at the same architectural gap.",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Both argue the same point: when two theories or works perform similarly on 'objective metrics,' the one humans ultimately choose to believe is often decided by aesthetic intuition rather than pure data fit — and achieving 'less' usually requires deeper understanding, not laziness. When Copernicus proposed heliocentrism, his 36-parameter model actually predicted planetary orbits less accurately than Ptolemy's 250-parameter geocentric model, but scientists chose to believe heliocentrism was closer to the truth because of its simplicity and elegance. Rubin makes the identical argument to explain why his credit on LL Cool J's first album read not 'producer' but 'reduced by': the more elements you stack, the less personality each one carries; achieving less requires first seeing clearly what's essential and what's noise, then having the courage to keep only the essential.",
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
