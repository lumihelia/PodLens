"""Publish ai-anthropomorphism-trust-responsibility (0624 batch, verified against extracted PDF text).

Restructured into the site's standard paper template (the original report used a
different, incomplete format missing 论文骨架/最值得读原文的几段/the private-layer
cutoff heading). Author byline was also corrected: the original report fabricated
2 of 3 author names; verified against the actual paper (Oldemburgo de Mello, Plaks,
Inzlicht, University of Toronto).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "ai-anthropomorphism-trust-responsibility",
    "report": "reports/0624/ai-anthropomorphism-trust-responsibility.md",
    "url": "https://online.ucpress.edu/collabra/article/12/1/161757/939204/",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "AI 拟人化对信任与责任的影响 · Victoria Oldemburgo de Mello et al.",
    "tags": ["AI拟人化", "信任博弈", "责任位移", "情感共鸣", "AI治理"],
    "connections": [
        {
            "slug": "if-llms-have-human-like-attributes-age-of-empires",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文从两个方向论证同一件事：LLM 是否「真的」拥有人类特质，和人类是否会「表现得像」它拥有人类特质，是两个完全独立的问题——而真正有后果的是后者。de Wynter 的论文证明：任何足够复杂的系统（哪怕是一个在《帝国时代II》上训练的简单神经网络）都可以被观察者解读出拟人化特质，说明这些特质是「表征层面」的产物，不是 LLM 独有的本质属性。Oldemburgo de Mello 等人的论文证明了这一点的现实后果：不管 AI 是否真的有情感，只要它表现得「像」有情感共鸣，用户的信任和责任归因就会被系统性地改变——而且这种改变是可以被公司设计利用的。",
            "this_point": "Abstract · \"the purported anthropomorphic attributes of LLMs are empirically non-unique: although some properties (e.g., responses to prompts) could remain invariant, others, such as the interpretation of their perceived behaviour, might change with the substrate.\"",
            "that_point": "Abstract · \"anthropomorphism simultaneously increases user trust while deflecting accountability from developers. These dynamics create a responsibility gap with significant implications for AI governance and institutional accountability.\"",
        },
        {
            "slug": "pavel-durov-telegram-freedom-resistance",
            "kind": "tension",
            "relation": "张力",
            "why": "这篇论文指出公司在拟人化 AI 设计上存在「结构性激励」——既提升信任又转移责任，双重有利。Durov 的商业实践构成一个反例：Telegram 不用算法信息流、不用个人数据变现，主动放弃了80%的潜在广告收入，选择了一条明显更难、更慢的盈利路径，而不是利用论文里描述的那类心理操纵机制去最大化参与度和信任。这构成一个值得追问的张力：论文论证的是「结构性激励」存在，但 Durov 案例说明这种激励并非不可抗拒——至少存在不利用它、依然能盈利的设计选择，只是这条路径需要更长的耐心和更彻底的所有权结构（100%自持）作为支撑。",
            "this_point": "General Discussion · \"anthropomorphism offers a twofold advantage companies may exploit when designing LLM assistants, underscoring the need for regulations that counterbalance such incentives.\"",
            "that_point": "[03:55]-[04:10] Durov 的商业模式：上下文广告不使用个人数据，主动放弃80%的潜在广告收入；2024年首次盈利，没有用算法信息流去最大化用户参与度和情感依赖。",
        },
    ],
    "en_title": "The Effects of AI Anthropomorphism on Trust and Responsibility · Victoria Oldemburgo de Mello et al.",
    "en_tags": ["AI anthropomorphism", "trust game", "blame displacement", "emotional attunement", "AI governance"],
    "en_connections": [
        {
            "slug": "if-llms-have-human-like-attributes-age-of-empires",
            "kind": "resonance",
            "relation": "The two papers argue the same point from two directions: whether an LLM 'genuinely' possesses human-like attributes, and whether humans will 'behave as if' it does, are two completely separate questions — and it's the second one that actually has consequences. de Wynter's paper proves that any sufficiently complex system (even a simple neural network trained on Age of Empires II) can be read by an observer as having anthropomorphic attributes, showing these attributes are a product of representation, not an essential property unique to LLMs. Oldemburgo de Mello et al.'s paper proves the real-world consequence of exactly this: regardless of whether an AI genuinely has emotions, the moment it merely appears to show emotional attunement, users' trust and blame attribution shift systematically — and that shift can be exploited by deliberate design.",
        },
        {
            "slug": "pavel-durov-telegram-freedom-resistance",
            "kind": "tension",
            "relation": "This paper argues that companies have a 'structural incentive' to design anthropomorphic AI — it's a twofold win, boosting trust while deflecting accountability. Durov's actual business practice is a counterexample: Telegram runs no algorithmic feed, doesn't monetize personal data, and deliberately forgoes 80% of potential ad revenue, choosing a path to profitability that is obviously harder and slower instead of exploiting the kind of psychological-manipulation mechanism the paper describes to maximize engagement and trust. This raises a tension worth asking about: the paper argues the structural incentive exists, but Durov's case shows that incentive isn't irresistible — there is at least one design choice that doesn't exploit it and still turns a profit, though it requires far more patience and a far more absolute ownership structure (100% self-held) to sustain.",
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
