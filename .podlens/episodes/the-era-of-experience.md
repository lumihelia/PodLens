## 这篇论文讲了什么

本篇论文由 David Silver 和 Richard S. Sutton 撰写（该文为即将由 MIT Press 出版的书籍《Designing an Intelligence》中的一个章节预印本）。论文探讨了人工智能（AI）正处于从“人类数据时代”向“经验时代”转变的临界点。作者指出，尽管当前的 AI（如大型语言模型，即 LLMs）通过在海量人类生成的数据上进行训练取得了巨大成功，但这种依赖模仿人类的方法在许多重要领域已接近极限。为了实现超人类的智能，AI 必须转向一种全新的范式——“经验时代”，即智能体主要通过与环境持续互动、自主产生经验并利用强化学习（RL）算法进行学习。论文详细阐述了经验时代的四个核心特征（流、动作与观察、奖励、规划与推理），论证了当前技术已具备实现这一转变的基础，并探讨了该范式带来的潜在社会影响与安全效益。

## 论文骨架

- **解决的问题**：人类数据时代的局限性。基于人类数据的监督学习由于高质量数据即将耗尽，其进步速度正在放缓，且无法产生超越人类当前理解范围的新见解。
  - 锚点：The Era of Human Data · "The pace of progress driven solely by supervised learning"
- **核心主张**：AI 正在迈入经验时代，智能体将主要通过自身与环境交互产生的经验进行持续学习，从而突破人类中心化 AI 系统的限制，获得超人类的能力。
  - 锚点：The Era of Experience · "experience will become the dominant medium of improvement"
- **论证方式**：论文采用立论性论文（position paper）的论证链。首先通过逻辑推理指出人类数据的瓶颈，接着通过最新案例（如 AlphaProof 在数学奥林匹克中的表现、DeepSeek-R1 的强化学习实践）证明经验学习的可行性。随后，作者从四个维度（流、动作与观察、奖励、规划与推理）对经验时代进行理论构建，并结合经典强化学习（RL）概念进行可行性论证，最后辩证地分析了该范式在安全与社会影响方面的后果。
- **关键证据与例子**：
  - **AlphaProof**：作为首个在国际数学奥林匹克中达到银牌标准的程序，它在人类生成的十万条形式证明基础上，通过强化学习算法与形式证明系统交互，自主生成了一亿条证明，从而探索了人类预设之外的数学可能性。
    - 锚点：The Era of Experience · "AlphaProof’s reinforcement learning (RL) algorithm subsequently generated"
  - **DeepSeek**：其最新工作（DeepSeek-R1）展示了强化学习的力量，无需显式教学，仅通过提供正确的激励，模型便能自主开发出先进的问题解决策略。
    - 锚点：The Era of Experience · "autonomously develops advanced problem-solving strategies"
  - **历史强化学习系统**：如 AlphaZero 在围棋和国际象棋中通过自我博弈发现了全新策略，证明了智能体自我发现知识的能力和可扩展性。
    - 锚点：Why Now? · "AlphaZero discovered fundamentally new strategies for chess"
- **承认的边界与局限**：
  - **物理时间的限制**：依赖物理经验的进步受限于在现实世界中执行动作和观察结果所需的实际时间，这无法一蹴而就。
    - 锚点：Consequences · "inherently constrained by the time it takes to"
  - **可解释性降低**：脱离人类数据和人类思维模式可能会使未来的 AI 系统更难被人类理解和解释。
    - 锚点：Consequences · "may also make future AI systems harder to interpret"
  - **对齐无法绝对保证**：尽管可以通过经验和双层优化来调整奖励函数以纠正偏差，但与人类目标的完全对齐仍然没有绝对的保证。
    - 锚点：Consequences · "there is no guarantee of perfect alignment"

## 核心论点清单

1. **人类数据红利正面临极限，无法引领 AI 达到超人类智能。**
   - 锚点：The Era of Human Data · "The pace of progress driven solely by supervised learning"
   - 类型：主张
   - 作者保留意见：无。作者明确指出，仅靠监督学习的进步速度正在放缓，且人类数据无法捕获超越人类当前理解的新科学突破。

2. **经验时代的智能体将存在于长期的、不间断的经验流中，而非简短的单次交互片段。**
   - 锚点：Streams · "An experiential agent can continue to learn throughout a lifetime"
   - 类型：定义
   - 作者保留意见：无。

3. **智能体将拥有更丰富的动作与观察空间，在真实或数字世界中进行自主交互，而非仅限于人类特权的形式（如纯文本对话）。**
   - 锚点：Actions and Observations · "act autonomously in the real world"
   - 类型：主张
   - 作者保留意见：无。

4. **依赖人类预判的奖励会给智能体性能设定无法逾越的上限，而来自环境的具地/接地奖励（grounded rewards）能让智能体发现超越人类现有知识的新策略。**
   - 锚点：Rewards · "Relying on human prejudgement in this manner usually leads"
   - 类型：主张
   - 作者保留意见：无。

5. **可以通过双层优化过程，将用户的宏观目标与环境的具地信号相结合，从而在用户引导下灵活调整奖励函数并纠正对齐偏差。**
   - 锚点：Rewards · "optimises user feedback as the top-level goal"
   - 类型：主张
   - 作者保留意见：作者指出这只是“勾勒出的一种可能满足这些要求的方法”，并承认可能还存在其他可行的方法。

6. **智能体可以利用非人类语言（如符号、分布式或连续计算）发现或改进更高效的思考机制，而无需局限于模仿人类的思维链。**
   - 锚点：Planning and Reasoning · "discover or improve such approaches by learning how to"
   - 类型：预测
   - 作者保留意见：无。

7. **智能体必须通过与现实世界交互（具地化）来测试和推翻继承自人类数据的错误思维假设，避免成为现有知识的“回音室”。**
   - 锚点：Planning and Reasoning · "grounding provides a feedback loop, allowing the agent to"
   - 类型：主张
   - 作者保留意见：无。

8. **经验时代的到来为重新审视和改进经典强化学习概念（如价值函数、探索、世界模型和时间抽象）提供了契机，从而铺平通往超人类智能的道路。**
   - 锚点：Reinforcement Learning Methods · "pave the way to truly superhuman intelligence"
   - 类型：主张
   - 作者保留意见：无。

9. **尽管经验学习会增加某些安全风险，但它也带来了独特的安全效益，例如智能体能动态适应环境变化，且其奖励函数可通过经验进行增量修正。**
   - 锚点：Consequences · "experiential learning will increase certain safety risks"
   - 类型：主张
   - 作者保留意见：作者承认，向经验时代的过渡确实需要进一步的研究来确保安全。

## 大白话重讲

这篇论文在跟什么较劲？简单来说，它在跟“AI 只能靠模仿人类来变聪明”这件事较劲。现在的 AI（比如各种大语言模型 LLMs）确实很厉害，能写诗、写代码，但它们都是靠“读人类写过的数据”训练出来的。作者们指出，这种靠模仿人类的套路已经快走到头了，因为高质量的人类数据快被吸干了。如果想让 AI 拥有超越人类的“超人类智能”，就必须让 AI 换个活法——从“人类数据时代”跨入“经验时代”。也就是说，AI 不能再只当个“书呆子”，而是要像小孩子一样，自己去和世界互动、自己去闯荡，通过“强化学习（RL）”从亲身经历的“经验”中学习。

论文的逻辑是这样展开的：首先，作者们指出了“人类数据时代”的死胡同。只靠模仿人类，AI 的进步速度已经明显慢下来了（The Era of Human Data · "The pace of progress driven solely by supervised learning"）。更重要的是，那些人类还没发现的新科学定理、新技术，人类数据里根本就没有，AI 怎么可能靠看书学会？

所以，AI 必须转向“经验时代”，通过与环境互动自己产生数据，并以此作为持续进步的动力（The Era of Experience · "experience will become the dominant medium of improvement"）。作者举了两个热乎的例子：一个是 AlphaProof，它在做奥数题时，人类只给了它十万条证明，它自己跟形式证明系统玩，硬是自主生成了一亿条证明，探索出了人类根本没想过的数学解法（The Era of Experience · "AlphaProof’s reinforcement learning (RL) algorithm subsequently generated"）；另一个是最近大火的 DeepSeek-R1，它证明了强化学习的魔力：我们不用手把手教它怎么一步步思考，只要给它对的激励（比如做对了就给糖），它自己就能摸索出超级厉害的解题策略（The Era of Experience · "autonomously develops advanced problem-solving strategies"）。

接下来，作者描绘了“经验时代”的四个核心特征。这四个特征非常反直觉，打破了我们对现在 AI 的认知：

第一，**“流（Streams）”**。现在的 AI 像个“金鱼脑”，你问一句它答一句，对话结束它就全忘了。但经验时代的 AI 拥有像人类一样长期的、不间断的“经验流”（Streams · "An experiential agent can continue to learn throughout a lifetime"）。它能活一辈子，记住过去的教训，为了几个月甚至几年后的长远目标（比如帮用户调理身体、学会一门新语言、研发新材料）去规划现在的每一步，哪怕这一步现在看起来没什么即时好处。

第二，**“动作与观察（Actions and Observations）”**。现在的 AI 被困在聊天框里，只能跟人类打嘴仗。未来的 AI 会像动物一样，拥有丰富的动作和观察能力，能自主在真实世界或数字世界里行动（Actions and Observations · "act autonomously in the real world"）。比如自己调 API、自己用人类的电脑界面、甚至在实验室里用机械臂做实验。它不再只是听人类的话，而是能自己去探索世界。

第三，**“奖励（Rewards）”**。这地方最反直觉：作者认为，**靠人类来给 AI 打分（评判好坏）其实是在害 AI**。因为如果一个策略连人类专家都看不懂、不理解，人类就会给它打低分，这直接给 AI 的能力封了顶（Rewards · "Relying on human prejudgement in this manner usually leads"）。要想超越人类，AI 的奖励必须来自环境本身（比如心率有没有变好、考试得没得分、物理模拟器里的材料结不结实）。那么怎么保证 AI 不失控呢？作者提出了一个“双层优化”的设想：最上面一层由人类用户给反馈，决定大方向；下面一层由 AI 自动去优化环境里的具体信号（Rewards · "optimises user feedback as the top-level goal"）。这样既能听人话，又能自主狂奔。

第四，**“规划与推理（Planning and Reasoning）”**。现在的 AI 思考时用的是人类的语言（比如“思维链”）。但人类语言真的是最聪明的思考方式吗？不见得。AI 完全可以用符号、连续计算等非人类语言，自己去发明更高效的思考机制（Planning and Reasoning · "discover or improve such approaches by learning how to"）。更重要的是，AI 必须通过和现实世界碰撞来检验自己的想法。如果只在人类数据里打转，AI 就会变成一个“偏见复读机”，继承人类所有的偏见和错误。只有去撞一撞南墙，AI 才能推翻那些错误的假设（Planning and Reasoning · "grounding provides a feedback loop, allowing the agent to"）。

为什么是现在？作者回顾了历史。以前的强化学习（比如击败围棋大师的 AlphaZero）虽然能自己发现新策略（Why Now? · "AlphaZero discovered fundamentally new strategies for chess"），但它只能在封闭的模拟器（比如棋盘）里玩，没法走到复杂的现实世界。后来大家发现人类数据真香，于是全去搞大模型了，结果把“自主发现知识”的灵魂给丢了。现在，我们有了大模型打底，又有了能和现实世界交互的工具，是时候把这两者结合，重新捡起经典强化学习的法宝（比如价值函数、探索、世界模型），铺平通往超人类智能的道路了（Reinforcement Learning Methods · "pave the way to truly superhuman intelligence"）。

当然，作者也很诚实地谈到了代价。AI 自己去闯荡，确实会带来安全风险，而且它发明了非人类的思考方式后，人类会越来越难理解它（Consequences · "may also make future AI systems harder to interpret"）。不过，经验学习也有独特的安全好处：第一，它能像活人一样根据环境变化自己调整，硬件坏了或者社会变了它能自己绕过去；第二，它的奖励机制可以在试错中不断微调，如果发现人类不高兴了，它能及时收手，不至于傻傻地把地球都做成回形针（Consequences · "there is no guarantee of perfect alignment"）；第三，在物理世界里做实验是需要时间的（比如研发新药做临床），这种物理时间的限制会成为 AI 自我进化的天然刹车（Consequences · "inherently constrained by the time it takes to"）。

## 术语小词典

1. **Supervised Learning (监督学习)**：AI 学习的一种常见方式，就像学生看着标准答案背书。AI 通过模仿人类写好的文本、代码等数据，来学习如何像人一样说话和做事。
   - 锚点：The Era of Human Data · "The pace of progress driven solely by supervised learning"
2. **Experience (经验)**：AI 不是通过看死书（静态数据），而是通过自己和环境进行互动（比如做动作、看结果、犯错、调整）所产生的一连串动态数据。
   - 锚点：The Era of Experience · "experience will become the dominant medium of improvement"
3. **Reinforcement Learning / RL (强化学习)**：一种“试错法”学习机制。AI 在环境里自己摸索，做对了获得奖励，做错了受到惩罚，从而不断优化自己的行为以获得更多奖励。
   - 锚点：The Era of Experience · "AlphaProof’s reinforcement learning (RL) algorithm subsequently generated"
4. **Grounded Rewards (具地/接地奖励)**：来自客观环境的直接反馈信号（如心率、考试分数、物理传感器的数值），而不是人类主观拍脑袋给出的评判。
   - 锚点：Rewards · "Relying on human prejudgement in this manner usually leads"
5. **Bi-level Optimisation (双层优化)**：一种两层嵌套的调优方法。上层由人类的宏观反馈（比如“让我更健康”）指明方向，下层则由 AI 自动去优化环境里的具体信号（比如睡眠、心率）来达成这个方向。
   - 锚点：Rewards · "optimises user feedback as the top-level goal"
6. **World Model (世界模型)**：AI 在脑子里对现实世界运行规律的模拟器。有了它，AI 在采取行动前，就能先在脑子里推演：“如果我做这件事，世界会发生什么变化？我会得到什么奖励？”
   - 锚点：Planning and Reasoning · "predicts the consequences of the agent’s actions upon the world"

## 这篇之前与之后

在这篇论文之前，AI 领域在过去几年里几乎全盘转向了“以人类为中心”的范式（如大语言模型 LLMs）。大家都默认：只要把全互联网人类写过的数据喂给 AI，再让人类专家对 AI 的回答进行打分和对齐（RLHF），就能造出最聪明的 AI。在这个过程中，经典的强化学习方法（比如让 AI 自己在脑子里推演的世界模型、自主探索新行为的机制）被边缘化了，因为模仿人类的捷径实在太好用了。
- 锚点：Reinforcement Learning Methods · "The rise of human-centric LLMs, however, shifted the focus"

这篇论文则发出了断言：只靠模仿人类已经快到头了，因为高质量的人类数据即将枯竭，而且模仿人类永远无法让 AI 产生超越人类当前认知的新发现。作者主张，AI 必须跨入“经验时代”，重新激活并升级经典的强化学习方法，让 AI 在长期的、与现实世界互动的“经验流”中自主学习。这直接挑战了当前极度依赖人类数据和人类主观评判的 AI 研发路线，指明了通往超人类智能的全新方向。
- 锚点：Reinforcement Learning Methods · "pave the way to truly superhuman intelligence"

## 最值得读原文的几段

1. **关于“人类数据枯竭”的危机论述**
   - 锚点：The Era of Human Data · "The majority of high-quality data sources - those that can actually"
   - **为什么值得读**：这段话一针见血地指出了当前大模型繁荣背后的隐忧——“数据墙”。它用大白话戳破了“只要堆数据，AI 就能无限变聪明”的幻想，是整篇论文立论的出发点。

2. **关于“人类主观评判会给 AI 设限”的反直觉论点**
   - 锚点：Rewards · "Relying on human prejudgement in this manner usually leads to an"
   - **为什么值得读**：这部分论证非常精彩且反直觉。我们通常觉得人类反馈（RLHF）是让 AI 变聪明的灵丹妙药，但作者指出，如果 AI 只能讨好人类评分员，它就永远无法发现那些超越人类理解的伟大策略。

3. **关于“AI 必须接地气才能打破思想回音室”的论证**
   - 锚点：Planning and Reasoning · "Without this grounding, an agent, no matter how sophisticated, will"
   - **为什么值得读**：作者在这里借用了人类科学史的演进（从万物有灵论到量子力学），说明了为什么只在人类文字里打转的 AI 会变成一个“偏见复读机”。想要获得真理，AI 必须像科学家一样去和物理世界碰撞。

4. **关于“物理时间是 AI 自我进化的天然刹车”的安全视角**
   - 锚点：Consequences · "inherently constrained by the time it takes to execute"
   - **为什么值得读**：在讨论 AI 失控风险时，这是一个非常务实且让人安心的视角。它提醒我们，即使 AI 智力爆炸，只要它需要和物理世界交互（比如做化学实验、等作物生长），它就必须遵守宇宙的物理时间规律，无法在虚拟世界里瞬间完成无限自我进化。