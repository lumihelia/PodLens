"""Publish ONE validated report (episode or paper) from reports/<slug>.md.

Generalizes publish_episode.py / publish_paper.py into a single parameterized
entry point so a backlog can be rolled out one item per invocation. The report
must already be reviewed; this step only strips the private layer, (for papers)
verifies anchors against the source PDF, finds cross-source connections, builds
the zh/en bundle, and publishes.

The slug is forced to the report's filename stem, so URLs stay deterministic and
series like CS153 keep an ordered, human-readable path.

API cost per run: one connections call + one translation call. Nothing else.

Usage:
    .venv/bin/python scripts/publish_one.py reports/<slug>.md "<source_url>" \
        --kind podcast --date 2026-06-09
    .venv/bin/python scripts/publish_one.py reports/<slug>.md "<source_url>" \
        --kind paper --pdf "论文/<file>.pdf" --date 2026-06-09
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import build_bilingual, find_connections
from podlens.publish import (
    build_candidates, extract_claims_section, extract_public_markdown,
    load_site_config, publish_report, slugify,
)

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish one reviewed report.")
    ap.add_argument("report", help="path to reports/<slug>.md")
    ap.add_argument("url", help="source URL (YouTube / paper)")
    ap.add_argument("--kind", choices=["podcast", "paper"], default="podcast")
    ap.add_argument("--date", default="2026-06-09")
    ap.add_argument("--pdf", default="", help="source PDF (papers only; enables anchor verify)")
    args = ap.parse_args()

    report_path = (ROOT / args.report).resolve()
    if not report_path.exists():
        print(f"错误: 报告不存在: {report_path}"); return 1
    slug = report_path.stem
    source_url = args.url.strip()
    section = "papers" if args.kind == "paper" else "episodes"

    config = load_config()
    site = load_site_config()
    report = report_path.read_text(encoding="utf-8")

    # 1) Papers only: neutralize any anchor quote not found verbatim in the PDF.
    if args.kind == "paper" and args.pdf:
        from podlens.papers import load_paper, verify_anchors
        pdf_path = (ROOT / args.pdf).resolve()
        if not pdf_path.exists():
            print(f"错误: PDF 不存在: {pdf_path}"); return 1
        paper = load_paper(str(pdf_path))
        report, ok, fixed = verify_anchors(report, paper)
        print(f"[校验] 锚点可追溯 {ok} 条; 查无此句已降级为释义 {fixed} 条")

    # 2) Title + tags from the report header.
    m_title = re.search(r"^#\s+(.+)$", report, re.M)
    if not m_title:
        print("错误: 报告缺少标题行。"); return 1
    title = m_title.group(1).strip()
    m_tags = re.search(r"标签[:：]\s*(.+)", report)
    tags = [t.strip() for t in re.split(r"[,，]", m_tags.group(1))] if m_tags else []
    tags = [t for t in tags if t][:6]
    print(f"[元数据] slug: {slug}")
    print(f"        标题: {title}")
    print(f"        标签: {', '.join(tags) if tags else '(无)'}")

    native_public = extract_public_markdown(report, site.private_cutoff)
    if not native_public:
        print("错误: 未提取到公开层(检查私人层切点)。"); return 1

    # 3) Cross-source connections against already-published items.
    candidates = build_candidates(tags, exclude_slug=slug)
    print(f"[关联] 在 {len(candidates)} 期往期中查找呼应/张力 ...")
    connections = find_connections(
        title, extract_claims_section(report), candidates, config, lang="zh"
    )
    for c in connections:
        print(f"        {c.get('kind')}: -> {c.get('slug')} ({c.get('relation')})")
    if not connections:
        print("        (未找到具体到论点级别的关联)")

    # 4) Bilingual: Chinese native body -> English mirror.
    print("[双语] 翻译公开层生成 /en 镜像 ...")
    _, zh_b, en_b = build_bilingual(native_public, title, tags, connections, config)

    entry = publish_report(
        report, zh_b["title"], site, date=args.date, slug=slug,
        source_url=source_url, tags=zh_b["tags"], connections=zh_b["connections"],
        en=en_b, primary_public_md=zh_b["body"], kind=args.kind,
    )

    # 5) Privacy gate on the CORRECT section dir (papers render to /papers).
    leaks = []
    for lang in ("zh", "en"):
        d = ROOT / "docs" / (section if lang == "zh" else f"en/{section}")
        p = d / f"{entry['slug']}.html"
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print("\n================ 发布完成(本地,未推送)================")
    print(f"slug: {entry['slug']}  kind: {args.kind}")
    print(f"zh 页面: docs/{section}/{entry['slug']}.html")
    print(f"en 页面: docs/en/{section}/{entry['slug']}.html")
    if leaks:
        print(f"!! 隐私检查失败, 发现私人层泄漏: {leaks}")
        return 2
    print("隐私检查: 通过(公开页零私人层泄漏)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
