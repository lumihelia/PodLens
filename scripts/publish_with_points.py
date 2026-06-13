"""Re-publish the 5 Claude-translated episodes with full connection fields (why, this_point, that_point)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEMS = [
    {
        "slug": "joscha-bach-nature-of-reality-dreams-consciousness",
        "report": "reports/joscha-bach-nature-of-reality-dreams-consciousness.md",
        "url": "https://youtu.be/rIpUf-Vy2JA?si=gXnGCO58t36qh8Ae",
        "kind": "podcast",
        "date": "2026-06-09",
        "title": "现实之网、梦境与意识的本质 · Joscha Bach",
        "tags": ["控制论", "注意力模型", "模拟假说", "自由意志", "认知基础设施", "意识形态"],
        "connections": [
            {
                "slug": "joscha-bach-life-intelligence-consciousness-future",
                "kind": "resonance", "relation": "同构",
                "why": "两期均为 Joscha Bach 主讲，共享控制论意识框架——将意识定义为注意力控制系统的自建模，将自我视为在神经基底上临时运行的软件。",
                "this_point": "[03:09-05:03] 意识是感知象与动机猴发生冲突时被激活的调解模型，本质是上层软件对底层硬件的实时调度。",
                "that_point": "[02:12-03:07] 自我意识发展是对心智进行逆向工程的过程，可划分为从 Attentional Self 到 Transcendence 的七个清晰度阶段。",
            },
            {
                "slug": "meditation-state-most-people-never-experience",
                "kind": "resonance", "relation": "延伸",
                "why": "Bach 从控制论建模角度分析意识边界，冥想那期从 Jhana 深定状态的实证角度出发，互为理论与现象学的补充。",
                "this_point": "[47:38-01:00:00] 反射性自我意识在开悟状态下会溶解——当系统不再对自身建模时，主观「我」的感知随之消失，与冥想深定状态高度同构。",
                "that_point": "[03:48-04:22] 冥想是可通过精准反馈回路大幅缩短学习周期的隐性技能；Jhana 深定状态不需要数千小时积累，可通过结构化方法加速触达。",
            },
            {
                "slug": "yann-lecun-world-models-next-ai-revolution",
                "kind": "tension", "relation": "张力",
                "why": "Bach 主张意识建立在离散化仿真之上，LeCun 倡导连续向量场的世界模型，两者在意识与智能的计算底层架构上存在根本性分歧。",
                "this_point": "[25:33-31:05] 物理空间是由离散网络涌现的宏观近似——连续几何是计算函数而非固定值；真正的意识仿真必须依赖离散化基底。",
                "that_point": "[00:00-00:38] 当前架构在样本效率和常识获取上面临严重瓶颈；LeCun 倡导基于连续向量场的世界模型来弥补这一缺口，而非离散化仿真。",
            },
            {
                "slug": "the-era-of-experience",
                "kind": "resonance", "relation": "补充",
                "why": "DeepMind 提出智能体必须通过长期连续经验流建模世界，与 Bach 的「意识是对世界实时仿真的自建模」在体验驱动学习的核心逻辑上互为印证。",
                "this_point": "[20:00-25:32] 人类感知的是大脑为最小化预测误差实时生成的三维游戏引擎——意识存在于这个仿真故事之内，而非原子层面的物理现实。",
                "that_point": "经验时代的智能体将存在于长期的、不间断的经验流中（而非单次交互片段），自主在真实或数字世界中行动，与 Bach 关于意识需要持续建模经验才能存在的主张高度吻合。",
            },
        ],
        "en_title": "The Nature of Reality, Dreams, and Consciousness · Joscha Bach",
        "en_tags": ["cybernetics", "attention model", "simulation hypothesis", "free will", "cognitive infrastructure"],
        "en_connections": [
            {
                "slug": "joscha-bach-life-intelligence-consciousness-future",
                "kind": "resonance", "relation": "companion episode",
                "why": "Both episodes feature Joscha Bach and share the same cybernetic consciousness framework — defining consciousness as the self-modeling of the attention control system and the self as temporary software running on a neural substrate.",
                "this_point": "[03:09-05:03] Consciousness is the mediator model activated when the perceptual elephant and motivational monkey conflict — upper-layer software orchestrating the lower-layer hardware in real time.",
                "that_point": "[02:12-03:07] Self-awareness develops as a reverse-engineering of the mind, divisible into seven clarity stages from Attentional Self to Transcendence.",
            },
            {
                "slug": "meditation-state-most-people-never-experience",
                "kind": "resonance", "relation": "extension",
                "why": "Bach analyzes the boundaries of consciousness through cybernetic modeling; the meditation episode approaches the same territory from the empirical phenomenology of deep Jhana states — theory and lived experience as mutual complements.",
                "this_point": "[47:38-01:00:00] Reflexive self-awareness dissolves in enlightened states — when the system stops modeling itself, the subjective sense of 'I' disappears, isomorphic to deep meditative absorption.",
                "that_point": "[03:48-04:22] Meditation is a tacit skill where precise feedback loops dramatically shorten the learning cycle; deep Jhana states don't require thousands of hours and can be accelerated through structured methods.",
            },
            {
                "slug": "yann-lecun-world-models-next-ai-revolution",
                "kind": "tension", "relation": "architectural tension",
                "why": "Bach argues consciousness requires discrete simulation substrates; LeCun advocates continuous vector-field world models — a fundamental architectural disagreement about how intelligence and consciousness are computed.",
                "this_point": "[25:33-31:05] Physical space is a macro approximation emerging from discrete networks — continuous geometry is a computational function, not a fixed value; genuine consciousness simulation must rest on a discrete substrate.",
                "that_point": "[00:00-00:38] Current ML architectures face severe bottlenecks in sample efficiency and common-sense acquisition; LeCun advocates continuous vector-field world models to bridge this gap, not discrete simulation.",
            },
            {
                "slug": "the-era-of-experience",
                "kind": "resonance", "relation": "complement",
                "why": "DeepMind's experiential AI thesis — agents must model the world through long, continuous streams of experience — directly echoes Bach's claim that consciousness is the real-time simulation self-model built to minimize prediction error.",
                "this_point": "[20:00-25:32] Humans perceive not atoms but a 3D game engine generated by the brain to minimize surprise — consciousness lives inside this simulated story, not in physical reality at the atomic level.",
                "that_point": "Experiential agents will exist in long, uninterrupted streams of experience (not brief single interactions), acting autonomously in real or digital worlds — precisely matching Bach's claim that consciousness requires continuous experiential modeling to exist.",
            },
        ],
    },
    {
        "slug": "jane-street-gpus-trading-hiring-dwarkesh",
        "report": "reports/jane-street-gpus-trading-hiring-dwarkesh.md",
        "url": "https://youtu.be/xKZ_8ULR91Y?si=BgAEuMWNMEKXXWWX",
        "kind": "podcast",
        "date": "2026-06-10",
        "title": "算力、交易与招聘：Jane Street 的技术与组织哲学 · Ron Minsky & Dan Ponttovo",
        "tags": ["Jane Street", "算力底座", "交易策略", "量化招聘", "协同设计"],
        "connections": [
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "resonance", "relation": "同构",
                "why": "两者均从实操层面剖析 AI 算力的经济逻辑——Jane Street 揭示金融机构的算力部署策略，class4 从企业落地侧揭示 AI 成本结构与上下文工程的核心矛盾。",
                "this_point": "[04:33-06:14] Jane Street 与 CoreWeave 签订 60 亿美元算力合约，战略上追求多样化模型架构实验而非单一巨型基础模型——算力是迭代速度的核心杠杆。",
                "that_point": "[01:42-03:43] 在 Ali Ghodsi 看来，AGI 按 AMPLab 2009 年的定义早已实现，但企业落地的真正瓶颈不是模型智能，而是上下文鸿沟与推理成本结构。",
            },
            {
                "slug": "cs153-08-jensen-huang-nvidia-compute",
                "kind": "resonance", "relation": "印证",
                "why": "Jensen Huang 阐释 GPU 算力扩张的技术底层逻辑，Jane Street 从大规模算力买家的实际使用角度印证了 Nvidia 协同设计（Codesign）战略的落地效果。",
                "this_point": "[17:01-18:47] 兆瓦级机架水冷管道系统与 AC/800V DC 直流输电的技术挑战——物理工程层是算力扩张中被低估的系统设计瓶颈。",
                "that_point": "[10:02-12:20] 在 Dennard Scaling 失效的背景下，Nvidia 通过 CPU、GPU、高速互联、交换机和库的全局协同设计，10 年内实现了 100 万倍的计算性能跨越。",
            },
            {
                "slug": "dan-loeb-ai-credit-third-point",
                "kind": "resonance", "relation": "延伸",
                "why": "两者均是金融世界内部对 AI 算力投资的一手视角——Dan Loeb 从宏观投资组合角度，Jane Street 从量化交易实际部署角度，共同勾勒算力作为战略资产的产业图景。",
                "this_point": "[20:55-22:02] Jane Street 当前拥有数万块 GPU 并计划扩展至数十万块，算力投入与招聘比例的战略权衡直接决定了量化团队的竞争边界。",
                "that_point": "[03:10-04:55] Dan Loeb 认为评估 AI 产业生态应采用自底向上的技术栈模型，重点追踪 Nvidia 等算力核心供应商的市场地位与投资价值。",
            },
            {
                "slug": "how-an-ai-chip-works-from-the-bottom-up-reiner-pope",
                "kind": "resonance", "relation": "补充",
                "why": "Reiner Pope 从芯片设计的最底层（乘加运算与内存带宽）向上解释 AI 算力架构，Jane Street 从量化系统的实际需求侧向下分解，两者形成完整的上下游视角。",
                "this_point": "[06:41-07:48] 极高顺序因果消耗的 NASDAQ 数据流使数据加载成为量化系统的核心设计瓶颈——算法与硬件的协同设计必须围绕数据带宽而非单纯浮点算力。",
                "that_point": "[00:00:42-00:02:36] AI 芯片中的基本操作是乘加（MAC），它是矩阵乘法嵌套循环的基本步骤——内存带宽与计算密度的权衡是芯片设计的核心约束。",
            },
        ],
        "en_title": "Compute, Trading, and Hiring: Jane Street's Technology and Organizational Philosophy · Ron Minsky & Dan Ponttovo",
        "en_tags": ["Jane Street", "compute infrastructure", "trading strategy", "quantitative hiring", "codesign"],
        "en_connections": [
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "resonance", "relation": "structural parallel",
                "why": "Both dissect the economic logic of AI compute from an operational insider lens — Jane Street from the financial institution deployment angle, class4 from the enterprise-side context gap and cost structure.",
                "this_point": "[04:33-06:14] Jane Street's $6B CoreWeave compute contract strategically pursues diverse model architecture experimentation rather than a single giant foundation model — compute is the core lever for iteration speed.",
                "that_point": "[01:42-03:43] Ali Ghodsi argues AGI under AMPLab's 2009 definition has already arrived, but the real bottleneck in enterprise deployment is not model intelligence — it's the context gap and inference cost structure.",
            },
            {
                "slug": "cs153-08-jensen-huang-nvidia-compute",
                "kind": "resonance", "relation": "validation",
                "why": "Jensen Huang articulates the technical substrate of GPU compute scaling; Jane Street's large-scale buying experience validates the real-world impact of Nvidia's codesign strategy from the demand side.",
                "this_point": "[17:01-18:47] Megawatt rack water cooling and AC/800V DC power transmission challenges — physical engineering is an underestimated system design bottleneck in the compute scaling race.",
                "that_point": "[10:02-12:20] With Dennard Scaling exhausted, Nvidia achieved a 1,000,000x compute performance jump over 10 years through global codesign of CPU, GPU, high-speed interconnects, switches, and libraries.",
            },
            {
                "slug": "dan-loeb-ai-credit-third-point",
                "kind": "resonance", "relation": "extension",
                "why": "Both are first-hand finance-world perspectives on AI compute investment — Dan Loeb from macro portfolio allocation, Jane Street from actual quantitative trading deployment, together mapping compute as a strategic asset class.",
                "this_point": "[20:55-22:02] Jane Street has tens of thousands of GPUs and plans to expand to hundreds of thousands — the strategic tradeoff between compute investment and hiring headcount directly defines the competitive boundary.",
                "that_point": "[03:10-04:55] Dan Loeb argues AI industry analysis should use a bottom-up technology stack model, with focus on tracking Nvidia and other core compute suppliers' market position and investment value.",
            },
            {
                "slug": "how-an-ai-chip-works-from-the-bottom-up-reiner-pope",
                "kind": "resonance", "relation": "complement",
                "why": "Reiner Pope explains AI compute architecture from the bottom up (MAC operations and memory bandwidth); Jane Street dissects compute needs from the demand side down — together forming a complete upstream-downstream view.",
                "this_point": "[06:41-07:48] The extremely high sequentially-causal NASDAQ data stream makes data loading the true throughput bottleneck — codesign must be organized around data bandwidth, not raw floating-point compute.",
                "that_point": "[00:00:42-00:02:36] The fundamental operation in AI chips is multiply-accumulate (MAC), the basic step in matrix multiplication nested loops — the memory bandwidth vs. compute density tradeoff is the core constraint in chip design.",
            },
        ],
    },
    {
        "slug": "rights-pre-modern-masculinist-fantasy",
        "report": "reports/rights-pre-modern-masculinist-fantasy.md",
        "url": "https://youtu.be/YK1aj39y55k?si=mqXBvOLIyINPGi8-",
        "kind": "podcast",
        "date": "2026-06-09",
        "title": "右翼的\"前现代\"男性气概幻想 · Helen Lewis",
        "tags": ["男性气概", "政治文化", "MAGA", "性别叙事", "保守主义"],
        "connections": [
            {
                "slug": "joscha-bach-life-intelligence-consciousness-future",
                "kind": "resonance", "relation": "同构",
                "why": "两期均从系统论视角解剖意识形态与认知架构的根本缺陷——Bach 揭示个体心智清晰度层级，Helen Lewis 揭示右翼政治运动如何在群体层面扭曲认知框架来填补意义真空。",
                "this_point": "[28:01-31:14] \"长屋\"隐喻缺乏具体历史依据，是将对现代制度一切不满进行符号化污名的话语工具——以虚构的过去填补真实的现实焦虑。",
                "that_point": "[07:00-09:18] 极客常因跳过 Stage 3（社会认同阶段）而陷入孤独，这种认知结构缺陷在成人期可通过刻意训练修复——个体意义真空与群体意识形态操控同源。",
            },
            {
                "slug": "mental-models-that-change-how-you-think",
                "kind": "tension", "relation": "张力",
                "why": "Bill Gurley 倡导系统思考与历史研究作为理性认知工具，Helen Lewis 揭示相同的历史与框架工具在政治叙事中如何被逆转为操控工具——理性框架的建设性与破坏性两面。",
                "this_point": "[31:15-32:42] 互联网右翼反智主义话语通过预设语言陷阱来堵死自由派的理性回应通道——任何针对事实的质疑都会被转化为对话者感性化、不够男性的「证据」。",
                "that_point": "[00:24-00:55] 复杂系统是多变量非线性的，一个微小变量即可改变整个系统轨道；必须避免 deterministic 的单一指标思考——但正是这种框架在政治语境下被工具化。",
            },
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "tension", "relation": "张力",
                "why": "AI 经济学课堂对技术加速的乐观预测，与 Helen Lewis 关于技术加速正在瓦解现代社会约束、加速政治极化的警告形成直接张力。",
                "this_point": "[41:57-43:38] 资本主义与社交媒体的算法性别隔离正在塑造年轻男女的认知分化——技术平台的结构性力量是男性政治极化的基础设施，而非中性工具。",
                "that_point": "[01:42-03:43] AI 以数字劳动力形式打破 20 年人口孵化周期带来的经济红利，正以前所未有的速度重塑社会结构——但这一技术加速在社会约束消解时也加速了极化。",
            },
        ],
        "en_title": "The Right's Pre-Modern Masculinist Fantasy · Helen Lewis",
        "en_tags": ["masculinity", "political culture", "MAGA", "gender narrative", "conservatism"],
        "en_connections": [
            {
                "slug": "joscha-bach-life-intelligence-consciousness-future",
                "kind": "resonance", "relation": "structural parallel",
                "why": "Both dissect fundamental flaws in cognitive architecture and ideology from a systems perspective — Bach at the individual level of mental clarity stages, Lewis at the collective level of how political movements distort cognitive frameworks to fill a meaning vacuum.",
                "this_point": "[28:01-31:14] The 'long house' metaphor lacks any specific historical grounding — it's a symbolic discourse tool for stigmatizing all modern institutions the right dislikes, using a fictional past to fill genuine contemporary anxiety.",
                "that_point": "[07:00-09:18] Nerds who skip Stage 3 (social belonging) experience profound childhood isolation — this cognitive architecture gap can be repaired through deliberate training, connecting individual meaning vacuums to collective ideological manipulation.",
            },
            {
                "slug": "mental-models-that-change-how-you-think",
                "kind": "tension", "relation": "inversion",
                "why": "Bill Gurley advocates systems thinking and historical study as rational cognitive tools; Lewis reveals how those same tools are reversed in political discourse to become manipulation instruments — the constructive and destructive faces of rational frameworks.",
                "this_point": "[31:15-32:42] The internet right's anti-intellectualist rhetoric pre-sets language traps that close off rational liberal responses — any fact-based challenge is reframed as emotional or insufficiently masculine 'evidence.'",
                "that_point": "[00:24-00:55] Complex systems are multi-variable and nonlinear; a single small variable can change the entire trajectory — yet it's precisely this kind of systems reasoning that gets weaponized in political contexts.",
            },
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "tension", "relation": "optimism vs warning",
                "why": "The AI supercycle course's optimistic projections about technological acceleration stand in direct tension with Lewis's warning that the same acceleration is dissolving modern social constraints and speeding up political polarization.",
                "this_point": "[41:57-43:38] Capitalism and social media's algorithmic gender segregation are shaping cognitive divergence between young men and women — tech platforms are the structural infrastructure of male political radicalization, not neutral tools.",
                "that_point": "[01:42-03:43] AI creates digital labor that breaks the 20-year population incubation cycle, reshaping social structures at unprecedented speed — but this same acceleration, as social constraints dissolve, accelerates polarization.",
            },
        ],
    },
    {
        "slug": "microglia-function-cns-development-plasticity",
        "report": "reports/microglia-function-cns-development-plasticity.md",
        "url": "https://cshperspectives.cshlp.org/content/7/10/a020545.full.pdf",
        "kind": "paper",
        "date": "2026-06-10",
        "title": "中枢神经系统发育与可塑性中的小胶质细胞功能 · Dorothy P. Schafer",
        "tags": ["小胶质细胞", "突触剪切", "经典补体级联", "活性依赖性", "发育可塑性"],
        "connections": [
            {
                "slug": "microglia-synaptic-pruning",
                "kind": "resonance", "relation": "承接",
                "why": "Schafer 综述奠定小胶质细胞在健康发育中主动剪切突触的基础机制，突触剪切那篇论文直接承接这一发育基础，聚焦 AD 病理情境下补体级联失调导致的突触丢失。",
                "this_point": "C1q 和 C3 蛋白将活性较弱的突触标记为「待清除」信号，小胶质细胞通过 CR3 受体识别并吞噬它们——这是活性依赖性突触修剪的核心补体级联机制。",
                "that_point": "海马体和联合皮质中的突触丢失与认知障碍的相关性显著强于淀粉样蛋白斑块或神经纤维缠结，是区别于正常衰老的极早期病理标志——同一补体级联在病理下失控。",
            },
            {
                "slug": "active-forgetting",
                "kind": "resonance", "relation": "同构",
                "why": "两篇论文共同揭示神经系统将「主动消除」作为维持功能可塑性的基本原则——发育期小胶质细胞修剪突触，成体期主动遗忘机制清除旧记忆，核心逻辑同构。",
                "this_point": "小胶质细胞的突触修剪是活性依赖性的——优先吞噬活性较弱的突触以集中神经资源，其本质是用选择性消除来构建高效回路。",
                "that_point": "主动遗忘是需要能量、由特定分子 cascade 调控的主动清除过程，用来维持大脑的行为灵活性——消除是功能维持，而非被动衰减。",
            },
            {
                "slug": "neurobiology-of-hunger-zachary-knight",
                "kind": "resonance", "relation": "补充",
                "why": "两篇都揭示分子层面的神经机制如何映射并调控宏观行为输出——小胶质细胞通过突触修剪塑造回路，AgRP 神经元通过负强化调控摄食，均体现了神经底层对行为的精密控制。",
                "this_point": "CX3CR1 基因敲除导致海马体突触成熟延迟与长程网络连接降低，最终引发学习、记忆和运动行为的显著异常——分子级缺陷直接映射至宏观行为输出。",
                "that_point": "[26:50-29:10] AgRP 神经元通过负强化（厌恶状态模拟）驱动摄食行为，当动物「看到」食物时神经元瞬间关闭——大脑的预测机制在行为调控中优先于物理反馈。",
            },
            {
                "slug": "agent-memory",
                "kind": "resonance", "relation": "印证",
                "why": "小胶质细胞的活性依赖性突触修剪原则（保留高频使用连接、清除弱连接）与 AI 智能体外部记忆系统的选择性保留与遗忘策略在系统设计逻辑上高度同构。",
                "this_point": "小胶质细胞选择性吞噬活性较弱的突触，同时通过 IGF-1 等营养因子支持活跃神经元的存活——「用进废退」的生物选择性原则是神经回路效率的根本来源。",
                "that_point": "外部记忆系统通过解耦上下文长度与存储容量来克服长上下文处理的系统级限制——选择性保留重要信息、让低相关内容自然衰减，与生物突触修剪共享核心设计哲学。",
            },
        ],
        "en_title": "Microglia Function in Central Nervous System Development and Plasticity · Dorothy P. Schafer",
        "en_tags": ["microglia", "synaptic pruning", "complement cascade", "activity-dependent", "developmental plasticity"],
        "en_connections": [
            {
                "slug": "microglia-synaptic-pruning",
                "kind": "resonance", "relation": "direct continuation",
                "why": "Schafer's review establishes the foundational mechanism of active synaptic pruning in healthy development; the synaptic pruning paper directly builds on this, focusing on how dysregulation of the same complement cascade drives synapse loss in AD pathology.",
                "this_point": "C1q and C3 proteins tag less-active synapses as 'eat-me' signals; microglia recognize and engulf them via CR3 receptors — this is the core complement cascade mechanism of activity-dependent synaptic pruning.",
                "that_point": "Synapse loss in hippocampus and association cortices correlates with cognitive impairment far more strongly than amyloid plaques or neurofibrillary tangles — the earliest pathological marker of AD, where the same complement cascade runs unchecked.",
            },
            {
                "slug": "active-forgetting",
                "kind": "resonance", "relation": "deep parallel",
                "why": "Both papers reveal that the nervous system treats active elimination as a fundamental principle for maintaining functional plasticity — microglia prune synapses during development, active forgetting clears old memories in the adult brain, sharing the same core logic.",
                "this_point": "Microglial synaptic pruning is activity-dependent — preferentially engulfing less active synapses to concentrate neural resources; its essence is building efficient circuits through selective elimination.",
                "that_point": "Active forgetting is an energy-requiring, molecularly regulated active clearance process that maintains the brain's behavioral flexibility — elimination is functional maintenance, not passive decay.",
            },
            {
                "slug": "neurobiology-of-hunger-zachary-knight",
                "kind": "resonance", "relation": "complement",
                "why": "Both papers reveal how molecular-level neural mechanisms map onto and govern macro behavioral outputs — microglia sculpt circuits through synaptic pruning, AgRP neurons regulate feeding through negative reinforcement, both demonstrating precise bottom-up behavioral control.",
                "this_point": "CX3CR1 knockout causes delayed hippocampal synapse maturation and reduced long-range connectivity, ultimately producing significant abnormalities in learning, memory, and motor behavior — molecular-level deficits map directly to macro behavioral outputs.",
                "that_point": "[26:50-29:10] AgRP neurons drive feeding behavior through negative reinforcement (simulating an aversive state) and instantly shut off when animals see food — the brain's predictive mechanism governs behavior ahead of physical feedback.",
            },
            {
                "slug": "agent-memory",
                "kind": "resonance", "relation": "design isomorphism",
                "why": "Microglia's activity-dependent pruning principle (retain high-frequency connections, eliminate weak ones) is isomorphic in design logic to the selective retention and forgetting strategies in AI agent external memory systems.",
                "this_point": "Microglia selectively engulf less active synapses while supporting active neurons via neurotrophic factors like IGF-1 — the biological 'use it or lose it' principle is the fundamental source of neural circuit efficiency.",
                "that_point": "External memory systems decouple context length from storage capacity to overcome system-level limitations — selectively retaining important information while allowing low-relevance content to decay, sharing the core design philosophy of biological synaptic pruning.",
            },
        ],
    },
    {
        "slug": "ms&e435-class3-economics-ai-supercycle",
        "report": "reports/ms&e435-class3-economics-ai-supercycle.md",
        "url": "https://youtu.be/4zk-hJ50vmU?si=9d_9Y7wbYavqltYO",
        "kind": "podcast",
        "date": "2026-06-11",
        "title": "AI超量扩张的电网硬壁垒与能源套利 · Chase Lock Miller",
        "tags": ["算力电能", "数据中心", "数字劳动力", "垂直整合", "电网基建"],
        "connections": [
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "resonance", "relation": "同系",
                "why": "同一课程的相邻两节：class3 从能源物理基建和每兆瓦成本结构出发，class4 从企业落地侧的上下文工程和推理成本出发，共同构成 AI 超级周期经济学的供给侧与需求侧视角。",
                "this_point": "[36:43-39:56] 每兆瓦 6000 万美元 CapEx 投入下，托管 API 服务（2年回本）相比裸算力出租（4年回本）带来翻倍利润——垂直整合是捕获「从电子到 Token」超额利润的唯一通路。",
                "that_point": "[01:42-03:43] AI 的真正落地瓶颈不是模型智能本身，而是上下文工程与推理成本结构——企业侧的需求侧约束与 Chase 揭示的能源侧供给约束构成完整的经济图景。",
            },
            {
                "slug": "cs153-08-jensen-huang-nvidia-compute",
                "kind": "resonance", "relation": "印证",
                "why": "Jensen Huang 在 CS153 阐述 GPU 协同设计的技术战略，Chase Lock Miller 从数据中心基础设施买家的角度实证了这一战略的产业链传导效应——芯片层与基建层的供需对话。",
                "this_point": "[08:56-10:51] AI 产业链的动态瓶颈已从芯片转向「带电数据中心」——拥有昂贵芯片而缺乏电网接入等于拥有一堆无用的硅片，物理电网成为新的竞争护城河。",
                "that_point": "[10:02-12:20] 通过 CPU、GPU、高速互联和库的极端协同设计，Nvidia 10 年内实现了 100 万倍的计算性能跨越；而这 100 万倍的算力必须有等量增长的电力和数据中心来承接。",
            },
            {
                "slug": "jane-street-gpus-trading-hiring-dwarkesh",
                "kind": "resonance", "relation": "同构",
                "why": "两者均从算力大规模买家视角揭示 AI 计算基础设施的真实运营逻辑——Jane Street 聚焦纳秒级到日级的量化交易系统，Chase 聚焦吉瓦级数据中心的物理工程，核心问题相同：如何最大化每兆瓦的价值产出。",
                "this_point": "[29:20-31:47] IT 设备每兆瓦约 4000 万美元：GPU 占 3000 万，网络 400 万，CPU 严重短缺——这恰好是 Jane Street 亿万量化集群在物理层的采购现实。",
                "that_point": "[17:01-18:47] 兆瓦级机架水冷与 800V DC 直流输电的技术挑战在量化数据中心同样适用——物理工程与 IT 软件的协同设计是算力产业共同面临的根本性设计约束。",
            },
            {
                "slug": "dan-loeb-ai-credit-third-point",
                "kind": "resonance", "relation": "补充",
                "why": "Dan Loeb 从宏观投资视角描绘 AI 算力的资本配置格局，Chase 从运营端提供了数据中心每兆瓦盈利模型的第一手账本，两者互为投资论题与运营现实的对照。",
                "this_point": "[21:11-26:24] 物理基建每兆瓦 2000 万美元 CapEx 中，施工劳动力（470 万）与天然气涡轮机（300 万/兆瓦）是两大膨胀点——这是算力基建成本高企的制造业端核心驱动力。",
                "that_point": "[03:10-04:55] AI 产业评估应采用自底向上的技术栈模型，从能源到芯片到基础设施到应用——Chase 揭示的能源与物理基建层正是 Dan Loeb 投资框架中最底层的硬壁垒变量。",
            },
        ],
        "en_title": "AI Overexpansion's Hard Grid Barriers and Energy Arbitrage · Chase Lock Miller",
        "en_tags": ["compute energy", "data centers", "digital labor", "vertical integration", "grid infrastructure"],
        "en_connections": [
            {
                "slug": "ms&e435-class4-economics-ai-supercycle",
                "kind": "resonance", "relation": "same series",
                "why": "Adjacent sessions of the same course: class3 approaches from energy physics infrastructure and per-MW cost structure, class4 from enterprise-side context engineering and inference cost — together forming the supply-side and demand-side perspectives of AI supercycle economics.",
                "this_point": "[36:43-39:56] With $60M/MW CapEx, managed API services (2-year payback) yield double the profit of bare compute rental (4-year payback) — vertical integration is the only path to capturing 'electrons to tokens' excess returns.",
                "that_point": "[01:42-03:43] The real AI deployment bottleneck is not model intelligence but context engineering and inference cost structure — enterprise-side demand constraints and Chase's energy-side supply constraints form a complete economic picture.",
            },
            {
                "slug": "cs153-08-jensen-huang-nvidia-compute",
                "kind": "resonance", "relation": "validation",
                "why": "Jensen Huang articulates GPU codesign technology strategy in CS153; Chase validates the industry-wide propagation of that strategy from the data center infrastructure buyer's angle — a supply-demand dialogue between the chip layer and the infrastructure layer.",
                "this_point": "[08:56-10:51] The AI supply chain's dynamic bottleneck has shifted from chips to 'energized data centers' — owning expensive chips without grid access means owning useless silicon; physical grid has become the new competitive moat.",
                "that_point": "[10:02-12:20] Through extreme codesign of CPU, GPU, high-speed interconnects, and libraries, Nvidia achieved a 1,000,000x compute performance jump over 10 years — and every order of magnitude of that compute needs an equivalent growth in power and data centers to absorb it.",
            },
            {
                "slug": "jane-street-gpus-trading-hiring-dwarkesh",
                "kind": "resonance", "relation": "structural parallel",
                "why": "Both reveal the real operating logic of AI compute infrastructure from the perspective of large-scale compute buyers — Jane Street on nanosecond-to-day quantitative trading systems, Chase on gigawatt-scale data center physical engineering — the core question identical: how to maximize value output per megawatt.",
                "this_point": "[29:20-31:47] IT equipment costs ~$40M/MW: $30M for GPUs, $4M for networking, CPUs severely constrained — this is the exact procurement reality at the physical layer for Jane Street's massive quantitative cluster.",
                "that_point": "[17:01-18:47] Megawatt rack water cooling and 800V DC power transmission challenges apply equally to quantitative data centers — physical engineering and IT software codesign is a fundamental design constraint shared across the entire compute industry.",
            },
            {
                "slug": "dan-loeb-ai-credit-third-point",
                "kind": "resonance", "relation": "complement",
                "why": "Dan Loeb paints the capital allocation landscape of AI compute from a macro investment perspective; Chase provides first-hand per-megawatt profitability models from the operating side — a paired view of investment thesis and operational reality.",
                "this_point": "[21:11-26:24] In the $20M/MW physical infrastructure CapEx, construction labor ($4.7M) and gas turbines ($3M/MW) are the two primary inflation drivers — the manufacturing-side core driver behind high compute infrastructure costs.",
                "that_point": "[03:10-04:55] AI industry analysis should use a bottom-up technology stack model from energy to chips to infrastructure to applications — the energy and physical infrastructure layer Chase reveals is the hardest, lowest-layer variable in Dan Loeb's investment framework.",
            },
        ],
    },
]


def main() -> int:
    site = load_site_config()
    errors = []

    for item in ITEMS:
        slug = item["slug"]
        section = "papers" if item["kind"] == "paper" else "episodes"
        print(f"\n{'='*60}")
        print(f"Publishing: {slug}")

        report_path = ROOT / item["report"]
        if not report_path.exists():
            print(f"!! SKIP: report not found at {report_path}")
            errors.append(slug)
            continue

        en_body_path = EN_BODIES_DIR / f"{slug}.md"
        if not en_body_path.exists():
            print(f"!! SKIP: en body not found at {en_body_path}")
            errors.append(slug)
            continue

        report_md = report_path.read_text(encoding="utf-8")
        public_md = extract_public_markdown(report_md, site.private_cutoff)
        if not public_md:
            print("!! SKIP: no public content extracted")
            errors.append(slug)
            continue

        en_body = en_body_path.read_text(encoding="utf-8")
        en = {
            "title": item["en_title"],
            "tags": item["en_tags"],
            "body": en_body,
            "connections": item["en_connections"],
        }

        print(f"  title:   {item['title']}")
        for c in item["connections"]:
            print(f"  {c['kind']}: -> {c['slug']}")

        entry = publish_report(
            report_md, item["title"], site,
            date=item["date"], slug=slug,
            source_url=item["url"],
            tags=item["tags"],
            connections=item["connections"],
            en=en,
            primary_public_md=public_md,
            kind=item["kind"],
        )

        leaks = []
        for lang in ("zh", "en"):
            d = ROOT / "docs" / (section if lang == "zh" else f"en/{section}")
            p = d / f"{entry['slug']}.html"
            if p.exists():
                h = p.read_text(encoding="utf-8")
                leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

        if leaks:
            print(f"!! 隐私检查失败: {leaks}")
            errors.append(slug)
        else:
            print("  隐私检查: 通过")

    print(f"\n{'='*60}")
    if errors:
        print(f"!! DONE WITH ERRORS: {errors}")
        return 1
    print("ALL 5 ITEMS RE-PUBLISHED (local, not pushed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
