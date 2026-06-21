"""Publish marc-andreessen-malleable-world-founder-capitalism using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "marc-andreessen-malleable-world-founder-capitalism",
    "report": "reports/marc-andreessen-malleable-world-founder-capitalism.md",
    "url": "https://youtu.be/qBVe3M2g_SA?si=4nH-M9kcrb9AqiAB",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "世界比你想象的更可塑：零内省、创始人资本主义与马斯克方法 · Marc Andreessen",
    "tags": ["零内省", "创始人资本主义", "管理主义批判", "道德恐慌", "马斯克方法"],
    "connections": [
        {
            "slug": "caa-co-founder-michael-ovitz",
            "kind": "resonance",
            "relation": "同构",
            "why": "Marc在这集里明确说A16Z是以CAA为模型建立的：「集群进攻法——如果你有一个A16Z合伙人，你就有整个公司」「7点员工会议，在竞争对手叫醒自己客户之前先叫醒客户的客户」。Marc研究了Ovitz的方法并在VC行业完整复制了它。但两者之间有一个深层张力：Ovitz是Marc定义的「管理主义者」——当好莱坞环境改变时，他无法适应（Disney决策、DreamWorks失误）。Marc整个论点的核心是创始人比管理者更能适应变化，但他建立的组织却以管理者中最成功的一个（Ovitz）为模型。两者最大的共同点是对关系和渠道的垄断性控制——控制人才供给，然后以集群方式部署，制造不对称优势。",
            "this_point": "[约40:00-50:00] Marc描述A16Z以CAA为组织模型：「Ovitz发明的这种集群进攻法——整个公司一起出击。如果你有一个A16Z合伙人，你就有整个公司背书。」早晨优势：7点员工会议让他们在竞争对手九点开始工作之前，已经打完了第一轮客户电话——直接打给客户的客户，不是客户自己。Marc把这描述为A16Z最重要的组织创新之一，是他从对CAA历史的研究中直接提取的。",
            "that_point": "[书的内容贯穿全集] Ovitz建立CAA的核心洞察：经纪行业的价值不在个人代理人，在整个公司的集体力量。CAA在好莱坞早期的7点员工会议、在竞争对手醒来之前已完成第一轮行动、把整个公司作为一个整体向客户呈现——这些都是Marc在A16Z复制的具体实践。Ovitz后来的失败（Disney谈判、市场环境改变）也印证了Marc的管理主义批判：即使是最聪明的管理者，当环境根本性改变时也会失去方向，因为他们的成功模式是为稳定环境设计的。",
        },
        {
            "slug": "daniel-ek-impact-happiness-self-mastery",
            "kind": "resonance",
            "relation": "同构",
            "why": "Marc（通过IBM大灰云分析）和Daniel（通过Gustav的「你在这里没什么帮助」故事）分别从外部观察者和内部当事人两个角度诊断了同一个组织病理：**当一个人达到足够的权力和成功后，真相停止向他流动**。Marc的分析是系统性的——12层管理的复合谎言让IBM的CEO对公司实况一无所知，而他毫不知情地活在泡泡里。Daniel的分析是个人的——他的产品评审变成了一场「让Daniel满意的表演」，整个团队的能量用于管理他，而不是做产品。Marc的解法是Elon式的：打破层级，直接接触做事的人。Daniel的解法是关系式的：保留一批无论你有多成功都还在说真话的人（母亲、Jack、妻子、Gustav）。两者都承认这是成功本身制造的最危险的副作用。",
            "this_point": "[01:32:07-01:37:02] Marc用IBM和Elon对比：「IBM在我工作的时候有12层管理——我和CEO之间有12层。每一层都在向上一层撒小谎，12层之后，CEO对公司里真正发生的事情一无所知。他们有个词叫'大灰云'——一群灰色西装跟着CEO，确保他永远不会和任何真正在做事情的人说话。CEO感觉非常好，直到感恩节。」Elon的极端反面：「他只和工程师说话。当有问题时，他直接找到负责那个问题的工程师，一起待到解决。几乎没有CEO这样做。」",
            "that_point": "[32:03-35:27, 53:56-55:16] Daniel讲Gustav的故事：「Gustav告诉我：你在产品评审里没什么帮助。我们都在试图安抚你，而不是做真正的工作。」Daniel的第一反应：想解雇他。然后他意识到这是情绪反应，给了三个月观察期。结果：产品团队效率大幅提升，Spotify的产品能力在他退出产品评审后明显改善。「从那以后我就不再运营产品评审了。」——这是Daniel主动寻找并接受真相的故事；Marc分析的是真相被系统性阻断的故事。同一病理，一个有好结局，一个有坏结局。",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "张力",
            "why": "两人都把「从失败中学习」作为创造力的核心机制，但学习的方式截然不同。Dyson：亲手做5127个原型，每一个失败都是物理信息，体验在手上，知识通过身体积累。Marc：系统性研究历史失败模式——读Burnham 1941来理解2024年的资本主义，研究爱迪生的留声机预测错误来理解AI预测的局限，分析IBM的衰落来理解Elon方法的价值。Dyson学于做；Marc学于读和跨越历史的模式匹配。两者都到达同一个信念：当前的世界只是「应然状态」的原始近似——但一个人带着这个信念进实验室，另一个人带着它进风险投资。更深的张力：Dyson对「知识」的定义是具身的、失败驱动的、不可绕过的（你必须亲手失败5127次）；Marc的定义是模式化的、历史性的、可以通过学习他人经验来加速的（你不必亲手失败，可以从爱迪生的失败里学）。",
            "this_point": "[约20:00-35:00] Burnham框架：Marc通过读1941年的书来理解2024年的创业生态，「这解释了我今天看到的几乎所有事情」。[01:12:01-01:14:14] 爱迪生留声机故事：Marc用这个1890年代的历史失败案例来论证「发明者是预测其发明影响最不可靠的人」，这个论证是他系统性历史研究方法的典型案例。他的结论不来自自己发明一个类似留声机的东西然后失败，而是来自跨越一个世纪的模式识别。",
            "that_point": "[07:19-09:49, 30:31-33:00] Dyson的5127个原型哲学：「每一个失败都让我更接近解决方案。失败比成功更有趣。」这种知识是完全具身的，不可以在书上读到——你必须亲手做，感受材料，感受什么不起作用，然后修正。Dyson甚至明确批评了那种「先研究再行动」的方法：他认为很多研究者花太多时间阅读别人的研究，而没有足够时间做自己的实验。这和Marc通过读Burnham和分析爱迪生来学习的方式是直接对立的。",
        },
    ],
    "en_title": "The World Is More Malleable Than You Think: Zero Introspection, Founder Capitalism, and the Musk Method · Marc Andreessen",
    "en_tags": ["zero introspection", "founder capitalism", "managerialism critique", "moral panics", "Elon's management method"],
    "en_connections": [
        {
            "slug": "caa-co-founder-michael-ovitz",
            "kind": "resonance",
            "relation": "Marc built A16Z explicitly on the CAA model — the phalanx approach (if you have one partner, you have the whole firm), the 7 AM staff meetings to call clients' clients before competitors were awake. He studied Ovitz and replicated the organizational structure in venture capital. The deeper tension: Ovitz is exactly what Marc's managerialism critique describes — a supremely skilled manager who could not adapt when his environment fundamentally changed (the Disney negotiation, the shift in Hollywood power). Marc adopted Ovitz's organizational innovation while his entire intellectual framework predicts why Ovitz's kind of manager ultimately fails.",
        },
        {
            "slug": "daniel-ek-impact-happiness-self-mastery",
            "kind": "resonance",
            "relation": "Both diagnose the same organizational pathology from opposite vantage points: as success and power accumulate, truth stops reaching the person who needs to act on it. Marc's analysis is systemic — IBM's twelve layers of management produced compounding lies that left the CEO completely insulated from reality, protected by what IBM called 'the Big Gray Cloud.' Ek's analysis is personal — his product reviews had become a performance designed to manage him rather than improve the product. Marc's remedy is structural (Elon's direct access to engineers, eliminating the layers); Ek's remedy is relational (maintaining people who will tell you the truth regardless of your power). Same disease, different prescriptions.",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both treat failure as the primary mechanism of learning — but the mechanism is opposite. Dyson: physical iteration, 5,127 prototypes built by hand, knowledge that accumulates in the body through direct failure. You must fail yourself. Marc: systematic study of historical failure patterns — reading Burnham from 1941 to understand 2024 capitalism, analyzing Edison's phonograph prediction to understand the limits of AI forecasting. You can learn from others' failures without repeating them. Dyson's epistemology is embodied and irreducible; Marc's is pattern-based and historical. Both arrive at the same conviction — the current world is a primitive approximation of what's possible — but one carries it into the lab, the other into venture capital.",
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
