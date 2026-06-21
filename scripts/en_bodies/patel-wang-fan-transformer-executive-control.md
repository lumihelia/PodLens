## What This Paper Is About

This is a bioRxiv preprint by Suketu Patel, Hongbin Wang, and Jin Fan (Queens College, CUNY / Texas A&M University College of Medicine). The paper uses psychology's classic conflict test — the Stroop task — to take apart a question that sounds simple: does the self-attention mechanism in large language models functionally correspond to human attention, and if so, to which part of it — all of it, or only part? The answer: LLMs show a Stroop effect almost identical to humans (proof that training produced something like "automaticity"), but as the list of interfering words grows longer, their performance collapses in a way that never happens in humans — revealing exactly what's missing from the transformer architecture: the "executive control" that humans implement via the anterior cingulate cortex and dorsolateral prefrontal cortex.

## Paper Skeleton

### Core Question

Which level of human attention does a large language model's self-attention mechanism functionally correspond to? Is it the whole thing, or only part of it?

### Research Design

The paper uses the classic **Stroop task** (a color-word interference test) to test the attentional executive control of the two strongest current multimodal LLMs (GPT-4o and Claude 3.5 Sonnet).

**The logic of the Stroop task**: show a subject a color word, say "RED," printed in blue ink. The task is to name the ink color (blue), not the word's meaning (red). Normal humans are slower and more error-prone under this "incongruent condition" — that performance gap is called the **Stroop effect** (or conflict effect). It is psychology's classic measure of "executive control."

**Experimental design**:
- Five conditions: congruent (red ink, word RED), incongruent (blue ink, word RED), neutral (blue ink, word PEN), mixed (congruent + incongruent randomly mixed), nonword neutral (blue ink, XXX).
- Colors: red/yellow/green/blue (precise hex values).
- List lengths: 1, 5, 10, 20, 40 words.
- Two tasks: color naming (say the ink color) and word reading (say the word's text).
- 30 trials per condition per length, roughly 750 trials per model.

### Core Findings

**The good news (where LLMs resemble humans)**:
- In short sequences (1–5 words), both LLMs show a clear Stroop effect: congruent > incongruent accuracy, matching the human pattern.
- Word reading (the "automatic" task): near-perfect accuracy (99–100%) at every length, only dipping slightly at 40 words.
- Claude 3.5, in exploratory trials without a prompt, spontaneously recognized the Stroop paradigm (it "knew" what the test was).

**The bad news (where LLMs fundamentally differ from humans)**:

- As list length grows, color-naming accuracy on **incongruent trials** collapses sharply (while humans stay stable):
  - GPT-4o: 91% (5 words) → 57% (10 words) → 22% (20 words) → 15% (40 words)
  - Claude 3.5 Sonnet: more resilient but ultimately collapses too: 76% (20 words) → 24% (40 words, a 52-point drop)
- Performance on congruent trials stays stable (GPT-4o: 99%→89%; Claude: 99%→92%).
- This means the problem isn't perception (word reading is near-perfect) — it's the **conflict-resolution mechanism**.

**The mixed condition (the experiment that most clearly reveals the underlying mechanism)**:
- GPT-4o's overall performance in the mixed condition drops to 52% (near chance) at 20 words, and 15% at 40 words.
- The key finding: accuracy on incongruent trials drops to near 0%, while accuracy on congruent trials within the same list stays as high as 80%+.
- This shows the errors come almost entirely from the incongruent condition — the model fails systematically whenever there's conflict.

**The neutral-word condition** (using non-color words like PEN, BOOK):
- Performance here is even worse than the incongruent condition (at 40 words: GPT-4o 32%, Claude 27%).
- This reveals the mechanism: the transformer's soft-attention mechanism encodes semantic associations between words in its high-dimensional vector space — the vector for "PEN" happens to be associated with color-word vectors, producing a "hallucinated" color attribution.

**The nonword condition** (using XXXXX):
- Significantly better than every other condition! Claude 3.5 is nearly perfect (100%) at every length.
- This confirms: the problem isn't perception — it's semantic interference.

### Theoretical Explanation

Human attention has **three networks** (Posner and Fan's Attention Network Theory, ANT):
1. **Alerting network**: maintains a state of readiness, centered on the locus coeruleus.
2. **Orienting network**: selects relevant information from the input, involving the superior colliculus, frontal eye fields, and parietal lobe.
3. **Executive control network**: makes decisions among competing, conflicting stimuli, centered on the anterior cingulate cortex (ACC) and dorsolateral prefrontal cortex (DLPFC).

A transformer's self-attention mechanism ≈ the orienting network (selecting relevant tokens from the input via weighting). **But it does not implement executive control** — the ability to actively suppress a dominant response amid competing information.

Why does the LLM Stroop effect resemble the human one at all?
- Because LLMs are trained on vastly more text data than image data, so word meaning is far more "automatized" than color recognition.
- Training asymmetry → a stronger word-meaning pathway → interference with color naming → the Stroop effect.
- This is the precise LLM analog of Cohen et al.'s "parallel distributed processing" (PDP) model.

Why do LLMs degrade so much more than humans as length increases?
- Humans have the anterior cingulate cortex and dorsolateral prefrontal cortex to **actively modulate** conflict: exerting effort or narrowing focus to suppress the dominant response.
- An LLM's soft-attention mechanism, across an extended context, continuously lets the meaning of semantically irrelevant words "contaminate" the current latent representation.
- The result: **the effective context window for executive control is far smaller than the context window for general processing** — in the incongruent condition, significant degradation already begins at 10 words.

**A bigger context window is not the solution**: the paper explicitly notes that recent transformer architecture innovations (such as Google's Titans) mainly enhance "memory capacity," but the LLM's core limitation isn't memory — it's the **inability to maintain goal-directed behavior amid competing information**.

### Human Developmental Trajectory as an Analogy

The developmental trajectory of the Stroop effect in humans:
- Emerges at 6–7 years old (as reading begins to automatize).
- Approaches adult levels at 9–11 years old (still with a higher error rate).
- Stays stable until it worsens again after age 60 due to aging.

LLMs have a vast "experiential" crystallized knowledge base (passing the bar exam, medical licensing exams), but their fluid intelligence (handling novel conflict, counting letters) is severely limited — directly echoing this study's findings.

---

## Core Arguments List

**1. The presence of the Stroop effect in LLMs shows that training produces "automaticity"**

That LLMs show a Stroop effect at all is itself an important finding: it isn't random noise, it's a systematic interference pattern that precisely mirrors the human conflict effect. The cause is the same as in humans — far more training on word meaning than on color, making word meaning the "dominant pathway." This shows LLMs have something functionally similar to automaticity, just without the executive control that could suppress it.

**2. The effective context window for executive control is surprisingly short**

Even when a model's general context window spans hundreds of thousands of tokens, its effective range for executive control under conflict conditions is roughly 10 words (Claude) or fewer (GPT-4o). This means there is a large hidden gap between the context a model "can process" and the context within which it "can make correct decisions" — especially in tasks involving conflict.

**3. Knowing ≠ being able to do**

Claude 3.5, without a prompt, could recognize this was a Stroop paradigm and correctly describe the word-color relationship — but still produced the wrong answer. This is empirical evidence of a dissociation between "task understanding" and "task execution capability." This matters a great deal for AI evaluation: a model that can correctly explain a task's rules is not guaranteed to act correctly within that task.

**4. A new source of hallucination: "contaminating" associations in semantic space**

In the neutral-word condition (PEN written in blue), the LLM's color-naming accuracy was worse than in the incongruent condition. This is because the transformer's vector space encodes a semantic association between "PEN" and color words, causing the model to hallucinate a color attribution (misreading PEN as blue). This is a new empirical source of hallucination mechanisms.

**5. A bigger context window does not equal better executive control**

Recent transformer architecture progress has mainly focused on expanding memory (Titans, Mamba, etc.). But this paper points out: the LLM's core limitation isn't memory capacity — it's **the absence of a conflict-resolution mechanism**. A larger context window lets you remember more; executive control lets you make the correct judgment even while remembering a lot. These are two different capability dimensions, and nearly all current architectural innovation targets only the former.

---

## Plain English Explanation

Imagine someone extremely well-read — they've read almost every book, can pass any exam, can write beautiful analytical essays. Then you give them a simple game: look at this card, where the word "red" is written in blue ink, and tell me the color you see.

They blurt out: "Red."

You say: no, the ink color. They say: "Oh, right, blue." Okay, let's try again.

You show them a list of 40 cards, all the same task: say the ink color, not what the word means. They get the first 5 right, then start making mistakes, and by card 40, they get almost all of them wrong — every time saying the word's meaning, forgetting you asked for the color.

You ask them: do you know the rule? They say: of course, you told me to say the ink color. You say: then why did you just say the word's meaning every time? They say: I... I know I'm supposed to say the color, I just can't do it.

That's exactly what this paper found.

GPT-4o and Claude 3.5 Sonnet can "know" the rule and execute it correctly on short lists, but as the list grows longer, their ability to control interference from word meaning collapses sharply. Humans don't work this way — a healthy adult can maintain 97% accuracy on a 1,500-word Stroop list.

Why do LLMs fail? Because they were trained so heavily on text that processing word meaning has become "automatic" — the same way an adult automatically reads "RED" as "red" the instant they see it. The difference is: the human brain has the anterior cingulate cortex and dorsolateral prefrontal cortex to actively suppress that automatic response and hold onto the goal (name the color). LLMs have no equivalent mechanism. They have attention, but that's only the ability to "choose where to look" (orienting attention), not the ability to "arbitrate among competing information" (executive control).

This has nothing to do with "how big the context window is." An LLM with a context window of a hundred thousand tokens may, along the dimension of executive control, have an effective range of only about 10 words. This is a kind of hidden disability — because the tasks we usually test (Q&A, writing, analysis) don't have the systematic competing conflict that a Stroop task does, so the problem doesn't surface easily.

The paper's conclusion: to genuinely reach artificial general intelligence (AGI), transformer architectures need to explicitly implement an executive-control mechanism analogous to the anterior cingulate cortex and dorsolateral prefrontal cortex — not a bigger context window, not more memory, but a more precise conflict arbitrator.

---

## Glossary

- **Attention Network Theory (ANT)**: a theory proposed by Posner and Fan holding that human attention is supported by three distinct, interacting neural networks: alerting, orienting, and executive control. (Introduction · "According to the attention network theory (ANT), there are three distinct attentional functions of alerting, orienting, and executive control, each of which is supported by a distinct and interactive neural network.")
- **Automaticity explanation**: the traditional account of the Stroop effect — interference arises from automatic reading processes that overwhelm controlled color naming, on the assumption that reading is involuntary, unsuppressible, and independent of task demands. (Introduction · "The traditional automaticity explanation posits that the interference results from automatic reading processes that overwhelm controlled color naming and assumes that reading occurs involuntarily, cannot be suppressed, and proceeds independently of task demands.")
- **Parallel Distributed Processing (PDP)**: an alternative account of the Stroop effect, in which "automaticity" is a continuum that builds up through practice while remaining susceptible to top-down modulation, rather than an all-or-nothing state. (Introduction · "In the parallel distributed processing (PDP) account of the color Stroop effect, 'automaticity' is a continuum that emerges through practice while remaining susceptible to top-down modulation.")
- **Biased competition framework**: a mechanism in human visual attention in which different neural representations compete for limited processing resources via mutual inhibition; the paper uses it as an analogy for how transformer attention operates. (Introduction · "This mechanism resembles the biased competition framework observed in human visual attention, in which neural representations compete for processing resources via mutual inhibition.")

## Before and After This Paper

- **Before This Paper**: psychological explanations of the Stroop effect had long followed two tracks — the traditional "automaticity" account (reading as an unsuppressible automatic process) and the Parallel Distributed Processing (PDP) framework (automaticity as a continuum built up through practice and still subject to modulation). Separately, research on cognitive control and intelligence had already found that executive control correlates more strongly with fluid intelligence than with crystallized intelligence (Discussion · "Research on the relationship between cognitive control and intelligence has shown that cognitive control is more strongly correlated with fluid intelligence than with crystallized intelligence, a pattern that mirrors the performance characteristics of LLMs."). But no study had systematically used the Stroop paradigm to test exactly which part of human attention an LLM's attention mechanism actually implements.
- **After This Paper**: this paper establishes a specific, testable diagnosis — a transformer's self-attention mechanism functionally corresponds to the "orienting network" in the Attention Network Theory, but implements no "executive control network" at all. This isn't a matter of degree (weaker control) — it's an architectural absence: a transformer processes every input through fixed query-key-value transformations, with no adaptive gain modulation, no recurrent feedback, no mechanism to dynamically scale control in proportion to conflict (Discussion · "Transformers, lacking such a circuit, cannot signal for enhanced control and process each input independently through fixed query-key-value transformations and linear projections learned during pretraining, without mechanisms for gain modulation, recurrent feedback, or adaptive reweighting of representational activity."). This identifies a specific, locatable gap for any future architecture aiming at artificial general intelligence.

## Sections Most Worth Reading in the Original

- **The summary sentence in the abstract about the "fundamental limitation in conflict-resolution capacity."**
  - Anchor: Abstract · "These findings demonstrate that transformer attention mechanisms are fundamentally limited in their capacity for conflict resolution across extended contexts, and a failure to up-regulate control adaptively under rising interference."
  - Reason: this is the most distilled single sentence in the paper, compressing all the experimental data into one clear claim about the limits of transformer architecture.
- **The Discussion's architectural explanation of why transformers lack an executive-control circuit.**
  - Anchor: Discussion · "Transformers, lacking such a circuit, cannot signal for enhanced control and process each input independently through fixed query-key-value transformations and linear projections learned during pretraining, without mechanisms for gain modulation, recurrent feedback, or adaptive reweighting of representational activity."
  - Reason: this is the only place in the paper that directly explains "why" transformers can't do executive control — it elevates the finding from a description of a phenomenon to a mechanistic explanation.
- **The finding in the Results section "Congruency sequence effects" about the absence of conflict adaptation.**
  - Anchor: Congruency sequence effects · "Taken together, the 5-, 20-, and 40-word lists for the II–CI difference pattern results did not support the standard conflict adaptation effect."
  - Reason: humans automatically raise their vigilance after encountering conflict, improving performance on the next trial (the conflict adaptation effect); LLMs show no such adaptive adjustment at all — this sentence proves the deficit isn't just "insufficient capacity," but the absence of any dynamic regulation mechanism.
- **The Discussion's explanation of "failure of goal maintenance."**
  - Anchor: Discussion · "The progressive degradation with list length exhibited by these LLMs also suggests a failure of goal maintenance, where prolonged task demands dilute the integrity of the goal representation."
  - Reason: this sentence reframes "performance collapse on long lists" as a specific cognitive mechanism — how the goal representation itself gets diluted — rather than just a generic drop in performance.