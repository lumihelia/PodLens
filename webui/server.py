"""Local FastAPI server for the PodLens self-service UI.

Runs on 127.0.0.1 only (single user, your machine). Reuses the headless core:
  /interpret  -> run the 3-stage pipeline, return full + public previews
  /publish    -> write the public layers to the site, git commit & push live

Start with the start_ui.command launcher, or:
  uvicorn webui.server:app --host 127.0.0.1 --port 8765
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

import markdown as md
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from podlens.config import load_config
from podlens.interpreter import build_bilingual, find_connections, interpret
from podlens.profile import load_profile
from podlens.publish import (
    _normalize_claims,
    build_candidates,
    extract_claims_section,
    extract_public_markdown,
    get_episode_for_edit,
    list_published,
    load_site_config,
    publish_report,
    slugify,
    update_episode,
)
from podlens.transcript import detect_language, load_transcript
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
    title: str = Form(""),
    source_url: str = Form(""),
    use_profile: bool = Form(True),
    file: UploadFile | None = None,
) -> JSONResponse:
    """Run the full interpretation and return previews (no publishing yet)."""
    title = title.strip()
    source_url = source_url.strip()

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

    # Interpret the PUBLIC layers in the transcript's OWN language (most
    # faithful); the private personal mapping stays in your reading language.
    source_lang = detect_language(transcript)
    try:
        result = interpret(transcript, profile, config, public_lang=source_lang)
    except RuntimeError as exc:
        raise HTTPException(500, f"解读失败:{exc}")

    final_title = title or result.title or "PodLens 解读"
    report_md = result.to_markdown(title=final_title)
    site = load_site_config()
    public_md = extract_public_markdown(report_md, site.private_cutoff)

    # Find cross-episode connections for the user to review/veto (in the same
    # language as this episode's public body, so they translate cleanly).
    slug = slugify(final_title, "")
    candidates = build_candidates(result.tags, exclude_slug=slug)
    cand_titles = {c["slug"]: c["title"] for c in candidates}
    raw_conns = (
        find_connections(final_title, extract_claims_section(report_md),
                         candidates, config, lang=source_lang)
        if candidates else []
    )
    connections = [
        {**c, "title": cand_titles.get(c["slug"], c["slug"])} for c in raw_conns
    ]

    return JSONResponse({
        "report_md": report_md,
        "full_html": md.markdown(_normalize_claims(report_md), extensions=_MD_EXT),
        "public_html": md.markdown(_normalize_claims(public_md), extensions=_MD_EXT),
        "had_profile": result.had_profile,
        "title": final_title,
        "tags": result.tags,
        "connections": connections,
        "cutoff": site.private_cutoff,
    })


@app.post("/publish")
def do_publish(
    report_md: str = Form(...),
    title: str = Form(...),
    source_url: str = Form(""),
    date: str = Form(""),
    tags: str = Form(""),
    connections: str = Form(""),
) -> JSONResponse:
    """Publish the public layers (bilingual), then git commit & push live."""
    config = load_config()
    site = load_site_config()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    conn_list = []
    if connections.strip():
        try:
            conn_list = [c for c in json.loads(connections) if isinstance(c, dict)]
        except json.JSONDecodeError:
            conn_list = []

    native_public = extract_public_markdown(report_md, site.private_cutoff)
    if not native_public:
        raise HTTPException(400, "没找到可公开的内容(检查报告结构)。")
    pub_date = date.strip() or datetime.now().strftime("%Y-%m-%d")
    extra = ""

    try:
        # Native interpretation -> translate the public layer to the other
        # language, so both /episodes and /en/episodes get a faithful page.
        _, zh_b, en_b = build_bilingual(
            native_public, title.strip(), tag_list, conn_list, config
        )
        # Slug from the English title (readable ASCII), stable across languages.
        slug = slugify(en_b["title"] or zh_b["title"], pub_date)
        entry = publish_report(
            report_md, zh_b["title"], site, date=pub_date, slug=slug,
            source_url=source_url.strip() or None,
            tags=zh_b["tags"], connections=zh_b["connections"],
            en=en_b, primary_public_md=zh_b["body"],
        )
    except RuntimeError as exc:
        # Translation/generation failed: publish a single-language version now
        # so nothing is lost; the English mirror can be added later via re-edit.
        try:
            entry = publish_report(
                report_md, title.strip(), site, date=pub_date,
                source_url=source_url.strip() or None,
                tags=tag_list, connections=conn_list,
            )
        except RuntimeError as exc2:
            raise HTTPException(400, f"生成失败:{exc2}")
        extra = f"(注意:翻译这一步没成功,先发了单语版。原因:{exc})"

    # Archive the FULL report (incl. the private personal-mapping layer) locally,
    # so the user can revisit their past mappings. reports/ is gitignored.
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / f"{entry['slug']}.md").write_text(report_md, encoding="utf-8")

    pushed, message = _git_publish(entry["title"])
    url = site.clean_base + f"/episodes/{entry['slug']}.html"
    return JSONResponse({
        "url": url,
        "slug": entry["slug"],
        "pushed": pushed,
        "message": (message + (" " + extra if extra else "")),
    })


@app.get("/episodes")
def do_list_episodes() -> JSONResponse:
    """List already-published episodes for the manage/edit view."""
    return JSONResponse({"episodes": list_published()})


@app.get("/episode/{slug}")
def do_get_episode(slug: str) -> JSONResponse:
    """Return one published episode's editable public body + editor note."""
    data = get_episode_for_edit(slug)
    if data is None:
        raise HTTPException(404, "未找到这一期。")
    site = load_site_config()
    data["public_html"] = md.markdown(_normalize_claims(data["public_md"]), extensions=_MD_EXT)
    data["url"] = site.clean_base + f"/episodes/{slug}.html"
    return JSONResponse(data)


@app.post("/update")
def do_update(
    slug: str = Form(...),
    public_md: str = Form(...),
    editor_note: str = Form(""),
    title: str = Form(""),
    tags: str = Form(""),
) -> JSONResponse:
    """Save edits to an already-published episode, then rebuild + push live.

    You edit the Chinese (primary) body and the From-Helia note; the English
    mirror is re-translated from your edits so both languages stay in sync.
    """
    config = load_config()
    site = load_site_config()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    extra = ""

    # Re-translate the edited public content (body + title + tags + note +
    # existing connections) into the English mirror.
    en_bundle = None
    existing = get_episode_for_edit(slug.strip())
    conns = existing.get("connections", []) if existing else []
    if public_md.strip():
        try:
            _, _, en_bundle = build_bilingual(
                public_md, title.strip(), tag_list, conns, config,
                editor_note=editor_note,
            )
        except RuntimeError as exc:
            extra = f"(英文版这次没更新成:{exc};中文已更新。)"

    try:
        entry = update_episode(
            slug.strip(), site,
            public_md=public_md,
            editor_note=editor_note,
            title=title.strip() or None,
            tags=tag_list,
            en=en_bundle,
        )
    except RuntimeError as exc:
        raise HTTPException(400, f"更新失败:{exc}")

    pushed, message = _git_publish(entry["title"])
    url = site.clean_base + f"/episodes/{entry['slug']}.html"
    return JSONResponse({
        "url": url,
        "slug": entry["slug"],
        "pushed": pushed,
        "message": (message + (" " + extra if extra else "")),
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
