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
- Pre-existing (not from this session): 3 episodes have a connection pointing at a slightly wrong slug, so that one backlink silently fails to render: `marc-andreessen-malleable-world-founder-capitalism` and `daniel-ek-impact-happiness-self-mastery` both reference `caa-co-founder-michael-ovitz` (should be `michael-ovitz-caa-frame-of-reference`); `sarah-paine-continental-maritime-powers-geopolitics` references `ms-e435-class3-economics-ai-supercycle` (should be `ms&e435-class3-economics-ai-supercycle`). Flagged as a spawned background task (`task_5836df04`), not fixed yet.

## Architecture Audits
(none logged yet)

## Completed (continued)
- **2026-06-21, later same day**: Verified and published 14 new episodes from a corrected batch. Helia had originally had "Anti-gravity" (Gemini) interpret `材料/0621`, but the first pass used a different "Skill" output format (Stage 1/2/3 + marketing Content Pack) that doesn't match this site's template — only 3 of 11 files (avi-wigderson, how-do-computers-work, robert-sapolsky) were affected; the other 8 were already in the correct template. Helia had it redone correctly into `reports/0621副本` (all 11, now in the standard template) and added 3 more in `reports/0621 plus`. Confirmed the first 5 episodes already published from `reports/0621` were byte-identical (or only trivially different — a stray `✱`→`*` character fix) to the `0621副本` versions, so no rework was needed there.
  - Published all 14: ed-catmull, g-memory (paper), michael-levin, simon-peyton-jones, skillcomposer (paper), tim-ferriss, thomas-sargent, david-berlinski (2+2=4), avi-wigderson, how-do-computers-work, robert-sapolsky, dave-eggers, simon-haines & fiona-mueller, tim-spector.
  - For every episode: spot-verified 4-6 specific claims/quotes against the actual source transcript or paper text in `材料/0621`, `材料/0621副本`, `材料/0621 plus` before publishing (all passed faithfulness checks; one instance of a transcription-ASR error in the source transcript — "Paulo Ferrero/Ferrera" — was correctly normalized by the original report to the real name, Paulo Freire).
  - Wrote 2 cross-episode connections per item (28 total), each grounded in verbatim quotes from both sides, cross-referencing existing site episodes (e.g. Sapolsky↔hunger-neuroscience on dopamine "wanting vs liking"; Levin↔G-Memory on software-layer rewrites without touching hardware; Sargent↔Patel-Wang-Fan on descriptive vs. structural AI capability).
  - Wrote full English bodies for all 14 (faithful translation/structuring into the site's standard template, no API calls).
  - Verified: all 14 pass the privacy gate (zero leakage of `证据锚定洞察`/`个人映射`/`值得收藏的概念`/`待追踪的问题`) in zh and en, zero collapsed-structure defects, all connections resolve to real published slugs, feed/sitemap/index all updated.
  - `docs/manifest.json` now has 81 items total (14 new on top of 67 from before).

## Next Steps
- Commit and push today's combined work (the June-14 fix batch + the 14 new 0621 episodes) once reviewed.
- Decide whether to action the spawned task fixing the 3 dangling connection slugs (`task_5836df04`).
