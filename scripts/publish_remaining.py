"""Publish the 4 remaining reports using Claude-generated translations (no Gemini API).

Reads pre-written en body files from scripts/en_bodies/, extracts zh public
content from the report, then calls publish_report() directly.

Usage:
    .venv/bin/python scripts/publish_remaining.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_BODIES_DIR = Path(__file__).resolve().parent / "en_bodies"
sys.path.insert(0, str(ROOT))

from podlens.publish import extract_public_markdown, load_site_config, publish_report

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]

ITEMS = [
    {
        "slug": "joscha-bach-nature-of-reality-dreams-consciousness",
        "report": "reports/joscha-bach-nature-of-reality-dreams-consciousness.md",
        "url": "https://youtu.be/rIpUf-Vy2JA?si=gXnGCO58t36qh8Ae",
        "kind": "podcast",
        "date": "2026-06-09",
        "title": "现实之网、梦境与意识的本质 · Joscha Bach",
        "tags": ["控制论", "注意力模型", "模拟假说", "自由意志", "认知基础设施", "意识形态"],
        "connections": [
            {"slug": "joscha-bach-life-intelligence-consciousness-future", "kind": "resonance", "relation": "同构"},
            {"slug": "meditation-state-most-people-never-experience", "kind": "resonance", "relation": "延伸"},
            {"slug": "yann-lecun-world-models-next-ai-revolution", "kind": "tension", "relation": "张力"},
            {"slug": "the-era-of-experience", "kind": "resonance", "relation": "补充"},
        ],
        "en_title": "The Nature of Reality, Dreams, and Consciousness · Joscha Bach",
        "en_tags": ["cybernetics", "attention model", "simulation hypothesis", "free will", "cognitive infrastructure"],
        "en_connections": [
            {"slug": "joscha-bach-life-intelligence-consciousness-future", "kind": "resonance",
             "relation": "companion episode by same speaker exploring the same cybernetic consciousness framework"},
            {"slug": "meditation-state-most-people-never-experience", "kind": "resonance",
             "relation": "both explore consciousness and altered mind states through first-person experience"},
            {"slug": "yann-lecun-world-models-next-ai-revolution", "kind": "tension",
             "relation": "Bach advocates discrete simulation-based consciousness; LeCun advocates continuous world model representations"},
            {"slug": "the-era-of-experience", "kind": "resonance",
             "relation": "DeepMind's experience-based AI thesis complements Bach's simulation hypothesis about consciousness requiring modeled experience"},
        ],
    },
    {
        "slug": "jane-street-gpus-trading-hiring-dwarkesh",
        "report": "reports/jane-street-gpus-trading-hiring-dwarkesh.md",
        "url": "https://youtu.be/xKZ_8ULR91Y?si=BgAEuMWNMEKXXWWX",
        "kind": "podcast",
        "date": "2026-06-10",
        "title": "算力、交易与招聘：Jane Street 的技术与组织哲学 · Ron Minsky & Dan Ponttovo",
        "tags": ["Jane Street", "算力底座", "交易策略", "量化招聘", "协同设计"],
        "connections": [
            {"slug": "ms&e435-class4-economics-ai-supercycle", "kind": "resonance", "relation": "同构"},
            {"slug": "cs153-08-jensen-huang-nvidia-compute", "kind": "resonance", "relation": "印证"},
            {"slug": "dan-loeb-ai-credit-third-point", "kind": "resonance", "relation": "延伸"},
            {"slug": "how-an-ai-chip-works-from-the-bottom-up-reiner-pope", "kind": "resonance", "relation": "补充"},
        ],
        "en_title": "Compute, Trading, and Hiring: Jane Street's Technology and Organizational Philosophy · Ron Minsky & Dan Ponttovo",
        "en_tags": ["Jane Street", "compute infrastructure", "trading strategy", "quantitative hiring", "codesign"],
        "en_connections": [
            {"slug": "ms&e435-class4-economics-ai-supercycle", "kind": "resonance",
             "relation": "both analyze compute economics and strategic AI infrastructure investment"},
            {"slug": "cs153-08-jensen-huang-nvidia-compute", "kind": "resonance",
             "relation": "Jane Street's GPU scale-up story validates Jensen Huang's compute scaling vision"},
            {"slug": "dan-loeb-ai-credit-third-point", "kind": "resonance",
             "relation": "both finance-world perspectives on AI's structural impact on markets and investment strategy"},
            {"slug": "how-an-ai-chip-works-from-the-bottom-up-reiner-pope", "kind": "resonance",
             "relation": "hardware-constrained co-design philosophy shared between chip engineering and trading system design"},
        ],
    },
    {
        "slug": "rights-pre-modern-masculinist-fantasy",
        "report": "reports/rights-pre-modern-masculinist-fantasy.md",
        "url": "https://youtu.be/YK1aj39y55k?si=mqXBvOLIyINPGi8-",
        "kind": "podcast",
        "date": "2026-06-09",
        "title": "右翼的\"前现代\"男性气概幻想 · Helen Lewis",
        "tags": ["男性气概", "政治文化", "MAGA", "性别叙事", "保守主义"],
        "connections": [
            {"slug": "joscha-bach-life-intelligence-consciousness-future", "kind": "resonance", "relation": "同构"},
            {"slug": "mental-models-that-change-how-you-think", "kind": "tension", "relation": "张力"},
            {"slug": "ms&e435-class4-economics-ai-supercycle", "kind": "tension", "relation": "张力"},
        ],
        "en_title": "The Right's Pre-Modern Masculinist Fantasy · Helen Lewis",
        "en_tags": ["masculinity", "political culture", "MAGA", "gender narrative", "conservatism"],
        "en_connections": [
            {"slug": "joscha-bach-life-intelligence-consciousness-future", "kind": "resonance",
             "relation": "both dissect postmodern collapse of ground truth and ideological drift in affluent societies"},
            {"slug": "mental-models-that-change-how-you-think", "kind": "tension",
             "relation": "Mack builds frameworks for clear thinking; Lewis reveals how frameworks can be weaponized in political manipulation"},
            {"slug": "ms&e435-class4-economics-ai-supercycle", "kind": "tension",
             "relation": "AI optimism about economic transformation vs Lewis's warning that political fragmentation accelerates as social constraints loosen"},
        ],
    },
    {
        "slug": "microglia-function-cns-development-plasticity",
        "report": "reports/microglia-function-cns-development-plasticity.md",
        "url": "https://cshperspectives.cshlp.org/content/7/10/a020545.full.pdf",
        "kind": "paper",
        "date": "2026-06-10",
        "title": "中枢神经系统发育与可塑性中的小胶质细胞功能 · Dorothy P. Schafer",
        "tags": ["小胶质细胞", "突触剪切", "经典补体级联", "活性依赖性", "发育可塑性"],
        "connections": [
            {"slug": "microglia-synaptic-pruning", "kind": "resonance", "relation": "承接"},
            {"slug": "active-forgetting", "kind": "resonance", "relation": "同构"},
            {"slug": "neurobiology-of-hunger-zachary-knight", "kind": "resonance", "relation": "补充"},
            {"slug": "agent-memory", "kind": "resonance", "relation": "印证"},
        ],
        "en_title": "Microglia Function in Central Nervous System Development and Plasticity · Dorothy P. Schafer",
        "en_tags": ["microglia", "synaptic pruning", "complement cascade", "activity-dependent", "developmental plasticity"],
        "en_connections": [
            {"slug": "microglia-synaptic-pruning", "kind": "resonance",
             "relation": "Schafer's CNS development paper is foundational context for the synaptic pruning review published separately"},
            {"slug": "active-forgetting", "kind": "resonance",
             "relation": "both papers explore selective elimination as a neural maintenance principle: phagoptosis for development, active forgetting for adult plasticity"},
            {"slug": "neurobiology-of-hunger-zachary-knight", "kind": "resonance",
             "relation": "both reveal how molecular-level neural mechanisms govern macro behavioral outputs"},
            {"slug": "agent-memory", "kind": "resonance",
             "relation": "activity-dependent pruning principle maps onto selective retention and forgetting in AI agent memory systems"},
        ],
    },
]


def main() -> int:
    site = load_site_config()
    errors = []

    for item in ITEMS:
        slug = item["slug"]
        section = "papers" if item["kind"] == "paper" else "episodes"
        print(f"\n{'='*60}")
        print(f"Publishing: {slug}")

        report_path = ROOT / item["report"]
        if not report_path.exists():
            print(f"!! SKIP: report not found at {report_path}")
            errors.append(slug)
            continue

        en_body_path = EN_BODIES_DIR / f"{slug}.md"
        if not en_body_path.exists():
            print(f"!! SKIP: en body not found at {en_body_path}")
            errors.append(slug)
            continue

        report_md = report_path.read_text(encoding="utf-8")
        public_md = extract_public_markdown(report_md, site.private_cutoff)
        if not public_md:
            print(f"!! SKIP: no public content extracted (check private cutoff heading)")
            errors.append(slug)
            continue

        en_body = en_body_path.read_text(encoding="utf-8")

        en = {
            "title": item["en_title"],
            "tags": item["en_tags"],
            "body": en_body,
            "connections": item["en_connections"],
        }

        print(f"  title:   {item['title']}")
        print(f"  tags:    {', '.join(item['tags'])}")
        for c in item["connections"]:
            print(f"  {c['kind']}: -> {c['slug']} ({c['relation']})")
        print(f"  [bilingual] using Claude translation from en_bodies/")

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

        # Privacy gate
        leaks = []
        for lang in ("zh", "en"):
            d = ROOT / "docs" / (section if lang == "zh" else f"en/{section}")
            p = d / f"{entry['slug']}.html"
            if p.exists():
                h = p.read_text(encoding="utf-8")
                leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

        print(f"\n{'='*30} 发布完成(本地,未推送) {'='*30}")
        print(f"slug: {entry['slug']}  kind: {item['kind']}")
        print(f"zh 页面: docs/{section}/{entry['slug']}.html")
        print(f"en 页面: docs/en/{section}/{entry['slug']}.html")
        if leaks:
            print(f"!! 隐私检查失败, 发现私人层泄漏: {leaks}")
            errors.append(slug)
        else:
            print("隐私检查: 通过(公开页零私人层泄漏)")

    print(f"\n{'='*60}")
    if errors:
        print(f"!! DONE WITH ERRORS: {errors}")
        return 1
    print("ALL 4 ITEMS PUBLISHED SUCCESSFULLY (local, not pushed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
