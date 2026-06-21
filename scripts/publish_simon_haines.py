"""Publish simon-haines-fiona-mueller-education-activism (0621 plus batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "simon-haines-fiona-mueller-education-activism",
    "report": "reports/0621 plus/simon-haines-fiona-mueller-education-activism.md",
    "url": "https://youtu.be/8uf6bmCYr1k?si=C6ar8-CMfZKjpGfH",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "教育的异化、官僚化与通识传统的复兴 · Simon Haines & Fiona Mueller",
    "tags": ["人文通识", "经典阅读", "批判性教育学", "管理主义", "逆向自审"],
    "connections": [
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "同构",
            "why": "两期节目用了同一个词——「管理主义」（Managerialism）——描述同一种制度性退化，只是发生在不同的机构里。Marc 引用 Burnham 1941 年的论述：管理主义是 1880-1920 年代的制度产物，让可互换的管理技能取代了创始人亲自掌舵，制造了无法适应环境变化的企业集团文化。Haines 描述的是这个理论在今天大学里的精确投影：巨型大学半数以上雇员沦为行政管理者，师生比持续恶化，教学一线被极度临时化，机构的核心精力从「育人」转移到了「填报合规审计表格」。两人都指向同一个诊断：当一个机构的管理层规模超过其核心使命所需要的程度，机构就会丧失对环境变化做出真实反应的能力，只剩下自我维持的官僚惯性。",
            "this_point": "[53:32]-[54:45] Haines 说巨型大学盲目追逐排名，将半数以上的雇员扩张为官僚与行政管理者，其主要职责是阻断教学创新与填报审计表格，导致一线教学教职被极度临时化与廉价化——他称之为引用 David Graeber 概念的「管理主义封建化」。",
            "that_point": "Marc 引用 Burnham《马基雅维利主义者》：管理主义（可互换的管理技能，1880-1920年代的制度产物）让管理者可以在任何稳定环境里运营任何公司，但当世界改变、需要做艰难决定时，他们没有内在驱动力——因为他们的承诺从来不是不可逆的。",
        },
        {
            "slug": "robert-sapolsky-biology-best-worst",
            "kind": "resonance",
            "relation": "同构",
            "why": "Sapolsky 的神经科学研究为 Haines 和 Mueller 的教育学担忧提供了一个值得严肃对待的生物学注脚：人脑对「我们」与「他们」的划分极其敏感，而且这种划分可以被一个符号在几毫秒内瞬间触发或瓦解——给一张异族面孔戴上同队棒球帽，杏仁核的敌意信号就会被同队认同覆盖。这意味着，把课堂内容组织成「压迫者 vs. 被压迫者」的二元对立框架，并不是一个价值中立的教学选择，而是在主动激活一套人脑里最古老、最容易被点燃的群体归属回路。两人从完全不同的角度——教育哲学批评 vs. 神经科学实验——共同指向了同一个事实：群体划分的符号一旦被植入，会比单纯的事实陈述更深、更快地塑造一个人对世界的反应方式。",
            "this_point": "[33:37]-[34:22] Haines 和 Mueller 说以 Paulo Freire 二元对立学说为核心的批判教育学，将大量课堂精力用于向学生灌输「压迫者 vs. 被压迫者」的身份政治框架，系统性瓦解了基础读写教学的专业技能建设。",
            "that_point": "[29:53]-[31:01] Sapolsky 说杏仁核在百毫秒内对异族面孔产生敌对信号，但只要给对方戴上同队棒球帽，这一种族层面的敌对信号在脑中就会在毫秒内被同队认同覆盖——人脑对「我们」与「他们」的划分极其敏感，且可以被符号瞬间重新配置。",
        },
    ],
    "en_title": "The Alienation of Education, Bureaucratization, and the Revival of the Liberal Arts Tradition · Simon Haines & Fiona Mueller",
    "en_tags": ["liberal arts", "reading the classics", "critical pedagogy", "managerialism", "oikophobia"],
    "en_connections": [
        {
            "slug": "marc-andreessen-malleable-world-founder-capitalism",
            "kind": "resonance",
            "relation": "The two episodes use the same word — 'managerialism' — to describe the same institutional decay, just playing out in different institutions. Marc cites Burnham's 1941 argument: managerialism was an institutional product of the 1880s-1920s, in which interchangeable management skill replaced founders running their own organizations, producing a conglomerate culture incapable of adapting to a changing environment. Haines describes the exact same theory's projection onto today's universities: more than half the employees at mega-universities are administrators, the student-to-teacher ratio keeps worsening, frontline teaching becomes extremely precarious, and the institution's core energy shifts from 'educating people' to 'filling out compliance audit forms.' Both point to the same diagnosis: once an institution's management layer outgrows what its core mission actually requires, the institution loses the capacity to genuinely respond to a changing environment, left with only self-perpetuating bureaucratic inertia.",
        },
        {
            "slug": "robert-sapolsky-biology-best-worst",
            "kind": "resonance",
            "relation": "Sapolsky's neuroscience offers a biological footnote worth taking seriously for Haines and Mueller's educational worries: the human brain is exquisitely sensitive to the division between 'us' and 'them,' and that division can be triggered or dissolved within milliseconds by a single symbol — putting the same team's baseball cap on a face from a different race instantly overrides the amygdala's hostile signal with in-group recognition. This implies that organizing classroom content around an 'oppressor vs. oppressed' binary isn't a value-neutral pedagogical choice — it actively engages one of the oldest, most easily ignited group-belonging circuits in the human brain. The two arrive from entirely different angles — a critique of educational philosophy versus a neuroscience experiment — at the same fact: once a symbol for group division is implanted, it shapes how a person responds to the world more deeply and more quickly than a plain statement of fact ever could.",
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
