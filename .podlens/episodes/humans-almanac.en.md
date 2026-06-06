## What This Paper Is About

This paper introduces ALMANAC, the first dataset of Action-Level Mental Model Annotations for human-agent collaboration. Although Large Language Model (LLM) agents possess multi-step reasoning and planning capabilities, they are mostly optimized for independent task completion and lack the shared mental model alignment capabilities required for collaboration. To fill this gap, the authors designed a theory-guided, two-step annotation framework. Based on the classic social science dyadic routing task "Map Task," they collected 2,987 collaborative actions from 50 participants, pairing each action with three-layer mental model annotations—self-reasoning, perceived partner intent, and perceived team goal—along with free-text rationales. Through benchmarking six mainstream LLMs, the study shows that mental model annotations significantly improve agent behavior prediction performance, but current LLMs still face major limitations in inferring humans' internal, private reasoning states.

## Paper Skeleton

- **Problem Solved**: Current LLM agents are mostly optimized for task completion, lacking the shared mental model alignment capabilities required to maintain the collaborative process; furthermore, academia lacks real human collaboration datasets containing action-level mental model annotations to guide agents. (1. Introduction · "primarily optimized for task completion")
- **Core Claim**: Proposes and constructs the ALMANAC dataset, demonstrating that mental model annotations can provide critical signals for predicting and simulating human collaborative behavior, and points out that existing large models face an inherent bottleneck in inferring others' private mental models. (1. Introduction · "Action-Level Mental model ANnotations")
- **Method of Argumentation**: The paper combines empirical data collection with large model benchmarking. First, it designs and implements a web-based data collection system based on the Map Task; next, it collects mental model data through a two-stage annotation process (during in-session checkpoints and retrospective reflection); then, it uses GPT-5.5 to automatically encode actions into grounding acts and performs human consistency validation (Fleiss’ κ = 0.81); finally, it evaluates the performance of 6 large models, including Qwen, Llama, GPT, and Claude, under two configurations—Persona-Based Prompting and Supervised Fine-Tuning—on two diagnostic tasks: Next Behavior Prediction and Mental Model Prediction.
- **Key Evidence & Examples**:
  - **Dataset Scale**: Contains 25 dyadic sessions, 50 participants, with a total of 2,987 behavioral data points paired with mental model annotations and rationales. (3.1. Annotation Framework · "checkpoint typically takes 10")
  - **Comparison of C_visible and C_not_visible**: When the Guide can see the Follower's real-time canvas (C_visible), the prediction accuracy of the Follower's actions is lower because the Guide relies on real-time visual alignment for fine-grained interventions, increasing the randomness of behavior; however, visual visibility simultaneously significantly improves the consistency of the team's mental models. (3.2.2. Data Collection Process · "Guide could not directly")
  - **Impact of Mental Model Input**: In the Next Behavior Prediction task, introducing human mental model annotations (+Mental Model) significantly improves the accuracy of models like Llama and GPT in predicting Follower behavior. (4.3.1. Next Action Prediction · "next action prediction is")
- **Acknowledged Boundaries & Limitations**:
  - **Retrospective Reporting Bias**: Retrospective reports are susceptible to recall bias and post-hoc rationalization. (7. Limitations · "retrospective reports, which are")
  - **Limited Sample Size**: 25 sessions and 50 samples are relatively modest compared to typical large-scale datasets in NLP.
  - **Single Closed-Scenario Limitation**: The Map Task is a task in a controlled environment, whereas real-world collaboration spans longer time horizons and has more complex interaction constraints.

## Key Takeaways List

1. **An agent's task execution capability alone is insufficient for effective human-agent collaboration; it must be able to establish and align mental models during the interaction process**.
   - Anchor: 1. Introduction · "Effective collaboration, however, requires"
   - Type: Claim
2. **Current LLM agent designs are primarily optimized for independent task completion, leading to a lack of process-level collaborative data in academia**.
   - Anchor: 1. Introduction · "primarily optimized for task completion"
   - Type: Fact
3. **When non-verbal cues are lacking in human-agent interaction channels, the agent's perception of the human partner's intent and team goals is central to collaborative success**.
   - Anchor: 1. Introduction · "verbal cues present in"
   - Type: Claim
4. **Setting up in-session checkpoints can effectively serve as memory anchors, mitigating recall bias during participants' retrospective annotations**.
   - Anchor: 3.1. Annotation Framework · "checkpoint typically takes 10"
   - Type: Claim
5. **In parallel Q&A and interaction, the frequency of the Guide's interventions on the Follower's actions exhibits systematic bias depending on whether the canvas is visible**.
   - Anchor: 3.2.2. Data Collection Process · "Guide could not directly"
   - Type: Fact
6. **Mental models can provide incremental signals for agents to predict and simulate future human interactive behaviors that traditional historical trajectories cannot provide**.
   - Anchor: 4.3.1. Next Action Prediction · "next action prediction is"
   - Type: Fact
7. **Large models perform acceptably in predicting shared mental model dimensions, but face severe bottlenecks in inferring private self-reasoning**.
   - Anchor: 4.3.2. Mental Model Prediction · "hardest dimension to predict"
   - Type: Fact
8. **The Follower's mental model is easier to predict than the Guide's, because the former's depth of reasoning is more directly constrained by the latter's explicit verbal instructions**.
   - Anchor: 4.3.2. Mental Model Prediction · (paraphrase, non-verbatim citation)
   - Type: Fact

## Plain English Explanation

Today's AI agents (like various coding or report-writing assistants) are getting better and better at executing specific commands. However, when they collaborate with humans, they often give off a feeling of "talking past each other and being absent-minded." Why? Because they are merely "task-execution machines" and have absolutely no concept of a "Mental Model" in their heads. When humans cooperate, we are constantly trying to read each other: "What does he mean by sending this message right now?", "Are our current goals aligned?", "How should I cooperate with him in the next step?". Current AI simply lacks this cognitive layer.

This paper aims to solve this problem. The authors built a dataset called ALMANAC, specifically designed to record the "inner monologue" of humans during collaboration. They had two participants play a classic social game—the "Map Task." In this game, the Guide has a route map, while the Follower has only a blank map. The Follower needs to draw the correct route on a web canvas based on the Guide's verbal instructions. Meanwhile, one of the landmarks on the two maps is intentionally set to be mismatched, thereby creating collaborative conflict and alignment difficulties.

The best design choice is that when the game reaches one-quarter, one-half, and three-quarters of the way through, the system suddenly cuts to a Checkpoint, asking the participants to record their voice answers to: "What do you think the team's goal is right now? What do you think the other person wants to do? What are you going to do next yourself?". After the game ends, participants also watch their own recordings to trace back the "inner thoughts" and detailed logic behind every action (such as sending a message, drawing a line, or erasing). This is "action-level mental model annotation."

The paper tested large models like GPT-5.5 and Llama 3.3 using this data. The research findings are very interesting:
First, if the human-annotated "inner monologue" (mental model) is fed to the large model as an additional prompt, the model can predict the human's next actions (what message to send, how to draw a line) very accurately. This proves that mental models are powerful signals for predicting human behavior.
Second, large models perform okay when predicting "team goals" and "inferring the other party's intent," but when predicting "what this participant is plotting in their own head (Self-reasoning)," the accuracy is a complete mess. This is because large models can only infer based on public chat text, whereas humans' deep, private inner thoughts are usually not written directly in the chat box.
Third, when the Guide can see the Follower's canvas in real-time (C_visible), the Follower's actions actually become extremely difficult to predict. Why? Because once the Guide can see, they will frequently interrupt and intervene with the Follower, making the interaction rhythm very fragmented and random. In contrast, without visibility, the Follower tends to explore systematically according to the verbal plan.

In short, this paper tells us: to make AI a qualified partner, just training them to execute commands is useless. We must train them to constantly update and align "mental models" about their partners, the team, and themselves in their minds, just like humans do.

## Glossary

- **Mental Model**: A cognitive map in the minds of team members regarding themselves, their partners, and the state of the collaborative task. Effective collaboration requires alignment of each party's mental models. (1. Introduction · "continuously maintain and align mental models")
- **Map Task**: A classic social science experimental paradigm where one person acts as a guide and another draws a map based on instructions, evaluating team collaboration efficiency through information asymmetry. (3.2.2. Data Collection Process · "reproduce the route")
- **Action-Level Annotation**: Pairing every micro-action in the interaction stream (such as sending a single message or completing a single segment of drawing) with the participant's subjective psychological activity annotation at that exact moment. (1. Introduction · "Action-Level Mental model ANnotations")
- **Retrospective Labeling**: Having participants review behavioral recordings and temporal checkpoint anchors after the task is completed to debrief and label their actual thoughts at historical moments. (3.1. Annotation Framework · "to retrospectively annotate the team")
- **Grounding Acts**: Types of interactions in dialogue used to confirm mutual understanding (such as "Acknowledge" to indicate receipt, or "Repair" to correct a discovered mismatch). (3.2.2. Data Collection Process · "reproduce the route")
- **Self-Reasoning**: In mental models, the participant's private psychological derivation of their own behavioral motivations, which is the hardest dimension for external observers to infer. (4.3.2. Mental Model Prediction · "hardest dimension to predict")

## Before and After This Paper

- **Before This Paper**: All agent evaluations (such as ToolBench, WebArena, etc.) assumed that "being able to help humans complete tasks" made a good agent. Existing collaborative datasets also only recorded chat dialogue content and final outcomes, completely missing the "subjective thinking process" of humans during each step of collaborative decision-making. (1. Introduction · "primarily optimized for task completion")
- **After This Paper**: This study opens up the evaluation dimension of "process-level collaborative competence," elevating mental model alignment to a core standard of agent collaboration, and exposing the significant shortcomings of current large models in inferring human private reasoning. (1. Introduction · "processlevel collaborative competence")

## Most Worth-Reading Sections

- **Section 1 Discussion on the difference between collaborative skills and task execution skills**: (1. Introduction · "primarily optimized for task completion")
  - *Why it's worth reading*: This section very astutely points out that agents merely being good at task-solving is far from enough for them to work alongside humans in real-world workflows. Collaboration requires continuously adjusting and calibrating the mental states of both parties over long sessions, which establishes the theoretical foundation for the necessity of this entire study.
- **Section 3.1 Paragraphs explaining the two-step annotation framework**: (3.1. Annotation Framework · "to retrospectively annotate the team")
  - *Why it's worth reading*: This section explains in detail how to use Checkpoints as memory anchors to cleverly overcome the "recall bias" and "post-hoc rationalization" commonly found in retrospective reviews. It is highly valuable for developers designing human-computer interaction experiments.
- **Section 4.3.2 Analysis of the asymmetry in prediction difficulty between Guide and Follower in mental model prediction**: (4.3.2. Mental Model Prediction · (paraphrase, non-verbatim citation))
  - *Why it's worth reading*: This section reveals the cognitive asymmetry in human-machine division of labor. The Guide's mental model is extremely difficult to predict because they have long-term spatial path planning and partner state monitoring in their heads, which they do not necessarily speak aloud; whereas the Follower's behavior almost entirely follows the Guide's words, making the Follower's mind relatively easier to guess.