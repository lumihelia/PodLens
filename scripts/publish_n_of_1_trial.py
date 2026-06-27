"""Publish n-of-1-clinical-trial-individualizing-medicine (0624 batch).

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
    "slug": "n-of-1-clinical-trial-individualizing-medicine",
    "report": "reports/0624/n-of-1-clinical-trial-individualizing-medicine.md",
    "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3118090/",
    "kind": "paper",
    "date": "2026-06-24",
    "title": "n-of-1 临床试验：个体化医疗的终极策略？· Elizabeth Lillie et al.",
    "tags": ["n-of-1试验", "个体化医疗", "临床均势", "自我实验", "精准医疗"],
    "connections": [
        {
            "slug": "the-curse-of-optionality-tim-ferriss-founder-mindset",
            "kind": "resonance",
            "relation": "同构",
            "why": "两者描述的是同一个愿景在不同时代的版本：用个体层面的反复测量，绕开传统大规模人群研究的繁琐流程,直接为单个个体（或单个受试者群体）找到最优答案。Lillie 等人在2011年系统论证了 n-of-1 试验的方法论合理性,并指出无线医疗设备会是关键的使能技术;Tim Ferriss 在播客中构想的「分布式科学」方案——用 Oura Ring、WHOOP 等可穿戴设备和家用血样采集技术,绕开传统学术机构 IRB 的漫长审批周期——正是这篇论文十几年前预言的技术路径变成现实后的延伸版本，只是把范围从「单个患者的最优治疗」扩展到了「大规模去中心化的生理学研究」。",
            "this_point": "Issues & Future Directions · \"Coordinated n-of-1 trials have the potential to radically change the way in which evidence-based and individualized medicine is pursued. The availability of relevant wireless clinical monitoring devices...will enhance their value.\"",
            "that_point": "[17:56]-[19:50] Tim Ferriss 构想分布式科学研究模型：通过 Oura Ring/WHOOP 和家用血样采集技术开展去中心化临床研究，绕开传统学术机构 IRB 漫长周期的招募效率瓶颈。",
        },
        {
            "slug": "pain-catastrophizing-critical-review",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文从两个方向论证了同一个事实：人群层面的平均效应,系统性地掩盖了个体之间巨大的真实差异。Pain Catastrophizing 的综述指出,同样的身体损伤,不同人感受到的痛苦程度可以天差地别——疼痛灾难化这个心理变量是这种差异的关键来源之一。n-of-1 试验论文则证明了,如果你直接对个体本人做反复测量,而不是依赖人群平均结论,可以揪出那些「对大多数人有效但对这个人完全无效」的过度治疗——Mahon 等人的茶碱研究就是一个具体例证。",
            "this_point": "Combining n-of-1 Trials (Mahon et al.) · \"less theophylline use without adverse effects on exercise capacity or quality of life... clinically important bias towards unnecessary treatment during open prescription\"",
            "that_point": "§Expert Commentary · 不同个体对同等程度伤害性刺激的疼痛体验和功能损害程度差异巨大，疼痛灾难化是这种个体差异背后的核心心理机制之一。",
        },
    ],
    "en_title": "The n-of-1 Clinical Trial: The Ultimate Strategy for Individualizing Medicine? · Elizabeth Lillie et al.",
    "en_tags": ["n-of-1 trials", "individualized medicine", "clinical equipoise", "self-experimentation", "precision medicine"],
    "en_connections": [
        {
            "slug": "the-curse-of-optionality-tim-ferriss-founder-mindset",
            "kind": "resonance",
            "relation": "Both describe the same vision in different eras: using repeated individual-level measurement to bypass the slow machinery of traditional large-scale population studies and find the optimal answer directly for a single individual (or a single pool of subjects). Lillie et al. systematically argued the methodological case for n-of-1 trials in 2011 and identified wireless medical devices as the key enabling technology to come; Tim Ferriss's vision of 'distributed science' on the podcast — using wearables like the Oura Ring and WHOOP plus at-home blood-sample collection to bypass the long IRB approval cycles of traditional academic institutions — is the extension of exactly the technology path this paper predicted over a decade earlier, just scaled up from 'optimal treatment for one patient' to 'large-scale decentralized physiological research.'",
        },
        {
            "slug": "pain-catastrophizing-critical-review",
            "kind": "resonance",
            "relation": "The two papers argue the same fact from two directions: population-level average effects systematically obscure enormous real differences between individuals. Pain Catastrophizing's review notes that the same physical injury can produce wildly different levels of suffering in different people — pain catastrophizing is one key source of that variation. The n-of-1 trial paper proves that if you repeatedly measure the individual directly, rather than relying on population-average conclusions, you can catch cases of overtreatment that work 'for most people' but do nothing for this particular person — Mahon et al.'s theophylline study is a concrete example.",
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
