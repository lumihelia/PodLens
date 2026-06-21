## What This Paper Is About

This paper explores how an LLM-driven agent can autonomously construct, optimize, and distill reusable "Agent Skills" at inference time [Abstract]. Traditional skill-extraction methods typically rely on "one-shot extraction," which creates a fundamental tension: a skill written too specifically fails to transfer to other tasks, while a skill written too abstractly fails to provide enough guidance for a concrete task [§1].

To break through this bottleneck, the authors propose the SkillComposer framework, which decomposes skill construction into three learnable meta-operations: **Skill Create** (extracting a raw skill from a successful trajectory), **Skill Merge** (merging similar skills to drive "generalization"), and **Skill Improve** (iteratively refining based on feedback from a new task to drive "specification") [§3.2]. SkillComposer proposes a rejection-sampling framework guided by "delta pass rate," used to train the model itself to master this skill-evolution capability [§3.4]. The framework supports three deployment modes: offline (building a general-purpose skill library), online (real-time task-level optimization), and hybrid (offline cold-start plus online specialization) [§3.3]. Experiments across three benchmarks — τ2-Bench (agent interaction), LiveCodeBench v6 (code generation), and AppWorld (unseen API calls) — show that SkillComposer significantly improves both the model's task success rate and its token efficiency [§4], [§5].

## Paper Skeleton

- **Abstract**: Proposes SkillComposer, clarifies the tension between specification and generalization, and introduces the three meta-operations and three deployment modes.
- **1 Introduction**: Points out the fragility of current skill extraction's heavy reliance on manual authoring or one-shot extraction, and defines the challenge of balancing generalization and specification.
- **2 Related Work**: Surveys the development of agent skill libraries (SkillX, SkillRL) and skill evolution and quality control (EvoSkill, CoEvoSkills, SkillClaw).
- **3 Methodology**:
  - **3.1 Preliminary**: Defines the triple (n, d, b) for Skill.md [§3.1].
  - **3.2 Skill Operations Formulation**: Defines the Skill Create, Skill Merge, and Skill Improve operations [§3.2].
  - **3.3 Inference-Time Skill Evolution**: Details the Offline, Online, and Hybrid operational pipelines [§3.3].
  - **3.4 Training via Rejection Sampling**: Explains the SFT data-generation mechanism using delta pass rate as the judging metric [§3.4].
- **4 Experiments**: Compares against baselines like No Skill and MemP, demonstrating cross-model, cross-domain generalization and token-evolution curves [§4.2]-[4.4].
- **5 Ablation and Analysis**: Runs a meta-operation ablation [§5.1], analyzes the cross-task transferability of skill composition [§5.2], runs an AppWorld zero-shot generalization test [§5.3], and compares the efficiency of iterative evolution against brute-force repeated sampling (Pass@k) [§5.4].
- **6 Conclusion**: Summarizes the value of the SkillComposer mechanism for adaptive inference, and notes the limitation of the expensive cost of collecting training samples.

## Core Arguments List

1. **A skill's "generalization" and "specification" are two mutually antagonistic quality dimensions.** Without intervention, skills generated directly by an LLM trend toward two extremes: either they narrowly recite the original task example (untransferable), or they over-abstract into generic platitudes (unable to guide action).
   - §1 Introduction, p.2: "Effective skills require both generalization... and specification... yet existing methods provide no systematic way to achieve either."
   - View
2. **Filtering generated skills via "delta pass rate" is the key filter for quality control.** A generated skill is only considered valid and accepted into the SFT training set when, after being injected into context, it produces a significant improvement in the executor's success rate over a vanilla baseline (e.g., exceeding a threshold ε).
   - §3.4, p.4-5: Equations (2)-(4)
   - Fact
3. **In offline skill-library construction, indiscriminately introducing "Skill Improve" specialization actually harms the library's generalization performance.** The goal of an offline library is to maintain broad cross-task coverage; introducing overly specialized Improve operations here tightly couples skills to specific tasks, offsetting the de-duplication and generality gains from Skill Merge.
   - §5.1, p.8-9: Table 2 (Create/Merge outperforms Create/Merge/Improve)
   - Fact
4. **Skill composition ability is a meta-ability that can transfer across task types (such as from agent tasks to code tasks).** A 4B model trained only on agent tasks (Tau2Bench interaction), despite never having seen code, still generates Merge and Improve skills that substantially improve a 27B executor's performance on LiveCodeBench.
   - §5.2, p.10: Table 3 ("Agent-only training still improves code performance...")
   - View
5. **Given the same inference budget, iteratively evolving a skill shows a stronger marginal gain than brute-force repeated sampling (vanilla Pass@k).** Brute-force repeated sampling is just repeated probabilistic attempts, while SkillComposer's Online mode (iteratively rewriting a skill using the previous failed/successful trajectory) produces a steeply rising success-rate curve, with the gap between the two continuing to widen as iterations increase.
   - §5.4, p.11: Figure 4
   - Fact

## Plain English Explanation

In current AI development, there's a cutting-edge idea: have a large model read a "skill document" (SKILL.md) with a written walkthrough before attempting a task. After reading the walkthrough, the AI's success rate jumps significantly [Introduction]. But this creates a headache: if the walkthrough is written too broadly (like "stay calm when you hit a problem"), the AI still won't know how to act after reading it; but if it's written too granularly (down to "step one, click the 2nd pixel on row 3"), the moment the task changes even slightly, the walkthrough becomes useless paper [Introduction].

SkillComposer's core purpose is to teach a large model to write, merge, and revise these "skill walkthroughs" itself, finding the perfect balance between "too broad" and "too narrow" [§1].

It breaks writing a walkthrough into three steps [§3.2]:

1. **Skill Create (write a first draft)**: after the AI successfully completes a task, it writes up its own path to success as a walkthrough;
2. **Skill Merge (consolidate and deduplicate)**: the AI notices the archive has accumulated too many similar walkthroughs (say, a thousand walkthroughs on how to register an account), so it generalizes and merges them into one universal walkthrough, keeping the archive lean [§3.2, Equation 1];
3. **Skill Improve (iterative correction)**: when the AI takes a general walkthrough to tackle a new game and finds some details don't quite fit, it patches the walkthrough based on this new experience, making it fit the current task more perfectly [§3.2].

To train the model to write truly high-quality walkthroughs, SkillComposer invents a "delta pass rate health check" [§3.4]. Whether the walkthrough the AI wrote is good doesn't need a human judge — it's simply handed to another AI to try clearing the task 5 times with that walkthrough. If the success rate is more than 40% higher than "without the walkthrough," that proves the walkthrough is solid gold, and it's immediately added to the training set; if reading it does nothing or even makes things worse, it's thrown out as garbage [§3.4].

This walkthrough-writing ability turns out to be highly general. The authors ran a remarkable experiment: they only taught a model how to write walkthroughs for "customer service chat," never teaching it how to write walkthroughs for "writing code." Yet this model was able to, entirely on its own, summarize excellent "programming debug walkthroughs" for a code-writing AI, dramatically boosting that AI's success rate [§5.2]! This shows that summarizing and distilling a walkthrough is a "meta-ability" — once learned, it pays off for life.

## Glossary

- **Skill Create**: Extracting an initial skill — containing trigger conditions and action steps — from a raw execution trajectory that wasn't guided by any skill.
- **Skill Merge**: Fusing two task-specific skills that are highly similar in semantics and code representation (above a threshold δ) into a single, highly generalized, highly transferable skill.
- **Skill Improve**: After an execution guided by a skill, capturing the gaps exposed by that execution and patching the old skill with customized fixes to improve its performance on the specific target task.
- **Delta Pass Rate**: The difference in the executor's task-success rate with versus without a given skill's guidance ($\Delta = P_{with\_skill} - P_{without\_skill}$), used as the sole hard filtering signal for rejection sampling.
- **Hybrid Mode**: First retrieving a relatively general skill from the offline skill library, then, as the online task proceeds, using the Online iterative Improve mechanism to rapidly specialize it into a skill tailored for the current scenario.

## Before and After This Paper

### Before This Paper

- **MemP / Trace2skill**: These methods explored a path for converting a trajectory (trace) into a skill stored in memory. But they are "one-shot creation," with no subsequent Merge or Improve mechanism, which easily leaves the skill library cluttered with thousands of extremely redundant, non-transferable specificity fragments.
- **EvoSkill**: Introduced the concept of iterative optimization, but relies too heavily on external manual unit tests or rigid rule-based judging, and cannot merge similar items offline — lacking the systematic lifecycle management (Create → Merge → Improve) that SkillComposer has.

### After This Paper

- **CoEvoSkills / SkillClaw**: Following SkillComposer's logic, these begin introducing "multi-agent co-evolutionary verification" and "multi-user collaborative correction." This means skill evolution is no longer confined to a single-model closed loop, but instead evolves into something like a GitHub-style collaborative multi-agent branch-commit-and-merge mechanism, collectively maintaining an all-purpose skill library through collective intelligence.

## Sections Most Worth Reading in the Original

- **Abstract (p.1)**:
  > "current skill construction methods treat the problem as one-shot extraction, overlooking a fundamental tension: a skill tailored to the specific task fails to transfer, while the abstracted skill often provides insufficient guidance. We attribute this fragility to the absence of explicit mechanisms for skill specification and generalization."
  - **Why it matters**: Clearly argued, this goes straight to the "generalization vs. specification" dilemma facing mainstream agent-skill development today, laying the foundation for decomposing the problem into the Create / Merge / Improve operators that follow.
- **§3.4 Rejection Sampling - Equation (2)-(4) (p.4-5)**:
  > "A training example is accepted only when the candidate improves the executor's pass@k relative to the appropriate baseline by at least a threshold ε."
  - **Why it matters**: One of the most valuable passages in the paper's methodology — using an objective pass-rate jump as the sole supervision signal, replacing hollow LLM self-grading, and guaranteeing the absolute rigor of the training data.
- **§5.4 Iterative Evolution vs. Repeated Sampling (p.10-11)**:
  > "iterative skill refinement compounds its advantage over independent sampling. This demonstrates that structured skill evolution is a more effective use of additional inference budget than brute-force repeated sampling."
  - **Why it matters**: This answers the essential question "why do we even need skills?" with real teeth. It uses experimental data to challenge the conventional wisdom that "brute force works miracles — just sample a few more times" and proves the superior cost-effectiveness of "iterative self-correction with memory and a walkthrough" on long-horizon tasks.
