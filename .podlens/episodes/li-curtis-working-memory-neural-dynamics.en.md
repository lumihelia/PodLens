A bioRxiv preprint by Hsin-Hung Li and Clayton E. Curtis (Department of Psychology and Center for Neural Science, New York University), posted February 10, 2023. The paper uses fMRI during a memory-guided saccade task to study how working memory representations evolve across time in the human cortex — and discovers that early visual cortex is not a passive memory store but an active computational transformer.

**The Classic View and Why It Was Incomplete**

Working memory research has long centered on a simple model: neurons in prefrontal cortex (PFC) fire persistently during a delay period to maintain a representation of absent information. This "persistent activity" framework — dominated by monkey neurophysiology studies — treats WM maintenance as essentially a cache: store the sensory content, hold it until it is needed.

More recent work in monkey PFC found something more complicated: neural population codes during WM exhibit both stable components (decodable across time) and dynamic components (where representations evolve during the delay). Li and Curtis asked whether the same structure appears in human cortex, and if so, where.

**The Task**

Participants performed a memory-guided saccade task while undergoing fMRI. A brief target dot appeared at 12° eccentricity from fixation at a pseudo-random polar angle. The target was visible for 500 milliseconds, then disappeared. Participants maintained gaze at the fixation point for a 12-second delay period while remembering the target location. At the end of the delay, they made a saccadic eye movement to report the remembered location and also reported their memory uncertainty using a manual arc-length adjustment.

A control experiment with a subset of participants (n=6) used the same timing but replaced the dim memory target with a high-contrast flickering checkerboard — a salient sensory stimulus that participants were asked to ignore rather than remember. This passive viewing condition allowed the researchers to distinguish WM-specific dynamics from simple sensory persistence.

Retinotopic mapping sessions allowed the researchers to define population receptive fields (pRF) for each voxel — the location and size of each voxel's "window" into visual space — across eight ROIs: V1, V2, V3, V3AB, IPS0, IPS1, IPS2, IPS3, and two frontal regions (iPCS, sPCS).

**Two Analytical Tools**

The paper uses two complementary approaches to characterize the WM neural code.

*Temporal generalization analysis*: a decoder trained on fMRI voxel activity patterns at one time point is tested on all other time points. A stable code produces above-chance decoding across the off-diagonal elements of the cross-decoding matrix — the same decoder works regardless of when during the delay it is applied. A dynamic code produces off-diagonal elements that are significantly worse than the corresponding diagonal — the neural population that encodes the target location at time T1 is not the same population doing so at time T2.

*PCA-based neural subspace analysis*: principal component analysis identifies the low-dimensional subspace that best captures variance in voxel activity patterns. Stable subspaces are derived from time-averaged data. Dynamic subspaces are derived from early, middle, and late time windows separately. The *principal angle* between the early and late subspaces quantifies how much the neural representation has rotated in high-dimensional space — a large principal angle means the brain is using substantially different neural populations to represent the target at different points in the delay.

**Finding 1: Stable and Dynamic Codes Coexist in All Regions**

The temporal generalization analysis found stable WM codes (above-chance cross-decoding) in every ROI, including PFC. Within approximately 1–2 seconds of target offset, the WM content became decodable and remained so throughout the delay. The memory holds.

Most ROIs also showed dynamic codes: off-diagonal elements significantly worse than diagonal, indicating that the neural population encoding the target location changed over time. The two types of code coexist — memory is maintained and transformed simultaneously.

**Finding 2: Dynamics Are Strongest in Early Visual Cortex**

The key finding is a gradient. The degree of dynamics — quantified by the principal angle between early and late neural subspaces — varied significantly across ROIs (F(7, 91) = 3.88, p < .00). V1 showed the largest principal angles, indicating the greatest change in neural subspace across the delay. V3AB and the parietal IPS regions showed substantially smaller angles. PFC showed a stable code throughout, with no significant dynamic clusters in the temporal generalization matrices.

This is counterintuitive. The standard view treats PFC as the seat of working memory, with posterior sensory regions playing a supporting role. Here, the most active computational transformation during the delay is happening in V1, not PFC.

**Finding 3: What V1 Is Actually Doing**

The pRF projection method makes the V1 dynamics interpretable by mapping voxel activity patterns directly into two-dimensional visual field space. The result, shown across sixteen snapshots spanning the 12-second delay (Figure 4), is striking.

Early in the delay (0–4.5 seconds): V1 activation concentrates at the target's peripheral eccentricity (12°), in a compact, narrowly tuned response at the target's polar angle. The brain appears to be representing "the target is there."

Late in the delay (4.5–12 seconds): activation at 12° eccentricity decreases, and the response spreads inward, filling in a diffuse line-like pattern along the polar angle of the target, connecting the peripheral target location to the foveal region.

By the end of the delay, activation peaks near the fovea with a tail extending toward the target — the opposite spatial profile from early in the delay.

The proposed interpretation: V1 is recoding the sensory representation of the target's location into a representation of the planned saccade trajectory. The "target was at 12° in that direction" code is being transformed into a "to move my eyes from here to there" code. Memory maintenance and motor preparation are not sequential — they overlap and interpenetrate within the same neural structure.

**The Control Condition Confirms This Is WM-Specific**

In the passive viewing experiment, V1 showed only a stable code, not a dynamic one. Activation appeared at the target's location early in the trial and diminished over time — the profile of a sensory response fading, not a WM computation unfolding. The foveal spread observed in the memory task was entirely absent.

This confirms that the dynamic transformation in V1 requires WM maintenance — it is not a byproduct of sensory processing but an active consequence of the task demand to hold and prepare to report the location.

**PFC Is the Stable Abstraction Layer**

Prefrontal cortex (iPCS and sPCS) maintained decodable WM content throughout the delay with a stable code and no significant dynamic clusters. However, the PFC stable subspace did not preserve the spatial topology of target locations — the circular arrangement of 32 target positions that was preserved in the topographic structure of visual and parietal cortex was not present in PFC.

PFC "knows" that you are remembering a location, but it does not store the location in retinotopic coordinates. It is the highest-level abstraction of the WM content — task-relevant but geometrically impoverished relative to the visual representations.

**A Revised Picture of Working Memory**

The paper argues for a distributed, gradient WM system rather than a PFC-centered one:

V1 performs the most dynamic transformation — recoding sensory inputs into motor-proximal formats over the 12-second delay. It is the most task-embedded of the WM-maintaining regions.

Higher visual cortex (V3AB) and parietal cortex maintain stable, topographically organized representations of the remembered location throughout the delay — the abstract spatial record.

PFC maintains the highest-level, most stable representation — task-relevant and decodable, but lacking the spatial geometry that the lower-level regions preserve.

Working memory is not one thing happening in one place. It is a set of parallel computations at different levels of abstraction, all maintaining different aspects of the same remembered content, with the most dramatic temporal evolution happening not at the apex of the hierarchy but at its base.

**The Broader Implication**

A memory is not a copy of an experience held in a buffer. It is an ongoing process of reinterpretation — the brain continuously reformats what it is holding in memory into whatever is most proximal to the demands of the next action. "Remembering" and "preparing to act on the memory" are not sequential phases. In V1, they are the same process, observed at different moments in its unfolding.