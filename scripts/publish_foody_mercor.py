"""Publish brendan-foody-mercor-teaching-ai-knowledge-work using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
    "report": "reports/brendan-foody-mercor-teaching-ai-knowledge-work.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "教 AI 的人与知识工作的未来 · Brendan Foody",
    "tags": ["AI训练", "知识工作", "评估体系", "劳动力市场", "强化学习"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "张力",
            "why": "Gopnik 主张 AI 是「文化技术」，因为它只汇总人类已有知识、永远无法主动接触外部现实；Foody 的 Mercor 正在系统性地把越来越多的隐性专家知识注入模型——这是一个对 Gopnik「文化技术」图景的动态挑战，暗示边界会随训练不断移动而非固定。",
            "this_point": "[23:04-24:11] Foody 说知识工作将转化为「构建 RL 环境」——专家把隐性知识外化为训练数据，模型持续吸收人类最高质量的判断能力；这个过程理论上没有上限。",
            "that_point": "[45:05-47:00] Gopnik 说 AI 是文化技术，做不到两岁儿童能做的主动实验；真正的智能体必须与物理世界互动产生新知识——而 Foody 的方案恰恰是继续深挖文化技术层面，而非突破它。",
        },
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "补充",
            "why": "Foody 区分「输出数据」（表层）和「评估数据」（深层）——后者让模型能反复尝试、打分、改进——这和 Efros 对「表层数据」（被动收集）vs「深层数据」（主动具身采集）的区分在结构上高度一致。两者都指向同一个结论：能衡量成功的反馈数据比纯内容数据更有价值。",
            "this_point": "[13:42-15:13] Foody 说评估数据（rubric、测试题、标准答案）远比输出数据（模型读的内容）宝贵，因为它让模型能「无限次尝试、不断打分、不断学习」——即形成真正的强化信号。",
            "that_point": "[20:15-21:00] Efros 说深层数据的关键是「物理世界的推回（pushback）」——当你对物体做错了，世界会告诉你；被动收集的表层数据缺乏这种反馈，因此无法训练真正的具身能力。",
        },
    ],
    "en_title": "The People Who Teach AI · Brendan Foody",
    "en_tags": ["AI training", "knowledge work", "evaluation systems", "labor markets", "reinforcement learning"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Gopnik argues AI is a fixed 'cultural technology' that can only aggregate existing human knowledge; Foody's Mercor is systematically injecting ever-deeper tacit expert knowledge into models — suggesting the cultural-technology ceiling is moving, not fixed, even without embodied interaction",
        },
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "Foody's distinction between output data (surface) and evaluation data (rubrics + graded answers that enable iterative learning) is structurally isomorphic to Efros's surface/deep data distinction — both identify feedback-rich data as the bottleneck, not content volume",
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
