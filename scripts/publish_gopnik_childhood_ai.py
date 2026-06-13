"""Publish alison-gopnik-childhood-learning-ai-cultural-technology using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
    "report": "reports/alison-gopnik-childhood-learning-ai-cultural-technology.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "儿童如何学习，AI 是什么文化技术 · Alison Gopnik",
    "tags": ["儿童学习", "认知科学", "AI文化技术", "探索与利用", "自然与养育"],
    "connections": [
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "互引",
            "why": "Gopnik 的「文化技术」框架被 Efros 直接引用并作为其「表层数据 vs 深层数据」论点的核心参照——两者对当前 AI 的诊断高度一致（缺乏主动具身实验），且他们出席了同一个工作坊，Gopnik 在 Efros 讲座的 Q&A 中直接发言。",
            "this_point": "[45:05-47:00] Gopnik 阐述「文化技术」论：AI = 印刷术/图书馆/互联网搜索，是人类获取彼此知识的工具；它做不到两岁儿童能做的事——主动与物理世界互动、做实验、得到具身反馈。",
            "that_point": "[24:09-24:29] Efros 在工作坊演讲中说「我非常喜欢 Alison 谈论当前 AI 的方式。她说，这些当前的 AI 不是智能体，它们是文化技术」——直接援引 Gopnik 的框架作为自己「表层数据」论点的哲学基础。",
        },
        {
            "slug": "the-era-of-experience",
            "kind": "resonance",
            "relation": "张力",
            "why": "Gopnik 主张 AI 是文化技术、无法通过接触现实产生新知识；而「经验时代」论文恰好提出了走出这个限制的路径——智能体主动与环境交互生成经验数据。两者诊断相同，方向相反：前者是对当前状态的本体论判断，后者是走出困境的工程路线图。",
            "this_point": "[44:30-47:00] Gopnik 说 LLM 产生文本而永不接触外部现实（「Derrida 的复仇」）；真正的智能体必须主动与物理世界交互来产生新知识；机器人学是这个鸿沟最清晰的呈现。",
            "that_point": "[The Era of Experience · 核心论断] 论文主张 AI 正从「人类数据时代」转向「经验时代」——智能体将通过与环境主动交互产生经验进行持续学习，突破监督学习的人类数据瓶颈。",
        },
        {
            "slug": "yann-lecun-world-models-next-ai-revolution",
            "kind": "resonance",
            "relation": "同构",
            "why": "Gopnik 的发展心理学和 Yann 的 AI 架构指向同一个洞察：智能的核心是建构对世界的因果模型，而这只能通过主动的具身交互来完成。儿童通过在物理世界中做实验来建立世界模型；Yann 的 JEPA 是试图在工程上实现同一机制的架构。",
            "this_point": "[23:52-25:30] Gopnik 的「贝叶斯构建主义」：儿童从物理实验数据中构建因果世界模型；这是 Piaget 构建主义的现代版本，也是 Gopnik 认为当前 AI 缺失的核心能力。",
            "that_point": "[05:37-08:05] Yann LeCun 提出动物与人类智能通过具身交互建立内部世界模型；JEPA（联合嵌入预测架构）是其工程实现；当前 LLM 的根本缺陷正是缺乏这个世界模型建构机制。",
        },
    ],
    "en_title": "How Children Learn and What AI Actually Is · Alison Gopnik",
    "en_tags": ["childhood learning", "cognitive science", "AI as cultural technology", "explore vs exploit", "nature and nurture"],
    "en_connections": [
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "Efros directly cites Gopnik's 'cultural technology' framing as the philosophical foundation for his surface/deep data thesis; they share the same diagnosis (current AI lacks active embodied experimentation); Gopnik appears in the Q&A of Efros's workshop talk",
        },
        {
            "slug": "the-era-of-experience",
            "kind": "resonance",
            "relation": "Gopnik diagnoses the limitation (AI as text-only cultural technology, 'Derrida's revenge'); the Era of Experience paper proposes the engineering path out — agents generating their own experiential data through active environmental interaction",
        },
        {
            "slug": "yann-lecun-world-models-next-ai-revolution",
            "kind": "resonance",
            "relation": "Gopnik's developmental psychology and Yann's AI architecture share the same core insight: intelligence is built through active construction of causal world models via embodied interaction; JEPA is the engineering attempt to implement what children do naturally",
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
