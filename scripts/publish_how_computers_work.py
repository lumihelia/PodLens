"""Publish how-do-computers-work-from-scratch (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "how-do-computers-work-from-scratch",
    "report": "reports/0621副本/how-do-computers-work-from-scratch.md",
    "url": "https://youtu.be/rl0jkP9kOMw?si=wdmL8iD4nOYAFGFf",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "计算机自底向上构建指南 · Unnamed Speaker",
    "tags": ["二进制", "逻辑门", "ALU", "寄存器", "内存映射I/O", "计算机体系结构"],
    "connections": [
        {
            "slug": "simon-peyton-jones-haskell-functional-programming",
            "kind": "resonance",
            "relation": "同构",
            "why": "这期视频是 Simon 那个论点的一份逐门电路级的实物证明。Simon 说，早年试图在硬件里直接跑解释器（SKI 组合子机、数据流机）是一个被验证为错误的设计——真正高效的路径是把复杂的运行时计算压缩到编译期，再在通用硬件上跑。这期视频从头展示了「通用硬件」具体是什么：控制核心根本不是一个会「思考」的解释器，只是一张固化在 ROM 里的微码查找表，根据操作码和时钟周期持续分发预先映射好的高低电平。而这套 8 位玩具计算机的寄存器、ALU、程序计数器设计，和真实的 32 位 ARM Cortex-M0+ 在概念上没有任何本质区别——这正是 Simon 论证「编译期收敛优于运行时硬件解释」的具体物理样本。",
            "this_point": "[07:53:48] 控制核心的本质是一张微码固化查找表。计算机大脑并没有进行主观思考，只是根据操作码与当前时钟步骤持续向控制线路分发映射好的高低电平；[10:47:55] 真实的 ARM Cortex-M0+ 处理器位宽达到 32 位，但其核心的寄存器、ALU 与程序计数器设计在概念上与这台 8 位计算机没有任何本质区别。",
            "that_point": "[16:09]-[18:16] Simon 说早期数据流机器和 SKI 组合子硬件试图在运行时动态重写表达式树，但这种在运行时完成的工作不如在编译期通过强力编译器生成高效机器码，再在通用处理器（Intel/ARM）上运行。",
        },
        {
            "slug": "thomas-sargent-ai-past-present-future",
            "kind": "resonance",
            "relation": "同构",
            "why": "Sargent 用费曼的「观察一盘棋推断整套规则」来描述科学和结构计量经济学的核心任务：从零散的表面数据（价格、棋子移动）逆向推断出看不见的底层博弈规则。这期视频做的事情正好相反，却揭示了同一枚硬币的另一面——它从最底层的电信号阈值开始，一层一层透明地正向构建出那套「规则」本身：逻辑门、加法器、寄存器、指令集，直到一盏 LED 被点亮。把两者放在一起看：Sargent 让你看到为什么从外部推断规则是科学最难的部分，这期视频则让你亲手搭建一遍那套规则，看清楚一旦你站在内部、拥有全部细节，所谓「神秘的底层规则」其实就是几十层简单二元开关的诚实叠加。",
            "this_point": "[05:27:04] 总线通信的核心红线是防范电气层面的数据写入冲突：任意时刻只能有一个硬件组件被允许向总线写入电平，否则会造成直接的物理短路并损坏芯片——这是这台计算机「博弈规则」里最基础的一条物理法则，正向、透明地被构建出来。",
            "that_point": "[56:58]-[01:00:52] Sargent 阐释费曼隐喻与结构计量经济学的同构关系：从零散的价格与数量数据中逆向推断底层的博弈规则（Von Neumann 游戏定义）——这是同一种「规则」从外部、用数据反推的版本。",
        },
    ],
    "en_title": "Building a Computer from Scratch, Bottom-Up · Unnamed Speaker",
    "en_tags": ["binary", "logic gates", "ALU", "registers", "memory-mapped I/O", "computer architecture"],
    "en_connections": [
        {
            "slug": "simon-peyton-jones-haskell-functional-programming",
            "kind": "resonance",
            "relation": "This video is a gate-by-gate physical proof of Simon's argument. Simon says that early attempts to run an interpreter directly in hardware (the SKI combinator machine, dataflow machines) were proven to be the wrong design — the truly efficient path is to compress complex runtime computation down to compile time and then run it on general-purpose hardware. This video shows, from the ground up, what 'general-purpose hardware' actually consists of: the control core isn't some 'thinking' interpreter at all, it's just a microcode lookup table burned into ROM, continuously dispatching pre-mapped high/low voltages based on the opcode and clock cycle. And the register, ALU, and program-counter design of this 8-bit toy computer is conceptually indistinguishable from a real 32-bit ARM Cortex-M0+ — exactly the concrete physical specimen proving Simon's argument that compile-time convergence beats runtime hardware interpretation.",
        },
        {
            "slug": "thomas-sargent-ai-past-present-future",
            "kind": "resonance",
            "relation": "Sargent uses Feynman's 'inferring the entire rule set by watching a single chess game' to describe the core task of science and structural econometrics: reverse-engineering the invisible underlying rules of the game from scattered surface data (prices, the movement of pieces). This video does the exact opposite, yet reveals the other side of the same coin — starting from the lowest-level voltage threshold, it transparently builds, layer by layer in the forward direction, the very 'rule set' itself: logic gates, adders, registers, an instruction set, all the way to lighting up an LED. Put the two together: Sargent shows you why inferring rules from the outside is the hardest part of science; this video lets you build that rule set with your own hands and see clearly that once you're standing on the inside, with every detail in view, the so-called 'mysterious underlying rules' are just dozens of layers of honest binary switches stacked together.",
        },
    ],
}


def main() -> int:
    site = load_site_config()
    item = ITEM
    slug = item["slug"]

    report_path = ROOT / item["report"]
    if not report_path.exists():
        print(f"!! report not found: {report_path}")
        return 1

    en_body_path = EN_BODIES_DIR / f"{slug}.md"
    if not en_body_path.exists():
        print(f"!! en body not found: {en_body_path}")
        return 1

    report_md = report_path.read_text(encoding="utf-8")
    public_md = extract_public_markdown(report_md, site.private_cutoff)
    if not public_md:
        print("!! no public content extracted (check private cutoff heading)")
        return 1

    en_body = en_body_path.read_text(encoding="utf-8")
    en = {
        "title": item["en_title"],
        "tags": item["en_tags"],
        "body": en_body,
        "connections": item["en_connections"],
    }

    print(f"Publishing: {slug}")
    for c in item["connections"]:
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:30]}...)")

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
        d = ROOT / "docs" / ("episodes" if lang == "zh" else "en/episodes")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
