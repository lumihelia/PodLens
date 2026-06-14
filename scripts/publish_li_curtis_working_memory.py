"""Publish li-curtis-working-memory-neural-dynamics as kind=paper (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "li-curtis-working-memory-neural-dynamics",
    "report": "reports/li-curtis-working-memory-neural-dynamics.md",
    "url": "https://doi.org/10.1101/2022.09.23.509245",
    "kind": "paper",
    "date": "2026-06-14",
    "title": "工作记忆的神经种群动力学：记忆不是存储，是变形",
    "tags": ["工作记忆不是存储而是计算", "视觉皮层的动态记忆码", "神经子空间与时间泛化", "感觉到运动的再格式化", "早期视觉皮层的记忆反馈"],
    "connections": [
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "同构/张力",
            "why": "Patel等人的论文发现LLM有「晶体知识」但缺乏「执行控制」——知道任务规则但无法在竞争干扰下执行。Li和Curtis的论文揭示了人类大脑的工作记忆不是简单的「知道」，而是持续的格式转换——从「我记住了目标在哪里」到「我的眼睛需要怎么动」。两篇论文共同指向同一个更深层的问题：知道（knowing）和行动（acting）之间存在巨大的计算鸿沟，这个鸿沟需要主动的神经计算来填补。LLM缺乏执行控制，正是因为它没有这种「持续格式转换」的计算过程——它只有晶体知识，但没有「把知识转换为当前行动格式」的动态机制。从这个角度看，Li和Curtis所描述的V1动态，正是人类大脑弥合这个鸿沟的具体实现。",
            "this_point": "[论文讨论，第12页] 「The sensory properties of the visual target were reformatted into a mnemonic code more proximal to the response required by the task.」[论文结论] WM dynamics in early visual cortex involves a propagation from neural populations selective for the peripheral location of targets to locations near the fovea — a recoding of sensory inputs into task-relevant representations.",
            "that_point": "[Patel等论文结论] LLM既展示出Stroop效应（说明有训练驱动的自动化），也在长列表不一致条件下崩溃（GPT-4o: 91%→15%；Claude: 76%→24%），说明有晶体知识但缺乏工作时的执行控制。「knowledge understanding and execution capabilities」的解离是其核心发现。论文建议未来需要在变换器中实现类似前扣带回/背外侧前额叶的执行控制机制。",
        },
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "张力",
            "why": "Gopnik认为儿童的前额叶皮层「欠发育」是探索优先的功能优势，前额叶成熟带来执行控制（快速目标导向行为）但减少开放探索。Li和Curtis的发现提供了一个有趣的反角度：即便是「最高级」的前额叶皮层，在工作记忆中所做的也是最抽象、最无细节的部分——它维持「我在记忆某个位置」但不保留空间拓扑结构。真正的精细空间计算在最低级的V1里。这挑战了「高级=更多功能」的假设：V1在工作记忆中承担的是最接近行动的任务相关计算，PFC承担的是最抽象的标记。两者都需要，但高级不等于更重要。Gopnik关注的是认知发展中前额叶的角色；这篇论文告诉我们在成熟的人类大脑中，前额叶对工作记忆的贡献是什么——而那个贡献比通常认为的要更「薄」。",
            "this_point": "[论文图8和第9页] 「In both frontal regions, we found a stable cluster throughout the memory delay in each of the ROIs, without significant dynamical clusters. Projecting the voxel activity pattern of each time point into the stable subspace extracted by PCA, we found that the locations of the targets remained largely stable and separable within the stable subspace. However, their spatial topology (in the visual field space) was not well-maintained like those observed in the visual and the parietal cortices.」",
            "that_point": "[Gopnik集核心论点] 前额叶皮层的成熟 = 执行控制能力增强 = 目标导向行为增强 = 探索性开放性下降。Gopnik认为前额叶是「开发」（exploitation）的神经基础，儿童前额叶欠发育是「探索」（exploration）优先的功能选择。她对前额叶的理解是「执行控制的中心」。Li和Curtis的发现暗示：即便在工作记忆这个前额叶的「传统领地」里，前额叶也可能是最薄弱的一环——它维持抽象信号，但空间计算和格式转换在视觉皮层。",
        },
        {
            "slug": "alexei-efros-surface-deep-data-curious-robot",
            "kind": "resonance",
            "relation": "同构",
            "why": "Efros区分「表面数据」（被动统计关联）和「深度数据」（主动探索、因果结构、感觉-运动反馈的同步）。他认为AI系统需要深度数据才能发展出真正的世界模型。Li和Curtis的发现提供了「深度数据产生什么样的内部表征」的神经科学案例：在工作记忆任务中，人类V1的神经代码不只是存储了「目标在哪里」的静态模式（这是表面数据能做到的），而是在12秒延迟中把感觉输入主动转换为扫视计划（感觉→运动的格式转换）——这需要大脑知道自己在视觉场中的位置（中央凹位置）、知道任务目标（眼跳到目标），然后计算两者的关系。这种「我的位置 + 目标位置 + 行动计划」的整合，正是Efros所说的主动具身探索（embodied active exploration）产生的深度计算。被动观看条件证明了这一点：相同的感觉输入，没有行动意图，V1就不执行这种转换——计算由任务驱动，而不是由感觉输入驱动。",
            "this_point": "[论文对照实验，第9页] 「Notably, when visualizing the activation maps for V1 during the passive viewing experiment, we did not observe dynamics like those in the WM experiment. The response emerged at the target's polar and eccentricity at the early time points, and diminished in the middle of the delay.」[论文讨论，第12页] 「The early visual cortex seems to concurrently reflect the immediate task demand that requires observers to concurrently hold fixation and the memorized target at far eccentricity, leading to an activity with a peak at more foveal locations with a tail pointing toward the target.」",
            "that_point": "[Efros集核心论点] 「表面数据」是AI从互联网的被动观察中学到的统计关联——图像识别、语言理解。「深度数据」是机器人通过主动探索获得的感觉-运动关联数据：伸手触碰物体时，同时获得视觉（物体移动）、触觉（手的感觉）、运动（手的位置）的同步反馈。Efros认为这种主动具身数据是构建真正世界模型的必要条件。他的「好奇心驱动的机器人」正是在主动生成这种深度数据。Li和Curtis所描述的V1动态是人类大脑利用这种深度数据（通过漫长的发展历史，通过眼动经验和感觉-运动协调）建立起来的「扫视引导计算」能力的体现。",
        },
    ],
    "en_title": "Neural Population Dynamics of Human Working Memory: Memory Is Not Storage, It Is Transformation",
    "en_tags": ["working memory is computation not storage", "dynamic memory codes in visual cortex", "neural subspaces and temporal generalization", "sensory-to-motor reformatting", "top-down feedback in early visual cortex"],
    "en_connections": [
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "The Patel paper shows LLMs have crystallized knowledge but lack executive control — they know the task rules but cannot sustain correct performance under conflicting interference. Li and Curtis show that in humans, the gap between knowing and acting is bridged by an ongoing neural computation: V1 continuously reformats the sensory memory trace into a motor-ready format over 12 seconds. LLMs lack precisely this reformatting process — they store pattern associations but have no dynamic mechanism for translating 'what I know' into 'what the current action requires.' The V1 dynamics described here are one neural implementation of the computation that bridges knowing and doing. Its absence, or its architectural analog, may be what the Stroop failure is measuring.",
        },
        {
            "slug": "alison-gopnik-childhood-learning-ai-cultural-technology",
            "kind": "resonance",
            "relation": "Gopnik's framework treats prefrontal cortex as the seat of executive control — it matures late, and its maturation enables goal-directed behavior at the cost of exploratory openness. Li and Curtis offer a complication: even in mature human WM, PFC's contribution is the thinnest. It maintains a stable, abstract signal — 'I am remembering a location' — but without the spatial topology or the dynamic transformation. The actual computational work — recoding sensory inputs into motor-proximal formats — happens in V1, the lowest-level visual region. Higher does not mean more important, or more computationally active. The most task-embedded WM computation sits at the base of the hierarchy, not the apex.",
        },
        {
            "slug": "alexei-efros-surface-deep-data-curious-robot",
            "kind": "resonance",
            "relation": "Efros argues that AI systems trained on passive surface data (statistical associations from text and images) cannot develop genuine world models — the missing ingredient is active, embodied, causally structured data. The V1 dynamics in this paper are a neural case study in what deep-data-derived computation looks like: during working memory, V1 does not merely store 'the target was there.' It transforms that record into a planned saccade trajectory — integrating current fixation position, remembered target location, and the action that will connect them. The passive viewing control confirms this is not a sensory effect but an action-driven computation. The same input, minus the task demand, produces none of the dynamics. This is exactly the distinction Efros draws: surface pattern recognition responds to the input; deep, action-oriented computation is driven by intention.",
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

    print(f"Publishing: {slug}  [kind=paper]")
    print(f"  title:   {item['title']}")
    print(f"  tags:    {', '.join(item['tags'])}")
    for c in item["connections"]:
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:40]}...)")
    print("  [bilingual] using en_bodies/")

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
        d = ROOT / "docs" / ("papers" if lang == "zh" else "en/papers")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    print(f"zh:   docs/papers/{entry['slug']}.html")
    print(f"en:   docs/en/papers/{entry['slug']}.html")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
