"""Publish avi-wigderson-p-vs-np-zero-knowledge-proofs (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "avi-wigderson-p-vs-np-zero-knowledge-proofs",
    "report": "reports/0621副本/avi-wigderson-p-vs-np-zero-knowledge-proofs.md",
    "url": "https://youtu.be/5GUcvSAJcJw?si=IzMRyU2jYXu5fJOZ",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "P vs NP、零知识证明与计算的胚胎阶段 · Avi Wigderson",
    "tags": ["计算复杂性", "随机性", "零知识证明", "量子计算", "MIP* = RE", "认知边界"],
    "connections": [
        {
            "slug": "simon-peyton-jones-haskell-functional-programming",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在自己的领域里，从图灵和丘奇的基础工作出发，论证「计算」本质上是一个数学对象，而不只是物理芯片上发生的事。Simon 回顾了图灵机与 lambda 演算的等价性，并以此为函数式编程「用值编程」的哲学奠基；Wigderson 则把这个基础推得更远，论证 P vs NP、随机性、零知识证明这些计算复杂性问题的本质，是关于人类认知能否触及某些真理边界的问题。两人都把「计算」从工程问题提升到了认识论问题。",
            "this_point": "[02:23]-[04:47] Simon 回顾 Alan Turing 与 Alonzo Church 在普林斯顿的工作，指出 Turing 机器与 lambda 演算的等价性——这是函数式编程「用值编程而非修改状态」这套哲学的数学根基。",
            "that_point": "[02:22] Wigderson 说 P vs NP 的本质是关于人类认知极限的问题——我们能否高效地解出所有我们想要解出的难题，即高效地获取我们想要知道的一切真理。",
        },
        {
            "slug": "why-does-2-plus-2-equal-4-math-deep-reality",
            "kind": "resonance",
            "relation": "同构",
            "why": "两期节目都在论证同一件事：纯粹由逻辑和数学推导出的抽象结构，能够以极其精确的方式命中我们尚未观测、甚至看似完全无关的现实领域，而这种命中本身就是一个需要被认真对待的谜题。Berlinski 等人用 Wigner 的「不合理的有效性」描述虚数 i 如何从一个16世纪解三次方程的思维游戏，变成20世纪量子力学不可或缺的基石；Wigderson 描述的是同一种谜题在计算理论里的版本——困难性与随机性之间存在的深刻对等关系，纯粹的数学结构竟然能精确刻画「随机性」这个看似物理的属性，而且这种对等关系是双向的。",
            "this_point": "[55:14] Wigderson 说随机性是一种相对的计算资源，其质量取决于观察者的计算能力而非物理属性本身——同一次硬币抛掷，对裸眼观察者是随机的，对连接了超级计算机与传感器阵列的物理学家则是完全可预测的。",
            "that_point": "[36:56]-[39:51] Berlinski 等人讨论虚数 i 的历史：16世纪意大利数学家为了解三次方程发明了这个在现实中不存在的「怪物」符号，但到了20世纪，物理学家发现没有它量子力学的方程式根本写不下去。",
        },
    ],
    "en_title": "P vs. NP, Zero-Knowledge Proofs, and the Embryonic Stage of Computation · Avi Wigderson",
    "en_tags": ["computational complexity", "randomness", "zero-knowledge proofs", "quantum computation", "MIP* = RE", "the boundary of knowledge"],
    "en_connections": [
        {
            "slug": "simon-peyton-jones-haskell-functional-programming",
            "kind": "resonance",
            "relation": "Both, in their own domains, build from Turing's and Church's foundational work to argue that 'computation' is fundamentally a mathematical object, not merely something that happens on a physical chip. Simon revisits the equivalence between the Turing machine and the lambda calculus, using it as the mathematical foundation for functional programming's philosophy of 'programming with values.' Wigderson pushes the same foundation further, arguing that the essence of computational complexity problems like P vs. NP, randomness, and zero-knowledge proofs is really about whether human cognition can reach certain boundaries of truth at all. Both elevate 'computation' from an engineering problem to an epistemological one.",
        },
        {
            "slug": "why-does-2-plus-2-equal-4-math-deep-reality",
            "kind": "resonance",
            "relation": "Both episodes argue the same point: an abstract structure derived purely from logic and mathematics can hit, with extraordinary precision, a domain of reality we hadn't yet observed or that seemed entirely unrelated — and that hit is itself a puzzle worth taking seriously. Berlinski and his guests use Wigner's 'unreasonable effectiveness' to describe how the imaginary number i went from a 16th-century thought-game for solving cubic equations to an indispensable cornerstone of 20th-century quantum mechanics; Wigderson describes the same kind of puzzle in computational theory — the profound equivalence between hardness and randomness, where a purely mathematical structure turns out to precisely characterize 'randomness,' a property that seems physical, and where that equivalence runs in both directions.",
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
