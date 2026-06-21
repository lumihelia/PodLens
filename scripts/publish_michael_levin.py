"""Publish michael-levin-bioelectricity-morphogenesis (0621 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "michael-levin-bioelectricity-morphogenesis",
    "report": "reports/0621/michael-levin-bioelectricity-morphogenesis.md",
    "url": "https://youtu.be/t6EFV2gSSmg?si=eDBbtGowW3yN2ANn",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "生物电、形态发生与两头涡虫 · Michael Levin",
    "tags": ["生物电", "形态发生", "群体智能", "涡虫再生", "缝隙连接", "异种机器人"],
    "connections": [
        {
            "slug": "g-memory-hierarchical-memory-multi-agent-systems",
            "kind": "resonance",
            "relation": "同构",
            "why": "两者揭示了同一个架构原则：复杂的适应性行为可以通过在一个不可变的底层基础设施之上叠加一层可重写的「软件」来实现，完全不需要改动底层本身。Levin 的核心论点是基因组只是「硬件」（决定通道蛋白等组件的生产），真正决定宏观解剖形态的是可以独立重编程的生物电「软件」——阻断缝隙连接就能让涡虫永久长出两个头，且基因完全没变。G-Memory 的核心卖点完全是同一个结构：在不修改 AutoGen、DyLAN、MacNet 等底层多智能体框架的前提下，单靠叠加一层可重写的层级记忆，就让协作行为发生质变。",
            "this_point": "[18:00]-[18:13], [01:08:40] Levin 说基因只负责决定硬件（通道蛋白的产生），而细胞间如何通电、形成何种宏观解剖形态，是由生物电生理软件决定的，可以通过改变电压来重新写入指令，不需要碰基因组。",
            "that_point": "G-Memory 摘要：论文反复强调其方法是「即插即用」（plug-and-play）的层级记忆系统，实验证明「在不修改任何底层框架的条件下」，G-Memory 让 AutoGen、DyLAN 和 MacNet 的成功率提升最多达 20.89%。",
        },
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在论证同一件反直觉的事：复杂、看似有目的的策略行为，可以在没有显式编程、没有奖励信号、甚至没有进化选择史的情况下直接「涌现」出来——它来自系统与约束环境的互动本身，而不是被写进代码或被训练出来的。Levin 用六行确定性的 bubble sort 代码举例：遇到锁死无法移动的故障数值时，算法会自发执行「先让数组更乱再排序」的延迟满足策略，这个策略不在代码里。Efros 用 2017 年与 Pathak 的无奖励 Mario 实验举例：把好奇心定义为预测误差后，AI 自发学会了存活、前进、杀敌——不是为了得分，只是因为这些事「有趣」。",
            "this_point": "[01:17:50]-[01:18:14], [01:19:46]-[01:20:04] Levin 说仅有几行代码、逻辑完全确定的 bubble sort 算法，在遇到不可移动的故障数值时，会自发出现「先让数组更无序」的延迟满足和聚类行为，这一策略从未被写在代码中。",
            "that_point": "[30:54]-[31:06] Efros 与 Pathak 2017 年的无奖励 Mario 实验：好奇心被定义为预测误差，AI 在没有任何奖励的情况下学会了存活、前进、杀死敌人——驱动探索的内在动机产生了一个自然课程（natural curriculum）的飞轮，而不是由外部奖励或预设目标指定的。",
        },
    ],
    "en_title": "Bioelectricity, Morphogenesis, and Two-Headed Worms · Michael Levin",
    "en_tags": ["bioelectricity", "morphogenesis", "collective intelligence", "planarian regeneration", "gap junctions", "xenobots"],
    "en_connections": [
        {
            "slug": "g-memory-hierarchical-memory-multi-agent-systems",
            "kind": "resonance",
            "relation": "Both reveal the same architectural principle: complex adaptive behavior can be achieved by layering a rewritable 'software' on top of immutable underlying infrastructure, with no need to touch the underlying layer at all. Levin's core argument is that the genome is merely 'hardware' (determining the production of components like channel proteins), while the actual macroscopic anatomical form is determined by independently reprogrammable bioelectric 'software' — blocking gap junctions permanently gives a planarian two heads, with the genome completely unchanged. G-Memory's core pitch is structurally identical: without modifying the underlying multi-agent frameworks AutoGen, DyLAN, or MacNet at all, simply layering a rewritable hierarchical memory on top produces a qualitative shift in collaborative behavior.",
        },
        {
            "slug": "alexei-efros-surface-data-deep-data",
            "kind": "resonance",
            "relation": "Both are arguing the same counterintuitive point: complex, seemingly purposeful strategic behavior can 'emerge' directly with no explicit programming, no reward signal, and not even an evolutionary selection history — it comes from the interaction between a system and its constraining environment itself, not from anything written into code or trained into a model. Levin's example is a six-line, fully deterministic bubble sort algorithm: when it hits a stuck, immovable faulty value, it spontaneously executes a 'temporarily make the array more disordered before sorting' delayed-gratification strategy that is nowhere in the code. Efros's example is his 2017 reward-free Mario experiment with Pathak: once curiosity is defined as prediction error, the AI spontaneously learns to survive, advance, and defeat enemies — not to score points, but simply because those things are 'interesting.'",
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
