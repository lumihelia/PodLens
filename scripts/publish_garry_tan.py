"""Publish garry-tan-yc-personal-ai-revolution using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "garry-tan-yc-personal-ai-revolution",
    "report": "reports/garry-tan-yc-personal-ai-revolution.md",
    "url": "https://youtu.be/bTxALvFKP8M?si=NluV8wvfo-MylOyk",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "YC、个人AI与那间七岁的屋子 · Garry Tan",
    "tags": ["YC创始文化", "个人AI", "技术民主化", "建造者伦理", "创始人心理"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构",
            "why": "Garry 的技术民主化谱系（火→书→印刷机→PC→AI，每次革命都把一个只有「祭司阶层」才能接触的能力交给所有人）与 Gopnik 对文化技术（写作、科学、学校教育）作为「认知棘轮」的论述在核心命题上完全重合：每种新技术都在扩展集体智慧的边界，AI 是这个链条的下一环而不是断裂。Garry 从创业生态的角度叙述，Gopnik 从认知科学的角度叙述，指向同一个结论：「让更多人进入」永远是技术的真正革命性。",
            "this_point": "[26:45-28:15] Garry 说「识字从一个祭司的小圈子突然变成每个人都能做的事——这就是每次关键时刻反复出现的模式。PC 是'无限之书'，iPhone 把 PC 放进口袋，AI 是智能计算机——同一条链条，下一环。」",
            "that_point": "[44:00-47:30] Gopnik 说语言、写作和科学是「文化棘轮」——每一代人不需要重新发明轮子，可以继承并超越前人的认知成就；AI 是这个过程的下一个工具，让个体能接触到原本只有专业训练才能触及的思维能力。",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都字面上使用「上帝给了你这个大脑」来描述创业的使命感，都把技术或商业定义为「服务彼此」的工具而不仅仅是经济活动，都将创业明确表述为一种精神旅程（Mackey：英雄之旅；Garry：从无神论到基督徒的信仰转变，Act 17 项目）。但触发点不同：Mackey 的使命感来自对天然食品行业本身价值的信仰；Garry 的使命感来自一笔具体的个人债务——「技术给了我一切，我想让所有人都拥有它」。",
            "this_point": "[01:26:02-01:26:27] Garry 说：「上帝给了你这个大脑和这些感知，我们能做如此之多。我们怎么能做更多？怎么能更好地服务彼此？技术肯定不是坏事——它就是一种服务彼此的方式。」",
            "that_point": "[01:38:57-01:39:43] Mackey 说创业之旅在最深层是一种英雄之旅，同时也是精神旅程——它要求你回应一个无法完全被外部理性化的内在召唤；他使用冥想、breathwork 和致幻剂作为精神工具（而不是治疗工具）来接触更深层的自我。",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "张力",
            "why": "两人都维持了数十年的极高强度工作，驱动力都与内在的未解决之处有关，但提取能量的方式在结构上相反：Rubin 几乎无法忍受创作过程，他的坚持来自等待一个外部的、无法预期的「天启时刻」（被动接收）；Garry 能随时主动走进「那间屋子」并从特定的创伤记忆中蓄意汲取能量（主动提取）。两人的访谈者都问了同一个问题：「这种强度可持续吗，它会不会烧毁你周围的人？」两人的回答都是：「我还在解决这个问题。」",
            "this_point": "[01:52:14-01:53:20] Garry 描述他能「随时走进那间屋子」——七岁时的公寓，然后那个七岁的自己「倒出一杯放射性铀235，然后我带着那杯走进我的一天——我有了它。」这是一种有意识的、主动的创伤能量提取，而不是被动的创伤反应。",
            "that_point": "[24:36-25:48] Rubin 说他对过程几乎无法忍受，他只是强迫自己去上班，因为「如果我不在那里，奇迹就不会发生」——他的持续力来自对那个无法预期的外部天启时刻的依赖，而不是来自过程本身或内部蓄积的能量。",
        },
    ],
    "en_title": "YC, Personal AI, and the Seven-Year-Old's Room · Garry Tan",
    "en_tags": ["YC founder culture", "personal AI", "technology democratization", "builder ethos", "founder psychology"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Garry's technology democratization lineage (fire → writing → printing press → PC → AI, each revolution handing a priestly-class capability to everyone) and Gopnik's account of cultural technologies (writing, science, schooling) as 'cognitive ratchets' are two formulations of the same claim: each new technology expands the boundary of collective intelligence, and AI is the next link in that chain rather than a rupture — Garry argues from the startup ecosystem, Gopnik from cognitive science, both conclude that 'letting more people in' is always the true revolution",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "Both literally use 'God gave you this brain' to frame their entrepreneurial mission, both define technology or business as a tool for 'serving each other' rather than purely economic activity, and both explicitly describe entrepreneurship as a spiritual journey (Mackey: hero's journey + psychedelics as spiritual tools; Garry: atheist to Christian, Act 17 project) — but their triggering debt differs: Mackey's mission comes from belief in natural food's intrinsic value; Garry's from a specific personal ledger ('technology gave me everything, I want everyone to have it')",
        },
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Both sustain decades of extreme-intensity work from unresolved inner sources, but extract energy through structurally opposite mechanisms: Rubin can barely tolerate the process, sustained only by waiting for an external, unpredictable 'revelation moment' (passive reception); Garry can walk into 'that room' any time and deliberately extract energy from a specific traumatic memory (active extraction) — both interviewers asked the same question ('is this intensity sustainable, will it burn the people around you?') and both answers were: 'I haven't resolved this yet'",
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
