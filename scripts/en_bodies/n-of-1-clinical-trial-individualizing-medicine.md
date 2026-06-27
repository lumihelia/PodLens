## What This Paper Is About

The gold standard of medical clinical trials is to recruit hundreds or thousands of people, run a randomized controlled trial, and arrive at a conclusion about "what works for most people." But "works for most people" is not the same as "works for you." The n-of-1 clinical trial takes a different road: the subject is you, the experimental object is you, and the conclusion serves only you. This review, published at the moment precision medicine was gaining momentum (2011), systematically surveys the design elements, statistical methods, technological support (wireless medical devices), and scaling pathways for n-of-1 trials, arguing for whether this road actually leads anywhere.

## Paper Skeleton

- **Abstract / Introduction**: standard randomized controlled trials (RCTs) produce population-level average effects, treating individual variation as "noise." The n-of-1 trial shifts the unit of statistical inference from "a group of people" to "one person," making the individual their own control.
- **Design elements**: surveys the core methodology of n-of-1 trials — ABAB crossover design, randomization, washout periods, double-blinding, placebo control — all borrowed from the statistical toolkit of standard population trials, just shrunk to a sample size of one.
- **Clinical Applications**: discusses which conditions are suited to n-of-1 design — chronic conditions that are relatively stable, have measurable clinical endpoints, and involve interventions with a relatively short half-life; acute infections, for example, are not suitable.
- **Combining n-of-1 Trials**: reviews the empirical experience of Guyatt, Larson, Mahon, and others, along with Australia's nationwide ADHD n-of-1 service program, arguing that individual trial results can be pooled and analyzed, serving both the individual (optimal treatment now) and the population (identifying responder characteristics).
- **Issues & Future Directions**: identifies the development of wireless medical monitoring devices as the key enabling factor for improving n-of-1 trial feasibility; the tolerance threshold for design heterogeneity in pooled analyses, and statistical handling of carryover effects, remain open problems.

## Core Arguments List

1. **N-of-1 trials are technically feasible in chronic-disease settings, and can directly serve the patient in front of you right now.** This is a structural advantage standard RCTs lack — an RCT produces a population average effect, while an n-of-1 trial's conclusion applies directly to the subject themselves.
   - Anchor: Clinical Applications · "chronic conditions for which there are easily measurable clinical end points… are the most amenable"
   - Type: Applicability review
2. **Multiple empirical studies show n-of-1 trials genuinely changed clinical decisions.** Over three years, Guyatt et al. found that the results of a large fraction of n-of-1 trials prompted physicians to change their planned treatment; Larson et al. found trial costs were comparable to conventional care, and both physician and patient confidence in treatment decisions rose significantly.
   - Anchor: Combining n-of-1 Trials · "not only were n-of-1 trials feasible, but [the] results of a large fraction of them prompted physicians to change their 'prior to the trial' plan of management"
   - Type: Clinical evidence
3. **N-of-1 trials can reveal "unnecessary overtreatment" specific to a given individual.** Mahon et al.'s randomized study found that using n-of-1 trials in patients with irreversible chronic airflow limitation reduced theophylline use without affecting exercise capacity or quality of life — indicating a systematic bias toward unnecessary treatment in standard prescribing practice.
   - Anchor: Combining n-of-1 Trials · "less theophylline use without adverse effects... suggests clinically important bias towards unnecessary treatment during open prescription"
   - Type: Clinical research findings
4. **Pooling data from multiple n-of-1 trials can extract population-level patterns from individual-level data.** The characteristics (genotype, clinical profile) of patients who respond well to a given intervention can be identified and, in turn, used to guide future treatment decisions for other patients — individual data accumulating upward into population knowledge.
   - Anchor: Combining n-of-1 Trials · "characteristics of patients who respond to one intervention can be identified"
   - Type: Methodological argument

## Plain English Explanation

You're sick, and your doctor has three drugs in front of her, each with some evidence of working for some people, but no way to know which one will work best for you. The usual approach: go by experience, go by guidelines, or try one and switch if it doesn't work.

This process is inefficient, slow, and full of uncertainty for the patient. That's exactly what the n-of-1 trial sets out to fix.

Here's how it works: you become your own experiment. Using an ABAB crossover design — A is treatment one, B is treatment two, alternating across several cycles, double-blinded, with data recorded — statistical methods at the end tell you which option actually works better for you specifically.

This isn't the standard clinical trial's goal of "finding what works for most people." It's "finding what works best for this one person."

That sounds niche, but research has found it sometimes reveals something startling: some people show zero response to a treatment widely considered effective, while simultaneously bearing its side effects — this is called "unnecessary overtreatment," and n-of-1 trials can identify it.

The scaling pathway is also interesting: if many n-of-1 trials are run simultaneously and their data pooled, you can discover which kinds of people (what genotype, what clinical features) respond best to which treatment — which in turn can guide future treatment decisions. Individual data accumulates into population-level knowledge.

## Glossary

**N-of-1 trial**: a single-subject experiment in which the subject serves simultaneously as their own treatment group and control group. Statistically compares the effects of different interventions across multiple crossover periods (e.g., ABAB).

**Clinical Equipoise**: a state of genuine uncertainty in medical decision-making — multiple treatment options each have supporting evidence, but it's unclear which is better. N-of-1 trials are designed precisely for this situation.

**Carryover Effect**: the effect of a previous intervention period "leaking" into the next period, confounding the assessment of the next intervention's effect. A washout period is used to reduce this problem.

**Randomized Controlled Trial (RCT)**: the gold standard of clinical evidence. Subjects are randomly assigned to a treatment group and a control group, and outcomes are compared. Produces a "population average effect."

**Time-series analysis**: a statistical method for analyzing data collected continuously over time. N-of-1 trials produce dense longitudinal data, which is better suited to time-series analysis than standard methods like the t-test (because measurements at adjacent time points are correlated).

## Before and After This Paper

### Preceding Works

Precision medicine had relied mainly on large-scale genomic data — finding associations between genetic features and treatment response through large population studies, then applying them to individuals. N-of-1 trials, although founded as early as the 1980s by Guyatt and colleagues, had not yet been taken seriously as a systematic pathway to individualized medicine, and lacked the technological conditions of the time (continuous, portable, objective measurement tools) to support large-scale application.

### Succeeding Lines

This paper systematically lays out n-of-1 trials as another technological pathway to individualized medicine, and explicitly identifies the development of wireless medical devices (just emerging in 2011) as the key enabling factor for improving feasibility. Looking back today, the paper accurately anticipated how technologies like wearable devices and continuous glucose monitoring would empower individualized health monitoring — its claim that "coordinated n-of-1 trials have the potential to radically change the way evidence-based and individualized medicine is pursued" has been borne out by over a decade of digital health development since.

## Sections Most Worth Reading in the Original

- **Abstract**:
  > "The ultimate goal of an n-of-1 trial is to determine the optimal or best intervention for an individual patient using objective data-driven criteria... Despite their obvious appeal and wide use in educational settings, n-of-1 trials have been used sparingly in medical and general clinical settings."
  - **Why it matters**: A single sentence that captures the entire reason this paper exists — the method's appeal is obvious, yet its clinical adoption rate is surprisingly low, and that gap is exactly what the paper sets out to explain and argue against.
- **Combining n-of-1 Trials (Mahon et al.'s theophylline study)**:
  > "they found n-of-1 trials led to less theophylline use without adverse effects on exercise capacity or quality of life... there was clinically important bias towards unnecessary treatment during open prescription of theophylline."
  - **Why it matters**: The most persuasive piece of evidence in the whole paper — it doesn't just claim "n-of-1 trials are feasible," it concretely proves that standard prescribing carries a systematic overtreatment bias, and that n-of-1 trials can catch it.
- **Issues & Future Directions**:
  > "Coordinated n-of-1 trials have the potential to radically change the way in which evidence-based and individualized medicine is pursued. The availability of relevant wireless clinical monitoring devices that are largely invisible to the user will enhance their value."
  - **Why it matters**: This 2011 prediction reads with unusual accuracy against today's backdrop of widespread wearables and continuous monitoring technology — the paper doesn't just describe the present, it precisely names which technological variable would become the key lever of the future.
