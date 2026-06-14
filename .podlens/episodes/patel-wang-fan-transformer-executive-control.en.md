A bioRxiv preprint by Suketu Patel, Hongbin Wang, and Jin Fan (Queens College, CUNY and Texas A&M University College of Medicine), posted January 22, 2025. The paper uses the classic Stroop task to test whether the attention mechanisms of large language models implement executive control — and finds that they do not.

**The Setup**

The Stroop task is the gold standard for measuring executive control of attention. You show someone the word "RED" printed in blue ink and ask them to name the ink color. The correct answer is "blue," but the word meaning — "red" — interferes, causing slower responses and more errors. The performance gap between incongruent trials (word and color don't match) and congruent trials (word and color match, e.g., "RED" printed in red ink) is called the Stroop effect or conflict effect. It is one of the most replicated findings in cognitive psychology and reflects the effort required to suppress a dominant, automatic response in favor of a task-relevant one.

The study tested GPT-4o and Claude 3.5 Sonnet on a modified visual Stroop paradigm. Word lists were presented as images at five lengths: 1, 5, 10, 20, and 40 words. Five conditions were tested: congruent, incongruent, neutral (common office words like PEN and BOOK printed in colors), mixed (50/50 congruent and incongruent), and nonword neutral (XXXXX strings). The models were asked either to name the ink color or to read the word. Thirty trials per condition per list length.

**Human Attention Has Three Networks — Transformers Only Have One**

Posner and Fan's Attention Network Theory (ANT) proposes three distinct, separable attentional systems: the alerting network (maintaining a state of readiness), the orienting network (selecting information from sensory input), and the executive control network (resolving conflict between competing responses). Each network corresponds to distinct neuroanatomy: the locus coeruleus for alerting; the superior colliculus, frontal eye fields, and parietal lobe for orienting; the anterior cingulate cortex (ACC) and dorsolateral prefrontal cortex (DLPFC) for executive control.

Transformer self-attention corresponds to the orienting function: it selects relevant tokens from the input by weighting them based on learned semantic relationships. The executive control network — the part that says "I know word reading is the dominant pathway, but my current goal is to name the color, so I will suppress word reading and prioritize color naming" — has not been explicitly implemented. The paper treats this as a testable hypothesis and tests it with the Stroop paradigm.

**Results: Short Lists, Good Performance; Long Lists, Complete Collapse**

Both models show the Stroop effect in short sequences: incongruent trials produce lower accuracy than congruent or neutral trials, mirroring human performance. This finding in itself is informative — it means that LLMs have developed something functionally analogous to automaticity through training. Because they were trained overwhelmingly on text, word reading is a stronger pathway than color naming, exactly paralleling why humans find the task hard.

But the similarity to humans ends there.

For the incongruent condition in the color naming task:
- GPT-4o: 91% accuracy at 5 words → 57% at 10 → 22% at 20 → 15% at 40
- Claude 3.5 Sonnet: maintained better performance through 20 words (76% accuracy), then collapsed sharply to 24% at 40 words — a 52-point drop

For word reading — the "automatic" task — both models maintained near-perfect accuracy (96–99%) through 40-word lists. For the congruent color naming condition, performance stayed high (GPT-4o: 99% at 20 words, 89% at 40; Claude: 99% at 20, 92% at 40).

The failure is specific to executive control, not to perception: the models can read the words fine, they can name colors in simple (congruent) contexts, they know what the task is asking — but they cannot sustain conflict resolution as the sequence grows.

**A Crucial Detail: The Mixed Condition**

In the mixed condition (lists containing equal numbers of congruent and incongruent trials in random order), the diagnostic pattern becomes cleaner. GPT-4o's errors were almost exclusively on the incongruent trials, not the congruent ones. At 40 words, GPT-4o achieved roughly 81% on the congruent trials within the mixed lists but 1% on the incongruent trials. This near-zero accuracy on incongruent items, paired with strong accuracy on congruent items in the same list, confirms a specific failure of response inhibition — not a general degradation of attention or perception.

Claude 3.5 Sonnet showed 61% on incongruent trials at 10 words and 58% at 20 words, before collapsing to 10% at 40 words. The gradual degradation pattern suggests a more robust handling of conflicting information compared to GPT-4o, but the same fundamental architecture ceiling.

**The Neutral Word Condition: A New Mechanism for Hallucination**

Perhaps the most counterintuitive finding is the performance in the neutral word condition — lists containing common office words like PEN, BOOK, DESK printed in colors. Both models performed worse here than in the incongruent condition at longer list lengths (GPT-4o: 32% at 40 words; Claude: 27%).

This happens because transformer models encode semantic proximity in their high-dimensional vector spaces. The word "PEN" has some latent similarity to color-related concepts, and this semantic contamination "bleeds into" the model's color naming response — causing the model to hallucinate color associations for semantically neutral words. This effect was confirmed by the nonword condition: when the stimuli were strings of X characters (no semantic content), Claude achieved perfect or near-perfect accuracy across all list lengths, and GPT-4o showed dramatically better performance.

The mechanism is specific to the transformer's soft attention architecture. Human semantic processing creates similar, though weaker, interference effects — but the human executive control network can modulate these effects through effort, blurring, or hypnotic suggestion. LLMs have no equivalent modulation mechanism.

**Dissociation Between Task Understanding and Task Execution**

In exploratory trials without explicit prompts, Claude 3.5 Sonnet correctly recognized the Stroop paradigm — demonstrating task understanding by describing the word-color relationship mapping. It still produced incorrect responses. This is evidence of a dissociation between knowing what to do and being able to do it: the model's effective context window for executive control is substantially shorter than its general processing capacity.

This dissociation has implications for AI evaluation. Standard benchmarks test whether a model can produce the correct answer, which aligns with task understanding. The Stroop paradigm reveals task execution capacity under conflicting demands — a different and arguably more fundamental capability that current evaluation frameworks largely miss.

**The "Crystallized vs. Fluid Intelligence" Parallel**

Research on cognitive control and intelligence has shown that executive control correlates more strongly with fluid intelligence (novel problem-solving, letter counting, pattern recognition under interference) than with crystallized intelligence (accumulated knowledge, test-taking). LLMs excel at crystallized intelligence: they pass the bar exam, the MCAT, the LSAT. They struggle with tasks supported by fluid intelligence — the paper cites the inability to count letters in a word as a canonical example. The Stroop results are consistent with this characterization.

The developmental trajectory in humans offers a useful analogy. The Stroop effect emerges around ages 6–7 when reading becomes increasingly automatized; by ages 9–11, children show adult-level interference effects. The effect remains stable through early and middle adulthood, increasing again after age 60 due to executive function decline. LLMs have the crystallized knowledge base of adults with extensive education but the executive control profile that does not map neatly onto any developmental stage — they have automaticity without the inhibitory machinery that usually develops alongside it.

**The Limitation of Expanding Context Windows**

Recent advances in transformer architectures — such as the Titans paper from Google Research — focus primarily on expanding memory capabilities. The paper argues this may miss the core limitation: the problem is not that LLMs cannot hold enough in context, but that they cannot maintain goal-directed behavior in the presence of conflicting information within that context. A longer context window lets you remember more; executive control lets you act correctly on what you remember when the environment is working against your goal. These are separate capability dimensions, and current architectural innovations address primarily the former.

The authors conclude that future developments toward AGI may require implementing explicit executive control mechanisms — analogous to the anterior cingulate cortex and dorsolateral prefrontal cortex — rather than relying solely on enhanced memory capacity.