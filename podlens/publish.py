"""Publish public-layer interpretations as a static site + RSS/JSON feed.

This turns PodLens output into a machine-readable, you-owned publishing surface
(per-episode HTML pages + RSS + JSON Feed + sitemap) suitable for GitHub Pages
and discovery/citation by search engines and agents.

Bilingual: the site is rendered in TWO language trees -- Chinese at the root
(/episodes/<slug>.html) and English under /en/ (/en/episodes/<slug>.html) --
linked by a visible switch and hreflang. Each episode is interpreted in its own
source language first (most faithful) and translated to the other; both bodies
are stored, and pages are re-rendered from those stored sources on every build.

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
EN_DIR = SITE_DIR / "en"
EN_EPISODES_DIR = EN_DIR / "episodes"
# Internal source-of-truth manifest (full entries, incl. slug/source_url/i18n).
MANIFEST = SITE_DIR / "manifest.json"
# Public JSON Feed (jsonfeed.org), generated from the manifest.
JSONFEED = SITE_DIR / "episodes.json"
# Stored public markdown per episode (outside docs/, so it is committed but
# NOT served). zh body at <slug>.md, en body at <slug>.en.md. Lets a rebuild
# re-render pages after a domain/brand/translation change.
SOURCES_DIR = Path(".podlens/episodes")

DEFAULT_PRIVATE_CUTOFF = "## 证据锚定洞察"

LANGS = ("zh", "en")

# The interpretation prompts hard-code a Chinese scaffold (section headers, the
# per-claim labels, and the type-tag vocabulary), so an episode interpreted
# natively in English still carries those Chinese labels around English prose.
# On the English tree we normalize the known scaffold terms to English at render
# time (deterministic, no API). Translated-from-Chinese bodies don't contain
# these exact tokens, so the replacements are simply no-ops there.
# Ordered longest/most-specific FIRST (so 核心观点清单 is handled before 核心观点,
# and 核心观点 before 观点).
_EN_TERMS = {
    "主持人追问": "Host prompt",
    "这期讲了什么": "What This Episode Covers",
    "时间线主题地图": "Timeline & Topic Map",
    "核心观点清单": "Key Claims",
    "值得精听的片段": "Worth a Second Listen",
    "大白话重讲": "In Plain Language",
    "不确定性": "Uncertainty",
    "核心观点": "Claim",
    "证据": "Evidence",
    "类型": "Type",
    "标签": "Type",
    "观点": "Opinion",
    "事实": "Fact",
    "例子": "Example",
    "预测": "Prediction",
    "猜想": "Speculation",
    "注": "Note",
}


def _englishize(text: str) -> str:
    for zh, en in _EN_TERMS.items():
        text = text.replace(zh, en)
    return text


# The model formats each Key Claim as an empty "N." line followed by nested
# "- **label:** value" bullets, which Markdown renders as a run-on blob. Reflow
# each claim into a clean numbered item: the claim as the item text, evidence /
# type / uncertainty as muted meta lines. Deterministic, no API. Runs BEFORE
# _englishize, and emits CANONICAL Chinese meta labels (证据/类型) so _englishize
# turns them into English on the en tree.
#
# The model is wildly inconsistent about the labels, so the parser is permissive:
# bold or not, half/full-width colon, colon inside or outside the **, and a
# vocabulary that varies per episode (观点/核心观点, 证据/锚点, 类型/标签) and even
# switches to English on the en body (Claim/Anchor/Type). We classify by meaning.
_CLAIM_NUM_RE = re.compile(r"^\s*(\d+)\.\s*(.*)$")
_CLAIM_BARE_NUM_RE = re.compile(r"^\s*\d+\.\s*$")
# bullet, optional **, label (no colon/star), optional **, colon, optional **, value
_CLAIM_FIELD_RE = re.compile(
    r"^\s*[-*]\s*\*{0,2}\s*([^:：*]+?)\s*\*{0,2}\s*[:：]\s*\*{0,2}\s*(.*)$"
)

_CLAIM_LABELS = {"观点", "核心观点", "主张", "论点", "claim", "point", "key claim"}
_EVIDENCE_LABELS = {"证据", "锚点", "依据", "出处", "来源", "evidence", "anchor", "source"}
_TYPE_LABELS = {"类型", "标签", "type", "tag"}
_UNCERTAINTY_LABELS = {"不确定性", "不确定", "注", "备注", "note", "uncertainty", "caveat"}


def _classify_label(label: str) -> str:
    l = label.strip().lower()
    if l in _CLAIM_LABELS:
        return "claim"
    if l in _EVIDENCE_LABELS:
        return "evidence"
    if l in _TYPE_LABELS:
        return "type"
    if l in _UNCERTAINTY_LABELS:
        return "uncertainty"
    return "other"


def _normalize_claims(public_md: str) -> str:
    marker = "## 核心观点清单"
    i = public_md.find(marker)
    if i == -1:
        return public_md
    j = public_md.find("\n## ", i + len(marker))
    section = public_md[i:j] if j != -1 else public_md[i:]
    lines = section.split("\n")[1:]  # skip the heading line
    # Only reflow the broken bare-number / labeled-bullet structure; leave
    # already-clean "N. text" sections untouched.
    has_bare = any(_CLAIM_BARE_NUM_RE.match(ln) for ln in lines)
    has_field = any(_CLAIM_FIELD_RE.match(ln) for ln in lines)
    if not (has_bare or has_field):
        return public_md

    claims: list[dict] = []
    cur: dict | None = None
    for ln in lines:
        fm = _CLAIM_FIELD_RE.match(ln)
        nm = _CLAIM_NUM_RE.match(ln)
        if nm and not fm:
            if cur:
                claims.append(cur)
            cur = {"text": nm.group(2).strip(), "ev": "", "type": "", "extra": []}
        elif fm:
            label, val = fm.group(1).strip(), fm.group(2).strip()
            kind = _classify_label(label)
            if cur is None:
                cur = {"text": "", "ev": "", "type": "", "extra": []}
            if kind == "claim":
                cur["text"] = (cur["text"] + " " + val).strip() if cur["text"] else val
            elif kind == "evidence":
                cur["ev"] = (cur["ev"] + ", " + val).strip(", ") if cur["ev"] else val
            elif kind == "type":
                cur["type"] = val
            elif kind == "uncertainty":
                if val:
                    cur["extra"].append(f"不确定性 {val}")
            elif val:
                cur["extra"].append(f"{label} {val}")
        elif cur is not None and ln.strip():
            cur["text"] = (cur["text"] + " " + ln.strip()).strip()
    if cur:
        claims.append(cur)
    if not claims:
        return public_md

    out = [marker, ""]
    for n, c in enumerate(claims, 1):
        out.append(f"{n}. {c['text']}".rstrip())
        # Each piece of evidence/type/uncertainty on its OWN line (a dot-joined
        # single line reads as cramped, especially with a long uncertainty note).
        meta = []
        if c["ev"]:
            meta.append(f"证据 {c['ev']}")
        if c["type"]:
            meta.append(f"类型 {c['type']}")
        meta += c["extra"]
        for k, piece in enumerate(meta):
            cls = "claim-meta claim-meta-first" if k == 0 else "claim-meta"
            out.append(f'   <span class="{cls}">{piece}</span>')
        out.append("")
    new_section = "\n".join(out).rstrip() + "\n"
    after = public_md[j:] if j != -1 else ""
    return public_md[:i] + new_section + after


# Connection relation labels: the connections prompt offers a Chinese vocabulary,
# so en-native episodes can carry a Chinese relation word with English text.
# Map the known labels to English on the English tree (no-op on translated bodies
# that already produced English labels).
_EN_RELATIONS = {
    "承接": "Follows on", "延伸": "Extends", "同构": "Parallel",
    "印证": "Corroborates", "补充": "Complements", "对照": "Contrast",
    "张力": "Tension", "关联": "Related", "反驳": "Refutes", "矛盾": "Contradicts",
}


def _rel_label(label: str, lang: str) -> str:
    if lang == "en":
        return _EN_RELATIONS.get(label, label)
    return label


@dataclass
class SiteConfig:
    base_url: str
    custom_domain: str
    title: str
    description: str
    description_en: str
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
        description=os.getenv("PODLENS_SITE_DESC", "解读有据,出处可查。").strip(),
        description_en=os.getenv(
            "PODLENS_SITE_DESC_EN", "Grounded readings, every point traceable to the source."
        ).strip(),
        author=os.getenv("PODLENS_SITE_AUTHOR", "lumihelia").strip(),
        private_cutoff=os.getenv("PODLENS_PRIVATE_CUTOFF", DEFAULT_PRIVATE_CUTOFF).strip(),
    )


# --- Localized UI strings -----------------------------------------------------

_UI = {
    "zh": {
        "html_lang": "zh-Hans",
        "switch_to": "English",
        "by_line": "由 PodLens 生成的忠实解读",
        "source": "原节目:",
        "seek_hint": "时间戳可点击,就地跳转播放器",
        "related": "与往期的关联",
        "resonance_heading": "与往期的呼应",
        "tension_heading": "与往期的张力",
        "conflict_genuine": "真冲突",
        "conflict_apparent": "表面张力",
        "this_ep": "本期",
        "related_ep": "往期",
        "default_rel": "关联",
        "foot": ('本页为对节目内容的忠实解读与大白话重述,由 '
                 '<a href="https://github.com/lumihelia/PodLens">PodLens</a> 生成。'),
        "subscribe": "订阅:",
        "empty": "还没有内容。",
        "disclaimer": ("这是以原文为依据的一次解读,不能替代原文。每条要点都标注了出处,"
                       "欢迎回到原文核对——也欢迎指出任何细微的偏差。"),
    },
    "en": {
        "html_lang": "en",
        "switch_to": "中文",
        "by_line": "A faithful, transcript-grounded reading by PodLens",
        "source": "Original episode:",
        "seek_hint": "Timestamps are clickable — they seek the player in place",
        "related": "Related episodes",
        "resonance_heading": "Resonances with past episodes",
        "tension_heading": "Tensions with past episodes",
        "conflict_genuine": "Direct conflict",
        "conflict_apparent": "Apparent tension",
        "this_ep": "This",
        "related_ep": "Related",
        "default_rel": "related",
        "foot": ('A faithful reconstruction and plain-language retelling of the '
                 'episode, generated by '
                 '<a href="https://github.com/lumihelia/PodLens">PodLens</a>.'),
        "subscribe": "Subscribe:",
        "empty": "Nothing published yet.",
        "disclaimer": ("This is one source-grounded reading, not a replacement for the "
                       "original. Every point is anchored to its source, so you can check "
                       "it yourself — and corrections are welcome."),
    },
}


# Paper-flavored overrides: a paper is not an "episode", so a few labels change.
# Everything else (layout, bilingual, feeds, connections) is shared with podcasts.
_PAPER_UI = {
    "zh": {
        "source": "原文:",
        "foot": ('本页为对论文内容的忠实解读与大白话重述,由 '
                 '<a href="https://github.com/lumihelia/PodLens">PodLens</a> 生成。'),
    },
    "en": {
        "source": "Source paper:",
        "foot": ('A faithful reading and plain-language retelling of the paper, '
                 'generated by '
                 '<a href="https://github.com/lumihelia/PodLens">PodLens</a>.'),
    },
}


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


def extract_claims_section(md_text: str) -> str:
    """Return the 核心观点清单 section text (used as a compact claims index)."""
    marker = "## 核心观点清单"
    i = md_text.find(marker)
    if i == -1:
        return ""
    rest = md_text[i + len(marker):]
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


# --- Per-language episode view ------------------------------------------------

def _episode_view(entry: dict, lang: str) -> dict | None:
    """The display fields for one episode in `lang`, or None if absent.

    zh is the primary tree (flat fields). en lives under entry['i18n']['en'].
    """
    if lang == "zh":
        return {
            "title": entry["title"],
            "tags": entry.get("tags", []),
            "summary": entry.get("summary", ""),
            "editor_note": entry.get("editor_note", ""),
            "connections": entry.get("connections", []),
        }
    data = (entry.get("i18n", {}) or {}).get(lang)
    if not data:
        return None
    return {
        "title": data.get("title") or entry["title"],
        "tags": data.get("tags", entry.get("tags", [])),
        "summary": data.get("summary", ""),
        "editor_note": data.get("editor_note", ""),
        "connections": data.get("connections", []),
    }


def _en_entry_data(en: dict) -> dict:
    """Normalize a translated en bundle into the stored i18n['en'] shape."""
    return {
        "title": str(en.get("title", "")).strip(),
        "tags": [str(t).strip() for t in en.get("tags", []) if str(t).strip()],
        "summary": _englishize(_first_sentences(en.get("body", ""))),
        "editor_note": str(en.get("editor_note", "")).strip(),
        "connections": [
            {"slug": c.get("slug", ""), "kind": c.get("kind", "resonance"),
             "conflict_type": c.get("conflict_type", ""),
             "relation": c.get("relation", ""), "why": c.get("why", ""),
             "this_point": c.get("this_point", ""), "that_point": c.get("that_point", "")}
            for c in en.get("connections", [])
        ],
    }


def _body_path(slug: str, lang: str) -> Path:
    return SOURCES_DIR / (f"{slug}.md" if lang == "zh" else f"{slug}.{lang}.md")


# --- JSON Feed ----------------------------------------------------------------

def _write_jsonfeed(items: list[dict], site: SiteConfig, lang: str, path: Path) -> None:
    # A JSON Feed (jsonfeed.org) for machine consumers, per language.
    desc = site.description if lang == "zh" else site.description_en
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": site.title,
        "language": _UI[lang]["html_lang"],
        "home_page_url": _index_url(site, lang),
        "feed_url": _index_url(site, lang) + "episodes.json",
        "description": desc,
        "authors": [{"name": site.author}],
        "items": [],
    }
    for it in items:
        v = _episode_view(it, lang) or _episode_view(it, "zh")
        url = _ep_url(site, it["slug"], lang)
        feed["items"].append({
            "id": url,
            "url": url,
            "title": v["title"],
            "date_published": it["date"],
            "summary": v.get("summary", ""),
            **({"tags": v["tags"]} if v.get("tags") else {}),
            **({"external_url": it["source_url"]} if it.get("source_url") else {}),
        })
    path.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8")


# --- Slug / summary helpers ---------------------------------------------------

def slugify(title: str, date: str) -> str:
    """URL-safe, stable slug. ASCII titles stay readable; others fall back to a
    date + short hash so non-Latin titles still get a stable, clean URL."""
    ascii_part = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(ascii_part) >= 3:
        if len(ascii_part) <= 60:
            return ascii_part
        # Cut at the last word boundary so a slug never ends mid-word ("human-da").
        capped = ascii_part[:60]
        if "-" in capped:
            capped = capped.rsplit("-", 1)[0]
        return capped.rstrip("-")
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
    return f"""<div class="player-wrap"><div class="player-box"><div id="ytplayer"></div></div></div>
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


_MD_MARK_RE = re.compile(r"[*_`]+")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


def _first_sentences(public_md: str, limit: int = 200) -> str:
    """A clean plain-text summary from the first real prose line of the body.

    Skips headings and list scaffolding, and strips inline Markdown so the
    summary never shows raw `**` / list markers / `[text](url)` on the index,
    meta description, JSON-LD, or feeds.
    """
    for raw in public_md.split("\n"):
        line = raw.strip()
        if not line or line.startswith(("#", ">")):
            continue
        # Strip up to two leading list markers (handles "2. - foo").
        for _ in range(2):
            line = _LIST_PREFIX_RE.sub("", line)
        line = _MD_LINK_RE.sub(r"\1", line)          # [text](url) -> text
        line = _MD_MARK_RE.sub("", line)             # drop * _ ` emphasis marks
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 12:
            return line[:limit] + ("…" if len(line) > limit else "")
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
  --border: #D4D0E0; --white: #FFFFFF; --radius: 12px; --shadow: rgba(76,67,111,0.08);
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
.disclaimer { margin-top: 16px; color: var(--muted); font-size: 0.82rem; line-height: 1.7; font-style: italic; opacity: 0.85; }
.index-disclaimer { margin: 48px 0 0; color: var(--muted); font-size: 0.82rem; line-height: 1.7; font-style: italic; opacity: 0.85; }
.topbar { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 48px; }
.back { color: var(--muted); }
.langswitch { color: var(--muted); font-size: 0.9rem; border: 1px solid var(--border); padding: 4px 12px; border-radius: 999px; }
.langswitch:hover { color: var(--primary); border-color: var(--primary); text-decoration: none; }
a.ts { color: var(--primary); font-variant-numeric: tabular-nums; white-space: nowrap; text-decoration: none; border-bottom: 1px dotted var(--border); }
a.ts:hover { border-bottom-style: solid; }
.source { color: var(--muted); font-size: 0.95rem; margin: 0 0 24px; }
.player-wrap { position: sticky; top: 0; z-index: 10; background: var(--bg); padding: 12px 0 16px; margin: 0 0 32px; }
.player-box { position: relative; width: 100%; max-width: 460px; margin: 0 auto; aspect-ratio: 16 / 9; border-radius: var(--radius); overflow: hidden; box-shadow: 0 2px 10px var(--shadow); }
.player-box #ytplayer, .player-box iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
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
.connections.tensions li { border-left-color: var(--primary); }
.ctype { font-size: 0.72rem; padding: 1px 9px; border-radius: 999px; margin-right: 8px; letter-spacing: 0.02em; }
.ctype-genuine { color: #fff; background: var(--primary); }
.ctype-apparent { color: var(--muted); background: #EDEBF4; }
.editor-note { background: #EDEBF4; border-radius: 12px; padding: 24px 28px; margin: 0 0 48px; }
.editor-note .en-label { font-family: 'Playfair Display', serif; font-weight: 600; color: var(--primary); font-size: 0.85rem; letter-spacing: 0.08em; margin-bottom: 10px; }
.editor-note p { margin: 0 0 12px; }
.editor-note p:last-child { margin-bottom: 0; }
.claim-meta { display: block; margin-top: 2px; color: var(--muted); font-size: 0.9rem; line-height: 1.6; }
.claim-meta-first { margin-top: 8px; }
.claim-meta a.ts { color: var(--muted); }
"""


def _page(title: str, body: str, site: SiteConfig, *, description: str,
          canonical: str, is_episode: bool, lang: str = "zh",
          json_ld: dict | None = None, keywords: list[str] | None = None,
          head_extra: str = "") -> str:
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
    feed_index = _index_url(site, lang)
    feed_link = (
        f'<link rel="alternate" type="application/rss+xml" '
        f'title="{html.escape(site.title)}" href="{feed_index}feed.xml">'
        f'<link rel="alternate" type="application/json" '
        f'title="{html.escape(site.title)}" href="{feed_index}episodes.json">'
    )
    return f"""<!DOCTYPE html>
<html lang="{_UI[lang]['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="author" content="{html.escape(site.author)}">
{kw}
<link rel="canonical" href="{canonical}">
{head_extra}
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


def _index_url(site: SiteConfig, lang: str) -> str:
    return site.clean_base + ("/en/" if lang == "en" else "/")


def _ep_url(site: SiteConfig, slug: str, lang: str = "zh",
            en_slugs: set | None = None) -> str:
    """Episode page URL in `lang`. For en, fall back to the zh page when the
    target has no English version (so cross-links never 404)."""
    use_en = lang == "en" and (en_slugs is None or slug in en_slugs)
    prefix = "/en" if use_en else ""
    return site.clean_base + f"{prefix}/episodes/{slug}.html"


def _hreflang_links(zh_url: str, en_url: str) -> str:
    return (
        f'<link rel="alternate" hreflang="zh-Hans" href="{zh_url}">'
        f'<link rel="alternate" hreflang="en" href="{en_url}">'
        f'<link rel="alternate" hreflang="x-default" href="{zh_url}">'
    )


def _render_connections(view: dict, slug_titles: dict, backrefs: list[dict],
                        site: SiteConfig, entry: dict, lang: str,
                        en_slugs: set) -> str:
    """Render the bidirectional related-episodes section, or '' if none."""
    ui = _UI[lang]
    this_vid = extract_video_id(entry.get("source_url", "") or "")

    def pts(mine: str, theirs: str, other_slug: str) -> str:
        mine_html = _linkify_seek(html.escape(mine), this_vid)
        theirs_html = _linkify_nav(
            html.escape(theirs), _ep_url(site, other_slug, lang, en_slugs)
        )
        return ('<div class="pts">'
                f'<div><b class="who">{ui["this_ep"]}</b>{mine_html}</div>'
                f'<div><b class="who">{ui["related_ep"]}</b>{theirs_html}</div>'
                '</div>')

    def row(conn: dict, arrow: str, other_slug: str, other_title: str,
            mine: str, theirs: str) -> str:
        rel = _rel_label(conn.get("relation", "") or ui["default_rel"], lang)
        ctype = conn.get("conflict_type", "") if conn.get("kind") == "tension" else ""
        ctype_html = ""
        if ctype in ("genuine", "apparent"):
            ctype_html = (f'<span class="ctype ctype-{ctype}">'
                          f'{ui["conflict_" + ctype]}</span>')
        return (
            f'<li><span class="rel">{html.escape(rel)}</span>{ctype_html}'
            f'{arrow} <a class="lk" href="{_ep_url(site, other_slug, lang, en_slugs)}">'
            f'{html.escape(other_title)}</a>'
            f'<div class="why">{html.escape(conn.get("why", ""))}</div>'
            + pts(mine, theirs, other_slug) + "</li>"
        )

    resonance: list[str] = []
    tension: list[str] = []

    def bucket(conn: dict) -> list[str]:
        return tension if conn.get("kind") == "tension" else resonance

    # Forward: this episode (本期) links to a referenced episode (往期).
    for c in view.get("connections", []):
        title = slug_titles.get(c["slug"])
        if not title:
            continue
        bucket(c).append(
            row(c, "→", c["slug"], title,
                c.get("this_point", ""), c.get("that_point", ""))
        )
    # Back: a later episode linked TO this one. From this page's view, the
    # current episode is 本期 -> that_point; the other is 往期 -> this_point.
    for b in backrefs:
        bucket(b).append(
            row(b, "←", b["from_slug"], b["from_title"],
                b.get("that_point", ""), b.get("this_point", ""))
        )

    out = ""
    if resonance:
        out += (f'<h2>{ui["resonance_heading"]}</h2>'
                '<ul class="connections">' + "".join(resonance) + "</ul>")
    if tension:
        out += (f'<h2>{ui["tension_heading"]}</h2>'
                '<ul class="connections tensions">' + "".join(tension) + "</ul>")
    return out


def render_episode_page(entry: dict, public_md: str, site: SiteConfig,
                        lang: str = "zh", slug_titles: dict | None = None,
                        backrefs: list[dict] | None = None,
                        has_sibling: bool = False,
                        en_slugs: set | None = None) -> str:
    ui = _UI[lang]
    # A paper rides the same pipeline as a podcast; only a few labels differ.
    kind = entry.get("kind", "podcast")
    pui = _PAPER_UI[lang] if kind == "paper" else {}
    source_label = pui.get("source", ui["source"])
    foot_text = pui.get("foot", ui["foot"])
    en_slugs = en_slugs or set()
    view = _episode_view(entry, lang) or _episode_view(entry, "zh")
    # Reflow the Key Claims list first (matches the Chinese field labels), then
    # translate labels to English on the en tree.
    public_md = _normalize_claims(public_md)
    if lang == "en":
        public_md = _englishize(public_md)
    content_html = md.markdown(public_md, extensions=["extra", "sane_lists"])
    source_url = entry.get("source_url", "")
    video_id = extract_video_id(source_url) if source_url else None
    content_html = _linkify_seek(content_html, video_id or "")
    connections_html = _render_connections(
        view, slug_titles or {}, backrefs or [], site, entry, lang, en_slugs
    )
    player_html = _video_embed(video_id) if video_id else ""
    canonical = _ep_url(site, entry["slug"], lang)

    # Language switch + hreflang (only when the sibling page actually exists).
    zh_url = _ep_url(site, entry["slug"], "zh")
    en_url = _ep_url(site, entry["slug"], "en")
    switch_html = ""
    head_extra = ""
    if lang == "en":
        # An en page always has a zh sibling (en is only created alongside zh).
        switch_html = f'<a class="langswitch" href="{zh_url}">{ui["switch_to"]}</a>'
        head_extra = _hreflang_links(zh_url, en_url)
    elif has_sibling:
        switch_html = f'<a class="langswitch" href="{en_url}">{ui["switch_to"]}</a>'
        head_extra = _hreflang_links(zh_url, en_url)

    source_line = ""
    if source_url:
        hint = ui["seek_hint"] if video_id else ""
        source_line = (
            f'<p class="source">{source_label}'
            f'<a href="{html.escape(source_url)}" target="_blank" rel="noopener">'
            f'{html.escape(source_url)}</a>'
            + (f'　·　{hint}' if hint else "") + '</p>'
        )

    tags = view.get("tags", [])
    tags_line = ""
    if tags:
        chips = "".join(f"<span>{html.escape(t)}</span>" for t in tags)
        tags_line = f'<div class="tags">{chips}</div>'

    # Async human editor's note ("From Helia"): a distinct voice set apart from
    # the AI interpretation that follows. Markdown. Blank by default.
    note = (view.get("editor_note", "") or "").strip()
    note_html = ""
    if note:
        note_body = md.markdown(note, extensions=["extra", "sane_lists"])
        note_html = (
            '<div class="editor-note"><div class="en-label">From Helia</div>'
            f"{note_body}</div>"
        )

    json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": view["title"],
        "datePublished": entry["date"],
        "inLanguage": _UI[lang]["html_lang"],
        "url": canonical,
        "description": view.get("summary", ""),
        "author": {"@type": "Person", "name": site.author},
        "publisher": {"@type": "Person", "name": site.author},
    }
    if tags:
        json_ld["keywords"] = ", ".join(tags)
    if source_url:
        json_ld["isBasedOn"] = source_url

    body = f"""<div class="topbar"><a class="back" href="{_index_url(site, lang)}">← {html.escape(site.title)}</a>{switch_html}</div>
<h1>{html.escape(view['title'])}</h1>
<p class="meta">{entry['date']} · {ui['by_line']}</p>
{source_line}
{player_html}
{tags_line}
{note_html}
{content_html}
{connections_html}
<p class="foot">{foot_text}</p>
<p class="disclaimer">{ui['disclaimer']}</p>
"""
    return _page(
        f"{view['title']} · {site.title}", body, site,
        description=view.get("summary", "") or (
            site.description if lang == "zh" else site.description_en),
        canonical=canonical, is_episode=True, lang=lang, json_ld=json_ld,
        keywords=tags or None, head_extra=head_extra,
    )


def render_index(items: list[dict], site: SiteConfig, lang: str = "zh") -> str:
    ui = _UI[lang]
    description = site.description if lang == "zh" else site.description_en
    rows = []
    for it in items:
        v = _episode_view(it, lang) or _episode_view(it, "zh")
        url = _ep_url(site, it["slug"], lang)
        rows.append(
            f'<li><span class="date">{it["date"]}</span>'
            f'<a class="title" href="{url}">{html.escape(v["title"])}</a>'
            f'<span class="summary">{html.escape(v.get("summary", ""))}</span></li>'
        )
    listing = "\n".join(rows) if rows else f"<p class='summary'>{ui['empty']}</p>"

    # Language switch to the other index (root <-> /en/).
    other = "en" if lang == "zh" else "zh"
    switch_html = (
        f'<a class="langswitch" href="{_index_url(site, other)}">{ui["switch_to"]}</a>'
    )
    feed_index = _index_url(site, lang)
    body = f"""<div class="topbar"><span></span>{switch_html}</div>
<div class="site-head">
<h1>{html.escape(site.title)}</h1>
<p class="tagline">{html.escape(description)}</p>
</div>
<ul class="episode-list">
{listing}
</ul>
<p class="index-disclaimer">{ui['disclaimer']}</p>
<p class="foot">{ui['subscribe']}<a href="{feed_index}feed.xml">RSS</a> · <a href="{feed_index}episodes.json">JSON Feed</a></p>
"""
    return _page(site.title, body, site, description=description,
                 canonical=feed_index, is_episode=False, lang=lang)


# --- Feeds & sitemap ----------------------------------------------------------

def _rfc822(date_iso: str) -> str:
    try:
        dt = datetime.fromisoformat(date_iso)
    except ValueError:
        dt = datetime.now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def build_rss(items: list[dict], site: SiteConfig, lang: str = "zh") -> str:
    desc = site.description if lang == "zh" else site.description_en
    feed_index = _index_url(site, lang)
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "<channel>",
        f"<title>{html.escape(site.title)}</title>",
        f"<link>{feed_index}</link>",
        f"<description>{html.escape(desc)}</description>",
        f"<language>{_UI[lang]['html_lang']}</language>",
        f'<atom:link href="{feed_index}feed.xml" rel="self" type="application/rss+xml" />',
    ]
    for it in items:
        v = _episode_view(it, lang) or _episode_view(it, "zh")
        url = _ep_url(site, it["slug"], lang)
        parts += [
            "<item>",
            f"<title>{html.escape(v['title'])}</title>",
            f"<link>{url}</link>",
            f'<guid isPermaLink="true">{url}</guid>',
            f"<pubDate>{_rfc822(it['date'])}</pubDate>",
            f"<description>{html.escape(v.get('summary', ''))}</description>",
            *[f"<category>{html.escape(t)}</category>" for t in v.get("tags", [])],
            "</item>",
        ]
    parts += ["</channel>", "</rss>"]
    return "\n".join(parts)


def build_sitemap(items: list[dict], site: SiteConfig, en_slugs: set) -> str:
    urls = [site.clean_base + "/"]
    if en_slugs:
        urls.append(site.clean_base + "/en/")
    urls += [_ep_url(site, it["slug"], "zh") for it in items]
    urls += [_ep_url(site, it["slug"], "en") for it in items if it["slug"] in en_slugs]
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
    en: dict | None = None,
    primary_public_md: str | None = None,
    kind: str | None = None,
) -> dict:
    """Add one report's PUBLIC layers to the site and rebuild feeds/index.

    The Chinese (primary) public body comes from `primary_public_md` if given,
    else it is extracted from `report_md`. `en` (optional) is a translated
    bundle {body, title, tags, editor_note, connections} for the /en/ tree.

    Returns the manifest entry. Idempotent on slug: re-publishing the same slug
    updates that episode in place.
    """
    public_md = (
        primary_public_md if primary_public_md is not None
        else extract_public_markdown(report_md, site.private_cutoff)
    )
    if not public_md:
        raise RuntimeError(
            "No public content found. Check that the report has the expected "
            "headings and that PODLENS_PRIVATE_CUTOFF matches."
        )

    date = date or datetime.now().strftime("%Y-%m-%d")
    slug = slug or slugify(title, date)
    prior = next((it for it in _load_manifest() if it["slug"] == slug), {})
    # Keep existing fields if none are supplied this time (e.g. --publish-existing).
    if tags is None:
        tags = prior.get("tags", [])
    if connections is None:
        connections = prior.get("connections", [])
    entry = {"slug": slug, "title": title, "date": date,
             # "podcast" | "paper" — drives a few labels + (future) the section.
             "kind": kind or prior.get("kind", "podcast"),
             "summary": _first_sentences(public_md),
             "source_url": source_url or prior.get("source_url", ""),
             "tags": tags or [],
             "connections": connections or [],
             # Async human editor's note. Preserved across re-publishes.
             "editor_note": prior.get("editor_note", "")}

    # English mirror: new translation if provided, else carry the prior one.
    if en is not None:
        entry["i18n"] = {"en": _en_entry_data(en)}
    elif prior.get("i18n"):
        entry["i18n"] = prior["i18n"]

    # Store the public markdown(s) so pages can be re-rendered on any rebuild.
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    _body_path(slug, "zh").write_text(public_md, encoding="utf-8")
    if en is not None and en.get("body", "").strip():
        _body_path(slug, "en").write_text(en["body"].strip(), encoding="utf-8")

    items = [it for it in _load_manifest() if it["slug"] != slug]
    items.insert(0, entry)
    items.sort(key=lambda it: it["date"], reverse=True)

    _rebuild_site(items, site)
    return entry


def _rebuild_site(items: list[dict], site: SiteConfig) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    EPISODES_DIR.mkdir(parents=True, exist_ok=True)

    # Which slugs have an English body (so cross-links/hreflang only point to
    # pages that actually exist).
    en_slugs = {it["slug"] for it in items if _body_path(it["slug"], "en").exists()}

    for lang in LANGS:
        if lang == "en" and not en_slugs:
            continue  # no English episodes yet -> don't create an empty /en/
        out_eps = EPISODES_DIR if lang == "zh" else EN_EPISODES_DIR
        out_eps.mkdir(parents=True, exist_ok=True)

        # Per-language title map + back-references (derived from forward
        # connections, so they are always consistent without mutating targets).
        slug_titles = {}
        for it in items:
            v = _episode_view(it, lang) or _episode_view(it, "zh")
            slug_titles[it["slug"]] = v["title"]
        backrefs: dict[str, list[dict]] = {}
        for it in items:
            v = _episode_view(it, lang)
            if v is None:
                continue
            for conn in v.get("connections", []):
                backrefs.setdefault(conn["slug"], []).append(
                    {"from_slug": it["slug"], "from_title": slug_titles[it["slug"]], **conn}
                )

        rendered = []
        for it in items:
            body_path = _body_path(it["slug"], lang)
            if not body_path.exists():
                continue  # no version in this language yet
            html_out = render_episode_page(
                it, body_path.read_text(encoding="utf-8"), site, lang=lang,
                slug_titles=slug_titles, backrefs=backrefs.get(it["slug"], []),
                has_sibling=(it["slug"] in en_slugs), en_slugs=en_slugs,
            )
            (out_eps / f"{it['slug']}.html").write_text(html_out, encoding="utf-8")
            rendered.append(it)

        if lang == "zh":
            (SITE_DIR / "index.html").write_text(render_index(rendered, site, "zh"), encoding="utf-8")
            (SITE_DIR / "feed.xml").write_text(build_rss(rendered, site, "zh"), encoding="utf-8")
            _write_jsonfeed(rendered, site, "zh", JSONFEED)
        elif rendered:
            EN_DIR.mkdir(parents=True, exist_ok=True)
            (EN_DIR / "index.html").write_text(render_index(rendered, site, "en"), encoding="utf-8")
            (EN_DIR / "feed.xml").write_text(build_rss(rendered, site, "en"), encoding="utf-8")
            _write_jsonfeed(rendered, site, "en", EN_DIR / "episodes.json")

    _write_manifest(items)
    (SITE_DIR / "sitemap.xml").write_text(build_sitemap(items, site, en_slugs), encoding="utf-8")
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


# --- Edit / annotate already-published episodes -------------------------------

def list_published() -> list[dict]:
    """A compact list of published episodes (newest first) for the edit UI."""
    return [
        {"slug": it["slug"], "title": it["title"], "date": it["date"],
         "has_note": bool((it.get("editor_note") or "").strip()),
         "has_en": bool((it.get("i18n", {}) or {}).get("en"))}
        for it in _load_manifest()
    ]


def get_episode_for_edit(slug: str) -> dict | None:
    """Everything needed to edit one episode: its public body + current note.

    Returns None if the slug is unknown. Editing happens on the Chinese
    (primary) body; the English mirror is re-translated on save.
    """
    entry = next((it for it in _load_manifest() if it["slug"] == slug), None)
    if entry is None:
        return None
    src = _body_path(slug, "zh")
    public_md = src.read_text(encoding="utf-8") if src.exists() else ""
    return {
        "slug": slug,
        "title": entry["title"],
        "date": entry["date"],
        "source_url": entry.get("source_url", ""),
        "tags": entry.get("tags", []),
        "editor_note": entry.get("editor_note", ""),
        "public_md": public_md,
        "connections": entry.get("connections", []),
    }


def update_episode(
    slug: str,
    site: SiteConfig,
    public_md: str | None = None,
    editor_note: str | None = None,
    title: str | None = None,
    tags: list[str] | None = None,
    en: dict | None = None,
    source_url: str | None = None,
) -> dict:
    """Edit an already-published episode in place, then rebuild the whole site.

    Only the fields passed (not None) are changed. The slug (URL identity) is
    NEVER changed here, so existing links and back-references stay valid.
    `en` (optional) replaces the English mirror with a freshly translated bundle.
    Returns the updated manifest entry.
    """
    items = _load_manifest()
    entry = next((it for it in items if it["slug"] == slug), None)
    if entry is None:
        raise RuntimeError(f"未找到这一期:{slug}")

    if public_md is not None:
        public_md = public_md.strip()
        if not public_md:
            raise RuntimeError("公开正文不能为空。")
        _body_path(slug, "zh").write_text(public_md, encoding="utf-8")
        entry["summary"] = _first_sentences(public_md)
    if title is not None and title.strip():
        entry["title"] = title.strip()
    if tags is not None:
        entry["tags"] = tags
    if editor_note is not None:
        entry["editor_note"] = editor_note.strip()
    if source_url is not None:
        # Changing the link re-derives the in-page player + timestamp seeking
        # (video id is re-extracted at render). Same video, any URL form, is safe.
        entry["source_url"] = source_url.strip()
    if en is not None:
        entry["i18n"] = {"en": _en_entry_data(en)}
        if en.get("body", "").strip():
            _body_path(slug, "en").write_text(en["body"].strip(), encoding="utf-8")

    items.sort(key=lambda it: it["date"], reverse=True)
    _rebuild_site(items, site)
    return entry
