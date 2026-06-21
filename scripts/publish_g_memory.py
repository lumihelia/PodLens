"""Publish g-memory-hierarchical-memory-multi-agent-systems (0621 batch, verified against arXiv PDF text)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "g-memory-hierarchical-memory-multi-agent-systems",
    "report": "reports/0621/g-memory-hierarchical-memory-multi-agent-systems.md",
    "url": "https://arxiv.org/pdf/2506.07398",
    "kind": "paper",
    "date": "2026-06-21",
    "title": "G-Memory：多智能体系统的层级记忆追踪 · Guibin Zhang",
    "tags": ["多智能体系统 (MAS)", "层级记忆", "图数据库", "自我演化", "上下文压缩", "认识论环境"],
    "connections": [
        {
            "slug": "agent-memory",
            "kind": "tension",
            "relation": "张力",
            "why": "agent-memory 对10种记忆系统做系统级实测后得出一个通用结论：没有任何记忆系统能同时在构建开销、查询延迟和任务准确度三者上都最优——总是存在前沿权衡。G-Memory 的实验结果看起来正好挑战了这条经验法则：它在 PDDL+AutoGen 上同时拿到了最高的性能提升和极低的 token 增量，明显优于 MetaGPT-M。这构成一个值得追问的张力：G-Memory 是真的找到了跳出这条权衡曲线的设计（角色定制化注入 + 图稀疏化过滤掉冗余对话），还是只是把代价转移到了 agent-memory 框架未测量的维度上（例如基于 LLM 的图稀疏化算子本身可能带来的额外延迟开销，G-Memory 论文并未系统测量这一项）？",
            "this_point": "G-Memory §5.3: \"G-Memory achieves high-performing collective memory without excessive token consumption... delivers the highest performance improvement (10.32%↑ over no-memory setting on PDDL+AutoGen) while maintaining a modest increase in token consumption (only 1.4×10^6). In contrast, MetaGPT-M incurred an additional 2.2×10^6 tokens for a mere 4.07% gain.\"",
            "that_point": "agent-memory 4.5. The Construction–Serve–Accuracy Frontier · \"No agent memory system is optimal across\" construction cost, query latency 与 task accuracy 三个维度。",
        },
        {
            "slug": "li-curtis-working-memory-neural-dynamics",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文都构建了「底层granular vs 顶层abstract」的记忆层级，并都发现了同一个反直觉结果：名义上更「高级」的抽象层未必承担更多实际计算功能，granular层反而更关键。G-Memory 的消融实验显示，仅保留细粒度交互图（Interaction）比仅保留高层洞察图（Insight）表现更好（PDDL 上 54.46 vs 50.00）；Li-Curtis 的fMRI研究发现，最「高级」的前额叶皮层（PFC）反而是表征最贫乏的——它知道「在记忆一个位置」，却不维持具体的空间拓扑结构，真正承担精细计算的是「最底层」的V1。两个系统不约而同地证明：分层记忆架构里，越靠近具体执行的那一层，可能携带越多的不可替代的功能性信息。",
            "this_point": "G-Memory §5.4 Figure 4c：仅启用细粒度交互图（Inter ✔, Insi ◦）时，AutoGen 在 PDDL 上得分 54.46；仅启用高层洞察图（Inter ◦, Insi ✔）时，得分降至 50.00。",
            "that_point": "Li-Curtis Discussion · \"Distinct from the neurophysiological results in macaque PFC, we find evidence for coexisting stable and dynamic WM codes in early visual cortex, not PFC.\" PFC 维持的是最抽象、最稀薄的记忆代码,不保留视觉场的空间拓扑;真正执行格式转换的计算发生在最「低级」的V1。",
        },
    ],
    "en_title": "G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems · Guibin Zhang",
    "en_tags": ["multi-agent systems (MAS)", "hierarchical memory", "graph databases", "self-evolution", "context compression", "epistemic environments"],
    "en_connections": [
        {
            "slug": "agent-memory",
            "kind": "tension",
            "relation": "agent-memory's systems-level survey of 10 memory architectures arrives at a general empirical law: no memory system is simultaneously optimal on construction cost, query latency, and task accuracy — there is always a frontier trade-off. G-Memory's own results appear to challenge exactly this law: on PDDL+AutoGen it delivers both the highest performance gain and a minimal token increase, clearly beating MetaGPT-M on both axes at once. This raises a genuine question worth asking: has G-Memory actually found a design that escapes this trade-off curve (role-specific injection plus graph sparsification filtering out redundant dialogue), or has it simply moved the cost onto a dimension agent-memory's framework doesn't measure — such as the latency overhead of its own LLM-based graph sparsifier, a gap G-Memory itself flags in its open questions?",
        },
        {
            "slug": "li-curtis-working-memory-neural-dynamics",
            "kind": "resonance",
            "relation": "Both papers build a memory hierarchy split between a granular bottom layer and an abstract top layer, and both arrive at the same counterintuitive result: the layer that's nominally 'higher-level' doesn't necessarily carry more of the actual computational weight — the granular layer turns out to matter more. G-Memory's ablation shows that keeping only the fine-grained Interaction Graph outperforms keeping only the high-level Insight Graph (54.46 vs. 50.00 on PDDL); Li-Curtis's fMRI study finds that the 'highest-level' region, prefrontal cortex, is in fact the most representationally impoverished — it knows 'I am remembering a location' but doesn't preserve the spatial topology, while the real fine-grained computation happens in the 'lowest-level' region, V1. Both systems independently demonstrate that in a layered memory architecture, the layer closer to actual execution may carry more irreplaceable functional information than the layer nominally considered smarter.",
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
        sec = "papers" if item["kind"] == "paper" else "episodes"
        d = ROOT / "docs" / (sec if lang == "zh" else f"en/{sec}")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
