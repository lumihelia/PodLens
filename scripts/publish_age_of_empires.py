"""Publish if-llms-have-human-like-attributes-age-of-empires (0624 batch).

This report was completely rewritten from the actual paper text (the original
0624 draft fabricated both the authorship and the entire methodology -- it
described a nonexistent "MBTI personality test on AoEII's built-in AI"
experiment; the real paper, by Adrian de Wynter, builds and trains a neural
network inside Age of Empires II to make a substrate-independence argument
and proves the game is functionally/Turing-complete). Verified against the
extracted PDF text in 材料/0624/extracted.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "if-llms-have-human-like-attributes-age-of-empires",
    "report": "reports/0624/if-llms-have-human-like-attributes-age-of-empires.md",
    "url": "https://arxiv.org/pdf/2605.31514",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "如果 LLM 有类人属性，那帝国时代II也有 · Adrian de Wynter",
    "tags": ["拟人化", "基质非唯一性", "图灵完备", "计算心智理论", "科学哲学"],
    "connections": [
        {
            "slug": "ai-anthropomorphism-trust-responsibility",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文从两个方向论证同一件事：LLM 是否「真的」拥有人类特质，和人类是否会「表现得像」它拥有人类特质，是两个完全独立的问题——而真正有后果的是后者。de Wynter 的论文证明：任何足够复杂的系统都可以被观察者解读出拟人化特质，说明这些特质依赖于表征方式，不是 LLM 独有的本质属性。Oldemburgo de Mello 等人的论文证明了这一点的现实后果：不管 AI 是否真的有情感，只要它表现得「像」有情感共鸣，用户的信任和责任归因就会被系统性地改变——而且这种改变可以被设计利用。",
            "this_point": "Abstract · \"the purported anthropomorphic attributes of LLMs are empirically non-unique: although some properties (e.g., responses to prompts) could remain invariant, others, such as the interpretation of their perceived behaviour, might change with the substrate.\"",
            "that_point": "Abstract · \"anthropomorphism simultaneously increases user trust while deflecting accountability from developers. These dynamics create a responsibility gap with significant implications for AI governance and institutional accountability.\"",
        },
        {
            "slug": "avi-wigderson-p-vs-np-zero-knowledge-proofs",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文都在用严格的形式逻辑，划出「什么可以被证明」和「什么本质上证明不了任何东西」之间的边界。de Wynter 证明：在「接受/拒绝」某个心智理论框架的前提下，关于 LLM 拟人属性是否存在的实验结论，无论正面还是负面，都逃不出循环论证或无信息量两种失败模式——这本身就是一种复杂性/可证明性的结果。Wigderson 整场访谈的核心也是同一类问题：哪些数学/计算命题原则上可以被证明或验证（零知识证明的普适性、P vs NP），哪些即使穷尽努力依然停留在「我们就是不知道」（乘法是否真的比加法更难）。两人都在说：弄清楚一个问题「能不能在当前框架下被回答」，本身就是和回答这个问题同样重要的工作。",
            "this_point": "§4.2 · \"positive outcomes... provide evidence that the hypothesis is true, and concluded that the assumptions were true. This is a circular argument... a negative experiment... [is] an uninformative/ambiguous outcome.\"",
            "that_point": "[02:07:08] Wigderson 说我们仍然不知道乘法是否比加法更难，P vs NP 问题在他整个职业生涯中没有实质性进展——理论计算机科学家的日常是失败，乐趣在于思考本身，大发现极其稀有。",
        },
    ],
    "en_title": "If LLMs Have Human-Like Attributes, Then So Does Age of Empires II · Adrian de Wynter",
    "en_tags": ["anthropomorphism", "substrate non-uniqueness", "Turing-completeness", "computational theory of mind", "philosophy of science"],
    "en_connections": [
        {
            "slug": "ai-anthropomorphism-trust-responsibility",
            "kind": "resonance",
            "relation": "The two papers argue the same point from two directions: whether an LLM 'genuinely' possesses human-like attributes, and whether humans will 'behave as if' it does, are two completely separate questions — and it's the second one that actually has consequences. de Wynter's paper proves that any sufficiently complex system can be read by an observer as having anthropomorphic attributes, showing these attributes depend on representation, not an essential property unique to LLMs. Oldemburgo de Mello et al.'s paper proves the real-world consequence of exactly this: regardless of whether an AI genuinely has emotions, the moment it merely appears to show emotional attunement, users' trust and blame attribution shift systematically — and that shift can be exploited by design.",
        },
        {
            "slug": "avi-wigderson-p-vs-np-zero-knowledge-proofs",
            "kind": "resonance",
            "relation": "Both papers use rigorous formal logic to draw the line between what can be proven and what is, by its very structure, incapable of proving anything at all. de Wynter proves that under an 'accept/reject' framework for some theory of mind, experimental conclusions about whether LLMs have anthropomorphic attributes — positive or negative — can never escape two failure modes: circularity or uninformativeness. That is itself a result about provability. The core of Wigderson's entire interview is the same kind of question: which mathematical/computational claims can, in principle, be proven or verified (the universality of zero-knowledge proofs, P vs. NP), and which remain stuck at 'we simply don't know' no matter how much effort is spent (whether multiplication is genuinely harder than addition). Both are saying: figuring out whether a question *can be answered at all* within a given framework is work just as important as trying to answer it.",
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
        sec = "papers" if item["kind"] == "paper" else "episodes"
        # Site is English-primary: en lives at docs/<sec>/, zh at docs/zh/<sec>/.
        d = ROOT / "docs" / (f"zh/{sec}" if lang == "zh" else sec)
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
