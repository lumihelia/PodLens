"""Publish arthur-brooks-reinvention-religion-happiness using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "arthur-brooks-reinvention-religion-happiness",
    "report": "reports/arthur-brooks-reinvention-religion-happiness.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "重塑人生、宗教与幸福科学 · Arthur Brooks",
    "tags": ["幸福学", "人生意义", "宗教与信仰", "职业转型", "认知科学"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构",
            "why": "Brooks 的「AI 是左脑延伸，无法做右脑为什么问题」框架和 Gopnik 的「AI 是文化技术，无法做具身主动实验」框架在诊断层面完全一致——两者都精确识别了 AI 的同一个限制，只是一个从神经科学/意义角度切入，另一个从认知发展/具身学习角度切入。两个框架可以互相加强：AI 既无法给你有具身接地性的知识，也无法给你有个人重量的意义。",
            "this_point": "[35:33-36:22] Brooks 说 AI 是左脑（「如何」「是什么」）引擎，无法回答任何有个人重量的「为什么」问题；人类的比较优势是意义建构——最优策略是用 AI 解放左脑时间，投入到爱、信仰、关系、美和苦难理解等右脑活动。",
            "that_point": "[45:05-47:00] Gopnik 说 AI 是文化技术（cultural technology），聚合人类已有知识，做不到两岁儿童能做的与物理世界主动互动——真正的智能体必须有具身接地性，而不只是语言汇总。",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "张力",
            "why": "Foody 对 AI 替代知识工作高度乐观（GPT-5 已达 64%，五年内大多数知识工作者将成为模型训练者）；Brooks 则说最高价值的「为什么」问题创造力是人类不可替代的比较优势。两者并不矛盾，但构成了「AI 能替代什么」这个问题的两面：Foody 聚焦于「是什么/如何做」层的执行（左脑），Brooks 聚焦于「为什么」层的意义建构（右脑）——有意思的是，两人从不同角度得出了相同的结构性划分。",
            "this_point": "[37:50-38:50] Brooks 说 think tank 里做基本数据分析的员工需求会减少，但 AI 永远无法提出正确的政策问题——「为什么」问题的创造性是人类的比较优势，也是 AI 永远无法替代的那 25%。",
            "that_point": "[23:04-24:11] Foody 说知识工作将转化为「构建 RL 环境」——投行分析师不再做数据分析，而是训练 agent 做数据分析；五年内大多数高端知识工作者将成为模型训练者。",
        },
    ],
    "en_title": "Reinvention, Religion, and the Science of Happiness · Arthur Brooks",
    "en_tags": ["happiness science", "meaning", "religion and faith", "career reinvention", "cognitive science"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Brooks's 'AI as left-brain extension that cannot answer why-questions' and Gopnik's 'AI as cultural technology that cannot do embodied active experimentation' are structurally isomorphic diagnoses of the same AI limitation — one from neuroscience/meaning, one from cognitive development/embodied learning — and mutually reinforce each other",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "Foody is optimistic that AI will replace most knowledge work (GPT-5 at 64%, most knowledge workers as model trainers in 5 years); Brooks says the why-question creativity is the irreplaceable human comparative advantage — both diagnose the same structural split (left-brain execution vs. right-brain meaning) from opposite starting points",
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
