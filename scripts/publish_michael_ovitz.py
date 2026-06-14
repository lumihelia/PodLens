"""Publish michael-ovitz-caa-frame-of-reference using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "michael-ovitz-caa-frame-of-reference",
    "report": "reports/michael-ovitz-caa-frame-of-reference.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "参照系与制霸好莱坞 · Michael Ovitz",
    "tags": ["好莱坞", "经纪人", "参照系", "组织建设", "销售哲学"],
    "connections": [
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都承认自己童年的物质匮乏记忆从未真正离开，并将它视为持续竞争驱动力的来源——但提取方式不同。Garry 是蓄意的：他能「随时走进那间屋子」取出放射性能量。Ovitz 的是不由自主的：他在餐厅菜单上无意识地看价格，虽然他早就不需要在乎钱了。两种形式，同一个来源：原始的匮乏和「不能回到那里」的恐惧，从未完全被后来的成功覆盖，持续提供燃料。",
            "this_point": "[01:55:55-01:56:35] Ovitz 说他的父亲会带他们去5:50的早鸟特惠餐厅（不允许点超出预算的菜）。「现在我不看账单，但我发现自己有时会自动看菜单价格，没有任何必要。那是我的童年，它偶尔会压过我。」他把这认为是积极的——让他仍然感到想要赢。",
            "that_point": "[01:52:14-01:53:20] Garry 描述他能「随时走进那间屋子」——七岁时的公寓，父亲随时可能喝醉打人——然后他的七岁自己「倒出一杯放射性铀235，我带着那杯走进我的一天——我有了它。」主动提取，而不是被动侵入。",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都把信息摄入量（而不是先天能力）识别为真正的护城河：Dyson 的5127个原型 = Ovitz 的每天200张图像 + 210本杂志订阅 + 70年好莱坞档案通读。两人都把这描述为一种「可以被蓄意建立」的能力，而不是天赋。Ovitz 字面上称之为「原始版 AI，机器学习，只是机器是我的大脑」；Dyson 用5127个原型在工程领域做了同样的事。都是用压倒性的信息体量建立竞争对手无法复制的判断力基础设施。",
            "this_point": "[34:56-35:56] Ovitz 说他每天看200张图像，「机器学习，我的大脑是那台机器——我放进去的图像越多，识别精度越高。」他还订阅了210本杂志、通读了好莱坞70年档案，以便在见任何人时都能「说他们的语言」。",
            "that_point": "[04:05-04:29] Dyson 说失败比成功更有趣，因为「失败你会质疑它，成功了你只说'太好了'就继续了」——每次失败都是信息密集的调查起点；5127个原型是把这个原则放大到商业可行性的规模。",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都把「诚实」制度化为核心竞争优势，而不仅仅是道德选择。Ovitz 的「不知道就说不知道」在1974年娱乐行业的谎言生态里是革命性的；Mackey 的「布道者」框架里同样包含了对「用真实信仰代替算计」的坚持。更深的共同点：两人都相信信任可以复利——Mackey 通过20年的天然食品网络得到了信任收购，Ovitz 通过退还可口可乐的支票建立了最有利可图的广告客户关系。诚实不是美德，是商业策略。",
            "this_point": "[01:01:30-01:02:23] Ovitz 说在1974年的娱乐行业，「每个人都觉得必须显得无所不知，所以每个人都撒谎。」他制定了一条制度：「如果你不知道答案，这是你的回答：'我不知道，我会回你电话。'撒谎的人永远无法把同一个故事说对两遍。」",
            "that_point": "[00:02-01:57] Mackey 说布道者和雇佣兵之间「没有对错」，但他的核心优势来自真实信仰——他雇不到他认为只是来拿钱的人，因为长期来看信仰的人会比计算的人走得更远更稳定，就像他的天然食品网络最终成了信任收购管道。",
        },
    ],
    "en_title": "Frame of Reference and the Conquest of Hollywood · Michael Ovitz",
    "en_tags": ["Hollywood", "talent agency", "frame of reference", "organization building", "sales philosophy"],
    "en_connections": [
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "Both acknowledge their childhood scarcity memories never fully left and treat them as ongoing motivational fuel — but in opposite control modalities: Garry's is deliberate (he 'walks into that room' and extracts plutonium energy at will); Ovitz's is involuntary (he finds himself automatically checking menu prices despite not needing to) — the same underlying origin story operating as conscious tool in one case and unconscious reflex in the other",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both identify information volume (not innate ability) as the real moat: Dyson's 5,127 prototypes = Ovitz's 200 images per day + 210 magazine subscriptions + 70 years of Hollywood archives — both describe this as a capacity that can be deliberately built rather than inherited; Ovitz literally calls it 'primitive AI — machine learning, my brain is the machine'; Dyson built the same information infrastructure in engineering; both created judgment capacity that competitors couldn't replicate because they couldn't match the input volume",
        },
        {
            "slug": "john-mackey-whole-foods-44-years",
            "kind": "resonance",
            "relation": "Both institutionalized honesty as competitive advantage rather than just ethical virtue: Ovitz's 'I don't know, I'll call you back' was revolutionary in a 1974 entertainment industry built on performative omniscience; Mackey's 'missionary' framework included replacing calculation with genuine belief; both discovered that trust compounds — Mackey's natural foods network became an acquisition pipeline built entirely on trust; Ovitz's returned Coca-Cola check became his most profitable client relationship",
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
