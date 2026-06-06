"""Publish the validated paper interpretation bilingually + push-ready.

Takes the prototype report (already reviewed), runs the anchor verifier against
the source PDF so no un-findable quote ships, finds cross-source connections to
existing episodes, builds the zh/en bundle, and publishes as kind="paper".

The FULL report (incl. the private personal-mapping layer) is archived to
reports/<slug>.md (gitignored, LOCAL only) — never published.

Usage:
    .venv/bin/python scripts/publish_paper.py "<source paper URL>"
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import build_bilingual, find_connections
from podlens.papers import load_paper, verify_anchors
from podlens.publish import (
    build_candidates, extract_claims_section, extract_public_markdown,
    load_site_config, publish_report, slugify,
)

DATE = "2026-06-06"
REPORT_PATH = ROOT / "reports" / "PROTOTYPE-era-of-experience.md"
PAPER_PATH = ROOT / "论文" / "The Era of Experience Paper.pdf"

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("用法: publish_paper.py \"<论文原文链接>\"")
        return 1
    source_url = sys.argv[1].strip()

    config = load_config()
    site = load_site_config()

    report = REPORT_PATH.read_text(encoding="utf-8")
    paper = load_paper(str(PAPER_PATH))

    # 1) Traceability guarantee: neutralize any anchor quote not in the source.
    report, ok, fixed = verify_anchors(report, paper)
    print(f"[校验] 锚点可追溯 {ok} 条;查无此句已降级为释义 {fixed} 条")

    # 2) Title + tags from the report header.
    title = re.search(r"^#\s+(.+)$", report, re.M).group(1).strip()
    m = re.search(r"标签[:：]\s*(.+)", report)
    tags = [t.strip() for t in re.split(r"[,，]", m.group(1))] if m else []
    tags = [t for t in tags if t][:6]
    print(f"[元数据] 标题: {title}\n        标签: {', '.join(tags)}")

    native_public = extract_public_markdown(report, site.private_cutoff)
    if not native_public:
        print("错误: 未提取到公开层。"); return 1

    # 3) Cross-source connections (this is where the paper meets your podcasts).
    slug_guess = slugify(title, DATE)
    candidates = build_candidates(tags, exclude_slug=slug_guess)
    print(f"[关联] 在 {len(candidates)} 期往期中查找呼应/张力 ...")
    connections = find_connections(
        title, extract_claims_section(report), candidates, config, lang="zh"
    )
    for c in connections:
        print(f"        {c.get('kind')}: -> {c.get('slug')} ({c.get('relation')})")
    if not connections:
        print("        (未找到具体到论点级别的关联)")

    # 4) Bilingual: Chinese is the validated native body; translate to English.
    print("[双语] 翻译公开层生成 /en 镜像 ...")
    _, zh_b, en_b = build_bilingual(native_public, title, tags, connections, config)

    slug = slugify(en_b["title"] or zh_b["title"], DATE)
    entry = publish_report(
        report, zh_b["title"], site, date=DATE, slug=slug,
        source_url=source_url, tags=zh_b["tags"], connections=zh_b["connections"],
        en=en_b, primary_public_md=zh_b["body"], kind="paper",
    )

    # 5) Archive the FULL report (incl. personal mapping) locally; gitignored.
    (ROOT / "reports" / f"{entry['slug']}.md").write_text(report, encoding="utf-8")

    # 6) Privacy gate: the published bodies must contain NO private heading.
    leaks = []
    for lang in ("zh", "en"):
        p = (ROOT / "docs" / ("episodes" if lang == "zh" else "en/episodes")
             / f"{entry['slug']}.html")
        if p.exists():
            h = p.read_text(encoding="utf-8")
            leaks += [(lang, head) for head in PRIVATE_HEADINGS if head in h]

    print("\n================ 发布完成(本地,未推送)================")
    print(f"slug: {entry['slug']}")
    print(f"zh 页面: docs/episodes/{entry['slug']}.html")
    print(f"en 页面: docs/en/episodes/{entry['slug']}.html")
    print(f"完整报告(含个人映射,本地): reports/{entry['slug']}.md")
    if leaks:
        print(f"!! 隐私检查失败,发现私人层泄漏: {leaks}")
        return 2
    print("隐私检查: 通过(公开页零私人层泄漏)")
    print("\n下一步: 复核两张页面后,再 git 提交并推送上线。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
