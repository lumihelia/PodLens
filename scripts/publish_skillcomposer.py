"""Publish skillcomposer-learning-to-evolve-agent-skills (0621 batch, verified against arXiv PDF text)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "skillcomposer-learning-to-evolve-agent-skills",
    "report": "reports/0621/skillcomposer-learning-to-evolve-agent-skills.md",
    "url": "https://arxiv.org/abs/2606.06079",
    "kind": "paper",
    "date": "2026-06-21",
    "title": "SkillComposer：大语言模型推理期 Agent 技能自适应演化 · Qi Zhang",
    "tags": ["Agent 技能", "推理期演化", "拒绝采样", "泛化与特异性", "认知基础设施", "编译型过滤器"],
    "connections": [
        {
            "slug": "g-memory-hierarchical-memory-multi-agent-systems",
            "kind": "resonance",
            "relation": "同构",
            "why": "两篇论文解决的是同一个母题在不同形式下的版本：如何让 LLM 智能体在不重新训练底层模型的前提下，跨多次试验持续积累、提炼并复用经验。G-Memory 用三层图结构（交互/查询/洞察）管理多智能体协作历史；SkillComposer 用三个可学习元操作（Create/Merge/Improve）管理可复用的技能文档。两者都面临同一个核心张力——太具体则无法迁移，太抽象则无法指导行动——并都用一种「闭环反馈」机制来解决它：G-Memory 靠环境反馈异步更新图节点，SkillComposer 靠 Delta 成功率拒绝采样过滤生成的技能。",
            "this_point": "SkillComposer Abstract: \"current skill construction methods treat the problem as one-shot extraction, overlooking a fundamental tension: a skill tailored to the specific task fails to transfer, while the abstracted skill often provides insufficient guidance.\"",
            "that_point": "G-Memory §4.3：群体经验的「机构化」必须依赖异步的多层图更新闭环——任务成功或失败的反馈必须沉淀为查询图的新节点、与相关查询的边，并通过 J 算子对洞察图节点进行聚类和修正。",
        },
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "同构",
            "why": "Patel-Wang-Fan 用 Stroop 任务证明了变换器自注意力机制在架构层面缺失执行控制电路——它无法在长上下文中维持目标导向行为、抑制干扰。SkillComposer 的整套机制，本质上是在不改变变换器架构本身的前提下，从外部「外包」出一套执行控制：Skill Improve 根据失败反馈不断修正攻略中容易被遗忘或干扰的细节，相当于用一份外部的、显式的「步骤清单」替代了模型内部缺失的前扣带回/背外侧前额叶式的冲突仲裁机制。SkillComposer 的存在本身，恰恰印证了 Patel-Wang-Fan 诊断的准确性：如果变换器自带执行控制，就不需要靠外部技能文档来防止它在长任务中「忘记自己该做什么」。",
            "this_point": "SkillComposer §3.2：Skill Improve 在有技能指导的执行后，捕获本次执行暴露出的遗漏点，为旧技能打上定制化的补丁，提升其在特定 target 任务上的表现——这是一种外部、显式的纠错循环。",
            "that_point": "Patel-Wang-Fan Discussion: \"Transformers, lacking such a circuit, cannot signal for enhanced control and process each input independently through fixed query-key-value transformations and linear projections learned during pretraining, without mechanisms for gain modulation, recurrent feedback, or adaptive reweighting of representational activity.\"",
        },
    ],
    "en_title": "SkillComposer: Inference-Time Adaptive Evolution of Agent Skills for LLMs · Qi Zhang",
    "en_tags": ["agent skills", "inference-time evolution", "rejection sampling", "generalization vs. specification", "cognitive infrastructure", "compiled filters"],
    "en_connections": [
        {
            "slug": "g-memory-hierarchical-memory-multi-agent-systems",
            "kind": "resonance",
            "relation": "The two papers solve the same underlying problem in different forms: how can an LLM agent keep accumulating, distilling, and reusing experience across many trials without retraining the underlying model. G-Memory manages multi-agent collaboration history with a three-layer graph (Utterance/Query/Insight); SkillComposer manages reusable skill documents with three learnable meta-operations (Create/Merge/Improve). Both face the same core tension — too specific and it can't transfer, too abstract and it can't guide action — and both resolve it with a closed feedback loop: G-Memory updates graph nodes asynchronously from environmental feedback, SkillComposer filters generated skills via delta-pass-rate rejection sampling.",
        },
        {
            "slug": "patel-wang-fan-transformer-executive-control",
            "kind": "resonance",
            "relation": "Patel-Wang-Fan used the Stroop task to prove that transformer self-attention is architecturally missing an executive-control circuit — it cannot sustain goal-directed behavior or suppress interference over a long context. SkillComposer's entire mechanism is, in effect, outsourcing executive control from outside the model, without changing the transformer architecture itself: Skill Improve continually patches the details in a skill document that are most prone to being forgotten or disrupted, based on failure feedback — substituting an explicit, external 'step checklist' for the anterior-cingulate/dorsolateral-prefrontal-style conflict arbitration the model lacks internally. SkillComposer's very existence is itself confirming evidence for Patel-Wang-Fan's diagnosis: if transformers came with built-in executive control, there would be no need for an external skill document to stop them from 'forgetting what they're supposed to be doing' over a long task.",
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
    for c in item["connections"]:
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:30]}...)")

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
        sec = "papers" if item["kind"] == "paper" else "episodes"
        d = ROOT / "docs" / (sec if lang == "zh" else f"en/{sec}")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
