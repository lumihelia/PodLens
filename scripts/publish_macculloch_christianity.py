"""Publish diarmaid-macculloch-christianity-sex-history using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "diarmaid-macculloch-christianity-sex-history",
    "report": "reports/diarmaid-macculloch-christianity-sex-history.md",
    "url": "https://youtu.be/VeDKWf80Z3M?si=tgYchuRPSXpo_dEk",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "基督教、性与颠覆定论 · Diarmaid MacCulloch",
    "tags": ["宗教史", "基督教", "性与婚姻", "历史方法论", "宗教改革"],
    "connections": [
        {
            "slug": "rights-pre-modern-masculinist-fantasy",
            "kind": "resonance",
            "relation": "张力",
            "why": "右翼基督教话语体系援引保罗来压制性别平等、援引「传统婚姻」来论证父权结构——但 MacCulloch 的历史考证直接拆解这一叙事：保罗最重要的婚姻文本恰恰是古代最平等的性别声明，而「传统」婚姻中的独身要求不过是12世纪的制度发明。",
            "this_point": "[05:45-06:22] 保罗《哥林多前书》7:3 声称丈夫的身体同样属于妻子——MacCulloch 称之为「真正非凡、前所未有的声明」，两千年来几乎被整个基督教传统搁置。",
            "that_point": "[34:47-38:07] 右翼基督教与福音派将耶稣男性化、偏好引用保罗来论证传统性别秩序——但这种援引建立在对保罗文本的选择性剪辑之上，与历史记录中保罗的实际立场相悖。",
        },
    ],
    "en_title": "Christianity, Sex, and Unsettling Settled Facts · Diarmaid MacCulloch",
    "en_tags": ["religious history", "Christianity", "sex and marriage", "historiography", "Reformation"],
    "en_connections": [
        {
            "slug": "rights-pre-modern-masculinist-fantasy",
            "kind": "resonance",
            "relation": "direct historical counter: MacCulloch's scholarship shows that what the New Right calls 'traditional Christianity' on gender and marriage is largely a 12th-century institutional invention — and that Paul's actual texts on sexuality are more egalitarian than the right-wing reading acknowledges",
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
        print(f"  {c['kind']} -> {c['slug']} ({c['relation'][:40]}...)")
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
