"""Publish patrick-oshaughnessy-principle-life-work using Claude translation (no Gemini API)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "patrick-oshaughnessy-principle-life-work",
    "report": "reports/patrick-oshaughnessy-principle-life-work.md",
    "url": "",
    "kind": "podcast",
    "date": "2026-06-14",
    "title": "原则、生命之业与不竭之欢 · Patrick O'Shaughnessy",
    "tags": ["原则与目标", "生命之业", "不竭之欢", "增长而无目标", "发现才华"],
    "connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "张力",
            "why": "Patrick和Rubin都围绕「真实自我表达是作品力量来源」这个核心哲学组织他们的工作——两人都拒绝把创作强行导向预设结果。但方法结构上相反：Rubin是激进的被动——作品通过你来到，你的工作是清空障碍、让它到达；Patrick是主动的原则驱动——他通过构建组织、做播客、写长篇特写来执行一个原则，这个原则本身也是真实的，但它是行动而非等待。Rubin的「少即是多」来自删除——「移除所有不属于它的东西」；Patrick的生命之业来自累积——一生的探索和建造。两者都在服务一个比自我更大的东西，但路径截然不同。",
            "this_point": "[01:23:32-01:24:10] Patrick定义生命之业：「一生的探索，去建立对他人有益并表达你自己的东西。」以及[09:05-10:43] 「增长而无目标」：所有真正有意义的事情都从视野边缘来——不是从精心设计的目标里，而是从你没有在找它的地方。Patrick的方法是主动的：他建播客、杂志、基金，每一个都是同一个原则的不同形式；但他从不把某个结果定为目标。",
            "that_point": "[28:00-35:00] Rubin的核心立场：艺术家是一个容器，作品本身存在于宇宙中，你的工作是清空自己的偏见和期望，让作品通过你来到。「删除所有阻碍它的东西。」Rubin的激进被动——不是「建造它」，而是「揭示它」——与Patrick的原则驱动主动性形成直接张力：同样的真实性哲学，完全相反的操作模式。",
        },
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都通过不同的路径抵达相同的目的地：一种当你使用时不会耗尽的喜悦——Patrick从26岁读《奥义书》，Brooks从五六十岁的幸福科学研究和宗教转变。两人都明确地把金钱/权力/声名画为陷阱：第一次拥有感觉极好，然后把你困住。两人都把「对他人的贡献」识别为唯一的非耗尽性燃料。更深层：两人都以死亡恐惧作为最初的探索驱动力（Patrick有严重的童年死亡恐惧；Brooks的父亲之死成为他重新反思什么是幸福的扳机），然后找到了某种「让死亡恐惧转化为服务意志」的路径。",
            "this_point": "[06:06-08:31, 40:53-41:48] Patrick从26岁起的世界观：「整件事的意义就是帮助他人。就这些。」《奥义书》的「不竭之欢」：「这是一种不会耗尽的喜悦，不像那么多资源被消耗掉。当你使用它时，你得到更多。」对比：金钱、权力、声名——「感觉非常好，第一次拥有时。然后它们把你困住了。」Patrick还提到儿时对死亡的严重恐惧，通过哲学和宗教探索找到了答案。",
            "that_point": "[18:00-28:00] Brooks的幸福科学框架：金钱/权力/声名满足「流动智力」的追求，但流动智力在35-45岁后开始下降——如果你的身份完全建立在它上面，你会在顶峰崩溃。真正的幸福来自信仰、家庭、友谊和对他人有意义的工作（贡献，而不是成就）。Brooks的父亲之死是扳机：他发现「我在追求的所有东西都不是我实际想要的」——与Patrick的Springsteen分析完全同构：顶峰→深渊→真正的东西。",
        },
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "同构",
            "why": "Patrick的核心原则（在他人之前看到未被发现的巨大潜力，有义务去揭示它）与Garry的YC使命（让更多人能进入这个帐篷、获得工具和资源）在结构上是同一个主张：把还没有被广泛接触到的东西带给更多的人。两人都直接被「有人在他们不值得时赌上了他们」的经历塑造：Tim O'Shaughnessy在Patrick刚到Notre Dame时的极度慷慨改变了他的整个人生轨迹；Garry在YC获得的早期支持同样是一个生命转折点。两人都理解「创始人不只是创立公司，也可以创立家庭」——David Senra的古巴祖父和Patrick的Tim故事都是「一个人的一个决定改写了整个家族轨迹」的同构叙事。",
            "this_point": "[06:06-08:31, 02:04:12-02:05:04] Patrick的核心乐趣和原则：在别人发现之前找到一个人和他们正在做的事，成为他们最热烈的支持者。Tim O'Shaughnessy故事：刚到Notre Dame的第一个学期，Tim主动把Patrick整合进社交圈，甚至在自己不能参加时打电话「我来不了，但Patrick来——好好照顾他」。Patrick后来遇到了他的妻子和他最好的朋友们。Tim年轻离世。「整个生活都是简单、快速的善意行为的下游产物。」",
            "that_point": "[01:26:02-01:26:27, 01:52:14-01:53:20] Garry的使命：让技术和工具进入更多人的手中，「技术就是一种服务彼此的方式」——他的民主化使命来自个人的技术债务感。关于「创立家庭的创始人」：David Senra的祖父从古巴出逃，那一个决定让整个后代的轨迹改写——David是他家族的「创始人」，他的存在和选择是那一个决定的远期涟漪。Garry对YC校友的「下注」是同一个原则在组织规模上的表达。",
        },
    ],
    "en_title": "Principle, Life's Work, and Abiding Joy · Patrick O'Shaughnessy",
    "en_tags": ["principle vs goal", "life's work", "abiding joy", "growth without goals", "discovering talent"],
    "en_connections": [
        {
            "slug": "rick-rubin-creative-act-less-is-more",
            "kind": "resonance",
            "relation": "Both organize their work around authentic self-expression as the source of creative power, and both resist forcing work toward predetermined outcomes (Patrick's 'growth without goals'; Rubin's 'clear the space, let it arrive'). But the method is structurally opposite: Rubin is radically passive — the work comes through the artist, who must empty themselves of expectations to receive it; Patrick is actively principle-driven — he builds podcasts, magazines, and investment funds to execute a principle, with intention and construction rather than waiting and receiving. Same commitment to authenticity, opposite operating modes.",
        },
        {
            "slug": "arthur-brooks-reinvention-religion-happiness",
            "kind": "resonance",
            "relation": "Both arrive at the same destination through different routes: a joy that does not deplete as you use it (Patrick from the Upanishads at twenty-six; Brooks from happiness science research and religious conversion in his fifties). Both explicitly map money, power, and fame as the trap — feels intensely good at first, then hollows you out. Both identify service-to-others as the only non-depleting fuel. Both used the fear of death as an early driver before finding a path toward something generative — Patrick's childhood terror of death resolved through philosophy; Brooks' father's death as the trigger for reconsidering what happiness actually is.",
        },
        {
            "slug": "garry-tan-yc-personal-ai-revolution",
            "kind": "resonance",
            "relation": "Patrick's organizing principle (see enormous unrealized potential before others do; it is your obligation to reveal it) and Garry's YC mission (bring more people into the tent, democratize tools and resources) are structurally the same claim: take something not yet widely accessible and spread it as broadly as possible. Both were fundamentally shaped by one person betting on them before they deserved it. Both understand the concept of 'founder of a family' — the person who makes the choice that rewrites the generational trajectory for everyone who comes after: Tim O'Shaughnessy for Patrick; David Senra's grandfather leaving Cuba.",
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
