"""Publish adam-neumann-wework-flow-community using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "adam-neumann-wework-flow-community",
    "report": "reports/adam-neumann-wework-flow-community.md",
    "url": "https://youtu.be/RAHsF4A8GLM?si=yEde8Tld7lZRPiq1",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "集体农庄到WeWork：社区愿景的失控与重建 · Adam Neumann",
    "tags": ["集体农庄精神", "WeWork失控", "社区即使命", "叙事让渡", "真实性比钱更性感"],
    "connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "同构",
            "why": "Rick Rubin是这次对话的采访者（Tetragrammaton播客）。这不只是形式上的关联——整个对话的结构体现了Rick的核心哲学：创造空间让真相自然浮现，而不是追问；沉默作为知识的容器；最深的洞见在耗尽之后到来（Adam和Andrew在凌晨2点快要晕倒时命名了WeWork；Adam的低谷之后信念降临）。Adam第一堂Kabbalah课的核心教训「暂停，多奇妙」和Rick的「减法即增加」是同一个认知结构：不是更努力地推，而是创造空间让结果进来。Adam说「我一直在说话，现在开始想听了」——这是Rick《创意行为》的核心主旨：接受状态（receptive）比主动推动（active）更接近真正的创造。两人都相信：最重要的东西不是被「做出来」的，而是被「允许出现」的。",
            "this_point": "[00:26–02:12] Adam描述他的早晨习惯：「冥想的本质是听，祈祷是说话。我一直在说话，现在开始想听了。」[31:53–33:43] 第一节Kabbalah课：「暂停，多奇妙」——不是做更多，而是先停。[40:19–42:44] WeWork命名：凌晨2点两人精疲力竭、快要放弃的那一刻，名字才来——「当你已经说了所有能说的，沉默里才有空间让它进来。」[43:37–46:01] Rick总结：「当你在最低处，已经做完所有工作，话说完了，就有了空间。有时候工作的时候我们一直在说话，那里没有空间。当你用尽了说话的力气，它才能穿透进来。」",
            "that_point": "[里克·鲁宾集核心论点] Rick的「减法即增加」和「创意行为」：最重要的创意决策是删除什么，而不是添加什么。Ruthless edit（无情剪辑）让作品的本质浮现。他对采访本身的态度也是这个哲学的体现：他不主导，他等待；他不反驳，他创造空间。「创意揭示」（creative revelation）——作品不是被制造的，而是被揭示的，艺术家的任务是清理所有障碍直到它浮现。这与Adam的宇宙论框架（「宇宙在写故事，我们只是演员」）在结构上完全同构：两人都相信最重要的东西不是主动创造的，而是在特定条件下允许它出现的。",
        },
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "同构",
            "why": "Arthur Brooks的幸福科学框架与Adam Neumann的整个生命弧在三个层面上精确对应。第一，「交易性成功vs.挣得的成功」：Brooks说WeWork时代的Adam是「交易性成功」的典型——市值、估值、数字带来的是虚假的满足感，不能持久。Adam自己也说：从Masa车里走出来的每一步，「自我在涨潮」，使命从「社区」悄然变成了「增长数字」。第二，「超越性」（transcendence）作为幸福的真实来源：Brooks引用研究说宗教实践者更快乐、更有韧性。Adam的整个叙事结构正是这个命题的实例——是Kabbalah课、安息日、灵性老师的一个电话，让他在2019年的最低点撑住了，而不是任何商业计划。第三，「再创业」（re-invention）哲学：Brooks谈到「螺旋形职业」——不是直线向上，而是在每一次下行后以更高的意识回来。Adam从WeWork到Flow正是这条路：同一个核心愿景（kibbutz社区），更深的自我认识，更好的伙伴选择。",
            "this_point": "[01:09:20–01:14:39] 「从那辆车走出来的每一步，自我在涨潮。使命从社区悄悄换成了数字。那不是Masa造成的，是我那时的灵性水平还没到那里。」[01:41:44–01:48:05] 2019年低谷：灵性老师说「在飞的时候相信宇宙不叫信念，那叫常识。信念是一切崩塌时你还能选择向上看。」[02:49:50–02:58:03] 安息日作为具体实践：「把手机放进饼干罐24小时。连续三小时感到手想摸口袋，说明你上瘾了。」以及「安静的革命」——年轻人回归教堂。",
            "that_point": "[Arthur Brooks集核心论点] Brooks的三种幸福成分（享乐、达成、意义）中，「意义」是最稳定的——来自家庭、信仰、人际联系、创造性工作。他说人们在中年危机时的错误是试图用更多的成就（交易性成功）来填补内心的空洞，而解决方案是转向超越性（transcendence）——宗教、精神实践、服务他人。他还具体指出冥想和祈祷的神经科学证据：改变大脑的激活模式，降低杏仁核反应性。Brooks的「spiral career」（螺旋形职业）和Adam的从WeWork到Flow的路径在结构上完全相同：以更高的意识、更少的恐惧、更准确的自我认识回到同一个核心使命。",
        },
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "张力",
            "why": "Tobi和Adam都经历了「使命漂移」的失控期，也都在反思中找到了更清醒的版本。但他们的核心诊断和解决方案截然相反，形成了关于「创始人与公司关系」最有张力的对话之一。Tobi的诊断：公司对特定创始人的依赖是一种风险，解决方案是建立Shopify OS——一个不依赖Tobi的系统性透明度机器。Adam的诊断：公司的使命感直接来自创始人的灵性状态，解决方案是让自己「灵性水平」更高，而不是建立一个替代这种状态的系统。Tobi在去除Tobi依赖；Adam在强化Neumann依赖（Flow的一切都扎根于他的个人愿景和a16z对他个人判断的信任）。更深的张力在「COVID重置时刻」：Tobi的COVID时刻是他发现自己16小时审查每个项目、取消60%并替换所有高管——他的结论是需要建立系统让这些判断不依赖他在场。Adam的COVID时刻是他在以色列静静待着，确认自己的愿景是对的——他的结论是需要找到真正相信这个愿景的合作伙伴（Mark and Ben）。一个向内建系统，一个向内深化使命。",
            "this_point": "[02:33:32–02:44:28] Flow的愿景与a16z合作结构：「Mark说，你的核心使命是社区和所有权，如果你真的做到，这会是一个改变世界的生意。他不是在说增长更快，而是在说做得更深、花更多时间做对的产品。」[02:39:47–02:42:10] Flow的CTO选择完全基于Adam和Ben之间的信任：「他选了WhatsApp的那个，不是Amazon的那个。我问他为什么，他说是因为那个人在会议上听到蠢话时脸上藏不住。」Flow的架构逻辑就是这样的人：小团队，极高标准，由创始人的判断和董事会的判断共同守护。",
            "that_point": "[Tobi集核心主题] Tobi的COVID重置：他发现自己「扮演一个严肃的上市公司CEO」多年，实际上是把公司托付给了高管层。COVID迫使他亲自审查每个项目——取消60%，替换所有高管。他的结论是需要建立Shopify OS：用Python+SAT求解器把整个公司结构写成机器可读配置文件，让所有人看到每一个决策的后果，消除政治，让系统在没有Tobi的情况下也能运作。这与Adam的结论相反：Adam的解决方案是找到Mark和Ben——因为他们告诉他实话（而不是他想听的），而不是建立一个消除他的系统。Shopify正在去除创始人依赖，Flow正在优化创始人的判断质量。",
        },
    ],
    "en_title": "Kibbutz to WeWork to Flow: The Community Vision, the Fall, and the Rebuild · Adam Neumann",
    "en_tags": ["kibbutz spirit", "WeWork collapse", "community as mission", "narrative surrender", "authenticity over wealth"],
    "en_connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Rick Rubin is the interviewer — this is his Tetragrammaton podcast. The structural resonance runs deeper than format. Neumann's first Kabbalah lesson — 'Pause. What a wonder.' — is the same cognitive architecture as Rubin's 'less is more': don't push harder, create space for a different answer to arrive. Neumann says explicitly: 'I've been doing a lot of talking. I'm starting to want to listen.' The WeWork name itself arrived at the moment of exhaustion and near-surrender, not during concentrated effort. Rubin's observation, sitting across from Neumann: 'When you've talked until you're empty, there's space. That's when it comes through.' Both believe the most important things aren't made — they're allowed to appear.",
        },
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "Brooks's happiness science maps almost exactly onto Neumann's life arc. Brooks distinguishes earned success from transactional success: WeWork's peak valuation was transactional — numbers, metrics, external validation — and it collapsed. What Neumann calls 'the mission' was earned. Brooks argues that transcendence — religious practice, spiritual community, service — is the most durable source of happiness and resilience. Neumann's account shows this in operation: it was the spiritual teacher's phone call, not any business plan, that held him together in 2019. Brooks's 'spiral career' — returning to the same core mission at a higher level of self-knowledge — describes the arc from WeWork to Flow precisely. Same underlying vision (the kibbutz), better self-awareness, better partner selection.",
        },
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "Both Lütke and Neumann went through a 'mission drift' period — Lütke 'cosplaying a serious public company CEO,' Neumann watching the mission shift from community to growth numbers in real time. Both had a reset moment around COVID. But their diagnoses and solutions are opposite. Lütke's conclusion: founder-dependence is a structural risk; build Shopify OS so the company can make correct decisions without Tobi present. Neumann's conclusion: the company's soul comes directly from the founder's internal state; find partners who will tell you the truth (Andreessen and Horowitz) rather than build a system that replaces your judgment. Shopify is systematically removing Tobi-dependence. Flow is optimizing the quality of Adam's judgment. The deep tension: what happens to each company when the founder is genuinely absent?",
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
