"""Publish public-layer interpretations as a static site + RSS/JSON feed.

This turns PodLens output into a machine-readable, you-owned publishing surface
(per-episode HTML pages + RSS + JSON Feed + sitemap) suitable for GitHub Pages
and discovery/citation by search engines and agents.

PRIVACY: only the PUBLIC layers are ever published. Everything from the
PODLENS_PRIVATE_CUTOFF heading onward (the evidence-grounded insights and
personal mapping) is stripped before rendering and never written to disk in the
site directory. The split is enforced here, not left to the caller.
"""

import hashlib
import html
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import markdown as md

from .youtube import extract_video_id

# A bracketed timestamp like [12:34] or [1:23:45] or a range [00:00-01:04].
# Captures the START time so it can deep-link into the source video.
_TS_RE = re.compile(
    r"\[(\d{1,2}:\d{2}(?::\d{2})?)(?:\s*[-–~]\s*\d{1,2}:\d{2}(?::\d{2})?)?\]"
)

# Site output dir (GitHub Pages can serve from /docs on the main branch).
SITE_DIR = Path("docs")
EPISODES_DIR = SITE_DIR / "episodes"
# Internal source-of-truth manifest (full entries, incl. slug/source_url).
MANIFEST = SITE_DIR / "manifest.json"
# Public JSON Feed (jsonfeed.org), generated from the manifest.
JSONFEED = SITE_DIR / "episodes.json"
# Stored public markdown per episode (outside docs/, so it is committed but
# NOT served). Lets --rebuild-site re-render pages after a domain/brand change.
SOURCES_DIR = Path(".podlens/episodes")

DEFAULT_PRIVATE_CUTOFF = "## 证据锚定洞察"


@dataclass
class SiteConfig:
    base_url: str
    custom_domain: str
    title: str
    description: str
    author: str
    private_cutoff: str

    @property
    def clean_base(self) -> str:
        return self.base_url.rstrip("/")


def load_site_config() -> SiteConfig:
    return SiteConfig(
        base_url=os.getenv("PODLENS_SITE_URL", "https://lumihelia.github.io/PodLens").strip(),
        custom_domain=os.getenv("PODLENS_CUSTOM_DOMAIN", "").strip(),
        title=os.getenv("PODLENS_SITE_TITLE", "PodLens").strip(),
        description=os.getenv("PODLENS_SITE_DESC", "播客的忠实解读。").strip(),
        author=os.getenv("PODLENS_SITE_AUTHOR", "lumihelia").strip(),
        private_cutoff=os.getenv("PODLENS_PRIVATE_CUTOFF", DEFAULT_PRIVATE_CUTOFF).strip(),
    )


# --- Public/private split -----------------------------------------------------

def extract_public_markdown(report_md: str, cutoff_heading: str) -> str:
    """Return only the public portion of a full report.

    Drops the leading report title / metadata blockquote, and everything from
    the cutoff heading (start of the private layers) onward.
    """
    text = report_md.replace("\r\n", "\n")
    # Cut everything from the private cutoff heading onward.
    idx = text.find("\n" + cutoff_heading)
    if idx == -1 and text.startswith(cutoff_heading):
        idx = 0
    if idx != -1:
        text = text[:idx]
    # Start at the first content section heading (drop title + metadata).
    first = text.find("## ")
    if first != -1:
        text = text[first:]
    return text.strip()


def extract_claims_section(md: str) -> str:
    """Return the 核心观点清单 section text (used as a compact claims index)."""
    marker = "## 核心观点清单"
    i = md.find(marker)
    if i == -1:
        return ""
    rest = md[i + len(marker):]
    j = rest.find("\n## ")
    return (rest[:j] if j != -1 else rest).strip()


def build_candidates(this_tags: list[str], exclude_slug: str, limit: int = 8) -> list[dict]:
    """Prior episodes to consider for connections, tag-prefiltered.

    Returns [{slug, title, tags, claims}]. Prefers episodes sharing a tag; if
    none share (small/diverse corpus), falls back to the most recent ones so
    the corpus still gets connected. Capped at `limit` to keep the call bounded.
    """
    items = [it for it in _load_manifest() if it["slug"] != exclude_slug]
    this_set = set(this_tags or [])
    shared = [it for it in items if this_set & set(it.get("tags", []))]
    pool = shared if shared else items
    pool = sorted(pool, key=lambda it: it["date"], reverse=True)[:limit]
    candidates = []
    for it in pool:
        src = SOURCES_DIR / f"{it['slug']}.md"
        claims = extract_claims_section(src.read_text(encoding="utf-8")) if src.exists() else ""
        candidates.append({
            "slug": it["slug"], "title": it["title"],
            "tags": it.get("tags", []), "claims": claims,
        })
    return candidates


# --- Manifest -----------------------------------------------------------------

def _load_manifest() -> list[dict]:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8")).get("items", [])
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _write_manifest(items: list[dict]) -> None:
    MANIFEST.write_text(
        json.dumps({"items": items}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _write_jsonfeed(items: list[dict], site: SiteConfig) -> None:
    # episodes.json is a JSON Feed (jsonfeed.org) for machine consumers.
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": site.title,
        "home_page_url": site.clean_base + "/",
        "feed_url": site.clean_base + "/episodes.json",
        "description": site.description,
        "authors": [{"name": site.author}],
        "items": [
            {
                "id": site.clean_base + f"/episodes/{it['slug']}.html",
                "url": site.clean_base + f"/episodes/{it['slug']}.html",
                "title": it["title"],
                "date_published": it["date"],
                "summary": it.get("summary", ""),
                **({"tags": it["tags"]} if it.get("tags") else {}),
                **({"external_url": it["source_url"]} if it.get("source_url") else {}),
            }
            for it in items
        ],
    }
    JSONFEED.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8")


# --- Slug / summary helpers ---------------------------------------------------

def slugify(title: str, date: str) -> str:
    """URL-safe, stable slug. ASCII titles stay readable; others fall back to a
    date + short hash so non-Latin titles still get a stable, clean URL."""
    ascii_part = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(ascii_part) >= 3:
        return ascii_part[:60]
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return f"{date}-{digest}"


def _ts_to_seconds(ts: str) -> int:
    parts = [int(p) for p in ts.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def _linkify_seek(content_html: str, video_id: str) -> str:
    """Make timestamps seek the in-page player (with a YouTube link as fallback).

    Returns the html unchanged if there is no video to seek.
    """
    if not video_id:
        return content_html

    def repl(m: re.Match) -> str:
        secs = _ts_to_seconds(m.group(1))
        fallback = f"https://www.youtube.com/watch?v={video_id}&t={secs}s"
        return (
            f'<a class="ts" href="{fallback}" target="_blank" rel="noopener" '
            f'onclick="return PL.seek({secs})">{html.escape(m.group(0))}</a>'
        )

    return _TS_RE.sub(repl, content_html)


def _linkify_nav(content_html: str, page_url: str) -> str:
    """Make timestamps link to another episode's page at that time (?t=seconds).

    Used for 往期 points in connections: clicking navigates to the linked
    episode's page, which seeks its own player on load.
    """
    sep = "&" if "?" in page_url else "?"

    def repl(m: re.Match) -> str:
        secs = _ts_to_seconds(m.group(1))
        return (f'<a class="ts" href="{page_url}{sep}t={secs}">'
                f'{html.escape(m.group(0))}</a>')

    return _TS_RE.sub(repl, content_html)


def _video_embed(video_id: str) -> str:
    """A sticky, privacy-enhanced YouTube player + JS for in-page seeking.

    Exposes PL.seek(seconds) for timestamp links, and seeks to ?t=SECONDS on
    page load (used when navigating from a related episode's 往期 timestamp).
    """
    return f"""<div class="player-wrap"><div id="ytplayer"></div></div>
<script>
var PL = (function() {{
  var player, ready = false, pending = null;
  window.onYouTubeIframeAPIReady = function() {{
    player = new YT.Player('ytplayer', {{
      videoId: '{video_id}',
      host: 'https://www.youtube-nocookie.com',
      playerVars: {{playsinline: 1, rel: 0}},
      events: {{onReady: function() {{ ready = true; if (pending != null) {{ var p = pending; pending = null; seek(p); }} }}}}
    }});
  }};
  function seek(s) {{
    if (!ready) {{ pending = s; return false; }}
    player.seekTo(s, true); player.playVideo();
    document.querySelector('.player-wrap').scrollIntoView({{behavior: 'smooth', block: 'start'}});
    return false;
  }}
  var tag = document.createElement('script');
  tag.src = 'https://www.youtube.com/iframe_api';
  document.head.appendChild(tag);
  document.addEventListener('DOMContentLoaded', function() {{
    var t = new URLSearchParams(location.search).get('t');
    if (t) {{ seek(parseInt(t, 10)); }}
  }});
  return {{seek: seek}};
}})();
</script>"""


def _first_sentences(public_md: str, limit: int = 200) -> str:
    """A plain-text summary from the first prose paragraph of the public body."""
    for block in public_md.split("\n\n"):
        b = block.strip()
        if b and not b.startswith("#") and not b.startswith(("-", "*", ">")):
            b = re.sub(r"\s+", " ", b)
            return b[:limit] + ("…" if len(b) > limit else "")
    return ""


# --- HTML rendering (editorial-minimalist, the user's design system) ---------

_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=Playfair+Display:wght@400;500;600;700&"
    'family=Source+Serif+Pro:wght@300;400;500;600&display=swap" rel="stylesheet">'
)

_CSS = """
:root {
  --text: #2C2C2C; --primary: #4C436F; --bg: #F4F3F7; --muted: #9A93B3;
  --border: #D4D0E0; --white: #FFFFFF;
}
* { box-sizing: border-box; }
body {
  font-family: 'Source Serif Pro', serif; color: var(--text);
  background: var(--bg); line-height: 1.75; margin: 0;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 720px; margin: 0 auto; padding: 96px 24px 128px; }
h1, h2, h3 { font-family: 'Playfair Display', serif; color: var(--text); line-height: 1.25; }
h1 { font-size: 2.6rem; font-weight: 600; margin: 0 0 8px; letter-spacing: -0.01em; }
h2 { font-size: 1.5rem; font-weight: 600; margin: 64px 0 16px; }
h3 { font-size: 1.15rem; font-weight: 600; margin: 32px 0 8px; }
p { margin: 0 0 20px; }
a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }
.meta { color: var(--muted); font-size: 0.95rem; margin: 0 0 64px; }
.site-head { margin-bottom: 80px; }
.site-head .tagline { color: var(--muted); font-size: 1.05rem; margin-top: 4px; }
ul, ol { padding-left: 1.4em; }
li { margin: 6px 0; }
.episode-list { list-style: none; padding: 0; }
.episode-list li { margin: 0 0 48px; }
.episode-list .date { color: var(--muted); font-size: 0.9rem; }
.episode-list .title { font-family: 'Playfair Display', serif; font-size: 1.45rem; font-weight: 600; display: block; margin: 4px 0 8px; }
.episode-list .summary { color: #5a5566; }
.foot { margin-top: 96px; color: var(--muted); font-size: 0.85rem; }
.back { display: inline-block; margin-bottom: 48px; color: var(--muted); }
a.ts { color: var(--primary); font-variant-numeric: tabular-nums; white-space: nowrap; text-decoration: none; border-bottom: 1px dotted var(--border); }
a.ts:hover { border-bottom-style: solid; }
.source { color: var(--muted); font-size: 0.95rem; margin: 0 0 24px; }
.player-wrap { position: sticky; top: 0; z-index: 10; background: var(--bg); padding: 12px 0 16px; margin: 0 0 32px; }
.player-wrap > div { position: relative; width: 100%; max-width: 460px; margin: 0 auto; aspect-ratio: 16 / 9; border-radius: var(--radius); overflow: hidden; box-shadow: 0 2px 10px var(--shadow); }
.player-wrap iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 48px; }
.tags span { font-size: 0.85rem; color: var(--primary); background: #EDEBF4; padding: 4px 12px; border-radius: 999px; }
.connections { list-style: none; padding: 0; margin: 0; }
.connections li { margin: 0 0 28px; padding-left: 16px; border-left: 2px solid var(--border); }
.connections .rel { font-size: 0.8rem; color: var(--primary); background: #EDEBF4; padding: 2px 10px; border-radius: 999px; margin-right: 8px; }
.connections .lk { font-family: 'Playfair Display', serif; font-weight: 600; }
.connections .why { margin: 8px 0 6px; }
.connections .pts { color: var(--muted); font-size: 0.92rem; }
.connections .pts > div { margin-top: 4px; }
.connections .who { color: var(--text); font-weight: 600; margin-right: 8px; }
"""


def _page(title: str, body: str, site: SiteConfig, *, description: str,
          canonical: str, is_episode: bool, json_ld: dict | None = None,
          keywords: list[str] | None = None) -> str:
    kw = ""
    if keywords:
        kw = f'<meta name="keywords" content="{html.escape(", ".join(keywords))}">'
    ld = ""
    if json_ld:
        ld = (
            '<script type="application/ld+json">'
            + json.dumps(json_ld, ensure_ascii=False)
            + "</script>"
        )
    feed_link = (
        f'<link rel="alternate" type="application/rss+xml" '
        f'title="{html.escape(site.title)}" href="{site.clean_base}/feed.xml">'
        f'<link rel="alternate" type="application/json" '
        f'title="{html.escape(site.title)}" href="{site.clean_base}/episodes.json">'
    )
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="author" content="{html.escape(site.author)}">
{kw}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'article' if is_episode else 'website'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
{feed_link}
{ld}
{_FONTS}
<style>{_CSS}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


def _ep_url(site: SiteConfig, slug: str) -> str:
    return site.clean_base + f"/episodes/{slug}.html"


def _render_connections(entry: dict, slug_titles: dict, backrefs: list[dict],
                        site: SiteConfig) -> str:
    """Render the bidirectional 与往期的关联 section, or '' if there are none."""
    this_vid = extract_video_id(entry.get("source_url", "") or "")

    def pts(mine: str, theirs: str, other_slug: str) -> str:
        # 本期 timestamps seek the in-page player; 往期 timestamps navigate to
        # the linked episode's page at that time.
        mine_html = _linkify_seek(html.escape(mine), this_vid)
        theirs_html = _linkify_nav(html.escape(theirs), _ep_url(site, other_slug))
        return ('<div class="pts">'
                f'<div><b class="who">本期</b>{mine_html}</div>'
                f'<div><b class="who">往期</b>{theirs_html}</div>'
                '</div>')

    rows = []
    # Forward: this episode (本期) links to a referenced episode (往期).
    for c in entry.get("connections", []):
        title = slug_titles.get(c["slug"])
        if not title:
            continue
        rows.append(
            f'<li><span class="rel">{html.escape(c.get("relation", "关联"))}</span>'
            f'→ <a class="lk" href="{_ep_url(site, c["slug"])}">{html.escape(title)}</a>'
            f'<div class="why">{html.escape(c.get("why", ""))}</div>'
            + pts(c.get("this_point", ""), c.get("that_point", ""), c["slug"]) + "</li>"
        )
    # Back: a later episode linked TO this one. From this page's view, the
    # current episode is 本期 -> that_point; the other is 往期 -> this_point.
    for b in backrefs:
        rows.append(
            f'<li><span class="rel">{html.escape(b.get("relation", "关联"))}</span>'
            f'← <a class="lk" href="{_ep_url(site, b["from_slug"])}">{html.escape(b["from_title"])}</a>'
            f'<div class="why">{html.escape(b.get("why", ""))}</div>'
            + pts(b.get("that_point", ""), b.get("this_point", ""), b["from_slug"]) + "</li>"
        )
    if not rows:
        return ""
    return '<h2>与往期的关联</h2><ul class="connections">' + "".join(rows) + "</ul>"


def render_episode_page(entry: dict, public_md: str, site: SiteConfig,
                        slug_titles: dict | None = None,
                        backrefs: list[dict] | None = None) -> str:
    content_html = md.markdown(public_md, extensions=["extra", "sane_lists"])
    source_url = entry.get("source_url", "")
    video_id = extract_video_id(source_url) if source_url else None
    content_html = _linkify_seek(content_html, video_id or "")
    connections_html = _render_connections(
        entry, slug_titles or {}, backrefs or [], site
    )
    player_html = _video_embed(video_id) if video_id else ""
    canonical = site.clean_base + f"/episodes/{entry['slug']}.html"

    source_line = ""
    if source_url:
        hint = "时间戳可点击,就地跳转播放器" if video_id else ""
        source_line = (
            f'<p class="source">原节目:'
            f'<a href="{html.escape(source_url)}" target="_blank" rel="noopener">'
            f'{html.escape(source_url)}</a>'
            + (f'　·　{hint}' if hint else "") + '</p>'
        )

    tags = entry.get("tags", [])
    tags_line = ""
    if tags:
        chips = "".join(f"<span>{html.escape(t)}</span>" for t in tags)
        tags_line = f'<div class="tags">{chips}</div>'

    json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": entry["title"],
        "datePublished": entry["date"],
        "inLanguage": "zh",
        "url": canonical,
        "description": entry.get("summary", ""),
        "author": {"@type": "Person", "name": site.author},
        "publisher": {"@type": "Person", "name": site.author},
    }
    if tags:
        json_ld["keywords"] = ", ".join(tags)
    if source_url:
        json_ld["isBasedOn"] = source_url

    body = f"""<a class="back" href="{site.clean_base}/">← {html.escape(site.title)}</a>
<h1>{html.escape(entry['title'])}</h1>
<p class="meta">{entry['date']} · 由 PodLens 生成的忠实解读</p>
{source_line}
{player_html}
{tags_line}
{content_html}
{connections_html}
<p class="foot">本页为对节目内容的忠实解读与大白话重述,由 <a href="https://github.com/lumihelia/PodLens">PodLens</a> 生成。</p>
"""
    return _page(
        f"{entry['title']} · {site.title}", body, site,
        description=entry.get("summary", site.description),
        canonical=canonical, is_episode=True, json_ld=json_ld,
        keywords=tags or None,
    )


def render_index(items: list[dict], site: SiteConfig) -> str:
    rows = []
    for it in items:
        url = site.clean_base + f"/episodes/{it['slug']}.html"
        rows.append(
            f'<li><span class="date">{it["date"]}</span>'
            f'<a class="title" href="{url}">{html.escape(it["title"])}</a>'
            f'<span class="summary">{html.escape(it.get("summary", ""))}</span></li>'
        )
    listing = "\n".join(rows) if rows else "<p class='summary'>还没有内容。</p>"
    body = f"""<div class="site-head">
<h1>{html.escape(site.title)}</h1>
<p class="tagline">{html.escape(site.description)}</p>
</div>
<ul class="episode-list">
{listing}
</ul>
<p class="foot">订阅:<a href="{site.clean_base}/feed.xml">RSS</a> · <a href="{site.clean_base}/episodes.json">JSON Feed</a></p>
"""
    return _page(site.title, body, site, description=site.description,
                 canonical=site.clean_base + "/", is_episode=False)


# --- Feeds & sitemap ----------------------------------------------------------

def _rfc822(date_iso: str) -> str:
    try:
        dt = datetime.fromisoformat(date_iso)
    except ValueError:
        dt = datetime.now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def build_rss(items: list[dict], site: SiteConfig) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "<channel>",
        f"<title>{html.escape(site.title)}</title>",
        f"<link>{site.clean_base}/</link>",
        f"<description>{html.escape(site.description)}</description>",
        "<language>zh</language>",
        f'<atom:link href="{site.clean_base}/feed.xml" rel="self" type="application/rss+xml" />',
    ]
    for it in items:
        url = site.clean_base + f"/episodes/{it['slug']}.html"
        parts += [
            "<item>",
            f"<title>{html.escape(it['title'])}</title>",
            f"<link>{url}</link>",
            f'<guid isPermaLink="true">{url}</guid>',
            f"<pubDate>{_rfc822(it['date'])}</pubDate>",
            f"<description>{html.escape(it.get('summary', ''))}</description>",
            *[f"<category>{html.escape(t)}</category>" for t in it.get("tags", [])],
            "</item>",
        ]
    parts += ["</channel>", "</rss>"]
    return "\n".join(parts)


def build_sitemap(items: list[dict], site: SiteConfig) -> str:
    urls = [site.clean_base + "/"] + [
        site.clean_base + f"/episodes/{it['slug']}.html" for it in items
    ]
    body = "\n".join(f"<url><loc>{u}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n"
    )


# --- Orchestration ------------------------------------------------------------

def publish_report(
    report_md: str,
    title: str,
    site: SiteConfig,
    date: str | None = None,
    slug: str | None = None,
    source_url: str | None = None,
    tags: list[str] | None = None,
    connections: list[dict] | None = None,
) -> dict:
    """Add one report's PUBLIC layers to the site and rebuild feeds/index.

    Returns the manifest entry. Idempotent on slug: re-publishing the same slug
    updates that episode in place.
    """
    public_md = extract_public_markdown(report_md, site.private_cutoff)
    if not public_md:
        raise RuntimeError(
            "No public content found. Check that the report has the expected "
            "headings and that PODLENS_PRIVATE_CUTOFF matches."
        )

    date = date or datetime.now().strftime("%Y-%m-%d")
    slug = slug or slugify(title, date)
    prior = next((it for it in _load_manifest() if it["slug"] == slug), {})
    # Keep existing tags if none are supplied this time (e.g. --publish-existing).
    if tags is None:
        tags = prior.get("tags", [])
    if connections is None:
        connections = prior.get("connections", [])
    entry = {"slug": slug, "title": title, "date": date,
             "summary": _first_sentences(public_md),
             "source_url": source_url or prior.get("source_url", ""),
             "tags": tags or [],
             "connections": connections or []}

    # Store the public markdown so the page can be re-rendered on any rebuild.
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    (SOURCES_DIR / f"{slug}.md").write_text(public_md, encoding="utf-8")

    items = [it for it in _load_manifest() if it["slug"] != slug]
    items.insert(0, entry)
    items.sort(key=lambda it: it["date"], reverse=True)

    _rebuild_site(items, site)
    return entry


def _rebuild_site(items: list[dict], site: SiteConfig) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    EPISODES_DIR.mkdir(parents=True, exist_ok=True)
    # Build the connection graph: slug -> title, and back-references (who linked
    # to me). Back-links are DERIVED from forward connections, so they are always
    # consistent and we never have to mutate target entries.
    slug_titles = {it["slug"]: it["title"] for it in items}
    backrefs: dict[str, list[dict]] = {}
    for it in items:
        for conn in it.get("connections", []):
            backrefs.setdefault(conn["slug"], []).append(
                {"from_slug": it["slug"], "from_title": it["title"], **conn}
            )
    # Re-render every episode page from its stored source markdown, so a domain,
    # branding, or connection-graph change propagates to all pages.
    for it in items:
        src = SOURCES_DIR / f"{it['slug']}.md"
        if src.exists():
            (EPISODES_DIR / f"{it['slug']}.html").write_text(
                render_episode_page(
                    it, src.read_text(encoding="utf-8"), site,
                    slug_titles=slug_titles, backrefs=backrefs.get(it["slug"], []),
                ),
                encoding="utf-8",
            )
    _write_manifest(items)
    _write_jsonfeed(items, site)
    (SITE_DIR / "index.html").write_text(render_index(items, site), encoding="utf-8")
    (SITE_DIR / "feed.xml").write_text(build_rss(items, site), encoding="utf-8")
    (SITE_DIR / "sitemap.xml").write_text(build_sitemap(items, site), encoding="utf-8")
    (SITE_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {site.clean_base}/sitemap.xml\n",
        encoding="utf-8",
    )
    # .nojekyll so GitHub Pages serves files as-is (no Jekyll processing).
    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    if site.custom_domain:
        (SITE_DIR / "CNAME").write_text(site.custom_domain + "\n", encoding="utf-8")


def rebuild_from_manifest(site: SiteConfig) -> int:
    """Regenerate index/feeds/sitemap from the existing manifest (no new episode)."""
    items = _load_manifest()
    _rebuild_site(items, site)
    return len(items)
