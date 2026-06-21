"""Publish john-mackey-whole-foods-44-years using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "john-mackey-whole-foods-44-years",
    "report": "reports/john-mackey-whole-foods-44-years.md",
    "url": "https://youtu.be/U8zqsiePKsg?si=tAe-6DiWmUOT_iCn",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "44年的布道者与全食超市的征服 · John Mackey",
    "tags": ["创业哲学", "使命驱动", "资本主义", "创业精神", "内在成长"],
    "connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "同构",
            "why": "Mackey 的「布道者 vs. 雇佣兵」框架和 Rubin 的「教堂生意 vs. 银行生意」框架是对同一个底层差异的两种命名——一种工作取向以相信产品本身的价值为前提，另一种以商业可行性为前提。Mackey 用这个框架解释了为什么他能和某些联合创始人合作、不能和另一些合作；Rubin 用来解释 Iovine 和他的差异。两者都认为两种取向都能成功，但必须认清自己是哪种。",
            "this_point": "[00:02-01:57] Mackey 说布道者和雇佣兵之间「没有对错」，但他们的游戏规则完全不同——布道者愿意20年复利，雇佣兵寻求快速出口；两者共处一家公司是灾难的根源。",
            "that_point": "[55:42-56:09] Rubin 说 Jimmy Iovine 的框架——「银行生意」（商业底线逻辑，这首歌会给你买一栋房）vs.「教堂生意」（信仰与激情，我听到了什么，我知道它很了不起）——是两种截然不同的职业取向，两者都能成功，但需要认清自己是哪种人。",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "张力",
            "why": "两人在同一次录音里相互引用对方——Mackey 说他准备去听 Dyson 的那期，并讨论了 Dyson「失败比成功更有趣」的主题。Mackey 轻轻地推回了一下：「成功也是有趣的，你从两者都能学到，只是从失败学到的更多。」这是对 Dyson 核心命题的唯一一次公开的、诚实的分歧——不是驳倒，而是修正为双轨版本（两者都有价值，但失败的信息密度更高）。",
            "this_point": "[01:02:53-01:03:13] Mackey 听到 Senra 引用 Dyson「失败比成功更有趣」的框架后，温和地推回：「成功也是有趣的……但你确实从失败中学到更多，因为你必须学。学习或死亡。」",
            "that_point": "[03:58-04:29] Dyson 说失败本质上比成功更有趣，因为失败迫使你质疑「为什么出了问题」——而成功时你只说「太好了」就继续了，不会深究为什么成功。",
        },
    ],
    "en_title": "44 Years of Building Whole Foods · John Mackey",
    "en_tags": ["entrepreneurial philosophy", "mission-driven", "capitalism", "founder psychology", "inner growth"],
    "en_connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Mackey's 'missionary vs. mercenary' framework and Rubin's 'church business vs. banking business' framework are two names for the same underlying distinction — one orientation presupposes belief in the product's value as the primary driver, the other presupposes commercial viability; both argue neither is wrong, but mixing them in a single partnership is the source of most co-founder conflict",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both appear in the same recording — Mackey says he's about to listen to Dyson's episode, then gently pushes back on Dyson's 'failure is more interesting than success' thesis: 'success is interesting too... but you learn more from failure because you have to, learn or die' — the only public, honest disagreement with Dyson's central claim in the entire corpus, correcting it to a dual-track version rather than refuting it",
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
