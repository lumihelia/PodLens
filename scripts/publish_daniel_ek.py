"""Publish daniel-ek-impact-happiness-self-mastery using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "daniel-ek-impact-happiness-self-mastery",
    "report": "reports/daniel-ek-impact-happiness-self-mastery.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "影响先于幸福：自我精通与造物者之道 · Daniel Ek",
    "tags": ["影响先于幸福", "自我精通", "企业家原型", "质量哲学", "能量管理"],
    "connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都把「质量」定义为对「永远无法实现的完美」的永恒追求，而不是一个可以达到的终点状态。Daniel的日本茶道大师故事（34年只做一件事，追求0.01%的改进）与Dyson的5127个原型是同一种精神的不同表达：不是「我完成了」，而是「它还可以更好」。更直接的连接：Daniel在对话中明确引用了Dyson写的《伟大发明史》——「他从1700年的发明里取出一小块，然后和今天的技术组合在一起。这就是创新。」Daniel自己对「创新=把已知的两件事以新方式组合」的定义，和Dyson的历史性学习方法完全同构。两人都是从历史中提取材料的思考者，不是从零开始的发明者。",
            "this_point": "[01:29:25-01:39:41] Daniel：「创新实际上是把两件或以上已经很有名的事情以新的方式组合。」他在前一段引用了Dyson写的《伟大发明史》——Dyson翻阅这本书，找到1700年的某个发明，取出一小部分，和今天的新技术结合，产生新产品。Daniel把这个创新框架用于Spotify：不是发明streaming，而是把已知的欲望（消费者想要任何音乐，不想付每首单价）和已知的技术（宽带、压缩）以未曾有人组合过的方式连接。另：[01:49:00-01:50:06] 日本茶道大师：34年只完善泡茶，追求0.01%的提升——「完美永远不存在，但对完美的渴望是非凡的。」",
            "that_point": "[07:19-09:49] Dyson把「失败比成功更有趣」的哲学应用于5127个原型：每一个失败都是信息，每一次「这不对」都是向完美收敛的一步。Dyson也在《伟大发明史》里做了完全相同的事：从历史中提取不同时代的技术片段，重新组合。这本书不是学术史，是他自己的「组合原料库」。他写了它，因为他相信理解技术的历史是创新的前提——Daniel在自己的讲述里印证了这一点。",
        },
        {
            "slug": "patrick-oshaughnessy-principle-life-work",
            "kind": "resonance",
            "relation": "张力",
            "why": "Patrick和Daniel在几乎所有宏观框架上一致（了解自己才能建公司、关系是最重要的投资、较少但更深入的连接），但在最核心的生命操作系统上截然不同。Patrick：「增长而无目标，一切从视野边缘来，我没有在追逐任何东西。」Daniel：「幸福是影响力的滞后指标，满足是危险的，你必须去找更难的挑战。」Patrick明确反对目标因为它创造「遮蔽」；Daniel则用「影响力」作为方向感，虽然他的「影响」也是高度个人化且非金融化的。表面上都是使命驱动，但Patrick的驱动力是「原则」（当原则被违反时有义务纠正），Daniel的驱动力是「影响」（克服最大的对抗产生最大的满足感）——前者被动响应，后者主动寻找。他们在这集里也直接交流：Daniel在对话中间发短信问Patrick要提问，Patrick评价Daniel是「在所有人中，应用所学最快最高的人」。",
            "this_point": "[02:17-05:14, 10:55-14:27] Daniel：「幸福是影响力的滞后指标。真正持续的幸福来自克服最大的对抗。」22岁的满足期（最抑郁时刻）：「满足不是幸福。我降档到轻松档，生活很轻松——但那不是我想要的。」以及：「我告诉Dara：自什么时候开始，生活是关于幸福的？它关于影响。」Daniel的驱动是主动的：寻找更难的问题，不让自己downshift，刻意保持不舒服。",
            "that_point": "[09:05-12:51, 20:13-21:20] Patrick：「增长而无目标。对非常有才华的人，设定目标通常会实现目标，但这会带来遮蔽——你已经知道前方的路，这让我感到无聊。」Patrick不是在追逐什么，他是在等待和识别从视野边缘来的机会。他的播客不是从某个目标演化来的，是从左场出现的。「更令我兴奋的是：它不会停止，未来十年将出现一组我今天无法想象的事情。」",
        },
        {
            "slug": "caa-co-founder-michael-ovitz",
            "kind": "resonance",
            "relation": "同构",
            "why": "这场对话里，David明确把Ovitz的故事讲给Daniel听了：「Ovitz现在80岁，他说在他那个位置的危险是没有人再告诉他真相了。他能维持25年老友关系的原因：那个人还在告诉他真相。」两人都在相似的地方做了相似的思考：在极度成功和权力之后，维持能说真话的人成为最重要的事，也是最难的事。Daniel的解法：20年关系的mom、Jack、妻子、Gustav——这些人不因为他的地位而改变他们对他说的话。但两人的终局不同：Ovitz最终因为没有足够的「镜子」而做出了严重误判（Disney/DreamWorks的决策，以及对自己局限性的误判）；Daniel的故事里，Gustav的那次坦诚「你在这里其实没什么帮助」反而成了Spotify产品能力提升的关键时刻。信任的维护机制不同，因此后果不同。",
            "this_point": "[32:03-35:27, 53:56-55:16] David把Ovitz的25年朋友谈到说真话，引入话题：「谁在给你说真话？」Daniel列举：母亲（对商业成就冷淡，只关心他是否克服了对他重要的挑战）、Jack、妻子、Gustav。Gustav的故事：告诉Daniel他在产品评审上没有帮助，「我们都在试图安抚你」——Daniel的第一反应是想解雇他，然后意识到这是情绪，给了三个月，结果产品团队更有效率。「从那以后，我不再运营产品评审了。」",
            "that_point": "[31:49-34:25, 01:15:35-01:19:08] Ovitz明确表述：「你到了我这个位置，大多数和你互动的人都是你的员工，这很危险。我生命中真正告诉我真相的人不多。」他的25年友谊的核心：那个人在他权力和财富都很大的时候还是直接说出不好听的东西。但Ovitz自己的错误——在Disney与Eisner的关系处理，以及对自己局限性的判断——表明即使有这样的镜子，也可能没有被充分使用或倾听。Daniel的Gustav故事是Ovitz故事的「有好结局的版本」。",
        },
    ],
    "en_title": "Impact Before Happiness: Self-Mastery and the Maker's Way · Daniel Ek",
    "en_tags": ["impact over happiness", "self-mastery", "founder archetypes", "quality philosophy", "energy management"],
    "en_connections": [
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Both define quality as the permanent aspiration toward an impossible perfection that can never be reached — Ek's Japanese tea master (34 years perfecting tea, pursuing 0.01% improvement) and Dyson's 5,127 prototypes are the same philosophy at different scales. More directly: Ek explicitly cites Dyson's book 'The History of Great Inventions' as the clearest illustration of his own innovation framework — take a piece from 1700, combine it with today's technology in a new way. Both are synthesizers drawing from history's material, not inventors starting from zero.",
        },
        {
            "slug": "patrick-oshaughnessy-principle-life-work",
            "kind": "resonance",
            "relation": "Two different operating systems for the same underlying commitment. Patrick: 'growth without goals, everything interesting came from the periphery, I am not chasing anything.' Ek: 'happiness is a trailing indicator of impact, contentment is the danger, you must seek the harder challenge.' Patrick organizes around a principle that compels correction when violated (passive, reactive); Ek organizes around impact that must be actively pursued (active, directional). Both reject money and status as primary drivers — but the mechanism is opposite. They know each other: Ek texted Patrick mid-conversation asking for questions; Patrick called Ek 'the person who applies what he learns fastest at the highest level.'",
        },
        {
            "slug": "caa-co-founder-michael-ovitz",
            "kind": "resonance",
            "relation": "David raised the Ovitz story directly in this conversation: at the top of power, almost no one tells you the truth anymore — the ability to maintain relationships with people who still will is one of the rarest things a successful person can possess. Both Ek and Ovitz built their worlds around trust as the foundational economic force. But the outcomes diverged: Ovitz lost his mirrors late and made consequential errors of self-assessment; Ek's mirror moment (Gustav telling him he wasn't helping in product reviews) became a turning point that improved Spotify's product capability. Same diagnosis, different resolution.",
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
