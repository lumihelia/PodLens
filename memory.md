# Project Memory

## Current State
PodLens publishes bilingual (zh/en) podcast/paper interpretations to a static site in `docs/` (GitHub Pages, custom domain `lens.lumihelia.com`). Source markdown bodies live in `.podlens/episodes/`, manifest at `docs/manifest.json`, rendering logic in `podlens/publish.py`. Each episode is published via a one-off `scripts/publish_<name>.py` script that calls `publish_report()`.

## Completed
- **2026-06-21**: Audited and fixed all 23 items published on 2026-06-14.
  - **Missing YouTube links**: all 21 podcast episodes that day had `source_url: ""` in the manifest (the per-episode publish scripts had `"url": ""` hardcoded). Backfilled all 21 from `材料/链接.txt`, both in the live manifest (via `update_episode`) and in the source `publish_*.py` scripts, so embedded players + clickable timestamp links now work in zh and en.
  - **Duplicate episode**: `alexei-efros-surface-deep-data-curious-robot` and `alexei-efros-surface-data-deep-data` were the same talk published twice. Kept the more complete one (`surface-data-deep-data`), deleted the other (manifest entry, rendered html, source `.md`/`.en.md`, `scripts/publish_alexei_efros.py`, its `en_bodies` file), and repointed 4 episodes' cross-references to the surviving slug.
  - **Collapsed "这期讲了什么"/"这篇讲了什么" structure**: 6 items (4 podcasts: adam-neumann, marc-andreessen, pavel-durov, tobi-lutke; 2 papers: li-curtis, patel-wang-fan) were missing the overview paragraph and had 时间线/核心观点/内部张力 nested as `###` under the overview heading instead of standalone `##` sections like every other episode on the site. Their English mirrors were unstructured prose with no section headers at all. Rewrote all 6 (zh: added overview + promoted headings using only existing report content, no new facts; en: rewrote into the matching structured template by faithful translation). Fixed via one-off scripts: `scripts/fix_june14_youtube_links.py`, `scripts/merge_efros_duplicate.py`, `scripts/fix_june14_structure_podcasts.py`, `scripts/fix_june14_structure_papers.py`.
  - Verified: privacy gate passes on all touched pages (no `证据锚定洞察`/`个人映射`/`值得收藏的概念`/`待追踪的问题` leakage), all H2 sections render correctly in zh and en, all timestamp links resolve to the correct YouTube id+seconds.

## Decisions
- Initially held off on fabricating the canonical paper template's `术语小词典`/`这篇之前与之后`/`最值得读原文的几段` sections for the 2 papers, since those need anchored quotes from the original paper text. Helia confirmed she wanted them filled in properly, so fetched the real papers (Li & Curtis via PMC mirror PMC10528783, published version in Current Biology; Patel/Wang/Fan via the published PNAS Nexus version at academic.oup.com/pnasnexus/article/5/6/pgag149) and built all 3 sections from verbatim quotes pulled from the actual text, with section-name anchors matching the canonical format used elsewhere on the site (e.g. `active-forgetting.md`). Both papers now have the full 7-section template (这篇讲了什么/论文骨架/核心论点清单/大白话重讲/术语小词典/这篇之前与之后/最值得读原文的几段) in zh and en, with zero fabricated quotes.
- No LLM API calls were made anywhere in this fix (no Gemini/Claude translation/interpretation calls) — all zh/en content was hand-written by Claude directly from the existing report text + the fetched original papers. The one exception, done with explicit confirmation, was using WebFetch/WebSearch to pull the original paper text (read-only, not a generation API).

## Verification
- `docs/manifest.json`: all 22 items dated 2026-06-14 (23 minus the merged duplicate) have non-empty `source_url`.
- Swept all `.podlens/episodes/*.md` for the "## 这期/这篇讲了什么" immediately followed by "###" pattern — zero remaining matches site-wide.
- Spot-checked rendered `<h2>` headings on all 6 restructured pages (zh + en) — clean standalone sections, no leftover Chinese in en pages, no private-layer leakage.
- Both papers now render all 7 canonical sections in both languages; all glossary/anchor quotes verified against the actual published paper text fetched live.

## Known Issues
(none currently open from this fix)

## Architecture Audits
(none logged yet)

## Next Steps
- Commit and push the fixed `docs/` output + source changes once reviewed.
