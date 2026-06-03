"""Local FastAPI server for the PodLens self-service UI.

Runs on 127.0.0.1 only (single user, your machine). Reuses the headless core:
  /interpret  -> run the 3-stage pipeline, return full + public previews
  /publish    -> write the public layers to the site, git commit & push live

Start with the start_ui.command launcher, or:
  uvicorn webui.server:app --host 127.0.0.1 --port 8765
"""

import subprocess
from datetime import datetime
from pathlib import Path

import markdown as md
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from podlens.config import load_config
from podlens.interpreter import interpret
from podlens.profile import load_profile
from podlens.publish import (
    extract_public_markdown,
    load_site_config,
    publish_report,
)
from podlens.transcript import load_transcript
from podlens.youtube import fetch_transcript, is_youtube_url

ROOT = Path(__file__).resolve().parent.parent
STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="PodLens")

_MD_EXT = ["extra", "sane_lists"]


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.post("/interpret")
async def do_interpret(
    title: str = Form(...),
    source_url: str = Form(""),
    use_profile: bool = Form(True),
    file: UploadFile | None = None,
) -> JSONResponse:
    """Run the full interpretation and return previews (no publishing yet)."""
    title = title.strip()
    source_url = source_url.strip()
    if not title:
        raise HTTPException(400, "请填写标题。")

    # Obtain the transcript: uploaded file first, else a YouTube URL.
    if file is not None and file.filename:
        raw = (await file.read()).decode("utf-8", errors="replace")
        transcript = load_transcript(raw)
    elif source_url and is_youtube_url(source_url):
        try:
            transcript = fetch_transcript(source_url)
        except RuntimeError as exc:
            raise HTTPException(400, f"抓取字幕失败:{exc}")
    else:
        raise HTTPException(400, "请上传字幕文件,或提供一个 YouTube 链接。")

    if not transcript.strip():
        raise HTTPException(400, "字幕内容为空。")

    config = load_config()
    if not config.has_api_key:
        raise HTTPException(400, "未配置 GEMINI_API_KEY(检查 .env)。")
    profile = load_profile(config.profile_path) if use_profile else None

    try:
        result = interpret(transcript, profile, config)
    except RuntimeError as exc:
        raise HTTPException(500, f"解读失败:{exc}")

    report_md = result.to_markdown(title=title)
    site = load_site_config()
    public_md = extract_public_markdown(report_md, site.private_cutoff)

    return JSONResponse({
        "report_md": report_md,
        "full_html": md.markdown(report_md, extensions=_MD_EXT),
        "public_html": md.markdown(public_md, extensions=_MD_EXT),
        "had_profile": result.had_profile,
        "cutoff": site.private_cutoff,
    })


@app.post("/publish")
def do_publish(
    report_md: str = Form(...),
    title: str = Form(...),
    source_url: str = Form(""),
    date: str = Form(""),
) -> JSONResponse:
    """Publish the public layers, then git commit & push the site live."""
    site = load_site_config()
    try:
        entry = publish_report(
            report_md, title.strip(), site,
            date=date.strip() or None,
            source_url=source_url.strip() or None,
        )
    except RuntimeError as exc:
        raise HTTPException(400, f"生成失败:{exc}")

    pushed, message = _git_publish(entry["title"])
    url = site.clean_base + f"/episodes/{entry['slug']}.html"
    return JSONResponse({
        "url": url,
        "slug": entry["slug"],
        "pushed": pushed,
        "message": message,
    })


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True
    )


def _git_publish(title: str) -> tuple[bool, str]:
    """Commit docs/ + .podlens/ and push. Returns (pushed, message)."""
    _git("add", "docs", ".podlens")
    status = _git("status", "--porcelain", "docs", ".podlens")
    if not status.stdout.strip():
        return False, "没有新内容需要提交(可能这一期已发布过)。"
    commit = _git("commit", "-m", f"Publish: {title}")
    if commit.returncode != 0:
        return False, f"git commit 失败:{commit.stderr.strip()[:200]}"
    push = _git("push", "origin", "main")
    if push.returncode != 0:
        return False, (
            "已在本地生成并提交,但推送失败(检查网络/凭据):"
            f"{push.stderr.strip()[:200]}"
        )
    return True, "已发布并推送上线。几分钟后 GitHub Pages 会更新。"
