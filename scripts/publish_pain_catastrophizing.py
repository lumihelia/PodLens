"""Publish pain-catastrophizing-critical-review (0624 batch).

Restructured into the standard paper template. Content and authors were
already verified faithful against the extracted PDF text in
材料/0624/extracted; no citation fix needed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "pain-catastrophizing-critical-review",
    "report": "reports/0624/pain-catastrophizing-critical-review.md",
    "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2696024/",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "疼痛灾难化：一篇批判性综述 · Phillip Quartana et al.",
    "tags": ["疼痛灾难化", "认知行为", "慢性疼痛", "注意偏向", "共同应对模型"],
    "connections": [
        {
            "slug": "two-arrows-of-pain-meditation-aversion-identification",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文从认知行为科学和佛教心理学两个完全不同的传统，描述了同一个机制的两种语言版本。Pain Catastrophizing 综述里的「反刍」和「无助」，与 Two Arrows of Pain 里佛教「两支箭」框架中的「第二支箭」（对疼痛的厌恶性心理反应）指向的是同一种心理过程——疼痛本身（第一支箭/生理损伤）相对固定，而由心理反应叠加上去的额外痛苦才是真正可以被干预、被测量、被改变的部分。一篇用 fMRI 和 PCS 量表给出神经科学和心理测量证据；一篇用 Granger 因果分析证明冥想如何作用于这同一过程的因果链上游。",
            "this_point": "CNS Mechanisms · \"catastrophizing associated with diminished endogenous pain inhibition\"",
            "that_point": "§The Two Arrows · the Buddhist framework distinguishing the first arrow (unavoidable physical pain) from the second arrow (the additional suffering created by aversion and resistance to that pain).",
        },
    ],
    "en_title": "Pain Catastrophizing: A Critical Review · Phillip Quartana et al.",
    "en_tags": ["pain catastrophizing", "cognitive behavioral", "chronic pain", "attention bias", "communal coping model"],
    "en_connections": [
        {
            "slug": "two-arrows-of-pain-meditation-aversion-identification",
            "kind": "resonance",
            "relation": "The two papers describe the same mechanism in two completely different traditions — cognitive-behavioral science and Buddhist psychology. The 'rumination' and 'helplessness' in the Pain Catastrophizing review point to the same psychological process as the 'second arrow' (the aversive mental reaction to pain) in the Two Arrows of Pain's Buddhist framework — the pain itself (the first arrow, the physiological injury) is relatively fixed, while the additional suffering layered on by the mental reaction is exactly the part that can be intervened on, measured, and changed. One paper offers neuroscience and psychometric evidence via fMRI and the PCS scale; the other uses Granger causality analysis to prove how meditation acts on the causal upstream of that exact same process.",
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
