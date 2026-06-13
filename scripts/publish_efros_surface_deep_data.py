"""Publish alexei-efros-surface-data-deep-data using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "alexei-efros-surface-data-deep-data",
    "report": "reports/alexei-efros-surface-data-deep-data.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "表层数据与深层数据 · Alexei Efros",
    "tags": ["具身智能", "好奇心驱动", "深层数据", "机器人", "世界模型"],
    "connections": [
        {
            "slug": "yann-lecun-world-models-next-ai-revolution",
            "kind": "resonance",
            "relation": "同构",
            "why": "两者共享同一核心洞察：在表示/特征空间做预测比在像素/token层面更有效。Efros 的2017好奇心论文正是「Yann 称之为世界模型之前的世界模型」，JEPA 是其系统化与命名。",
            "this_point": "[30:25-31:44] Efros 将2017年好奇心论文称为「pre-JEPA」——在特征空间做预测、同步训练逆模型学习特征表示，显式说这是「Yann 之前就存在的世界模型」。",
            "that_point": "[23:36-25:00] Yann LeCun 提出 JEPA（联合嵌入预测架构）：不在像素空间而在表示空间做抽象预测，以过滤噪声并捕获物理规律——即 Efros 2017年工作的系统化后继。",
        },
        {
            "slug": "the-era-of-experience",
            "kind": "resonance",
            "relation": "印证",
            "why": "Silver & Sutton 提出 AI 正从「人类数据时代」转向「经验时代」——智能体主动与环境交互产生经验来学习；这正是 Efros 的深层数据飞轮。Efros 在演讲末甚至直接说 Sutton 最新论文「提到数据18次，非常同意我们」。",
            "this_point": "[37:00-37:28] Efros 说 Rich Sutton 最新论文「非常同意我们，提到了数据18次」，并提出飞轮宣言：「不要问数据能为你的机器人做什么，要问你的机器人能为数据做什么」。",
            "that_point": "[The Era of Experience · 核心论断] 论文主张 AI 正从「人类数据时代」转向「经验时代」——智能体将通过与环境主动交互产生的经验进行持续学习，突破监督学习的人类数据瓶颈。",
        },
        {
            "slug": "human-data-and-robotics-gpt-3-moment-danfei-xu",
            "kind": "resonance",
            "relation": "补充",
            "why": "Efros 诊断了机器人深层数据危机（数量为零、质量错误），但未给出采集路径；Danfei Xu 的 EgoMimic 工作正好填补这个缺口：以第一人称人类数据作为可规模化的具身深层数据来源。",
            "this_point": "[20:15-21:00] Efros 指出机器人数据「几乎为零」且「种类错误」——遥操作缺乏规模和负样本，物理世界的「推回」无法从被动数据中获得。",
            "that_point": "[01:23:53] Danfei Xu 指出第一人称人类视频（EgoMimic）在数据精确度与可规模化之间找到甜蜜点——让采集者佩戴 AR 眼镜主动生活即可采集具身交互数据，是机器人深层数据的当前最佳路径。",
        },
    ],
    "en_title": "Surface Data vs. Deep Data · Alexei Efros",
    "en_tags": ["embodied intelligence", "curiosity-driven", "deep data", "robotics", "world models"],
    "en_connections": [
        {
            "slug": "yann-lecun-world-models-next-ai-revolution",
            "kind": "resonance",
            "relation": "Efros's 2017 curiosity paper is explicitly called 'pre-JEPA' — prediction in feature space with a simultaneously trained inverse model, i.e. a world model before Yann named it",
        },
        {
            "slug": "the-era-of-experience",
            "kind": "resonance",
            "relation": "both argue that agents must actively interact with environments to generate experiential data — Efros's deep data flywheel and Silver/Sutton's 'era of experience' are the same thesis from different traditions; Efros even cites Sutton's newest paper as 'very much agreeing with us'",
        },
        {
            "slug": "human-data-and-robotics-gpt-3-moment-danfei-xu",
            "kind": "resonance",
            "relation": "Efros diagnoses the robotics deep-data crisis (near-zero data, wrong kind); Danfei Xu's EgoMimic work provides the acquisition path: first-person human video as scalable embodied deep data for robots",
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
    print(f"  title:   {item['title']}")
    print(f"  tags:    {', '.join(item['tags'])}")
    for c in item["connections"]:
        print(f"  resonance -> {c['slug']} ({c['relation'][:40]}...)")
    print("  [bilingual] using Claude translation from en_bodies/")

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

    print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
    print(f"slug: {entry['slug']}  kind: {item['kind']}")
    print(f"zh:   docs/episodes/{entry['slug']}.html")
    print(f"en:   docs/en/episodes/{entry['slug']}.html")
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 1
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
