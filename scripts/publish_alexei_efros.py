"""Publish alexei-efros-surface-deep-data-curious-robot using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "alexei-efros-surface-deep-data-curious-robot",
    "report": "reports/alexei-efros-surface-deep-data-curious-robot.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "表面数据与深度数据：好奇心、体现与AI的下一个前沿 · Alexei Efros",
    "tags": ["深度数据", "具身学习", "好奇心驱动探索", "苦涩教训批判", "婴儿即科学家"],
    "connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "同构",
            "why": "Efros在演讲开头明确说：「这个演讲是Alison之前演讲的呼应（a rhyme）。」两人从不同学科——发展心理学和计算机视觉——独立到达了同一个核心结论：当前AI系统是「文化技术」（cultural technology），不是智能代理。Gopnik的框架：AI像印刷机和百科全书，它放大和传播人类已知的东西。Efros的表述：当前AI是对2000年人类书写知识的蒸馏，是插值机器，不是外推机器。「婴儿即科学家」（scientist in the crib）是Gopnik的框架，Efros直接借用并延伸为「婴儿床里的机器人科学家」——他的终极愿景。Gopnik还出现在Q&A中，与Efros讨论探索-利用的区别，进一步确认了两人框架的互补性：Gopnik从认知机制，Efros从工程实现。",
            "this_point": "[00:37-01:09] Efros开场：「这个演讲是对Alison本周早些时候演讲的呼应，是我思考了一段时间的东西。」[16:18-16:37] Efros直接引用Gopnik的框架：「我真的很喜欢Alison对当前AI系统的描述方式——她说，这些AI不是智能代理，它们是文化技术。就像百科全书或印刷机。」[29:30-29:52] Efros借用Gopnik的「婴儿即科学家」来定义他的终极目标：「婴儿床里的机器人科学家——利用Alison的'婴儿是科学家'，用某种好奇心、内在动机，来挖掘深度数据。」[41:05-41:52] Gopnik在Q&A中出现并与Efros讨论：「RL在某种意义上也是在做深度数据，它也在行动，在做事……但只为目标服务的数据获取，和纯粹的认知好奇探索，是有区别的。」",
            "that_point": "[大约45:00-60:00] Gopnik的核心论点：婴儿不是小型成人，而是进化设计的学习机器——他们的「软脑」、延长的童年、以及纯粹的探索行为，是人类进化出来专门用于学习的适应。AI当前作为「文化技术」的框架：AI就像印刷机——它放大和加速文化知识的传播和组合，但并不生产新知识。这与Efros「蒸馏」和「插值」的批判完全同构——都在说同一件事：当前AI最擅长的是重组和传播人类已知的东西，而不是真正超越。两人在同一个研讨会上，从不同角度论证了同一个论题。",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "同构",
            "why": "Dyson的5127个原型哲学在Efros的框架里就是「深度数据收集」的人类版本。核心对应：Dyson「你无法通过读书学会做吸尘器」=Efros「你无法通过爬取表面数据学会物理世界」。Dyson的每一个原型失败都是负反馈——Efros说这正是当前机器人训练方法最缺少的。Dyson的具身知识（必须亲手做才能理解材料、气流、结构）=Efros的深度数据（只有通过行动才能获取的关于世界的信息）。更深的共鸣：Dyson明确批评「先研究再做」的路线——这与Efros对「表面数据优先」的AI训练方法的批判是镜像。两人都相信某类知识只能通过主动行动来获取，而不能通过被动观察来传递。Dyson把这个信念用于产品开发，Efros把这个信念用于理解AI的根本局限。",
            "this_point": "[19:35-24:29] Moravec悖论的引入：「国际象棋解决了30年了，但这个移棋子的家伙——还没有机器人能做到。」深度数据的三个具体例子：拿起刀才能知道它的重量；倒出液体才能看到粘度；试图打开Mac才能知道哪个方向；「环顾四周，想象你手机的味道——有点可怕，我们能做到。我们能做到是因为我们小时候把这个房间里的所有东西都放进嘴里了。」[26:33-29:04] 当前机器人训练方法的三个不足：遥操作（缺少负反馈，被动）、模拟器（缺乏真实感）、视频学习（「我试图通过看电视学萨尔萨舞——不可能，你真的需要进去做」）。",
            "that_point": "[07:19-09:49, 30:31-33:00] Dyson的5127个原型哲学：「每个失败都让我更接近解决方案。失败比成功更有趣。」他的迭代方法：拿起来，问怎么改进，改进，放下，重复。Dyson明确批评「先研究再行动」：太多研究者读别人的研究多于做自己的实验。他的具身知识论：「对于循环吸尘器，你必须发明一个，因为没有其他方法能理解它为什么这样工作。」Dyson的5127次失败全都是物理反馈——材料如何响应，气流如何变化，结构如何崩溃。这正是Efros说机器人最缺少的：负反馈，真实的物理世界推回。",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "张力",
            "why": "Foody对当前AI能力持乐观态度，认为AI正在重构知识工作，Mercor正在训练AI做原本需要人类专业知识的任务（法律、财务分析等）。Efros则从计算机视觉研究者的角度提出了结构性批判：当前AI系统在本质上是高维度插值机器，依赖表面数据，无法真正外推，无法产生真正的新知识。两者的对比不是乐观vs悲观，而是时间尺度和应用场景的差异：Foody关注的是「今天的AI能做什么知识工作」，这些任务在Efros的框架里也许正好处于高维插值的能力圈内（结构化文档、先例检索、标准分析）。Efros关注的是更长期的问题：这个范式的边界在哪里，哪些任务永远不会在这个框架内解决（物理世界理解、真正的创造性外推）。这个张力也是一个互补：也许Foody的任务都是表面数据可以处理的，而真正的「深度数据」任务（机器人、物理科学发现）需要Efros的框架。",
            "this_point": "[17:55-18:43] Efros对当前AI本质的批判：「我们在把2000年的人类书写知识蒸馏进这个模型。我们知道蒸馏模型不如真实的东西——它们不能外推，不能持续学习……有些东西在窃取知识和自己生成知识之间是劣质的。」「这种爬取的数据能给我们下一个博尔赫斯或下一个巴赫吗？我不这么认为。」[33:01-33:15] 总结：「我担心我们不会超越这种模仿和拼贴。要走得更远，我们需要深度数据。」",
            "that_point": "[Foody集的主要论点] Foody的核心主张：当前AI系统（GPT-4级别）正在做的工作已经相当于顶尖人类专家——法律文件分析、财务建模、技术评估——而Mercor正在构建基础设施来训练AI系统做更多这类知识工作，并把这些能力部署给更广泛的人群。他的乐观来自具体的能力证明：AI在律师资格考试、医学执照考试等高门槛测试上的表现。Efros的框架提供了一种理解这个现象的方式：这些任务都高度结构化、有大量先例数据、答案都存在于2000年的书写知识里——正是高维插值最擅长的领域。两者并不矛盾，但边界在哪里，是开放问题。",
        },
    ],
    "en_title": "Surface Data, Deep Data, and the Curious Robot: What Current AI Is Missing · Alexei Efros",
    "en_tags": ["deep data", "embodied learning", "curiosity-driven exploration", "bitter lesson critique", "babies as scientists"],
    "en_connections": [
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Efros opens by saying this talk is meant as 'a rhyme to Alison's earlier talk' at the same workshop. Both reach the same conclusion from different disciplines: current AI systems are cultural technologies — sophisticated amplifiers and recombinators of existing human knowledge, not genuine agents. Gopnik's 'scientist in the crib' is Efros's direct inspiration for his ultimate goal: the robot scientist in the crib, a system with no assigned task, whose only objective is to mine the world for deep data. In the Q&A, Gopnik appears and pushes on the distinction between goal-directed RL and pure epistemic curiosity — both agree that RL with fixed objectives is different from the kind of open-ended exploration that produces genuine understanding.",
        },
        {
            "slug": "james-dyson-5127-prototypes-invention",
            "kind": "resonance",
            "relation": "Dyson's 5,127 prototypes are a human implementation of what Efros calls deep data collection. Both argue that certain kinds of knowledge can only be acquired through physical action — you cannot learn it by reading about it, watching it, or scraping it from the internet. Dyson's embodied knowledge (how a material responds under stress, how airflow behaves, how a structure fails) is exactly what Efros says is missing from all current AI training pipelines. Both explicitly critique the 'study first, act later' approach: Dyson says reading others' research is no substitute for your own experiments; Efros shows that learning salsa from videos doesn't work. The key difference is scale: Dyson applied this at the level of a product and a bench; Efros is arguing for it as the defining challenge of the next generation of AI.",
        },
        {
            "slug": "brendan-foody-mercor-teaching-ai-knowledge-work",
            "kind": "resonance",
            "relation": "Foody is optimistic about deploying current AI capabilities in knowledge work — legal analysis, financial modeling, technical assessment — tasks where AI performance already matches or exceeds human experts. Efros is identifying a structural limitation in the same generation of systems: they are high-dimensional interpolators trained on surface data, incapable of genuine extrapolation, producing mimicry and pastiche rather than new knowledge. The tension resolves partially when you notice that the tasks Foody is optimistic about — structured documents, legal precedent, standardized tests — are exactly the kind of tasks that high-dimensional interpolation handles best. The tasks Efros says surface data cannot solve — physical world understanding, genuine creative invention — may simply not be in scope for Foody's use cases. Where the boundary falls is the open question.",
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
