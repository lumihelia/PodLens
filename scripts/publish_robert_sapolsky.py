"""Publish robert-sapolsky-biology-best-worst (0621副本 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "robert-sapolsky-biology-best-worst",
    "report": "reports/0621副本/robert-sapolsky-biology-best-worst.md",
    "url": "https://youtu.be/GRYcSuyLiJk?si=UISur_5lDov4_Z4K",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "人类最好与最坏行为的生物学 · Robert Sapolsky",
    "tags": ["神经生物学", "攻击性", "认知偏见", "表观遗传学", "自由意志", "我们与他们"],
    "connections": [
        {
            "slug": "michael-levin-bioelectricity-morphogenesis",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在论证：决定一个系统行为边界的，往往不是固定不变的「硬件」（基因组/神经回路本身），而是可以在极短时间内被重新配置的「符号/信号」层。Sapolsky 展示了人脑对种族他者的杏仁核敌意反应可以在几毫秒内被一顶象征同队的棒球帽彻底瓦解——基因和神经回路完全没变，只是符号层的输入变了。Levin 展示的是同一个原理在发育生物学里的版本：阻断缝隙连接可以让涡虫永久长出两个头，而且这种「软件」改写在基因完全不变的情况下跨代遗传。两人都指向同一个结论：行为/形态的边界由可重写的信号层决定，而不是由看起来更底层、更「硬」的基因或神经结构决定。",
            "this_point": "[29:53]-[31:01] Sapolsky 说杏仁核在百毫秒内对异族面孔产生敌对信号，但只要给对方戴上同队棒球帽，这一种族层面的敌对信号在脑中就会在毫秒内被同队认同覆盖——没有任何基因或神经连接发生改变。",
            "that_point": "[18:00]-[18:13] Levin 说基因只负责决定硬件（通道蛋白的产生），而细胞间如何通电、形成何种宏观解剖形态，是由生物电生理软件决定的，可以通过改变电压来重新写入指令，不需要碰基因组。",
        },
        {
            "slug": "neurobiology-of-hunger-zachary-knight",
            "kind": "resonance",
            "relation": "同构",
            "why": "两期节目独立验证了神经科学里同一个核心发现：多巴胺编码的不是「获得奖励」本身的愉悦感，而是对奖励的「渴望」与「期待」。Sapolsky 从赌博和惩罚快感的角度论证——50% 的「也许」概率让多巴胺飙升至最高峰，比确定获得奖励时更高；Knight 从摄食行为的角度给出了几乎一模一样的结论——多巴胺不负责食物带来的即时愉悦感（liking），而是负责驱动对食物的渴望（wanting）以及摄食后的强化学习。两个完全不同的研究对象（社会行为/赌博 vs. 进食/体重调节），却收敛到了同一条神经回路的同一个功能定义上。",
            "this_point": "[22:28] Sapolsky 说不确定性概率处于 50% 的「也许」状态时，多巴胺的分泌量飙升至最高峰，构成了赌博、惩罚快感以及追求行为的神经底座——多巴胺分子底盘对「期待」的映射远胜于「获得」。",
            "that_point": "Knight 说多巴胺并不代表你嘴里嚼着食物时的「愉悦感」（liking），而是代表「渴望」（wanting）和摄食后强化——小鼠胃肠道感应到高热量后，会通过神经通路让大脑释放多巴胺，潜意识里标记「这个味道值得下次再要」。",
        },
    ],
    "en_title": "The Biology of Humans at Our Best and Worst · Robert Sapolsky",
    "en_tags": ["neurobiology", "aggression", "cognitive bias", "epigenetics", "free will", "us vs. them"],
    "en_connections": [
        {
            "slug": "michael-levin-bioelectricity-morphogenesis",
            "kind": "resonance",
            "relation": "Both argue that what determines a system's behavioral boundary is often not the fixed 'hardware' (the genome, or the neural circuit itself) but a 'symbol/signal' layer that can be reconfigured in an extremely short time. Sapolsky shows that the amygdala's hostile response to a racial outgroup face can be completely dissolved within milliseconds by putting the same person in a hat from the observer's own team — the genes and neural circuits haven't changed at all, only the input at the symbolic layer has. Levin shows the same principle's version in developmental biology: blocking gap junctions permanently gives a planarian two heads, and this 'software' rewrite is heritable across generations with the genome completely unchanged. Both point to the same conclusion: the boundary of behavior or form is determined by a rewritable signal layer, not by the genes or neural structure that appear more fundamental and 'hard.'",
        },
        {
            "slug": "neurobiology-of-hunger-zachary-knight",
            "kind": "resonance",
            "relation": "The two episodes independently confirm the same core neuroscience finding: dopamine doesn't encode the pleasure of 'obtaining a reward' itself — it encodes the 'wanting' and 'anticipation' of a reward. Sapolsky argues this from the angle of gambling and the pleasure of punishment — a 50% 'maybe' probability spikes dopamine higher than a certain reward does; Knight arrives at almost the identical conclusion from the angle of eating behavior — dopamine doesn't drive the immediate pleasure (liking) of food, it drives the wanting of food and post-ingestive reinforcement learning. Two completely different research subjects — social behavior/gambling versus eating/weight regulation — converge on the exact same functional definition of the same neural circuit.",
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
