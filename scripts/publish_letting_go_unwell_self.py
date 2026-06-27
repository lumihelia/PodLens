"""Publish letting-go-unwell-self-chronic-conditions (0624 batch).

Restructured into the standard paper template; corrected author byline
(Chloe Wells, not "Craig Williamson") and the placeholder DOI. Content
verified faithful against 材料/0624/extracted.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "letting-go-unwell-self-chronic-conditions",
    "report": "reports/0624/letting-go-unwell-self-chronic-conditions.md",
    "url": "https://doi.org/10.1007/s12671-025-02682-w",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "放下「病患自我」：慢性病中的无我觉察 · Chloe Wells et al.",
    "tags": ["无我", "佛教心理学", "慢性病", "身份认同", "正念"],
    "connections": [
        {
            "slug": "two-arrows-of-pain-meditation-aversion-identification",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文都建立在佛教「两支箭」框架上，描述的是同一个机制在不同时间尺度上的版本。Two Arrows of Pain 用 Granger 因果分析证明，「认同感」（这是我的痛）在时间上先于疼痛加剧出现——认同是疼痛的上游变量，不是结果。Letting Go of the Unwell Self 描述的是同一个认同过程被拉长到数月、数年后的样子：当「这是我的痛」反复发生，逐渐固化成「我是一个病人」的身份叙事，这种身份融合本身又会反过来加重疼痛灾难化和功能损害。一篇是实验室里测出的瞬时因果链，一篇是临床观察到的长期身份结果，描述的是同一条因果线的两端。",
            "this_point": "Attachment to Identity · \"higher levels of intertwinement are associated with greater levels of disruption to daily life due to pain catastrophising and the impact of symptoms, both physical and emotional (Paschali et al., 2021)\"",
            "that_point": "§Relationships with the Models · \"The identification state in the previous trial predicted the pain experience at the next trial, in terms of causal influence.\"",
        },
        {
            "slug": "pain-catastrophizing-critical-review",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文从两个不同的研究传统——佛教心理学的临床指南 vs. 疼痛医学的系统综述——独立指向同一个变量：一个人和自己疼痛/疾病之间的「认同与叙事关系」，比疼痛本身的生理强度更能预测心理痛苦和功能损害。Pain Catastrophizing 的综述显示，灾难化思维（放大、反刍、无助）本身会加剧疼痛体验；Letting Go of the Unwell Self 描述的「身份融合」（schema-enmeshment）则是灾难化思维背后更深层的身份结构——当一个人把疾病编织进「我是谁」的核心叙事，灾难化思维就有了更稳固的心理基础去反复发生。",
            "this_point": "Attachment to Identity · \"higher levels of intertwinement are associated with greater levels of disruption to daily life due to pain catastrophising and the impact of symptoms, both physical and emotional (Paschali et al., 2021)\"",
            "that_point": "§Expert Commentary · \"enough evidence has accumulated to suggest that high levels of catastrophizing about pain should be considered a 'risk marker' for adverse immediate and long-term pain-related outcomes.\"",
        },
    ],
    "en_title": "Letting Go of the \"Unwell Self\" in Chronic and Life-Challenging Conditions · Chloe Wells et al.",
    "en_tags": ["non-self", "Buddhist psychology", "chronic illness", "identity", "mindfulness"],
    "en_connections": [
        {
            "slug": "two-arrows-of-pain-meditation-aversion-identification",
            "kind": "resonance",
            "relation": "Both papers build on the Buddhist 'two arrows' framework, describing the same mechanism at two different timescales. The Two Arrows of Pain uses Granger causality analysis to prove that 'identification' (this is my pain) appears before pain intensifies in time — identification is an upstream variable for pain, not a downstream result. Letting Go of the Unwell Self describes what that same identification process looks like stretched out over months or years: as 'this is my pain' repeats, it gradually hardens into the identity narrative 'I am a sick person' — and that identity fusion, in turn, makes pain catastrophizing and functional impairment worse. One paper measures the instantaneous causal chain in a lab; the other observes the long-term identity outcome clinically — they're describing two ends of the same causal line.",
        },
        {
            "slug": "pain-catastrophizing-critical-review",
            "kind": "resonance",
            "relation": "The two papers, from entirely different research traditions — a Buddhist-psychology clinical guideline versus a systematic review in pain medicine — independently point at the same variable: the narrative relationship a person has with their own pain or illness predicts psychological distress and functional impairment more than the physical intensity of the pain itself. Pain Catastrophizing's review shows that catastrophic thinking (magnification, rumination, helplessness) itself worsens the pain experience; Letting Go of the Unwell Self describes 'schema-enmeshment' as the deeper identity structure underneath catastrophic thinking — once illness is woven into the core narrative of 'who I am,' catastrophic thinking has a far more stable psychological foundation to keep recurring on.",
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
