"""Publish james-dyson-5127-prototypes-invention using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "james-dyson-5127-prototypes-invention",
    "report": "reports/james-dyson-5127-prototypes-invention.md",
    "url": "https://youtu.be/Se64B8TKfjA?si=7yTNRW0n8_3-H-Lv",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "5127次原型与发明家的宿命 · James Dyson",
    "tags": ["发明与创新", "工程哲学", "失败与坚持", "制造业", "专注力"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构",
            "why": "Dyson 的「天真即优势」论和 Gopnik 的高温搜索论是同一个认知命题的两个版本：有经验的人做低温（目标性）搜索，知道哪里不能去；天真的人做高温（随机）搜索，找到经验者永远看不见的解。Dyson 雇用 17-18 岁学生、创办 Dyson 大学，正是将高温搜索制度化——他的核心商业决策建立在和 Gopnik 儿童认知论完全相同的前提上。",
            "this_point": "[11:47-12:25] Dyson 说有经验的人「知道为什么不该做某事」，而天真的人「想得更努力、更智慧」因为他们不知道如何解决问题——这是他创办 Dyson 大学（只招 17-18 岁学生并付薪 £45,000）的核心认知前提。",
            "that_point": "[29:44-31:30] Gopnik 说高温搜索（儿童式探索）能找到通过有目的性低温搜索（成人科学家）永远找不到的全局最优解——约束越少、探索越随机，意外发现的质量反而更高。",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "张力",
            "why": "两人都维持了 50 年以上的高强度工作，但驱动力的认知结构完全不同：Rubin 说他几乎无法忍受过程，只对那个无法预期的「天启时刻」上瘾——他是忍受过程以等待外部天启；Dyson 说「失败比成功更有趣」——他从每一次失败本身（内部的学习循环）中获得动力。两者都没有依赖「享受成功」来维持工作，但通往持续力的路径相反：Rubin 向外等待，Dyson 向内挖掘。",
            "this_point": "[04:05-04:19] Dyson 说失败是他的驱动力：「失败你会质疑它……成功了你说'太好了'，你甚至不会停下来想为什么成功了。」每次失败都是信息密集的调查起点，而不是需要克服的障碍。",
            "that_point": "[24:36-25:48] Rubin 说他对过程几乎无法忍受，他强迫自己去上班只是因为「如果我不在那里，奇迹就不会发生」——他的持续力来自对那个无法预期的「天启时刻」的成瘾，而不是对过程本身的任何喜爱。",
        },
    ],
    "en_title": "5,127 Prototypes and the Inventor's Fate · James Dyson",
    "en_tags": ["invention and innovation", "engineering philosophy", "failure and persistence", "manufacturing", "focus"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Dyson's 'naivete is more valuable than experience' thesis and Gopnik's high-temperature search theory are two versions of the same cognitive claim: experienced people do targeted low-temperature search (knowing where not to go); naive people do random high-temperature search (finding solutions experienced people filter out before they're even considered); Dyson institutionalized this by founding Dyson University to recruit 17-18 year olds — his core hiring policy rests on the same premise as Gopnik's developmental psychology",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Both sustained 50+ years of high-intensity work, but from completely opposite motivational structures: Rubin says he can barely tolerate the process, addicted only to the unpredictable 'revelation moment' (enduring process to wait for external arrival); Dyson says 'failure is more interesting than success' (extracting energy from each failure's internal learning loop) — neither depends on enjoying success to sustain the work, but the paths to persistence run in opposite directions",
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
