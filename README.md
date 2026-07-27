# PodLens

A transcript-grounded interpretation and publishing workspace for podcasts,
videos, and papers.

**Live site:** [lens.lumihelia.com](https://lens.lumihelia.com) ·
**RSS:** [English](https://lens.lumihelia.com/feed.xml) /
[中文](https://lens.lumihelia.com/zh/feed.xml) ·
**JSON Feed:** [episodes.json](https://lens.lumihelia.com/episodes.json)

PodLens follows one hard rule:

> Faithful reconstruction first. Plain language second. Personal mapping last.
> Every insight must remain traceable to the source.

It is both a command-line interpretation pipeline and a local editorial
workbench. The workbench is the main publishing surface: review the full
interpretation, edit the public layer, inspect suggested connections, and only
then publish the bilingual static pages.

## What It Does

PodLens runs three grounded interpretation stages:

1. **Faithful reconstruction**: topic, central question, chronological map,
   source-anchored claims, and clear claim types.
2. **Plain-language retelling**: cause-and-effect explanations, useful
   metaphors, and moments worth revisiting.
3. **Evidence-grounded insight and personal mapping**: confidence-marked
   insights connected to the local `profile.md`.

The public site receives only the first two layers. The personal mapping layer
and complete reports stay local under the ignored `reports/` directory.

Supported inputs:

- YouTube URLs, using subtitle tracks rather than video downloads
- `.srt`, `.vtt`, `.txt`, and `.md` transcripts
- Research papers as `.pdf`, `.txt`, or `.md`
- Piped standard input for CLI use

## Local Workbench

The local workbench supports the full editorial handoff:

- Switch between podcast/video and paper interpretation
- Upload source files or provide a YouTube/source link
- Review the complete private report and the proposed public layer separately
- Edit title, tags, source link, and public Markdown before publishing
- Review evidence-grounded connections to earlier episodes and papers
- Remove suggested connections before publication
- Manage already-published content and add a signed `From Helia` note
- Edit the local personal background used by the mapping stage
- Generate the English and Chinese publication trees
- Commit the generated public files and push them to GitHub Pages

Start it by double-clicking `start_ui.command`, or from Terminal:

```bash
./start_ui.command
```

The launcher installs current requirements, starts the server on
`http://127.0.0.1:8765`, and opens the browser. Keep its Terminal window open;
press `Ctrl-C` to stop it.

Publishing from the workbench is a real Git operation. After confirmation it:

1. Writes the public static output under `docs/`.
2. Updates the editable publication sources under `.podlens/`.
3. Commits only those two paths, excluding `.DS_Store`.
4. Pushes the commit directly to `origin/main`.

Other staged paths are not included in the publication commit. The current
workflow is intended for a single-owner repository whose `main` branch deploys
`docs/` through GitHub Pages.

## Setup

```bash
bash setup.sh
```

This creates `.venv`, installs dependencies, and creates `.env` and
`profile.md` from their examples when those files do not already exist.

Configure one provider in `.env`:

```env
# gemini or deepseek
PODLENS_PROVIDER=gemini

GEMINI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here

# Optional. Leave blank for the selected provider's default model.
PODLENS_MODEL=
```

Provider defaults:

- Gemini: `gemini-2.5-pro`
- DeepSeek: `deepseek-chat`

Only the key for the selected provider is used. `profile.md`, `.env`, complete
reports, transcripts, and source papers are ignored by Git.

## CLI

Activate the environment:

```bash
source .venv/bin/activate
```

Common commands:

```bash
# Interpret a YouTube video
python -m podlens "https://youtu.be/VIDEO_ID"

# Interpret a local transcript
python -m podlens examples/sample_transcript.txt

# Save a report
python -m podlens my_transcript.srt -o report.md

# Pipe text from the clipboard
pbpaste | python -m podlens -

# Skip personal mapping
python -m podlens my_transcript.txt --no-profile

# Produce English interpretation output
python -m podlens my_transcript.txt --lang en

# Inspect the full prompt pipeline without an API call
python -m podlens examples/sample_transcript.txt --dry-run
```

Subtitle files are the most reliable podcast input because they preserve
timestamps and avoid YouTube bot checks. If YouTube blocks caption fetching,
you can let `yt-dlp` use an existing browser session:

```env
PODLENS_COOKIES_FROM_BROWSER=chrome
PODLENS_SUB_LANGS=zh.*,en.*,.*
```

## Providers And Long Inputs

Gemini and DeepSeek share the same internal provider boundary in
`podlens/interpreter.py`.

For long podcast transcripts, DeepSeek uses `podlens/chunking.py` to split
Stages 1 and 2 on transcript-line boundaries, interpret each segment, and merge
the partial results. Stage 3 and paper interpretation use the already-condensed
intermediate output and are not chunked. Gemini keeps the single-call path.

Chunking increases the number of calls and may lose some cross-segment nuance.
DeepSeek output, especially names, institutions, translations, and suggested
connections, should be read end-to-end before publication.

## Bilingual Publishing

The public site is English-primary:

- English: `/`, `/episodes/`, `/papers/`, `/feed.xml`
- Chinese: `/zh/`, `/zh/episodes/`, `/zh/papers/`, `/zh/feed.xml`

The two language versions are connected with a visible language switch and
`hreflang`. Legacy `/en/...` HTML pages redirect to the English root paths.

CLI publishing commands:

```bash
# Interpret and publish
python -m podlens "Episode.srt" --title "My Episode" --publish

# Publish an existing report without another interpretation call
python -m podlens --publish-existing report.md --title "My Episode"

# Rebuild indexes, feeds, and sitemap from the manifest
python -m podlens --rebuild-site
```

`PODLENS_PRIVATE_CUTOFF` defines where private report layers begin. Everything
from that heading onward is removed before static files are written.

## GitHub Pages Deployment

The repository is configured for GitHub Pages from `main` and `/docs`, with
`docs/CNAME` pointing to `lens.lumihelia.com`.

Deployment flow:

```text
review in local workbench
    -> generate docs/ and .podlens/
    -> scoped Git commit
    -> push origin/main
    -> GitHub Pages build
    -> lens.lumihelia.com
```

The workbench reports Git commit and push failures separately. A successful
push does not mean the Pages build has finished; allow a few minutes, then
verify the public page and feed.

## Verification

Run the offline verification suite:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q podlens webui
python3 -m podlens examples/sample_transcript.txt --dry-run
git diff --check
```

The tests cover provider defaults, transcript chunking, publication commit
scope, XML parsing, bilingual route inventory, source URLs, and public-layer
privacy headings. Real model calls, translations, Git pushes, and Pages
deployment still require explicit live verification.

## Known Limits

- Audio-file transcription and podcast RSS ingestion are not implemented.
- YouTube caption fetching can be blocked by bot checks or rate limits.
- PDF extraction quality depends on the paper layout; `.txt` or `.md` is the
  fallback for difficult PDFs.
- DeepSeek chunking reduces context pressure but does not remove the need for
  editorial review.
- The workbench is a local single-user tool, not a hosted multi-user CMS.

## Repository Map

- `podlens/`: interpretation, provider, publishing, and source-processing logic
- `webui/`: local editorial workbench
- `.podlens/episodes/`: editable bilingual publication sources
- `docs/`: generated GitHub Pages site
- `scripts/`: one-off publishing and maintenance tools
- `tests/`: offline regression tests
- `.context/`: durable project context for future development sessions

## License

[MIT](LICENSE)
