"""Publish a validated episode interpretation from a saved report.

Reads an already-reviewed report (full local report including private mapping),
strips the private layer, finds connections, translates, and publishes as
kind="podcast". Only costs one translation + one connections API call.

Usage:
    .venv/bin/python scripts/publish_episode.py "<youtube_url>"
"""

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

DATE = "2026-06-06"
REPORT_PATH = ROOT / "reports" / "人类数据与机器人学的gpt-3时刻-danfei-xu.md"

PRIVATE_HEADINGS = ["证据锚定洞察", "个人映射", "值得收藏的概念", "待追踪的问题"]


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("用法: publish_episode.py \"<YouTube链接>\"")
        return 1
    source_url = sys.argv[1].strip()

    config = load_config()
    site = load_site_config()

    report = REPORT_PATH.read_text(encoding="utf-8")

    # 1) Title + tags from the report header.
    m_title = re.search(r"^#\s+(.+)$", report, re.M)
    if not m_title:
        print("错误: 报告缺少标题行。"); return 1
    title = m_title.group(1).strip()
    m_tags = re.search(r"标签[:：]\s*(.+)", report)
    tags = [t.strip() for t in re.split(r"[,，]", m_tags.group(1))] if m_tags else []
    tags = [t for t in tags if t][:6]
    print(f"[元数据] 标题: {title}")
    print(f"        标签: {', '.join(tags)}")

    native_public = extract_public_markdown(report, site.private_cutoff)
    if not native_public:
        print("错误: 未提取到公开层。"); return 1

    # 2) Cross-source connections.
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

    # 3) Bilingual: Chinese is the native body; translate to English.
    print("[双语] 翻译公开层生成 /en 镜像 ...")
    _, zh_b, en_b = build_bilingual(native_public, title, tags, connections, config)

    slug = slugify(en_b["title"] or zh_b["title"], DATE)
    entry = publish_report(
        report, zh_b["title"], site, date=DATE, slug=slug,
        source_url=source_url, tags=zh_b["tags"], connections=zh_b["connections"],
        en=en_b, primary_public_md=zh_b["body"], kind="podcast",
    )

    # 4) Archive full report locally (gitignored).
    archived = ROOT / "reports" / f"{entry['slug']}.md"
    if archived != REPORT_PATH:
        archived.write_text(report, encoding="utf-8")

    # 5) Privacy gate.
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
    if leaks:
        print(f"!! 隐私检查失败: {leaks}")
        return 2
    print("隐私检查: 通过")
    print("\n下一步: 复核页面后 git 提交并推送上线。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
