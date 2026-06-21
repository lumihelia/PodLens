## 这篇论文讲了什么

这篇论文探讨了如何让大语言模型（LLM）驱动的智能体在推理期自主构建、优化和提炼可重用的“Agent 技能 (Agent Skills)” [Abstract]。传统的技能抽取方法通常采用“单次抽取 (one-shot extraction)”，这带来了一个根本性的张力：如果技能写得太具体，就很难迁移到其他任务上；如果技能写得太抽象，又无法对具体任务提供足够的指导 [§1]。

为打破这一瓶颈，作者提出了 SkillComposer 框架，将技能构建解构成三个可学习的元操作：**Skill Create**（从成功轨迹中提取原始技能）、**Skill Merge**（将相似技能合并，推动“泛化”）和 **Skill Improve**（根据新任务的反馈迭代优化，推动“特异化”） [§3.2]。SkillComposer 提出了一种基于“Delta 成功率 (delta pass rate)”引导的拒绝采样框架，用来训练大模型自身掌握这种技能演化能力 [§3.4]。该框架支持三种部署模式：离线模式（构建通用技能库）、在线模式（任务级实时优化）和混合模式（离线冷启动 + 在线特异化） [§3.3]。在 τ2-Bench（智能体交互）、LiveCodeBench v6（代码生成）和 AppWorld（未见过的 API 调用）三个基准上的实验表明，SkillComposer 显著提升了模型的任务解决率与 Token 使用效率 [§4], [§5]。

## 论文骨架

*   **Abstract**: 提出 SkillComposer，阐明 specification 与 generalization 之间的张力，介绍三种元操作和三种部署模式。
*   **1 Introduction**: 指出当前技能提取过于依赖人工编写或单次提取的脆弱性，定义 generalization 和 specification 的平衡挑战。
*   **2 Related Work**: 梳理 Agent 技能库（SkillX, SkillRL）、技能演化与质量控制（EvoSkill, CoEvoSkills, SkillClaw）的发展脉络。
*   **3 Methodology**: 
    *   **3.1 Preliminary**: 定义 Skill.md 的三元组元组（n, d, b） [§3.1]。
    *   **3.2 Skill Operations Formulation**: 定义 Skill Create、Skill Merge、Skill Improve 操作 [§3.2]。
    *   **3.3 Inference-Time Skill Evolution**: 详述 Offline、Online、Hybrid 三种运行流路 [§3.3]。
    *   **3.4 Training via Rejection Sampling**: 详解以 delta pass rate 为判断指标的 SFT 数据生成机制 [§3.4]。
*   **4 Experiments**: 对比 No Skill、MemP 等基线，展示跨模型、跨域泛化能力及 Token 演化曲线 [§4.2]-[4.4]。
*   **5 Ablation and Analysis**: 进行元操作消融 [§5.1]、技能组合的跨任务迁移性分析 [§5.2]、AppWorld 零样本泛化测试 [§5.3]，以及迭代演化与暴力多次采样 (Pass@k) 的效率对比 [§5.4]。
*   **6 Conclusion**: 总结 SkillComposer 机制在自适应推理上的价值，并指出训练样本收集成本昂贵的 Limitation。

## 核心论点清单

1.  **技能的“泛化度（Generalization）”与“特异度（Specification）”是相互拮抗的两个质量维度。** 如果不进行干预，大模型直接生成的技能会走向两个极端：要么极度狭隘地复述原任务示例（不可迁移），要么过度抽象流于泛泛而谈（无法指导行动）。
    *   §1 Introduction, p.2: "Effective skills require both generalization... and specification... yet existing methods provide no systematic way to achieve either."
    *   观点
2.  **通过“Delta 成功率（Delta Pass Rate）”过滤生成的技能，是实现技能质量控制的关键过滤器。** 只有当大模型编写的技能在注入上下文后，执行器（Executor）的成功率比 vanilla 基线有显著提升（例如提升超过阈值 $\epsilon$），该生成样本才被认为有效并被接纳进 SFT 训练集。
    *   §3.4, p.4-5: Equations (2)-(4)
    *   事实
3.  **在离线技能库构建中，一味引入“Skill Improve”特异化优化反而会损害库的泛化性能。** 离线库的目标是保持跨任务的广泛覆盖率，此时引入过度特异化的 Improve 会使库中的技能与特定任务深度绑定，从而抵消了 Skill Merge 带来的去冗余和通用性收益。
    *   §5.1, p.8-9: Table 2 (Create/Merge 表现好于 Create/Merge/Improve)
    *   事实
4.  **技能组合能力（Skill Composition）是一种可以跨越任务类型（如从 Agent 任务向 Code 任务）迁移的元能力（Meta-Ability）。** 只在 Agent 任务（Tau2Bench 交互）上训练的 4B 模型，即便从未见过代码，其生成的 Merge 和 Improve 技能依然能大幅提升 27B 执行器在 LiveCodeBench 上的代码表现。
    *   §5.2, p.10: Table 3 ("Agent-only training still improves code performance...")
    *   观点
5.  **在推理预算相同的情况下，迭代演化技能比暴力多次采样（Vanilla Pass@k）表现出更强健的边际增益。** 暴力多次采样只是重复概率尝试，而 SkillComposer 的 Online 模式（利用上一次失败/成功轨迹迭代改写技能）能使成功率曲线呈陡峭上升趋势，且二者差距随着迭代次数增加而持续拉大。
    *   §5.4, p.11: Figure 4
    *   事实

## 大白话重讲

在现在的 AI 开发中，有一个非常前沿的思路：让大模型在做任务之前，先去阅读一篇写有攻略的“技能文档 (SKILL.md)”。读完攻略后，AI 的通关率会大幅提升 [Introduction]。但这带来了一个让人头疼的问题：攻略如果写得太宽泛（比如“遇到问题要冷静”），AI 读完还是不会操作；但如果攻略写得太细碎（比如具体到“第一步点按第 3 行第 2 个像素点”），只要稍微换个新任务，这篇攻略就成了废纸 [Introduction]。

SkillComposer 的核心目的，就是让大模型自己学会撰写、合并以及修改这些“技能攻略”，并在“太泛”和“太窄”之间找到完美平衡 [§1]。

它把写攻略这件事拆成了三步 [§3.2]：
1.  **Skill Create（写初稿）**：AI 成功完成一次任务后，顺手把自己的通关路径写成一篇攻略；
2.  **Skill Merge（合并去重）**：AI 发现档案库里积攒了太多类似的攻略（比如一千篇关于如何注册账号的攻略），于是把它们归纳合并成一篇通用攻略，让档案库变得精简 [§3.2, Equation 1]；
3.  **Skill Improve（迭代修正）**：当 AI 拿着通用攻略去挑战一个新游戏时，发现有些细节不对劲，于是根据这次的新经验，给攻略打个升级补丁，让它更完美地契合当前任务 [§3.2]。

为了训练大模型写出真正高质量的攻略，SkillComposer 发明了“Delta 成功率体检机制” [§3.4]。AI 写出的攻略好不好，不需要人工去判分，而是直接扔给另一个 AI 拿着这篇攻略去通关 5 次。如果通关成功率比“没读攻略”时提升了 40% 以上，就证明这篇攻略是干货，立刻录入训练集；如果读完没效果甚至帮了倒忙，就直接当成垃圾扔掉 [§3.4]。

这种写攻略的能力是高度通用的。作者做了一个神奇的实验：只教大模型怎么写“客服聊天”的攻略，从来没教过它写“写代码”的攻略。但这个大模型却能无师自通地帮写代码的 AI 总结出了非常优秀的“编程Debug攻略”，让写代码的 AI 成功率大幅提升 [§5.2]！这说明，总结和提炼攻略是一种“元能力”，一旦学会，终身受用。

## 术语小词典

*   **Skill Create (技能创建)**: 从一条没有使用技能指导的原始执行轨迹（Trajectory）中，提炼出包含触发条件和动作步骤的初始技能。
*   **Skill Merge (技能合并)**: 将两篇在语义和代码表示上具有高度相似性（超过阈值 $\delta$）的特定技能，融合成一篇高度概括、高迁移性的通用技能。
*   **Skill Improve (技能优化)**: 在有技能指导的执行后，捕获本次执行暴露出的遗漏点，为旧技能打上定制化的补丁，提升其在特定 target 任务上的表现。
*   **Delta 成功率 (Delta Pass Rate)**: 指在有无该技能指导下，执行器解决任务的成功率之差（$\Delta = P_{with\_skill} - P_{without\_skill}$），用作拒绝采样的唯一硬核过滤信号。
*   **混合部署模式 (Hybrid Mode)**: 先从离线技能库（Offline Lib）中检索出一个相对通用的技能，再在此基础上，随着在线任务的推进，利用 Online 迭代 Improve 机制将其快速特异化为契合当前场景的专属技能。

## 这篇之前与之后

### 之前 (Preceding Works)
*   **MemP / Trace2skill**: 这些方法探索了将轨迹（Trace）转换为技能并存入记忆的通路。但它们是“单次创建（One-shot）”，没有后续的 Merge 和 Improve 机制，容易导致技能库中充斥着成千上万个极度冗余、毫无迁移价值的 specificity 碎片。
*   **EvoSkill**: 引入了迭代优化的概念，但过于依赖外部的人工单元测试或死板的规则评判，且无法在离线状态下合并同类项，缺乏 SkillComposer 所具备的系统化生命周期管理（Create -> Merge -> Improve）。

### 之后 (Succeeding/Concurrent Works)
*   **CoEvoSkills / SkillClaw**: 沿着 SkillComposer 的逻辑，开始引入“多智能体共演化（Co-evolutionary verification）”和“多用户协同修正”。这意味着技能演化不再局限于单模型闭环，而是演变为类似 GitHub 协作式的多 Agent 分支提交与 Merge 机制，以集体智慧共同维护一个全能技能库。

## 最值得读原文的几段

*   **Abstract (p.1)**:
    > "current skill construction methods treat the problem as one-shot extraction, overlooking a fundamental tension: a skill tailored to the specific task fails to transfer, while the abstracted skill often provides insufficient guidance. We attribute this fragility to the absence of explicit mechanisms for skill specification and generalization."
    *   **核心意义**: 论述清晰，直戳了目前主流 Agent-Skill 开发的“泛化度与特异度”两难处境，为后续拆解为 Create / Merge / Improve 三个算子奠定了坚实的立论根基。
*   **§3.4 Rejection Sampling - Equation (2)-(4) (p.4-5)**:
    > "A training example is accepted only when the candidate improves the executor’s pass@k relative to the appropriate baseline by at least a threshold \epsilon."
    *   **核心意义**: 本文方法论中含金量极高的一段，以客观的 pass rate 跃迁作为唯一的监督信号，替代了空洞的 LLM 自我打分（Self-grading），保证了训练集数据的绝对硬度。
*   **§5.4 Iterative Evolution vs. Repeated Sampling (p.10-11)**:
    > "iterative skill refinement compounds its advantage over independent sampling. This demonstrates that structured skill evolution is a more effective use of additional inference budget than brute-force repeated sampling."
    *   **核心意义**: 深刻地回答了“我们为什么需要 Skill？”这个本质问题。它用实验数据向主张“大力出奇迹，暴力多采样几次就能通关”的传统路线发起挑战，证明了“带记忆和攻略的迭代自修正”在长周期任务中的优越性价比。