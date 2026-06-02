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

# Site output dir (GitHub Pages can serve from /docs on the main branch).
SITE_DIR = Path("docs")
EPISODES_DIR = SITE_DIR / "episodes"
MANIFEST = SITE_DIR / "episodes.json"

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


# --- Manifest -----------------------------------------------------------------

def _load_manifest() -> list[dict]:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8")).get("items", [])
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_manifest(items: list[dict], site: SiteConfig) -> None:
    # episodes.json doubles as a JSON Feed (jsonfeed.org) for machine consumers.
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
            }
            for it in items
        ],
    }
    MANIFEST.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8")


# --- Slug / summary helpers ---------------------------------------------------

def slugify(title: str, date: str) -> str:
    """URL-safe, stable slug. ASCII titles stay readable; others fall back to a
    date + short hash so non-Latin titles still get a stable, clean URL."""
    ascii_part = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(ascii_part) >= 3:
        return ascii_part[:60]
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return f"{date}-{digest}"


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
"""


def _page(title: str, body: str, site: SiteConfig, *, description: str,
          canonical: str, is_episode: bool) -> str:
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
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'article' if is_episode else 'website'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
{feed_link}
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


def render_episode_page(entry: dict, public_md: str, site: SiteConfig) -> str:
    content_html = md.markdown(public_md, extensions=["extra", "sane_lists"])
    canonical = site.clean_base + f"/episodes/{entry['slug']}.html"
    body = f"""<a class="back" href="{site.clean_base}/">← {html.escape(site.title)}</a>
<h1>{html.escape(entry['title'])}</h1>
<p class="meta">{entry['date']} · 由 PodLens 生成的忠实解读</p>
{content_html}
<p class="foot">本页为对节目内容的忠实解读与大白话重述,由 <a href="https://github.com/lumihelia/PodLens">PodLens</a> 生成。</p>
"""
    return _page(
        f"{entry['title']} · {site.title}", body, site,
        description=entry.get("summary", site.description),
        canonical=canonical, is_episode=True,
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
) -> dict:
    """Add one report's PUBLIC layers to the site and rebuild feeds/index.

    Returns the manifest entry. Idempotent on slug: re-publishing the same slug
    updates that episode in place.
    """
    EPISODES_DIR.mkdir(parents=True, exist_ok=True)

    public_md = extract_public_markdown(report_md, site.private_cutoff)
    if not public_md:
        raise RuntimeError(
            "No public content found. Check that the report has the expected "
            "headings and that PODLENS_PRIVATE_CUTOFF matches."
        )

    date = date or datetime.now().strftime("%Y-%m-%d")
    slug = slug or slugify(title, date)
    entry = {"slug": slug, "title": title, "date": date,
             "summary": _first_sentences(public_md)}

    (EPISODES_DIR / f"{slug}.html").write_text(
        render_episode_page(entry, public_md, site), encoding="utf-8"
    )

    items = [it for it in _load_manifest() if it["slug"] != slug]
    items.insert(0, entry)
    items.sort(key=lambda it: it["date"], reverse=True)

    _rebuild_site(items, site)
    return entry


def _rebuild_site(items: list[dict], site: SiteConfig) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    _save_manifest(items, site)
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
