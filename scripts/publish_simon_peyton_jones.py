"""Publish simon-peyton-jones-haskell-functional-programming (0621 batch, verified against transcript)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEM = {
    "slug": "simon-peyton-jones-haskell-functional-programming",
    "report": "reports/0621/simon-peyton-jones-haskell-functional-programming.md",
    "url": "https://youtu.be/xcB_LF3cdqw?si=5-v3_z7m1oGjg5oC",
    "kind": "podcast",
    "date": "2026-06-21",
    "title": "纯粹函数式编程、类型系统与 AI 时代的代码演化 · Simon Payton Jones",
    "tags": ["函数式编程", "Haskell", "类型系统", "编译器设计", "软件维护性", "AI 辅助编程"],
    "connections": [
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人在完全不同的领域里，独立得出了同一个架构原则：声明式的「值/状态」描述比指令式的「修改步骤」更适合管理长期演化的复杂系统。Simon 说函数式编程的本质是「用值编程」——像 Excel 公式一样，只要输入确定，输出就唯一确定，避免了指令式语言里全局可变状态造成的隐性耦合。Tobi 把同样的原理直接搬进了公司管理：Shopify OS 借用 React 的核心思想——只声明「期望状态」是什么，再计算和「当前状态」的差异，找出最小变更步骤——用这套声明式逻辑取代了「谁在高尔夫球场上随口承诺了什么」式的命令式管理。",
            "this_point": "[00:57], [01:44] Simon 说函数式编程的本质是「用值编程」而非「修改状态」，类似电子表格公式：只要 A2 和 A3 确定了，A1 的结果就是唯一的，不需要关心计算的先后顺序。",
            "that_point": "[26:40-40:00] Tobi 说 Shopify OS 借用 React 的「期望状态系统」（Desired State System）：计算「应该是什么状态」，比较「现在是什么状态」，找到抵达目标的最小步骤——这让部门主管要50个新销售时，所有人立刻能看到这意味着从哪里拿走资源，政治由此消失。",
        },
        {
            "slug": "pavel-durov-telegram-freedom-resistance",
            "kind": "resonance",
            "relation": "同构",
            "why": "两人都奉行同一条原则：宁可暂时承受「不够成功」或「不够赚钱」的代价，也不为了迎合大众而妥协核心设计原则——而且都等到了这个原则被验证为正确的那一天。Simon 的座右铭「不惜一切代价避免成功」（avoid success at all costs）意思是绝不为了讨好用户而引入破坏纯粹性的特性；多年后，正是这种类型纯粹性让静态类型语言成为 LLM 自动编程时代的最大赢家。Durov 放弃了80%的潜在广告收入也不用用户数据变现；多年后，Telegram 反而靠1500万订阅用户在2024年首次盈利，证明了原则和商业回报并不是非此即彼。",
            "this_point": "[01:09:19]-[01:09:59] Simon 说他多年来常讲一句双关语「不惜一切代价避免成功」——如果你为了讨好大众而妥协核心原则，最终会被向后兼容性的沉重负担拖垮；他宁可让 Haskell 暂时保持小众和「无用」，也要守住设计精髓。",
            "that_point": "[03:55-04:10] Durov 的商业模式：上下文广告不使用个人数据，主动放弃80%的潜在广告收入；2024年首次盈利，靠1500万付费订阅用户贡献年收入5亿美元以上——没有用用户数据变现，没有算法信息流。",
        },
    ],
    "en_title": "Pure Functional Programming, Type Systems, and Code Evolution in the AI Era · Simon Peyton Jones",
    "en_tags": ["functional programming", "Haskell", "type systems", "compiler design", "software maintainability", "AI-assisted programming"],
    "en_connections": [
        {
            "slug": "tobi-lutke-companies-as-technology-shopify-os",
            "kind": "resonance",
            "relation": "Working in completely different domains, the two arrive independently at the same architectural principle: a declarative description of 'values/state' is better suited to managing a long-lived, evolving complex system than an imperative sequence of 'mutation steps.' Simon says the essence of functional programming is 'programming with values' — like an Excel formula, once the inputs are fixed, the output is uniquely determined, avoiding the invisible coupling that global mutable state creates in imperative languages. Tobi ports the exact same principle straight into company management: Shopify OS borrows React's core idea — declare only what the 'desired state' should be, compute the diff against the 'current state,' and find the minimal set of changes — replacing command-and-control management ('someone promised something on the golf course') with this declarative logic.",
        },
        {
            "slug": "pavel-durov-telegram-freedom-resistance",
            "kind": "resonance",
            "relation": "Both follow the same principle: better to accept the temporary cost of being 'not successful enough' or 'not profitable enough' than to compromise a core design principle to please the mainstream — and both lived to see that principle vindicated. Simon's motto, 'avoid success at all costs,' means never introducing a feature that breaks purity just to please users; years later, that very purity is what makes statically typed languages the biggest winner of the LLM auto-coding era. Durov forgoes 80% of potential ad revenue rather than monetize user data; years later, Telegram turned its first profit in 2024 on the back of 15 million paying subscribers, proof that principle and commercial return aren't mutually exclusive.",
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
