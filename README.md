# PodLens

A transcript-grounded podcast interpretation tool.

**Live site:** https://lumihelia.github.io/PodLens/ · **Feed:** [RSS](https://lumihelia.github.io/PodLens/feed.xml) · [JSON Feed](https://lumihelia.github.io/PodLens/episodes.json)

Most "podcast summarizers" jump straight to clever-sounding insights, and you
never know which sentence came from the episode and which the AI made up.
PodLens refuses to work that way. It follows one hard rule:

> **Faithful reconstruction first. Then plain language. Personal mapping last.
> Every insight points back to a timestamp in the transcript.**

## How it works

PodLens runs three Gemini calls in order. Each stage is grounded in the verified
output of the previous one, so a later layer can never run ahead of an earlier
one — the product's core principle is enforced by the architecture, not just
asked for in a prompt.

1. **忠实还原** — what the episode actually says: topic, central question, a
   chronological topic map with timestamps, and a list of key claims each tagged
   as fact / claim / example / prediction / speculation / host-prompt.
2. **大白话重讲** — the same content re-explained as a smart friend would, with
   metaphors and cause-and-effect chains, plus which moments are worth re-listening.
3. **证据锚定洞察 + 个人映射** — insights with confidence levels and evidence
   anchors, then connections to *your* interests (from `profile.md`), every one
   tied back to a timestamp. Concepts to save and open questions to track.

## Setup

```bash
bash setup.sh
```

This creates a virtual environment, installs dependencies, and copies
`.env.example` → `.env` and `profile.example.md` → `profile.md`.

Then:

1. Open `.env` and paste your `GEMINI_API_KEY`
   (free key: https://aistudio.google.com/apikey).
2. (Optional) Edit `profile.md` with your own long-term interests and projects —
   this powers the personal-mapping layer.

## Usage

```bash
source .venv/bin/activate

# Interpret a YouTube video by URL (captions fetched automatically)
python -m podlens "https://youtu.be/VIDEO_ID"

# Interpret a transcript file, print to terminal
python -m podlens examples/sample_transcript.txt

# Save the report to a file
python -m podlens my_transcript.txt -o report.md

# Pipe a transcript in
pbpaste | python -m podlens -

# Skip personal mapping (reconstruction + plain language only)
python -m podlens my_transcript.txt --no-profile

# Output in English instead of Chinese
python -m podlens my_transcript.txt --lang en
```

### Inputs

PodLens accepts a **YouTube URL**, a **subtitle file** (`.srt` / `.vtt`), a
**transcript file** (`.txt`/`.md`), piped **stdin** (`-`), or raw transcript
**text**. Subtitle files are the most reliable input with timestamps — and
sidestep YouTube's bot-blocking entirely. Timestamps (`[12:34]`, `1:23:45`, or
SRT/VTT cue times) are preserved and used as evidence anchors; if a pasted plain
transcript has none, PodLens falls back to short verbatim quotes as anchors.

```bash
# A downloaded subtitle file (e.g. exported from YouTube) — recommended
python -m podlens "My Episode.srt" -o report.md
```

YouTube captions are fetched with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
(only the subtitle track is downloaded, never the video).

**If YouTube blocks you** (HTTP 429 / "Sign in to confirm you're not a bot"),
that is an IP/bot check, not a bug. The fix is to let yt-dlp use your browser
login — set in `.env`:

```env
PODLENS_COOKIES_FROM_BROWSER=chrome   # or safari / firefox / edge
```

For non-English videos, set `PODLENS_SUB_LANGS` (e.g. `zh.*,en.*,.*`).

> Audio-file transcription and podcast RSS are still intentionally left out of
> this version. They are plumbing that can be added later without changing the
> core — the valuable part is the interpretation, not the intake.

## How do I know it works?

Without an API key, inspect the full prompt pipeline:

```bash
python -m podlens examples/sample_transcript.txt --dry-run
```

With a key set in `.env`, run the real thing:

```bash
python -m podlens examples/sample_transcript.txt
```

You should get a Markdown report with all the layers, in order.

## Where it can break

- **No API key / wrong key** → you'll get a clear error pointing at `.env`.
  Use `--dry-run` to verify everything else first.
- **Very long transcripts** → Gemini's context window is large (1M+ tokens), so
  typical episodes fit without chunking. Multi-hour transcripts could eventually
  exceed it; chunking is a future improvement.
- **No timestamps in the transcript** → evidence anchors degrade to short
  verbatim quotes instead of timestamps. PodLens notes this at the top of the report.
- **Rate limits on the free tier** → three calls per run; heavy use may hit
  limits. Switch `PODLENS_MODEL` to `gemini-2.5-flash` for lighter, faster runs.

## Roadmap (next logical improvements)

- Audio-file transcription and podcast RSS as input adapters.
- A thin web UI that calls the same `interpret()` core.
- Append accepted concepts to a growing personal knowledge file.

## Publishing a public feed (optional)

PodLens can publish the **public layers** of your interpretations as a static
site with an RSS feed, JSON Feed, and sitemap — a you-owned, machine-readable
surface that search engines and agents can discover and cite.

**Privacy is enforced:** only the public layers (what the episode is about, the
topic map, core ideas, the plain-language re-telling, moments worth hearing) are
published. Everything from `PODLENS_PRIVATE_CUTOFF` onward — your evidence-grounded
insights and personal mapping — is stripped and **never written to the site**.

```bash
# Interpret and publish in one go (personal layers stay local)
python -m podlens "Episode.srt" --title "My Episode" --publish

# Publish an already-saved report without re-spending an API call
python -m podlens --publish-existing report.md --title "My Episode"

# Rebuild index/feeds/sitemap from the manifest (no new episode)
python -m podlens --rebuild-site
```

Output goes to `docs/`, which GitHub Pages can serve directly. Configure the
site in `.env` (`PODLENS_SITE_URL`, `PODLENS_SITE_TITLE`, `PODLENS_CUSTOM_DOMAIN`,
etc.). To serve it: enable GitHub Pages on the `main` branch `/docs` folder, and
point a subdomain at it with a CNAME DNS record (your DNS host stays wherever it
is — only the CNAME needs to point to `<user>.github.io`).

## License

[MIT](LICENSE) — free to use, modify, and distribute.
```
