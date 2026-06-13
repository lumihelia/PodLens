## What This Episode Is About

This episode originates from the fourth lecture of Stanford University's Spring 2026 course MS&E435 (Economics of the AI Supercycle), hosted by Apoorv Agrawal, featuring guest Ali Ghodsi, co-founder and CEO of Databricks. The conversation revolves around the real-world adoption of the AI industry, challenging Silicon Valley's current fanatical pursuit of Superintelligence and the resulting collective anxiety. Ali Ghodsi points out that AGI on a technical metric level was actually achieved under the 2009 definition by UC Berkeley AMPLab, but the root cause of the high failure rate in enterprise-side applications lies in the "Context Gap"—the model's lack of business context that only key internal employees possess. Through Databricks' own process restructuring experience, he demonstrates that the bottleneck for productivity gains lies in human organizational structures rather than model capabilities. At the same time, he deeply explores the value flow of the AI industry chain, predicting that the frontier model layer will face commoditization pressure from open source and dwindle into low-margin Token factories, while the true long-term core value will settle in the application layer and enterprises with proprietary data. Finally, he advises students in this period of technological transition to remain rational and make career choices that align with long-term slow variables, much like Jeff Bezos did in the early days of founding Amazon.

## Timeline Topic Map

- [00:00-01:30] Apoorv Agrawal opens with questions, and Ali Ghodsi discusses the current hype and anxiety in the AI industry, as well as the career planning pressure it places on Databricks interns.
- [01:30-04:03] Defining the concept of AGI: Ali Ghodsi cites the historical 2009 definition from UC Berkeley AMPLab, pointing out that AGI has actually already been achieved, and demonstrates the cognitive mismatch regarding the definition of AGI live in the classroom.
- [04:03-07:23] The current state of enterprise AI applications: analyzing the "Context" issue behind the 75% to 95% failure rate of PoC projects, where data and critical business knowledge fail to be fed into the model.
- [07:23-11:20] A dialectical analysis of the "death of software" theory: the new competitive landscape triggered by AI lowering barriers to entry and switching costs, and hard moats beyond software (such as brand, proprietary data, economies of scale, and trust).
- [11:20-13:38] The differing fates of legacy workflow software and data-centric software in the AI era, and the distribution, customer, and scale advantages held by incumbent software vendors.
- [13:38-16:42] Commenting on Ethan Mollick's "Jagged Frontier" chart, using Databricks technical support as an example to explain why edge cases are extremely difficult for AI to automate.
- [16:42-20:13] The productivity paradox in technological revolutions: citing Paul David's research on how the diffusion of the dynamo took 40 years to show benefits, illustrating the necessity for enterprises to restructure their organizational frameworks.
- [20:13-24:48] Case study of Databricks internally restructuring its Salesforce connector R&D process: using first principles to break through traditional product management, testing, and staffing bottlenecks to achieve a leap in productivity.
- [24:48-31:10] Value distribution in the AI industry chain: based on the five-layer architecture proposed by NVIDIA founder Jensen Huang, exploring how value moves upward, and comparing Cisco routers in the Internet era with the rise of Uber and Amazon.
- [31:10-33:30] The competitive landscape between open source and proprietary models, using Moonshot's release of Kimi 2.6 and 2.5 as examples to illustrate the pricing pressure open-source models exert on closed-source models.
- [33:30-35:58] Ali Ghodsi's personal favorite AI tool (Cursor) and Databricks' numerical decision assistant Genie.
- [35:58-39:00] Message to Stanford University students: do not be swayed by Twitter opinions; return to Jeff Bezos's long-term perspective of choosing books as an entry point, and focus on solving complex problems with long-term value.

## Core Insights List

1. The industry's frenzy and panic over AGI and Superintelligence are unnecessary, because according to the 2009 definition by UC Berkeley AMPLab, AGI has actually already been achieved.
   - Anchor: [01:42-03:43]
   - Type: Insight
   - Uncertainty/Hedging: Ali Ghodsi admits that people tend to move the definition's "goalpost" when AI fails to solve certain specific edge cases (such as counting the number of r's in "strawberry").

2. The PoC failure rate of enterprise AI applications is extremely high. This is fundamentally not a problem of insufficient intelligence in AI models, but rather that models lack the business context in the minds of human employees.
   - Anchor: [05:20-06:38]
   - Type: Insight

3. The introduction of AI has not led to the death of software, but has significantly lowered the barriers to entry and switching costs of software, forcing traditional software vendors to improve efficiency to cope with competition.
   - Anchor: [08:56-11:08]
   - Type: Insight

4. Traditional moats such as brand (e.g., Ferrari or Rolex), data, economies of scale, and trust (security certifications, etc.) cannot be directly replaced by cheap AI software.
   - Anchor: [11:08-12:28]
   - Type: Insight

5. Even in areas widely recognized as easily replaceable by automation, such as technical support, AI still cannot fully take over for highly complex platforms like Databricks, because what remains are edge cases that even human experts find difficult to resolve.
   - Anchor: [15:04-16:20]
   - Type: Example

6. Historical technological revolutions (such as dynamos replacing steam engines, PCs replacing typewriters) take decades to reflect improvements in the overall productivity of the economy, as this requires redesigning physical and process architectures.
   - Anchor: [17:07-19:57]
   - Type: Fact

7. The true efficiency gains of AI-assisted R&D depend on human process reforms rather than pure technology usage; Databricks multiplied efficiency only by breaking traditional long-cycle product requirement gathering, outsourced test environment setup, and shifting dedicated-manpower connector development to shared team responsibility.
   - Anchor: [22:05-24:44]
   - Type: Example

8. In the five-layer architecture of the AI industry chain, commercial value will ultimately move upward to the application layer (Applications) as historical patterns dictate, similar to how the ultimate winners in the Internet revolution were application providers like Uber and Amazon, rather than underlying router equipment providers like Cisco.
   - Anchor: [25:01-28:37]
   - Type: Prediction

9. Under the rapid approach of open source models and price wars, closed-source frontier models will eventually evolve into low-margin Token factories, with the competition essentially being a game of economies of scale similar to Amazon's book retailing.
   - Anchor: [32:17-34:44]
   - Type: Prediction
   - Uncertainty/Hedging: Believes that due to the existence of the Edge, there will be some small models running locally, but Token factories in large centralized data centers will remain the mainstream.

10. Truly outstanding business ideas (such as Airbnb, founded in 2009) often surface only years after the technology matures, because humans are naturally slow at conceiving great ideas and are easily limited by the "Tunnel Vision" of immediate technological frenzy.
    - Anchor: [36:42-37:45]
    - Type: Insight

## Internal Tensions & Self-Corrections

- [02:15] vs [05:20]: In the first half of the conversation, Ali Ghodsi insists that artificial general intelligence (AGI) has long been achieved and is already smarter than most people, but in the second half, when discussing enterprise applications, he bluntly points out that AI models lacking context are "useless" inside enterprises. This assertion creates a sharp internal tension between "technically powerful AGI has arrived" and "commercially, AI cannot deliver productivity."

## Plain English Retelling

We can set aside those tech myths plastered all over Twitter that keep people up at night with anxiety. The "Superintelligence" and ultimate singularity that Silicon Valley is currently chasing are, in many cases, just empty buzzwords. The truth is, if we go by our 2009 standards, we have long been surrounded by artificial general intelligence (AGI). Today's LLMs can easily answer highly complex academic questions, yet when you walk into any large enterprise, you don't see armies of AI employees working in an orderly fashion. It is still ordinary humans handling tedious spreadsheets in companies.

Behind this gap lies an extremely simple truth: even if an AI model has read all the books in the world, it cannot understand the specific circumstances of your company. In every department, there are one or two key employees known as "living dictionaries." If they leave, the entire system collapses because all the complex business details, historical baggage, and unwritten rules are in their heads. If this "context" cannot be fed into the model, even the most powerful AI will make utterly absurd mistakes in actual work.

Software is indeed undergoing a reshuffle, but it has not been declared dead. Because of the popularization of AI-assisted programming, anyone can now develop an application at an extremely low cost, which means the barrier to entry has been lowered, and the switching cost for users between different software interfaces has dropped to almost zero. However, the collapse of technical barriers actually makes traditional moats appear even more precious: your brand trust, your exclusive real-world data, and your scale of operations—these cannot be instantly wiped out by a string of cheap code.

Many enterprises complain that they have invested in AI but see no improvement in productivity data, which is just like when the dynamo was first invented at the end of the 19th century. For as long as 40 years, factories simply replaced steam engines with electric motors but continued to use the old multi-story, compact factory designs of the past, resulting in flat productivity. It wasn't until people realized they had to completely restructure the factory layout based on the distributed nature of electricity—establishing single-machine drives and more spacious single-story factory areas—that the true electrification revolution was completed. During the process of developing connectors internally at Databricks, the team initially fell into this trap as well. It took the CEO only two days to write a prototype personally, but it still took nine months for the product to go to market because the traditional organizational processes—spending a quarter on requirements research, consuming massive energy to configure third-party test environments, and low fault tolerance of solo operations—remained unchanged. Only by starting from first principles, shortening the requirement cycle to one week, parallelizing outsourced testing, and replacing single-point development with shared team responsibility, did R&D efficiency multiply through genuine organizational refactoring.

If we examine the value flow of the entire AI industry chain, the current frenzy is mainly concentrated on the underlying chips and computing hardware. But this is only a temporary supply mismatch. The history of technological evolution shows that all value eventually overflows to the level above the infrastructure, flowing to the application layer. This is just like during the dot-com bubble, when people rushed to buy Cisco routers to solve network transmission puzzles like "multicast." But as the cost of fiber-optic bandwidth plummeted, those technical hurdles became irrelevant, and the ones who made the real money were applications that didn't seem "sexy" at the time, like Amazon for online book selling, Uber for taxi matching, and Airbnb for home sharing. The rapid iteration of open-source models is also quickly pushing closed-source frontier models into a corner. Ultimately, the models themselves will become a low-margin Token commodity, as cheap as electricity.

Therefore, there is no need to feel suffocated by not keeping up with new models every day. The greatest applications (like Airbnb) are often created only years after the underlying technology has fully matured. In this transition period, the smartest strategy is to look far ahead, find real-world pain points that truly require rich context to solve, and take solid steps in the long process of organizational restructuring, rather than getting lost in the tech carnival on Twitter.

## Recommended Segments for Close Listening

- [00:35-01:30] **Intern Panic and De-escalation Advice**: Ali Ghodsi humorously describes the absurd anxiety of a 22-year-old intern rushing to start a business out of fear that AGI will instantly upend the world. Listening to this segment offers a direct sense of the ease and clarity this veteran business leader maintains amidst the noise.
- [02:23-02:57] **AGI Live Hypnosis Test**: In the classroom, Ali Ghodsi extremely cleverly reveals the cognitive bias of how humans constantly "move the goalposts" when defining AGI through live questions to Stanford University students, creating a highly dramatic effect.
- [20:50-22:05] **CEO Gets "Slapped in the Face" by the Team**: Ali Ghodsi recounts proudly boasting to his R&D team that he could write a Salesforce connector in two days using AI, only to have the team bluntly point out his naivety using rigorous production environment logic. This dialogue showcases the real collision between technical ideals and engineering reality.
- [26:12-27:28] **The Bankruptcy Story of the Multicast Problem**: Ali Ghodsi recalls his PhD days when the entire academic community was obsessed with multicast technology, dedicating countless brilliant minds to it, only to have the problem invisibly dissolve due to a sudden drop in fiber-optic costs. This history is highly cautionary for investors currently harboring the illusion that "GPU compute bottlenecks will last forever."