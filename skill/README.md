# PodLens Interpreter

**Turn long podcasts, interviews, papers, and transcripts into evidence-grounded content packs — for solo founders who think before they publish.**

---

## Who it is for

Solo founders, independent researchers, creators, and knowledge workers who:

- Listen to or read long-form content and want to extract real signal, not just highlights
- Need to repurpose insights into newsletters, posts, or research without losing fidelity to the source
- Are tired of AI summaries that paraphrase instead of reconstruct
- Want a publishable content pack they can actually stand behind

## What it does

Three stages, always in this order:

**Stage 1 — Faithful Reconstruction**
Rebuilds the source's actual argument with evidence anchors: timestamps or direct quote fragments. Every claim must trace back to a specific moment in the text. Speculation is labeled as speculation. Nothing is invented.

**Stage 2 — Plain Language Retelling**
Explains the content as if to a smart friend who has not read it — concrete analogies, actual argument structure, no bullet-point flattening. Minimum 300 words of flowing prose.

**Stage 3 — Content Pack**
Produces ready-to-use output: X thread, LinkedIn post, newsletter intro, five follow-up content angles, and a field note draft — all grounded in Stage 1 evidence. For research papers, switches to Research Brief + Evidence Table + Business Angles.

## What input it needs

- Plain text: paste a transcript, upload a `.txt` or `.md` file, or copy paper text
- Subtitle files: `.srt` or `.vtt` content pasted as text
- Any language — output matches input language by default
- Minimum useful length: ~800 words
- No API key required. No local setup required. No web UI.

## What output it produces

For a 60-minute podcast transcript (~8,000 words):
- Core findings with timestamp anchors (minimum 4)
- 300+ word plain-language retelling
- 5–8 tweet X thread with source-verified claims
- 150–200 word LinkedIn post
- 100–150 word newsletter intro
- 5 follow-up content angles
- Field note draft ready to post

For a research paper:
- Core findings with direct quote anchors
- 300+ word plain-language explanation
- Research Brief (practical implications for solo founders)
- Evidence Table (claim → direct quote → section)
- Business and creator application angles
- Field note draft

## How much time it saves

| Task | Manual | PodLens Interpreter |
|------|--------|---------------------|
| 60-min podcast → content pack | 90–120 min | ~4 min |
| Research paper → research brief | 45–60 min | ~3 min |
| Interview → X thread with sources | 30–45 min | ~2 min |

## How to install

```
botlearn skillhunt podlens-interpreter
```

Then invoke through your local Agent:

```
Use PodLens Interpreter on [paste your transcript or paper text here]
```

## Example input

See `examples/demo_a_input.txt` — a 28-minute podcast transcript about attention and productivity (~280 words).

See `examples/demo_b_input.txt` — a research paper excerpt on cognitive overhead for one-person businesses (~700 words).

## Example output

See `examples/demo_a_output.md` — full podcast content pack including Stage 1, Stage 2, X thread, LinkedIn post, newsletter intro, and field note draft.

See `examples/demo_b_output.md` — full paper research brief including Stage 1, Stage 2, Research Brief, Evidence Table, Business Angles, and field note draft.

## Why it is different from generic summarizers

| Generic AI summarizer | PodLens Interpreter |
|-----------------------|---------------------|
| Compresses and paraphrases | Reconstructs argument structure first |
| May hallucinate details | Every claim requires a timestamp or quote anchor |
| Loses source specificity | Speculation is labeled with the source's own hedging |
| Output could apply to anything | Content pack flows from verified reconstruction |
| No evidence trail | Stage 1 is independently verifiable against the source |

## Scenario

**Content Production Automation** · **Knowledge Management & Research** · **Personal Brand Growth**

## Tags

podcast to content · transcript analysis · evidence grounded summary · founder content · research synthesis · personal brand · OPC workflow · newsletter draft · social content · paper to brief · solo founder · one person company

## Field Note

Every PodLens Interpreter output ends with a pre-filled field note draft. Fill in the blanks and post to BotLearn community. See `field_note_template.md` for the standalone template.

## About

PodLens Interpreter is built on the PodLens methodology: faithful reconstruction before content production. The principle is that what you publish should be traceable to what was actually said or written — not to what an AI predicted the content probably said.
