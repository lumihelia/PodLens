## What This Episode Is About

In this lecture, Yann LeCun explores the core role of World Models as the enabler of the next generation of the artificial intelligence revolution. Yann LeCun points out that current Large Language Models (LLMs) based on auto-regressive architectures have fundamental flaws when dealing with high-dimensional, continuous, and noisy real physical world data, making them unable to truly acquire human- or animal-level physical common sense and autonomous planning capabilities. He systematically explains how to achieve non-generative self-supervised learning through Joint Embedding Predictive Architecture (JEPA) and Energy-Based Models (EBM), avoiding pixel-level generation in high-dimensional spaces, and discusses how to prevent representation collapse through information maximization (such as the SIGREG algorithm and distillation methods). Finally, he introduces his newly founded company, Emmy Labs, which aims to apply Physical AI and control technologies to robotics and industrial processes.

## Timeline Topic Map

* **[00:00 - 01:07]** Bottlenecks in machine learning and the gap in learning efficiency: A comparison of learning efficiency between machines and humans/animals.
* **[01:07 - 02:40]** The dilemma of autonomous driving: The limitations of imitation learning and the lack of physical common sense, leading to Moravec's paradox.
* **[02:40 - 04:12]** The historical debate between Jean Piaget and Noam Chomsky regarding the innateness of language, and Seymour Papert's pointing out and re-advocacy of the limitations of perceptrons.
* **[04:12 - 05:37]** The essence of intelligence is the ability to quickly adapt to new tasks, rather than the accumulation of declarative knowledge or specific skills.
* **[05:37 - 08:05]** Infants learn about the 3D world and intuitive physics (gravity and inertia) through passive observation.
* **[08:05 - 09:54]** Violation of Expectation experiments: Measuring physical common sense in psychology and machine learning, mentioning collaborations with Jitendra Malik and Emmanuel Dupoux.
* **[09:54 - 11:39]** Comparative estimation of data volume: The equivalence between the text training volume of LLMs and the visual input volume of a four-year-old child.
* **[11:39 - 14:11]** Revolution in reasoning modes: Feedforward reactive systems versus reasoning systems based on energy minimization optimization search.
* **[14:11 - 15:54]** Structural flaws of auto-regressive LLMs and the action planning architecture of autonomous world models.
* **[15:54 - 17:26]** Guardrails and system safety based on energy minimization, contrasting with the safety vulnerabilities of LLM fine-tuning.
* **[17:26 - 19:54]** Hierarchical Planning: The unsolved challenge of decomposing high-level goals into low-level concrete actions in autonomous agents.
* **[19:54 - 23:36]** The failure of pixel-level video prediction: Pixel ambiguity and blurry prediction problems faced by generative models.
* **[23:36 - 26:05]** The proposal of Joint Embedding Predictive Architecture (JEPA): Making abstract predictions in representation space to filter out prediction noise.
* **[26:05 - 28:24]** The representation collapse problem in joint embedding architectures and its prevention mechanisms.
* **[28:24 - 33:20]** The conceptual framework of Energy-Based Models (EBM), and a taxonomic comparison between contrastive and regularized methods.
* **[33:20 - 34:49]** The principles, advantages, and disadvantages of dimensional contrast (such as VICReg) versus sample contrast (CLIP) in self-supervised learning.
* **[34:49 - 38:24]** Levels of abstraction in science: Ignoring low-level details to achieve long-range predictions, emphasizing that world models are not simulators.
* **[38:24 - 40:02]** Control requirements of complex physical systems (such as turbojet engines or patients): Learning phenomenological models to replace dynamical equations.
* **[40:02 - 45:11]** Principles of the SIGREG algorithm: Utilizing high-dimensional random projections and cumulative distribution function gradients to achieve isotropic Gaussian regularization.
* **[45:11 - 47:37]** Self-supervised learning of target networks based on distillation and Exponential Moving Average (EMA) (BYOL, Dino, I-JEPA, V-JEPA).
* **[47:37 - 51:14]** Experimental results of V-JEPA: Acquisition of physical common sense (violation of expectation) and 3D depth prediction.
* **[51:14 - 52:58]** Conclusion: Abandoning generative models and reinforcement learning, focusing on self-supervised representation learning based on world models.
* **[52:58 - 53:38]** Leaving Meta to found Emmy Labs, focusing on physical artificial intelligence and industrial control in high-dimensional, continuous, and noisy environments.
* **[53:38 - 58:40]** Q&A Session: How to implement physical constraints and guardrails in latent space representations.

## Core Viewpoints List

1. **Current mainstream machine learning architectures face severe bottlenecks in sample efficiency and common sense acquisition**
   * **Evidence Anchor**: [00:00 - 00:38]
   * **Type**: Fact
   * **Note**: Compared to humans and animals, machine learning models learn extremely slowly when facing new tasks and lack zero-shot adaptation capabilities.
2. **Text-only training cannot bring about true human-level intelligence**
   * **Evidence Anchor**: [10:50 - 11:52]
   * **Type**: Opinion
   * **Note**: The 20-30 trillion tokens consumed in LLM training would take a human 400,000 years to read, whereas the total amount of physical world information a four-year-old child obtains through vision is equivalent to it. Pure text lacks the physical world mapping of embodied common sense.
3. **The essence of intelligence is adaptability rather than the accumulation of declarative knowledge**
   * **Evidence Anchor**: [04:12 - 05:24]
   * **Type**: Opinion
   * **Note**: Jean Piaget's ideas show that intelligence is not the accumulation of declarative knowledge or specific skills, but rather the adaptability to cope with unknown situations and the ability to quickly acquire new skills.
4. **Reasoning based on energy optimization search is more powerful than direct feedforward computation**
   * **Evidence Anchor**: [11:58 - 13:32]
   * **Type**: Opinion
   * **Note**: Searching during the reasoning phase for action outputs that minimize the energy function provides a higher computational and reasoning ceiling than directly running a feedforward neural network with a fixed number of layers.
5. **World models should not be generative pixel-level prediction systems**
   * **Evidence Anchor**: [19:54 - 21:18]
   * **Type**: Prediction
   * **Note**: Redundant information and unpredictability in videos doom pixel-level prediction to failure (such as producing blurry predictions or only predicting the mean). The correct path is to make predictions in the abstract Representation Space.
6. **Hierarchical planning is the most central unsolved problem in the current field of agents and robotics**
   * **Evidence Anchor**: [17:26 - 19:54]
   * **Type**: Opinion
   * **Note**: How to decompose long-term macro goals (such as traveling to Paris) into sub-goals at various levels that do not require real-time fine planning (such as walking to the elevator, pushing the button) has not yet been systematically solved by anyone.
7. **Preventing representation collapse in self-supervised learning must rely on effective information maximization regularization methods**
   * **Evidence Anchor**: [26:05 - 27:31]
   * **Type**: Fact
   * **Note**: In non-contrastive methods, encoder outputs of constant values can be avoided by maximizing the information entropy between the dimensions of the representation vectors (making each dimension independent of the others).
8. **Reinforcement learning is extremely inefficient and its use should be minimized on the basis of complete feature representation**
   * **Evidence Anchor**: [52:21 - 52:58]
   * **Type**: Opinion
   * **Note**: RL sample efficiency is extremely low and should be used as a last resort when all else fails. Most learning should build a world model through observation, and then use RL at the top level after obtaining excellent representations.

## Internal Tensions and Self-Corrections

* **[55:27] vs [55:31]**: After declaring "I have been calling to abandon reinforcement learning," Yann LeCun immediately made a self-correction, clarifying "I don't mean abandoning it completely, but minimizing its use because its sample efficiency is extremely low." He further added that after the world model provides a good self-supervised representation, using reinforcement learning on top of that representation is reasonable and necessary.

## Plain English Retelling

Imagine you hired an extremely smart assistant who has absolutely no common sense about life. He has read every book in human history, can recite all the laws of physics, and can even write beautiful term papers. However, when you place an apple in front of him and remove its support, he doesn't know that the apple will fall—unless you explicitly wrote about it in a book. This is the current state of Large Language Models (LLMs) today: they possess a massive amount of "declarative knowledge" but know nothing about the physical world.

Yann LeCun issues a sharp warning: stop expecting to reach human-level AI by continuing to scale up LLMs (stacking computing power and feeding more data). A four-year-old child doesn't need to read 400,000 years of books to learn how to walk and avoid obstacles. Just during their waking hours, by staring at the world with their eyes, they receive an absurdly massive amount of visual data (about 10 to the 14th power bytes). This is equivalent to all the text data on the internet. Infants build a "world model" in their brains through passive observation.

What is this world model useful for? It can make "broad-direction predictions." For example, if you are in your office at NYU and want to plan a trip to Paris tomorrow. You don't plan in your head how your muscles should move every microsecond or how many centimeters your left foot should step forward. Instead, your world model gives rough steps: go to the airport, take a plane. In this process, concrete details (like going downstairs, waiting for a taxi, pressing the elevator button) are dynamically planned at different levels. This is hierarchical planning. In contrast, existing generative models, like Sora or various pixel prediction tools, try to precisely predict every single pixel in a video, which is as absurd as simulating the trajectory of every air molecule when designing a space shuttle. What we need is "abstraction"—filtering out unimportant pixel noise and keeping only the core structure.

The solution Yann LeCun offers is JEPA (Joint Embedding Predictive Architecture). Its brilliance lies in the fact that it does not make predictions in pixel space, but in "representation space." For example, if I show you half of a video and ask you to predict what happens next, JEPA won't try to draw everyone's face and the water cup on the table; instead, it predicts the abstract meaning that "this person will walk toward the podium." This not only saves an immense amount of computing power but also allows the model to capture true physical laws and causal chains.

So, how do we train this model without letting it "slack off" (i.e., causing representation collapse, where it only outputs all zeros or identical content)? Yann LeCun introduces a new method called SIGREG (Isotropic Gaussian Regularization). By projecting in multiple directions, it makes the data distribution resemble a uniform spherical Gaussian distribution, forcing each dimension of data to carry unique, non-redundant information.

Finally, Yann LeCun makes a highly controversial declaration: abandon pure generative models, minimize the use of reinforcement learning, and stop competing over LLMs in academia. He founded the new company Emmy Labs precisely to tackle how to make Physical AI achieve truly safe automatic planning through world models in complex industrial and robotic scenarios where formulas do not exist.

## Recommended Segments for Close Listening

* **[09:54 - 11:39]** Equivalence calculation of visual and text data: Yann LeCun uses very specific numbers to intuitively demonstrate the equivalence between a four-year-old's visual input and hundreds of thousands of years of text training. This is a key argument for dispelling the illusion that "LLM scaling can solve everything."
* **[17:26 - 19:54]** The Paris example explaining hierarchical planning: Using an extremely common daily travel example to break down what hierarchical planning means, and pointing out that this is an unsolved ultimate problem in the fields of robotics and AI to this day.
* **[49:37 - 51:14]** V-JEPA's "violation of expectation" experimental data: When scenes that violate physical laws, such as objects disappearing for no reason, appear in a video, V-JEPA's prediction error spikes. This fundamentally proves that self-supervised models can learn physical common sense through pure visual observation.