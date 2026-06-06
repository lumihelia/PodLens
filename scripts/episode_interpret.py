"""Run the full episode interpretation pipeline from the CLI.

Usage:
    .venv/bin/python scripts/episode_interpret.py <transcript.md>

Output saved to reports/<slug>.md (gitignored, local only).
"""

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.config import load_config
from podlens.interpreter import interpret
from podlens.profile import load_profile


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    capped = s[:60]
    if len(s) > 60:
        capped = capped.rsplit("-", 1)[0]
    return capped


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: episode_interpret.py <transcript.md>"); return 1
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"File not found: {src}"); return 1

    config = load_config()
    if not config.has_api_key:
        print("未配置 GEMINI_API_KEY。"); return 1

    transcript = src.read_text(encoding="utf-8")
    profile = load_profile(config.profile_path)
    print(f"[transcript] {len(transcript)} chars, timestamps={'yes' if '[' in transcript else 'maybe'}")
    print(f"[profile]    {'loaded' if profile else 'none'}")
    print(f"[model]      {config.model}")

    def on_stage(s: str) -> None:
        print(f"  {s}")

    result = interpret(transcript, profile, config, on_stage=on_stage)

    slug = slugify(result.title)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = (
        f"# {result.title}\n\n"
        f"> 模型 {result.model} · {stamp}\n"
        f"> 标签:{', '.join(result.tags)}\n\n"
        f"{result.reconstruction.strip()}\n\n"
        f"{result.plain_language.strip()}\n\n"
        f"{result.mapping.strip()}\n"
    )

    out = ROOT / "reports" / f"{slug}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report, encoding="utf-8")

    print(f"\n================ 结果 ================")
    print(f"标题: {result.title}")
    print(f"标签: {', '.join(result.tags)}")
    print(f"slug: {slug}")
    print(f"完整报告 (含私人层,本地): {out}")

    # Show tension section if present
    if "## 内部张力与自我修正" in result.reconstruction:
        start = result.reconstruction.find("## 内部张力与自我修正")
        end = result.reconstruction.find("\n## ", start + 1)
        section = result.reconstruction[start:end if end != -1 else start + 2000]
        print(f"\n---- 内部张力与自我修正 ----")
        print(section.strip())
    else:
        print("\n[内部张力与自我修正: 本期无，章节省略]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
