## What This Paper Is About

This is a bioRxiv preprint by Hsin-Hung Li and Clayton E. Curtis (Department of Psychology and Center for Neural Science, New York University), studying how working memory representations evolve over time in the human cortex. The question: during the delay period, is the neural representation of remembered content **stable**, or does it **change dynamically**? And does this differ across brain regions? The paper answers this with a memory-guided saccade task under fMRI — and the answer differs by region, and that difference itself reveals how working memory actually works: not as a single unified "cache," but as a distributed process that progressively transforms sensory input into a plan for action.

## Paper Skeleton

### Core Question

How do working memory (WM) representations evolve over time in the human brain? Is the neural representation of memory content during the delay period **stable**, or **dynamically changing**? Does the memory code differ across brain regions?

### Background

The classic picture of working memory is "persistent activity": neurons fire continuously during the delay period to maintain memory content, like a simple cache. This picture comes mainly from electrophysiological recordings in non-human primate prefrontal cortex (PFC). But recent work in monkey PFC found that neural population codes contain both stable and dynamic components (Spaak et al., 2017; Murray et al., 2017). The open question: what does this look like in human visual and parietal cortex?

### Experimental Design

**Main experiment: memory-guided saccade task**
- Participants fixated centrally inside an fMRI scanner.
- A brief (500ms) target dot appeared at a random polar angle at 12° eccentricity (32 positions covering the full circle).
- This was followed by a 12-second **delay period**: the target disappeared, and participants had to maintain memory of its location.
- After the delay, participants made a saccade to the remembered target location.
- Participants also reported their memory uncertainty (by adjusting an arc length).

**Control experiment: passive viewing**
- n=6 participants completed an additional experiment.
- Display conditions were similar, but the stimulus was a high-contrast flickering checkerboard (no memory required).
- Purpose: to separate whether delay-period neural activity is just slow sensory decay, or genuine WM maintenance.

**Key ROIs**:
- Early visual cortex: V1, V2, V3, V3AB
- Intraparietal sulcus (IPS): IPS0, IPS1, IPS2, IPS3
- Prefrontal cortex: inferior precentral sulcus (iPCS), superior precentral sulcus (sPCS)

**Analysis methods**:
1. **Temporal generalization analysis**: train a decoder at time point T1, test it at all time points T2 → a stable code decodes well across time points; a dynamic code decodes worse across time points than within the same time point.
2. **Principal component analysis (PCA)**: construct neural subspaces — a stable subspace (time-averaged) and dynamic subspaces (split into early/middle/late time windows) — and use the **principal angle** to quantify how much the subspaces have rotated relative to each other.
3. **Population receptive field (pRF) projection**: project voxel activity patterns into two-dimensional visual field space, visualizing where in the visual field the brain is "looking."

### Core Findings

**1. Stable and dynamic codes coexist in nearly every brain region**

Temporal generalization analysis showed a stable code in every ROI (cross-time decodable) — the memory target's location could be decoded throughout the entire delay period. At the same time, most ROIs also showed a dynamic code (diagonal performance > off-diagonal performance), meaning the neural code differs across time points.

**2. The degree of dynamics varies by brain region (the key finding)**

- **V1 is the most dynamic**: the neural subspace rotation angle between early and late time windows is largest.
- **V3AB and parietal cortex (IPS) are the most stable**: subspace rotation is smallest.
- F(7, 91) = 3.88, p < .00 (stability differs significantly across ROIs).
- PCA visualization: in V1, the target location's "trajectory" in space (a 3D spiral) shows clear evolution over time; in V3AB, the trajectory is more stable.

**3. V1's dynamic pattern: from periphery to fovea (the most specific finding)**

Via pRF projection into visual field space (Figure 4):
- **Early** in the delay (0–4.5s): V1 activation concentrates at the target's 12° peripheral eccentricity, a narrowly tuned point of activation.
- **Late** in the delay (4.5–12s): activation spreads from the target's eccentricity **toward the fovea**, forming a line of activation between the target location and central fixation.
- In other words: the code shifts from "where the target is" to "the path from here to the target."

**4. This dynamic is absent during passive viewing**

When participants merely passively viewed a flickering checkerboard (no memory required), V1 showed only a stable code, with activation decaying quickly over time. The dynamic spread toward the fovea appeared only under WM maintenance — proof that this is a genuine WM computation, not sensory residue.

**5. Prefrontal cortex: stable but without topographic structure**

Prefrontal regions (iPCS, sPCS) showed a stable code throughout the delay, with memory content decodable, but:
- Decoding error was larger than in visual and parietal cortex.
- The target location's position within the stable subspace did not preserve topographic relationships the way visual cortex did (it did not retain the visual field's spatial structure).
- PFC "knows" you are remembering a location, but does not store it in retinotopic coordinates.

---

## Core Arguments List

**1. Working memory is not a simple cache — it is an active format conversion**

The dynamics in early visual cortex (V1) show that memory is not "storing what was seen," but reformatting the sensory input (the target at 12° eccentricity) into a representation closer to the task's actual demand (a trajectory from fovea to target). The authors propose that V1's late-delay activation may represent a planned memory-guided saccade — the brain is already pre-computing "how my eyes need to move," not just "where the target is."

**2. The mechanism of the dynamics: different neural populations are recruited at different times**

PCA analysis shows the dynamics are not driven by "rotation" (a neural subspace rotating around an axis, as found in monkey PFC), but by different time windows using different neural populations to represent the target. The early and late subspaces are orthogonally rotated relative to each other — the activated population of neurons itself changes.

**3. Stability increases up the visual hierarchy**

V1 is most dynamic → V2, V3, V3AB become progressively more stable → IPS is more stable still → PFC is most stable. This gradient may reflect a division of labor: low-level visual cortex (V1) handles task-relevant format conversion (sensory → motor), higher visual and parietal cortex maintain abstract spatial memory (no need to change over time), and PFC maintains the highest-level task-relevant signal.

**4. The dynamics in early visual cortex come from top-down feedback**

The passive-viewing control rules out the explanation that the dynamics are merely slow sensory decay. Combined with the widening of V1's tuning width late in the delay (from narrow to broad, while V3AB does not change), the authors propose: V1's late-delay dynamics come from top-down feedback signals, originating in higher cortical areas with larger receptive fields, which "smooth" the precise point-like sensory representation into a broader path-like representation.

**5. A key difference between human and monkey PFC**

The coexistence of stable and dynamic codes found in monkey PFC studies was found in this study mainly in **visual cortex**, while the human PFC's WM code is predominantly stable with no significant dynamics. Whether this is a species difference or a methodological difference (fMRI vs. electrophysiology) cannot yet be determined.

---

## Plain English Explanation

You close your eyes and imagine a set of keys sitting on the upper-left corner of a table. What is your brain doing?

The classic answer: some neurons start firing, and keep firing, until you find the keys. This is called "persistent activity" — the brain as a cache that can briefly hold a charge.

This paper says: no, that's not what's happening.

The experiment is simple: in an fMRI scanner, a dot appears slightly to the left of where you're looking. It disappears after 0.5 seconds. You need to remember where it was, wait silently for 12 seconds, then point your eyes at its location.

The scanner recorded what happened in your visual cortex during those 12 seconds.

The result is surprising: in the most basic visual cortex (V1), the neural code for the memory **keeps changing**.

In the first 4 seconds, the area of V1 that activates corresponds to the target's peripheral position (12 degrees from the center of the eye). It's as if V1 is saying: "the target is over there, that direction, that distance."

But over the next 8 seconds, the activated area starts to **drift** toward the center of the eye — eventually forming a line extending from the fixation point toward the target's direction. It's as if V1 is now saying: "starting from here, go that way."

This isn't "storage" — it's **path planning**. V1 is reformatting "what was sensed" into "how the eyes need to move."

What's even more interesting: when participants merely passively watched a flickering light at the same location, with no need to remember it, this drift **doesn't happen at all**. The dynamic is specific to working memory — it's the result of the brain actively engaging with the task's demands.

This contrasts with higher-level brain regions. In parietal and prefrontal cortex, the neural representation of the target location stays fairly stable across all 12 seconds — but what they "know" isn't "the path from here to the target," it's the more abstract "I am remembering a location."

This gives us a new picture of working memory:

**Different brain regions work at different "levels" of memory.**

V1 is the layer closest to action — it re-encodes sensory information into task-relevant motor instructions. V3AB and parietal cortex are the middle layer — maintaining an abstract spatial position that doesn't change over time. PFC is the most abstract layer — it knows you're remembering something, but doesn't retain the specific spatial details.

Working memory is not a place, and not a single activity. It is a **dynamic transformation process distributed across brain regions**, gradually converting "what I saw" into "what I need to do."

---

## Glossary

- **Persistent activity**: the mechanism assumed by classic working memory theory — neurons fire continuously during the memory delay to maintain memory content, based mainly on electrophysiological recordings in monkey prefrontal cortex. (Summary · "The activity of neurons in macaque prefrontal cortex (PFC) persists during working memory (WM) delays providing a mechanism for memory")
- **Stable vs. dynamic WM code**: a stable code is a neural representation that stays consistent throughout the delay and can be identified by the same decoder across time; a dynamic code is one where the neural population representing the memory content changes over time. This paper finds the two coexist in most brain regions. (Results · "We found coexisting stable and dynamic neural representations of WM during a memory-guided saccade task.")
- **Neural subspace & principal angle**: a low-dimensional subspace extracted from neural activity via PCA; the principal angle measures how much the subspaces from different time windows have rotated relative to each other, and is the core metric for quantifying the "degree of dynamics." (Results · Neural subspaces · "We found that the stability of WM representations, quantified by principal angles, varied across ROIs.")
- **Population receptive field (pRF) projection**: a method that projects voxel activity patterns into two-dimensional visual field space, turning an otherwise abstract neural activity pattern into something you can directly "see" — exactly where in the visual field the brain is attending. (Discussion · "By projecting voxel activity in V1 into the visual field space, we found that the stimulus is reformatted into a representation that is more proximal to the behavior guided by the memory.")

## Before and After This Paper

- **Before This Paper**: working memory research long relied on electrophysiological recordings in monkey prefrontal cortex (PFC) as its central evidence, treating "persistent activity" (neurons firing continuously during the delay) as the primary mechanism of memory maintenance. More recent multivariate reanalyses found that stable and dynamic codes coexist in monkey PFC (Spaak et al., 2017; Murray et al., 2017), but whether this also holds in the human brain — and in which regions — was unknown.
- **After This Paper**: this paper establishes a picture that runs counter to the "PFC-centered" view — the region with the strongest dynamic code is not PFC, but early visual cortex (V1); V1 performs a format conversion during the memory delay, from a "sensory representation" into a "behaviorally relevant abstraction" (Discussion · "Neural dynamics in V1 resulted from the format of the WM representation changing into a behaviorally relevant abstraction of the stimulus."). This means future theories of working memory must account for both sensory features and their task-relevant abstractions, since a change in the format of remembered content itself drives neural dynamics — a fundamental revision to any single "persistent activity" model.

## Sections Most Worth Reading in the Original

- **The description in the Results section "Factors driving WM dynamics" of V1's spatial dynamics moving from periphery to fovea.**
  - Anchor: Factors driving WM dynamics · "In V1, the spatial pattern of the population neural response showed clear changes across time. The response first emerged at the target's polar angle and eccentricity...then spread inward across the visual field in a line between the target and the fovea."
  - Reason: this is the most concrete, most visualizable finding in the paper — one sentence precisely captures how V1 converts "where the target is" into "how to get there."
- **The theoretical statement in the Discussion about the stimulus being "reformatted into something closer to behavior."**
  - Anchor: Discussion · "By projecting voxel activity in V1 into the visual field space, we found that the stimulus is reformatted into a representation that is more proximal to the behavior guided by the memory."
  - Reason: this sentence is the condensed version of the paper's entire argument, elevating the specific V1 finding into a general claim about the nature of working memory itself.
- **The Discussion's contrast with monkey PFC research.**
  - Anchor: Discussion · "Distinct from the neurophysiological results in macaque PFC, we find evidence for coexisting stable and dynamic WM codes in early visual cortex, not PFC."
  - Reason: this sentence directly names the key tension between this study and the existing animal-model literature — the location of "dynamics" moves from PFC to V1, arguably the single most disruptive sentence in the paper.
- **The description in the Results section "Neural code during WM is stable in PFC" of V3AB's stability.**
  - Anchor: Neural code during WM is stable in PFC · "In V3AB, the ROI with the greatest stability, we found that the peak of activation remained at the target's peripheral location over the course of the trial."
  - Reason: provides the "control group" evidence that contrasts sharply with V1's dynamics, making V1's distinctiveness more credible.