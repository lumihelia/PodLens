"""Publish tim-spector-gut-microbiome-mental-health (0621 plus batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "tim-spector-gut-microbiome-mental-health",
    "report": "reports/0621 plus/tim-spector-gut-microbiome-mental-health.md",
    "url": "https://youtu.be/A3_fG1h2a_g?si=A2qdjxmoCtRGF08u",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "肠道微生态、神经免疫与膳食多中心主义 · Tim Spector",
    "tags": ["肠道微生态", "神经免疫学", "膳食多样性", "慢性炎症", "限时禁食"],
    "connections": [
        {
            "slug": "robert-sapolsky-biology-best-worst",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在论证同一件事：我们习惯归因为「心理状态」或「人格判断」的东西，往往是身体某个看不见的化学信号在替我们做决定。Sapolsky 说假释法官饿了4小时之后，假释率会从60%跌到接近零——前额叶因为血糖不足而丧失了进行复杂道德权衡的生理能量。Spector 描述的是同一种机制在更长时间尺度上的版本：肠道慢性炎症产生的化学警报通过迷走神经持续向上传输，大脑接到这个系统性危机信号后会自发触发「生病避役行为」——下调社交意愿、产生持续疲劳——这种状态在外部看起来和抑郁症完全一样，但根源完全不在于「心理脆弱」，而是肠道在向脑部发送求救信号。两人都在拆解同一个迷思：我们以为是「自由选择」或「性格缺陷」的行为，常常只是身体某个器官的化学状态在做主。",
            "this_point": "[17:33]-[18:05] Spector 说抑郁、疲劳等精神症状本质上是脑部对肠道慢性炎症发出的「生病避役行为」的体现：长期劣质饮食或创伤压力破坏肠黏膜屏障，引发全身性慢性炎症，大脑读取这一系统性危机信号后会自发下调社交、活动意愿，并产生持续疲劳。",
            "that_point": "[28:20]-[28:48] Sapolsky 说以色列假释委员会的法官刚吃完饭时给出60%的假释概率，四小时后饿了，假释率逼近零值——血糖匮乏导致前额叶皮层进行深度道德换位思考的生理能量发生严重退化。",
        },
        {
            "slug": "michael-levin-bioelectricity-morphogenesis",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都在论证：智能和决策并不只发生在大脑里，而是分布在身体的化学/电信号网络中，且这套网络比大脑古老得多。Spector 说肠道拥有独立于脑部、被称为「第二大脑」的神经元网络，通过迷走神经这条「高速光纤」持续向上发送决定脑部炎症和情绪状态的化学信号——这条通讯几乎是单向的，肠道决定大脑，而不是反过来。Levin 描述的是同样原理在发育生物学里的版本：「认知粘合剂」（生物电网络）在人类大脑和神经元进化出来之前就已经存在，是细胞集体获得整体目标、偏好和记忆的底层机制。两人都在说同一件事：在神经元出现之前，身体早已有了自己的「思考」方式，而这套更古老的系统至今仍在决定我们的行为。",
            "this_point": "[08:31]-[09:00], [09:58]-[10:23] Spector 说肠脑轴的信号交通是高度不对称的，大多数通讯由肠道向上单向发送给大脑——大脑通过迷走神经这条高速光纤，被动读取肠道因食物、压力产生的分子级化学警报，并自适应调整行为认知状态。",
            "that_point": "[02:30]-[04:19] Levin 说在人类大脑和神经元进化出来之前，大自然就已经使用离子通道和缝隙连接在胚胎发育中传递全局信息了——这种「认知粘合剂」让独立的细胞组织成具有整体目标、偏好和记忆的生命共同体。",
        },
    ],
    "en_title": "The Gut Microbiome, Neuroimmunity, and Dietary Polycentrism · Tim Spector",
    "en_tags": ["gut microbiome", "neuroimmunology", "dietary diversity", "chronic inflammation", "time-restricted eating"],
    "en_connections": [
        {
            "slug": "robert-sapolsky-biology-best-worst",
            "kind": "resonance",
            "relation": "Both argue the same point: what we habitually attribute to 'psychological state' or 'character judgment' is often a chemical signal somewhere in the body, invisible to us, making the decision on our behalf. Sapolsky says a parole judge's approval rate drops from 60% to near zero after four hours without food — the prefrontal cortex has lost the physiological energy for complex moral weighing due to low blood sugar. Spector describes the same mechanism's version on a longer timescale: the chemical alarm produced by chronic gut inflammation travels continuously upward via the vagus nerve, and once the brain receives this systemic distress signal, it spontaneously triggers 'sickness behavior' — reduced sociability, persistent fatigue — a state that looks identical to depression from the outside, but whose root cause has nothing to do with 'psychological fragility' and everything to do with the gut sending a distress call to the brain. Both are dismantling the same myth: what we think is 'free choice' or a 'character flaw' is often just the chemical state of some organ calling the shots.",
        },
        {
            "slug": "michael-levin-bioelectricity-morphogenesis",
            "kind": "resonance",
            "relation": "Both argue that intelligence and decision-making don't happen only in the brain — they're distributed across the body's chemical and electrical signaling networks, and this network is far older than the brain itself. Spector says the gut has its own neuron network, independent of the brain, called the 'second brain,' continuously sending chemical signals up the 'fiber-optic cable' of the vagus nerve that determine the brain's inflammation and mood — and this communication runs almost entirely one way, the gut deciding the brain, not the reverse. Levin describes the same principle's version in developmental biology: 'cognitive glue' (the bioelectric network) existed before the human brain and neurons ever evolved, and is the underlying mechanism by which a collective of cells acquires a shared goal, preference, and memory. Both are saying the same thing: long before neurons appeared, the body already had its own way of 'thinking,' and that older system still determines our behavior today.",
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
