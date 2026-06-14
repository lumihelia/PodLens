"""Publish pavel-durov-telegram-freedom-resistance using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "pavel-durov-telegram-freedom-resistance",
    "report": "reports/pavel-durov-telegram-freedom-resistance.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "自由高于金钱：Pavel Durov与Telegram的坚守",
    "tags": ["自由高于金钱", "人类是攻击向量", "活在奖励时间里", "稀缺即目的", "手艺的道德重量"],
    "connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都做了一件商业意义上「没有必要」的事：从零开始重建所有人都接受的现成方案。Dyson拒绝使用集尘袋，发明气旋分离技术，5127个原型；Pavel拒绝使用第三方库，自己写了数据库引擎、网页服务器、加密协议、后端API编程语言，设计了矢量贴纸格式（几千字节，180帧，60fps），花了几千小时审视渐变变体来确定Telegram默认聊天背景的四色渐变。两人最深的共同点是对「不被注意但能被感受到」的细节抱有道德义务感。Dyson：真正的创新是解决别人假设必须接受的问题。Pavel：每天有几千万人删除消息，那个消散动画应该让他们的心升起一点点喜悦——乘以10亿用户，这个快乐的总量是值得整个团队投入的。两人都对「平均水平的可接受」感到根本的道德不满。不同之处：Dyson的拒绝针对现有技术，Pavel的拒绝同时针对现有技术和现有权威——但方法论完全一样：在别人认为不可能改变的地方使用最多的努力。",
            "this_point": "[02:28–02:45] 删除动画的设计哲学：「Thanos消散」效果——消失与填充必须同时发生，需要几千行代码适配所有设备所有OS版本；Pavel说「如果我们能把一点点价值带进人们的生活，哪怕通过这些微小的细节，我们必须投入时间。」[02:09–02:20] Telegram默认聊天背景的四色渐变：「我看过几千个变体才确定了这个配置——这是全世界每天打开Telegram的10亿人首先看到的东西。」[02:40–02:50] 矢量贴纸：几千字节，180帧，60fps，「没有人尝试过做这样的事，因为极其困难，但我们做到了，于是整个行业都在抄。」[00:50–01:00] 50ms延迟哲学：「乘以10亿用户乘以每天几十次，那是几个世纪，几千年的人类时间无缘无故流失——只是因为有人写代码时不够用心。」",
            "that_point": "[Dyson集核心主题] 5127个原型不是执着的表现，是工程诚实的表现：现有解决方案根本上是错的（集尘袋用自己阻塞自己），只有从零开始才能找到正确答案。Dyson的核心方法：每次原型失败都是信息，不是挫折；拒绝接受「这就是行业标准」作为终止思考的理由。他的工厂和实验室的美学——干净、精准、没有装饰——和他的工程哲学是同一件事：多余的东西掩盖真实的问题。他发明了在洗手间和厨房同样出现的无扇叶风扇，不是因为有人要求，是因为他认为现有风扇从根本上是危险的（扇叶可以伤人）。这和Pavel「自己写数据库引擎因为现有解决方案有安全漏洞」是同一个认知结构。",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "张力",
            "why": "Andreessen的核心主张：这个世界是可塑的（malleable），由坚定的建造者来塑造。创始人资本主义的基础假设是：如果你足够确信、足够行动，世界会让路。Pavel的故事是这个主张在现实中最精确的压力测试——同时是它最有力的证明，也是它最清晰的反例。证明：Pavel比任何Andreessen所描述的建造者都更彻底地实践了这个信条（100%持有，从不出售一股，拒绝所有政府要求，用自己的钱补贴公司多年，被逮捕后没有退缩，被投毒后说「感觉更自由了」），而Telegram确实在他这样的坚持下重塑了全球通讯的私密性标准。反例：当建造者的产品直接威胁国家权力时，国家并不像市场那样让路——它用12名持枪警察回应。这不是市场竞争，这是主权对主权。Andreessen说建造者应该被尊为文明引擎，Pavel的存在证明这个「应然」在「实然」层面还远未成立——至少在欧洲的2024年没有成立。两人其实是同一个理论的两面：一个在描述世界应该是什么样，另一个在承受它实际上是什么样的代价。",
            "this_point": "[01:02–01:20] 法国逮捕：「我们用15项基于用户行为的指控来迎接一个创始人，这在科技史上前所未有。」[01:20–01:35] 情报机构通过司法施压：「当我听说情报官员和我的法官「沟通」的时候，这是整个事件里最令我警觉的时刻——不是逮捕本身，而是两个系统的融合。」[01:35–01:45] 罗马尼亚选举：「法国情报机构负责人亲自要求我审查保守派候选人的频道。我拒绝了，然后公开了整个对话。我从不与政府官员签保密协议。」[03:10–03:18] 暗杀未遂：「我以为自己要死了……之后感觉更自由了，因为每一天都是奖励时间。」",
            "that_point": "[Andreessen集核心主张] 「世界是可塑的」：技术可以重写规则，建造者不应该默认世界不可改变。他的投资逻辑建立在对founder-mode的深度信念上：真正的创始人能在别人认为不可能的地方找到路径。「创始人资本主义」：这些人不是套利者，不是管理者，是真正在用意志力重写现实的人，社会应该让他们有空间。他对Marc Andreessen描述的Elon Musk的方式：「他不是在建公司，他在建文明」——这和Pavel对自己使命的理解（保护全球信息自由）在尺度上完全对应。关键差异：Andreessen的可塑世界论在商业竞争中被大量验证；但Pavel的故事表明，当你在「政治权力对信息的控制」这个层面上建造，世界的阻力会以完全不同的方式呈现——不是市场竞争，而是主权工具。",
        },
        {
            "slug": "sarah-paine-continental-maritime-powers-geopolitics",
            "kind": "resonance",
            "relation": "同构",
            "why": "Sarah Paine的地缘政治理论：大陆强权（俄罗斯、中国）的逻辑是零和控制，边界封闭，信息垄断，中央化权威。海洋强权（英国、美国）的逻辑是正和贸易，开放流通，信息自由，去中心化节点。Pavel的整个生命轨迹和技术架构就是这个理论的个人史。他从苏联（大陆帝国的核心）出逃；俄罗斯和伊朗封禁Telegram（大陆逻辑：异见信息=威胁）；他把基地建在迪拜（海洋贸易枢纽）；他的服务器架构分布在多个法律管辖区，密钥分开存储，没有任何政府可以要求单一入口（海洋策略在数字基础设施层面的直接实现）。Paine关于「谁制定规则」的分析和Telegram的商业模式也精确对应：大陆逻辑=控制信息流通；海洋逻辑=促进交换并从中抽成（上下文广告、订阅、5%Mini App佣金）。最具体的对应：Paine说海洋强权的优势是对异见者的包容，因为创新需要异见；Pavel说他从不与政府官员签保密协议，因为透明度是他唯一的防御机制——这两句话是同一个信念在制度层和个人层的表达。",
            "this_point": "[00:50–01:00] Telegram架构的分布式原则：「密钥存储在不同法律管辖区的服务器上，没有任何政府可以要求单一入口来访问它们。」[01:02–01:20] 法国逮捕和俄罗斯封禁、伊朗封禁——三个大陆逻辑的国家对同一个平台使用同一种手段：如果你不服从，我们就关闭你。[03:45–03:55] 2011年，拒绝删除Navalny反对派组织，武装警察登门——大陆强权对信息自由的典型回应。[01:35–01:45] 「法国情报机构要求我审查罗马尼亚保守派候选人的频道。我公开了整个对话。」——大陆逻辑渗透进自称海洋价值观的民主国家的具体案例。",
            "that_point": "[Sarah Paine集核心论点] 大陆与海洋的分野不只是地理，是两种对待人、信息和权威的根本不同的逻辑体系。大陆强权的生存逻辑是：控制内部异见，因为外部威胁是存在性的；任何不在自己控制范围内的信息流都是潜在的武器。海洋强权的生存逻辑是：鼓励流通，从流通中获益，用开放性吸引人才和资本。Paine说这不是价值观的选择，是地理的产物，是生存策略的历史沉淀。历史上的分水岭时刻：英国的海洋霸权在于它可以控制全球交换的节点（港口、航线、海峡），而不是占领所有土地。Pavel的Telegram本质上是一个数字港口：你的消息流经它，他从流通中获益，但他不控制内容本身——这和大陆强权的「我控制一切发生在我境内的事」是根本对立的。",
        },
    ],
    "en_title": "Freedom Over Money: Pavel Durov and Telegram's Line in the Sand",
    "en_tags": ["freedom over money", "humans as attack vectors", "living on bonus time", "scarcity enables purpose", "the moral weight of craft"],
    "en_connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both Dyson and Durov did something that made no commercial sense: rebuild from scratch what everyone else accepts as given. Dyson refused the dust bag and invented cyclonic separation across 5,127 prototypes. Durov's team built their own database engines, web servers, cryptographic protocols, and backend programming language from scratch — and designed a vector animation format so stickers are a few kilobytes, 180 frames at 60fps. Both are driven by a conviction that unnoticed details have moral weight. Dyson: real innovation is solving problems people assume must be accepted. Durov: tens of millions of people delete messages every day, and that dissolution animation should make their hearts lift a little — multiplied by a billion users, that's a meaningful total. Both express a fundamental moral dissatisfaction with 'acceptable average.' The difference: Dyson's refusal is aimed at existing technology; Durov's is aimed at existing technology and existing authority simultaneously. The method is identical: apply maximum effort exactly where others assume nothing can change.",
        },
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "Andreessen's thesis: the world is malleable, shaped by determined builders. Founder capitalism's baseline assumption is that if you believe enough and act enough, the world yields. Durov's story is the most precise stress test of that claim — simultaneously its strongest confirmation and its clearest counterexample. Confirmation: Durov has practiced the founder-capital thesis more thoroughly than almost anyone Andreessen describes (100% ownership, never sold a share, refused all government demands, funded the company from his own money for years, arrested and still didn't yield, poisoned and felt 'even more free'). Telegram genuinely reshaped global privacy norms through that stubbornness. Counterexample: when a builder's product directly threatens state power, the state does not yield the way markets do — it sends twelve armed police officers. That is not market competition, it is sovereignty meeting sovereignty. Andreessen says builders should be honored as civilization's engine; Durov's existence proves this 'ought' is far from true in the 'is' — at least not in France in 2024. They are two sides of the same theory: one describing what the world should be, the other bearing the cost of what it actually is.",
        },
        {
            "slug": "sarah-paine-continental-maritime-powers-geopolitics",
            "kind": "resonance",
            "relation": "Sarah Paine's geopolitical theory: continental powers (Russia, China) operate on zero-sum control logic — closed borders, information monopoly, centralized authority. Maritime powers (Britain, the US) operate on positive-sum trade logic — open circulation, distributed nodes, information freedom. Durov's life trajectory and Telegram's technical architecture are a personal-history version of this theory. He escaped the Soviet Union (a continental empire's core). Russia and Iran banned Telegram (continental logic: dissident information equals threat). He built his base in Dubai (a maritime trade hub). His server architecture — distributed across multiple legal jurisdictions, decryption keys stored separately, no single government can compel a single point of access — is maritime strategy applied directly to digital infrastructure. Even the business model maps: Paine's maritime powers enable exchange and take a cut (subscription, context ads, five-percent Mini App commission). Most precisely: Paine argues maritime powers' advantage is their tolerance for dissent, because innovation requires it; Durov says he never signs NDAs with government officials because transparency is his only defense. These are the same belief at the institutional level and the personal level.",
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
