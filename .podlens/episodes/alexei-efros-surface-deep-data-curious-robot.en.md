Alexei Efros — known to this audience, he notes, primarily as Shiri's PhD advisor — opens by saying that this talk is meant to be a rhyme to Alison Gopnik's earlier presentation at the same workshop. Two researchers from very different disciplines — developmental psychology and computer vision — have arrived at the same frontier question: what is fundamentally missing from the current generation of AI systems, and what would it take to cross that threshold?

**Is the Bitter Lesson Bitter?**

Rich Sutton's 2019 manifesto, *The Bitter Lesson*, argues that annoyingly simple methods scaled up with computation work better than methods that try to encode human knowledge and structure. It has become one of the most cited frameworks in AI.

Efros has two problems with it.

First: is it even bitter? He walks through the history of science. Before Darwin, biologists like Linnaeus were cataloging every animal in elaborate hierarchies, building an edifice that seemed to require a lifetime of work. Then Darwin proposed a meta-model — evolution by natural selection — that was dramatically simpler and explained everything. The biologists who had spent their lives cataloging might have felt their work was overturned. But was it bitter? Efros doesn't think so. The goal of science is to find simple answers to what seemed complicated. Darwin's answer was simple. That's not failure — that's the whole point.

Newton did the same thing to pre-Newtonian physics. A colleague had called computer vision in 2007 "miscellaneous early efforts" before Newton — before something came along to unify the field. The arrival of the unifying principle isn't bitter. It's what you were working toward.

Second problem: is it even the right lesson? Sutton's manifesto mentions *computation* twenty-one times. It mentions *data* once, in passing. Efros thinks this misses what's actually driving progress.

**The Irreducible Entropy Argument**

There are researchers who believe in a deep equivalence between data and computation: any problem you can solve with lots of data, you could in principle solve without it if you're willing to generate your own data using compute. Simulate from the beginning of time with enough GPUs, and you get to our world without needing to scrape the internet.

Efros thinks this is wrong for a specific and important reason.

What you want to simulate is not *a* world. It's *our* world. The gap between those two things is enormous.

If you start simulating the universe from first principles, you immediately face an infinite sequence of random decisions. Did the asteroid hit the Earth and kill the dinosaurs? Which specific evolutionary path did each lineage take? There are billions of such coin flips between the beginning of time and the world we live in now. That vector of coin flips is what makes our world *our* world rather than one of the infinitely many other worlds the simulation could have produced.

This irreducible entropy — the specific history of our world — cannot be recovered from first principles. It has to be injected into any model of our world through data. There is no computational shortcut.

Efros has believed this for a long time. A 2009 paper he co-authored argued for the "unreasonable effectiveness of data." His intuition has only strengthened.

**What the Models Are Actually Doing**

His own lab has done data attribution work. You give a text-to-image model a prompt — a green creature made of leaves and vines bursting from the ground — and ask which images in the training set were most responsible for the generated output. The answer, found using a learned distance metric, is six specific paintings that were sitting in LAION, the training dataset. No one had looked at them before. They weren't famous. But once you see them, the generated image seems less miraculous. The model found these images and recombined them.

A paper Efros describes as one of his favorites this year (Surya et al.) provides a theoretical framework for this. Image diffusion models are, in essence, doing texture synthesis: finding nearest neighbors of patches in the training data, then stitching them together in a coherent way. They're not doing nearest neighbor lookup on whole images — they're working at the patch level, which is why the interpolation is so seamless. But it is interpolation.

This leads to his Arthur C. Clarke paraphrase: *interpolation in sufficiently high-dimensional space may be indistinguishable from magic.*

**Neural Thickets and What Post-Training Is Actually Doing**

Phil Isola (MIT) has a recent paper called Neural Thickets. If you take a randomly initialized small model and walk around its weight space, the nearby models are all terrible. But if you take a large model trained on enormous amounts of data and do the same random walk, the nearby models are remarkably good — often better than the original model on specific tasks like programming or mathematics.

This has a striking implication. You can do fine-tuning, you can improve performance on specific tasks, without any new data, without reinforcement learning — just random search in weight space near the original model.

Efros interprets this as evidence that the knowledge is already inside the pre-trained model. Post-training isn't adding knowledge. It's orientation. He uses the analogy of attending a party the night before an exam and showing up the next morning having forgotten which subject you're being tested on. The first question on the exam tells you whether it's physics or chemistry, and then you're fine — because you knew the subject, you just needed to know which one to activate.

The knowledge was always there. Post-training tells the model where it is.

**The Real Lesson: We Discovered How Simple We Are**

The humbling lesson from the past decade is not about AI. It's about humans.

Ninety-nine percent of the time, Efros argues, we are nearest neighbor machines — stochastic parrots, walking clichés, pastiches from our high school reading lists. We do what was done before, slightly recombined, slightly adapted to context. Only very rarely do we have what he calls "a flight of fancy" — a genuine moment of extrapolation that goes beyond what we've seen.

This is the Copernican revolution that the humanities hasn't fully reckoned with yet. AI systems have exposed something about human cognition that is uncomfortable: most of what we do looks, from the outside, a lot like what these models do. The question of whether there's something more — and if so, what — is now sharper than it has ever been.

**Surface Data versus Deep Data**

Current AI runs on what Efros calls surface data. Text scraped from the web. Photographs scraped from the internet. Audio passively received. These are things you can acquire without doing anything — just by sitting there and collecting what arrives.

Deep data is different. It's the data you have to work for. It's data that can only be obtained through action.

He gives three examples, each illuminating a different dimension of the problem.

How heavy is this knife? You can guess — you know that knives are usually metal, and metal is usually heavy, and this knife appears to be a standard kitchen knife. But you don't actually know. To know, you have to reach out and pick it up.

Is this liquid tea or honey? Looking at the color gives you a guess. You can't know without pouring it and watching the viscosity.

How do you open this MacBook? Try this edge. Try the other edge. Try again. No amount of looking at it tells you — you have to interact with it.

Babies are extraordinarily good at collecting deep data. They are, in Efros's framework, the most efficient deep data miners on the planet. He has a thought experiment: look around the room, pick up your phone or your keys, and try to imagine what they taste like. It's a slightly disturbing realization — that you can do this, with some accuracy. You can do it because when you were a child, you put everything in this room in your mouth. That's where the knowledge comes from. That's the deep data.

Surface data trains models that are very good at interpolation. They can produce, in Gopnik's phrase, an encyclopedia or a printing press — something that stores and recombines existing human knowledge with remarkable efficiency. What they cannot do is extrapolate. They can give you the pastiche; they cannot give you the next Borges or the next Bach. They are, in Efros's formulation, a distillation of two thousand years of written human knowledge — and we already know that distilled models don't generalize the way the original does.

Surface data has three characteristics: it's cheap, it's parallelizable, and the samples have roughly similar information density. Deep data is the opposite on every dimension. Expensive. Sequential — you can't parallelize deep data collection, because each action depends on the result of the previous one. And the variance between samples is enormous. Some interactions with the world reveal whole new layers of structure. Between those moments, you're gathering nothing interesting. You have to be a hunter for good samples.

**The Robotics Data Crisis**

Efros lays out what he calls the VC decision tree: to assess whether an AI company will succeed, look at how much data they have.

Text data: great. Image data: getting there. Video data: on the way. Robotics data: nothing.

The absence of robotics data is not just quantitative — it's qualitative. The data that does exist for robotics is the wrong kind. Teleoperation, the most common method, produces passive surface data. The human operator is doing the work; the robot is just recording. There's no negative feedback — the kind you get when you reach for something, fail to grip it, and have to adjust. And there's no scale.

Simulation, the other major approach, can in principle provide the physical feedback that teleoperation lacks. But current simulators don't have visual realism, tactile realism, or material realism. The reason goes back to the core argument: to make a simulator realistic, you'd have to inject all that irreducible entropy from the real world into it. Which means you've just restated the deep data problem. You haven't solved it.

Learning from video provides enormous quantities of data. But it provides surface data — you see what happens, you don't feel what happens. Efros tried to learn salsa dancing by watching videos. He confirms, from personal experience, that it doesn't work.

**Curiosity as the Engine**

If surface data produces interpolation and nothing more, and deep data is too expensive to collect the way we collect surface data — how do you build a system that collects deep data efficiently?

Efros's answer: curiosity. Not a metaphor. An engineering specification.

Define curiosity as prediction error. If a system tries to predict what will happen next — given some action in some state — and the prediction is wrong, that's information. The system encountered something it couldn't predict. That means it's in a region it doesn't understand. That region is worth exploring. The curiosity signal increases.

He and Deepak Pathak built a system in 2017 that implemented this idea and put it in front of Mario Brothers. No rewards. No score signals. No external feedback of any kind. Just a joystick and pixels, and a curiosity signal that increased when the system's predictions were wrong.

The result: the system learned to play. Not to *win* — it didn't care about the score. It cared about exploration. It stayed alive because dying ended the exploration. It moved forward because new levels contained new things it couldn't predict. It killed enemies not for points but because interacting with them revealed how they behaved.

He also has footage of the system playing ping pong this way. Its goal isn't to score. Its goal is to keep the rally going as long as possible — because a longer rally is more interesting. A shorter rally ends the data collection.

This work was done in simulation. It has never successfully generalized to a real robot. The real world is too complex, the feedback too slow, the state space too vast. Efros is honest about this. But he believes the direction is right.

The ultimate target, as he frames it: the scientist in the crib. A robot that has no assigned task. Whose only objective is to understand the world better. That opens doors because doors lead to new things it doesn't understand. That picks up objects because it doesn't know what they weigh. That never stops, because there's always something it hasn't predicted yet.

The slogan: *Ask not what the data can do for your robot. Ask what your robot can do for data.*

**What This Implies for AI's Future**

Efros is careful to say he could be wrong. The situation is evolving fast — "if we had recorded this talk six months ago, it would already be different." He might be wrong about the limits of interpolation. He might be wrong about curiosity being the right driver. He explicitly acknowledges that he's doing the work that comes *before* the scientific method — hypothesis selection — and that this part is art, not science.

But his intuition, grounded in thirty years of working with visual data, is that the current setup will hit a wall. Surface data can produce systems that seem magical for a long time. Interpolation in high dimensions is genuinely impressive. But the next Borges will not come from a system that has only ever scraped the surface.

He imagines a future — possibly near, possibly far — where small, seemingly useless robots wander through the world, picking things up, pouring liquids, opening doors, collecting the kind of data that no scraper can reach. Building the foundation for the generation of AI after this one.

Rich Sutton, after Efros gave the version of this talk that circulated as a preprint, published a new paper of his own. In the original Bitter Lesson, data was mentioned once. In the new paper, Sutton mentions data eighteen times.

Efros takes this as evidence that things are moving in the right direction. Or, as he puts it: "we feel like, you know, things are getting worse." He smiles.