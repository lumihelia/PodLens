"""Publish why-does-2-plus-2-equal-4-math-deep-reality (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "why-does-2-plus-2-equal-4-math-deep-reality",
    "report": "reports/0621副本/why-does-2-plus-2-equal-4-math-deep-reality.md",
    "url": "https://youtu.be/bY3ZMOn9mHQ?si=YK8r0tH5d5ikIR8Q",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "数学实在、物理规律与唯物主义之死 · David Berlinski",
    "tags": ["数学实在论", "唯物主义批判", "物理规律", "Wigner 谜题", "科学哲学", "审美原理"],
    "connections": [
        {
            "slug": "thomas-sargent-ai-past-present-future",
            "kind": "resonance",
            "relation": "同构",
            "why": "两期节目独立引用了同一个历史案例（哥白尼日心说战胜托勒密地心说），却用它论证了完全相同的「审美原理」：当两个理论在数据拟合度上接近甚至处于劣势时，人类最终选择相信的那一个，是由数学之美而不是纯粹的预测精度决定的。Sargent 从科学史和经济学方法论的角度论证这一点；Berlinski、Klainerman 和 Meyer 则引用 Crick「它太美了，所以一定是对的」和 Dirac「理论优美比与数据一致更重要」，把同一个观察上升为一个形而上学命题：宇宙底层运行在某种数学的理性与和谐之上，这种理性无法被纯粹的唯物主义还原。",
            "this_point": "[49:44]-[50:52] Berlinski、Klainerman 和 Meyer 引用 Crick 评价 DNA 双螺旋「它如此美丽，所以一定是对的」，以及 Dirac「理论优美比与数据一致更重要」——审美上的对称与和谐被证明是人类逼近物理客观真理的可靠罗盘。",
            "that_point": "[26:15]-[28:22] Sargent 说哥白尼 36 参数的日心说模型，预测精度其实远低于托勒密 250 参数的地心说模型；但科学家们因为日心说模型的简洁与优美，选择相信它更接近真理——这跟今天大模型追求的「正则化」和「参数压缩」是同一个道理。",
        },
        {
            "slug": "joscha-bach-nature-of-reality-dreams-consciousness",
            "kind": "tension",
            "relation": "张力",
            "why": "两期节目在数学的本体论地位上给出了正面对立的答案。Berlinski、Klainerman 和 Meyer 主张数学实在论（柏拉图主义）：2+2=4、虚数 i 这样的数学事实，独立于人类心智和物质世界客观存在，是非物质的、永恒的真理，其终极归宿甚至指向超越性的神圣心智。Joscha Bach 则站在完全相反的立场：他主张连续几何和无理数（如 pi）根本不是固定存在的数学对象，而是计算函数——物理空间是离散网络的涌现，连续性只是大量离散粒子碰撞的统计宏观表现。一个说数学是被发现的永恒真理，一个说看似永恒的数学结构其实是计算过程的副产品。",
            "this_point": "[36:56]-[39:51] Berlinski 等人讨论虚数 i = √(-1) 的历史：16世纪意大利数学家为了解三次方程发明了这个在现实中不存在、概念上说不通的「怪物」符号，但到了20世纪，物理学家发现没有它量子力学的方程式根本写不下去——这正是数学实在独立于物理世界又精确命中物理世界的证据。",
            "that_point": "[27:27-31:05] Joscha Bach 说真实物理世界并不存在真正的「连续性」或「无限解析度」，无限在物理上会导致逻辑自相矛盾；pi 和其他无理数本质上是计算函数而非固定数值，连续的几何仅是大量离散粒子碰撞的统计宏观表现。",
        },
    ],
    "en_title": "Mathematical Reality, Physical Law, and the Death of Materialism · David Berlinski",
    "en_tags": ["mathematical realism", "critique of materialism", "physical law", "Wigner's puzzle", "philosophy of science", "the beauty principle"],
    "en_connections": [
        {
            "slug": "thomas-sargent-ai-past-present-future",
            "kind": "resonance",
            "relation": "Two separate episodes independently cite the same historical case — Copernican heliocentrism beating Ptolemaic geocentrism — to argue the identical 'beauty principle': when two theories are close in (or one is even worse at) fitting the data, the one humans ultimately choose to believe is decided by mathematical beauty, not raw predictive accuracy. Sargent makes the point from the angle of the history of science and economic methodology; Berlinski, Klainerman, and Meyer cite Crick's 'it's so beautiful, it's gotta be right' and Dirac's claim that a theory's beauty matters more than its consistency with the data, elevating the same observation into a metaphysical claim: the universe runs on a deep mathematical rationality and harmony that pure materialism cannot reduce away.",
        },
        {
            "slug": "joscha-bach-nature-of-reality-dreams-consciousness",
            "kind": "tension",
            "relation": "The two episodes give opposite answers to the ontological status of mathematics. Berlinski, Klainerman, and Meyer argue for mathematical realism (Platonism): facts like 2+2=4 or the imaginary unit i exist objectively, independent of human minds and the material world, as non-material, eternal truths whose ultimate origin may even point toward a transcendent divine mind. Joscha Bach takes the exact opposite position: he argues continuous geometry and irrational numbers (like pi) aren't fixed mathematical objects at all — they're computational functions; physical space emerges from a discrete network, and continuity is merely the statistical macro-appearance of countless discrete particle collisions. One says mathematics is a discovered eternal truth; the other says apparently eternal mathematical structure is actually a byproduct of computation.",
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
