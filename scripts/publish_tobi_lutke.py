"""Publish tobi-lutke-companies-as-technology-shopify-os using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "tobi-lutke-companies-as-technology-shopify-os",
    "report": "reports/tobi-lutke-companies-as-technology-shopify-os.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "公司即技术：差异化的义务与创始人的工艺 · Tobi Lütke",
    "tags": ["公司即社会技术", "Shopify操作系统", "差异化即义务", "竞争vs竞争对手", "大脑即叙事对齐机制"],
    "connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "David在这集里直接把Dyson的原话读给Tobi听：「差异化与保持完全控制。让它与众不同，哪怕更差。」Tobi的反应是完全认同，并用SpaceX猛禽发动机的演化史来阐述这个哲学——发动机经过数代迭代变得越来越小、越来越轻、越来越简洁——他称之为他见过的最鼓舞人心的图像。两人都在论证同一个命题：你必须首先拥有第一个版本，才能迭代超越它。但规模不同：Dyson在产品/原型层面做这件事（5127个吸尘器原型），Tobi在公司/组织层面做这件事（Shopify OS，把公司架构写成机器可读的配置文件）。SpaceX猛禽是桥梁——它是Dyson哲学在工业规模上最纯粹的体现，Tobi用它来向David证明他理解Dyson的核心。",
            "this_point": "David在对话中直接引用Dyson传记原文读给Tobi：「差异化与保持完全控制。让它与众不同，哪怕更差。」Tobi立即回应：如果你复制别人的7分方案，上限就是7分。但如果你从第一原理出发建立自己的6分方案，你拥有每一个细节，你可以迭代到7分以上。他随后指出SpaceX猛禽发动机的演化照片——同一台发动机逐代变小、变轻、变简洁——是他见过的最鼓舞人心的图像，是Dyson「让它与众不同」哲学在工业规模上的完美体现。Shopify OS本身也是这个哲学的产物：没有现成系统可以复制，Tobi从头用Python+SAT求解器建立，完全控制每一个设计决策。",
            "that_point": "[07:19-09:49, 30:31-33:00] Dyson的5127个原型哲学：「每个失败都让我更接近解决方案。失败比成功更有趣。」他的方法论：拿起来，问怎么改进，改进，放下，重复。他明确批评「先研究再行动」的方法——他认为太多研究者读别人的研究多于做自己的实验。差异化是强制性的，不是可选的：「如果你想要一个循环吸尘器，你必须发明一个，因为没有其他方法能理解它为什么这样工作。」Dyson的知识是完全具身的——你必须亲手做，感受材料，感受什么不起作用，然后修正。",
        },
        {
            "slug": "daniel-ek-impact-happiness-self-mastery",
            "kind": "resonance",
            "relation": "同构",
            "why": "David在这集里直接点名Daniel Ek和Ramp的Karim，说两人都独立向他提到了「要找有尖峰的人，而不是全面发展的人」——Tobi立即认同。但更深的联系在于两人都有一个「cosplay」时期：Tobi在上市后开始「cosplay一个严肃的上市公司CEO」，将决策权完全委托给高管，直到COVID迫使他重新亲手审视每一个项目；Daniel在Spotify也经历了类似的身份偏移，直到Gustav的一句话让他意识到产品评审已经变成了「让Daniel满意的表演」。两人也都用内部音频媒体保存决策语境和机构记忆：Tobi的「Context」播客（23分钟，匹配Shopify员工平均通勤时间），Daniel与团队关于产品历史的内部叙事传统（David narrates Gustav narrated A Product Story的平行结构）。",
            "this_point": "David在对话中明确说：「我有另一位嘉宾Daniel Ek也说过同样的话——要找有尖峰的人，而不是全面发展的人；Ramp的Karim也说了同样的话。」Tobi立即确认：「这就是高能动性。」Tobi对「cosplay」的描述与Daniel的自我诊断几乎同构——上市后他开始表演一个他不是的CEO角色，把真实判断权委托出去，直到危机暴露了他失联的程度。Tobi的救援方法：COVID期间直接去找被收购公司的创始人们求助，把他们放在关键位置上——而不是让他们待在「创始人托儿所」（skunkworks）里。「Context」内部播客：23分钟每集，专门设计成能在Shopify员工平均通勤时间内听完，用来保存公司决策的背景和动机。",
            "that_point": "[32:03-35:27, 55:16-58:00] Daniel的Gustav故事：Gustav直接告诉Daniel「你在产品评审里没什么帮助，我们都在试图安抚你，而不是做真正的工作。」Daniel的第一反应是想解雇他，然后意识到这是情绪反应，观察三个月后完全认同——从此不再主持产品评审。Daniel关于「spikiness」的论点：对自己最重要技能中某一项达到极端值，其他方面可以平庸。高能动性作为招聘指标：「当事情出错时他做了什么？」Daniel在公司战略最黑暗时期（2015年版税危机）召集的是那些会在危机中说真话、而不是管理他情绪的人。",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "张力",
            "why": "Marc和Tobi在同一个创业哲学问题上站在截然对立的位置：创始人应该深度内省自身内部状态，还是应该把全部能量向外部署？Marc明确表示「零内省」——他认为弗洛伊德式的自我检视是历史偶然，内省消耗的能量本可以用来改变世界。Tobi则建立了一整套系统：大脑即叙事对齐机制（可以被有意更新）、肯定语（他用写「我喜欢公开演讲」改变了自己对公开演讲的恐惧）、给未来自己的「漂流瓶信息」。但更有趣的是组织层面的张力：两人都在反管理主义，都认为公司需要消除层级谎言问题——但采用了完全相反的架构。Tobi：Shopify OS（把公司结构写成机器可读的配置文件，让所有决策及其后果完全可见，政治无处可藏）。Marc/Elon方法：消除所有层级，CEO直接找到做那件事的工程师，绕过中间所有层。同一病理，一个解法是让层级变得完全透明，另一个解法是完全消除层级。",
            "this_point": "Tobi的大脑叙事对齐机制框架：大脑不是记录仪，而是回顾性叙事对齐机制，它奖励与自我认同一致的行动。具体实践：他花一周每天写「我喜欢公开演讲」，一周后他确实喜欢了——不是安慰剂，他理解机制。对高管的肯定语部署：要求每位高管每年公开演讲，讲述Shopify在他们所负责领域如何做得与行业不同且更好——一旦公开说出，大脑不会允许你成为说了假话的人。给未来自己的「漂流瓶信息」：在洞见顶峰时写下，定时发送给未来的自己，用于间隔重复。Shopify OS：把整个公司结构写成机器可读的Python配置文件，用SAT求解器计算应然状态，与当前状态比较，找出最小步骤集。",
            "that_point": "[约前30分钟] Marc的零内省立场：「西格蒙德·弗洛伊德和他创造的文化是一个历史偶然。1910-1920年代之前，没有人认为有效的人应该坐下来审视自己的感受。亚历山大大帝没有治疗师。凯撒没有。拿破仑没有。福特没有。他们向前走。去。」Marc对那些在公司失败压力下服用迷幻药、出来「平静了」然后搬去巴厘岛当冲浪教练的创始人的评论：「你怎么知道他们不更幸福了？」「他们的公司在失败。」Marc对Elon方法的描述：直接找工程师，绕过全部管理层，与做这件事的人待到问题解决。IBM的「大灰云」（12层管理，每层都撒小谎，CEO完全脱离现实）正是Tobi用Shopify OS要解决的问题，但Tobi的解法是透明化层级，而Marc/Elon的解法是消除层级。",
        },
    ],
    "en_title": "Company as Technology: The Obligation of Differentiation and the Founder's Craft · Tobi Lütke",
    "en_tags": ["company as social technology", "Shopify OS", "obligation of differentiation", "rivalry vs competition", "brain as narrative alignment mechanism"],
    "en_connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "David reads Dyson's exact words to Lütke during the conversation: 'Differentiation and retention of total control. Make it different, even if it's worse.' Lütke agrees completely and uses the SpaceX Raptor engine evolution as his most inspiring image of this philosophy in action — the same engine becoming progressively smaller, lighter, and simpler across iterations. Both argue you must own the first version to iterate past it. The difference is scale: Dyson applies this at the product/prototype level (5,127 vacuum prototypes), Lütke applies it at the company/organizational level (Shopify OS, writing the company's structure as machine-readable configuration files).",
        },
        {
            "slug": "daniel-ek-impact-happiness-self-mastery",
            "kind": "resonance",
            "relation": "David explicitly names Daniel Ek — and Ramp's Karim — in this episode as two prior guests who independently made the same point about hiring for spikes over roundedness; Lütke immediately agrees. Deeper: both founders had a 'cosplaying' period — Lütke 'cosplaying a serious public-company CEO' after IPO, delegating until COVID forced a direct reckoning; Ek's parallel realization that his product reviews had become a performance designed to manage him. Both also use internal audio media to preserve decision context and institutional memory: Lütke's 'Context' podcast (episodes tuned to the average Shopify employee commute time) and Ek's internal audio traditions for product history.",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "Andreessen and Lütke take directly opposite positions on whether a founder should do deep internal work. Marc: zero introspection — the energy spent examining yourself is energy not spent changing the world. Tobi: the brain is a retrospective narrative alignment mechanism that can be deliberately calibrated through affirmations, structured commitment, and messages to your future self. The organizational tension is equally sharp: both are anti-managerialism and both are trying to solve the compounding-lies problem of management hierarchy — but through opposite architectures. Lütke: make every decision and its consequences fully legible (Shopify OS, the SAT solver model). Andreessen/Elon: eliminate all layers, CEO goes direct to the engineer doing the work. Same disease, opposite cures.",
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
