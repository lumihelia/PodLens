"""The interpretation prompts. This module is the soul of PodLens.

Three stages, each grounded in the verified output of the previous one:

  Stage 1  Source reconstruction   -- low interpretation, high fidelity
  Stage 2  Plain-language re-telling
  Stage 3  Evidence-grounded insight + personal mapping

The ordering is enforced by the architecture (separate calls), not merely
requested in text. Every later stage receives the earlier stages as grounding,
which makes evidence linking natural and prevents free-floating "insight".
"""

# --- Language directives -----------------------------------------------------

_LANG_DIRECTIVE = {
    "zh": (
        "用简体中文输出。无论原始 transcript 是什么语言,你的解读一律用中文。"
        "正文里不要夹杂未翻译的英文词(例如不要写“actionable”“insight”这类),"
        "一律用中文表达;只有专有名词、人名、或确无中文对应的术语可保留原文,"
        "并在其后用括号给出中文。"
    ),
    "en": (
        "Write the output in English, regardless of the transcript's language. "
        "Do not leave untranslated foreign words in the prose; only proper nouns "
        "may stay in their original form."
    ),
}


def _lang(output_lang: str) -> str:
    return _LANG_DIRECTIVE.get(output_lang, _LANG_DIRECTIVE["zh"])


# --- Shared grounding rules --------------------------------------------------

_FIDELITY_RULES = """\
GROUNDING RULES (apply to every stage):
- Stay faithful to the transcript. Do not invent facts, names, numbers, or
  claims that are not supported by the text.
- When the transcript has timestamps, cite them (e.g. [12:34]) as evidence
  anchors. When it has none, quote a short verbatim phrase from the transcript
  as the anchor instead.
- Clearly separate what the speaker actually said from your own inference.
- Do not add outside knowledge as if it came from the episode. If you must
  note context the episode did not state, label it explicitly as your own note.
- No hype, no motivational filler, no decorative summary. Plain and serious.
- Output ONLY the requested Markdown sections. Do not add any preamble,
  acknowledgement, or sign-off before the first heading or after the last.
"""


# --- Stage 1: Source reconstruction -----------------------------------------

def build_reconstruction_prompt(transcript: str, output_lang: str) -> str:
    return f"""\
You are a meticulous listener producing a faithful reconstruction of a podcast
or talk, working ONLY from the transcript below. This is the fidelity layer:
low interpretation, high faithfulness. Do not yet explain in plain language and
do not yet draw personal connections.

{_FIDELITY_RULES}

{_lang(output_lang)}

Produce Markdown with EXACTLY these sections and headers, in this order:

## 这期讲了什么
A short, faithful overview: the episode's topic, who is speaking (guest/host if
identifiable), the central object of discussion, the main question being
explored, and the overall logical arc -- in a few sentences, like high-quality
lecture notes. No personal interpretation.

## 时间线主题地图
A chronological map of the episode broken into segments. For each segment give a
timestamp range (or a verbatim anchor phrase if no timestamps exist) and one
line describing what that stretch covers. Keep it tight and in order.

## 核心观点清单
A numbered list of the KEY claims -- the substantive points the episode makes,
not every sentence. Merge closely related statements into one coherent claim,
and never split a single idea across multiple entries. Aim for roughly 5-10
meaningful claims for a typical episode; a long episode may have more, but each
entry should stand on its own as a real point worth noting. For EACH claim:
- the claim, stated faithfully (you may combine a few transcript lines into one
  well-formed claim, as long as you do not distort meaning)
- its evidence anchor (timestamp or short verbatim quote); if a claim spans
  several moments, you may cite a small range
- a type tag, one of: 事实 / 观点 / 例子 / 预测 / 猜想 / 主持人追问
  (fact / claim / example / prediction / speculation / host-prompt)
- if relevant, a one-line note on uncertainty or hedging the speaker expressed

TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"
"""


# --- Stage 2: Plain-language re-telling --------------------------------------

def build_plain_language_prompt(
    transcript: str, reconstruction: str, output_lang: str
) -> str:
    return f"""\
You now have a faithful reconstruction of an episode (below), plus the original
transcript. Your job is the plain-language layer: re-explain the episode as a
smart, honest friend sitting next to the listener -- lowering the barrier to
understanding WITHOUT dumbing it down and WITHOUT drifting from what was said.

{_FIDELITY_RULES}

Additional rules for this layer:
- Translate jargon into everyday language and use concrete metaphors where they
  genuinely help.
- Compress complex reasoning into clear cause-and-effect chains.
- Where a claim is counterintuitive, say plainly WHY it is counterintuitive.
- Preserve the original argument structure -- do not reorder the logic.
- Flag common misunderstandings the audience might have.
- This is a flowing re-telling, not a bullet summary. It can have voice and
  rhythm, but it must stay anchored to the episode's actual content.
- Do NOT greet or address the reader, and do not open with a salutation. The
  reader is reading a written interpretation, not chatting with an assistant.
  Never start with things like "你好" / "Hi" / "好的". You may start straight
  into the content (e.g. "那我们来聊聊..." is fine; "你好,我们来聊聊..." is not).

{_lang(output_lang)}

Produce Markdown with EXACTLY these sections and headers, in this order:

## 大白话重讲
The plain-language re-telling described above. Prose, vivid but grounded.

## 值得精听的片段
A short list of moments worth going back to hear in the original audio. For
each: the timestamp (or anchor phrase), and why it is worth it -- high
information density, a key turn in the argument, or emotional/tonal nuance
(hesitation, emphasis, a shift) that a transcript flattens.

FAITHFUL RECONSTRUCTION:
\"\"\"
{reconstruction}
\"\"\"

ORIGINAL TRANSCRIPT (for verification and quoting):
\"\"\"
{transcript}
\"\"\"
"""


# --- Stage 3: Evidence-grounded insight + personal mapping -------------------

def build_metadata_prompt(reconstruction: str, output_lang: str) -> str:
    """Ask for a title and 3-6 SPECIFIC topical tags in one JSON object.

    Title format: a concise topic phrase + " · " + the guest/speaker name,
    e.g. "时间的本质 · Jim Al-Khalili". Tags must be concrete concepts actually
    discussed, not the broad field.
    """
    return f"""\
From the faithful reconstruction below, produce a title and topical tags.

TITLE rules:
- Format: a concise topic phrase, then " · ", then the main guest/speaker's name.
  Example: "时间的本质 · Jim Al-Khalili"
- The topic phrase captures what THIS episode is really about (specific, not
  generic).
- The name MUST be the person's ORIGINAL name as commonly written — normally the
  English / Latin spelling (e.g. "Jim Al-Khalili", "Dana Reyes"). NEVER
  transliterate or translate the name into Chinese (NOT "达娜·雷耶斯"). If the
  person is more widely known by an English name, use that English name even if
  they also have a name in another language.
- Do NOT invent a show name or episode number; only use what the content gives.

TAGS rules:
- 3 to 6 SPECIFIC concepts, entities, theories or terms ACTUALLY discussed
  (e.g. "量子退相干", "块状宇宙", "时间膨胀"), NOT the broad field
  (NOT "物理", NOT "科学"). 2-6 words each, no punctuation.

{_lang(output_lang)} (the title's topic phrase and the tags in this language;
keep proper names as-is.)

Return ONLY a JSON object, nothing else. Example:
{{"title": "时间的本质 · Jim Al-Khalili", "tags": ["量子退相干", "块状宇宙", "时间之箭"]}}

RECONSTRUCTION:
\"\"\"
{reconstruction}
\"\"\"
"""


def build_connections_prompt(
    this_title: str, this_claims: str, candidates_block: str, output_lang: str
) -> str:
    """Find MICRO, evidence-grounded connections to prior episodes.

    Each connection must name the SPECIFIC point + timestamp on BOTH sides and
    the specific relationship. Vague macro links ("both about physics") are
    forbidden. Returns [] if there is no genuine specific connection.
    """
    return f"""\
You are linking a NEW episode to PRIOR episodes in a personal knowledge base.
Find only GENUINE, SPECIFIC, MICRO-level connections.

IRON RULES:
- A connection must point to a SPECIFIC claim in the new episode (with its
  timestamp) AND a SPECIFIC claim in a prior episode (with its timestamp), and
  state the precise relationship between those two specific claims.
- BANNED: vague macro links like "both discuss physics" / "both about science"
  / "same field". If the only link is the broad topic, do NOT create it.
- Only use prior episodes from the candidate list below. Cite a prior episode by
  its exact "slug".
- Relationship label (`relation`): one short word/phrase such as 承接 / 延伸 /
  同构 / 印证 / 补充 / 对照 / 张力(or an equally precise label).
- If there is no genuine specific connection, return an empty array [].
- {_lang(output_lang)}

Return ONLY a JSON array. Each item:
{{"slug": "<prior episode slug>", "relation": "同构",
  "this_point": "本期在 [12:30] 说……(具体观点)",
  "that_point": "那期在 [52:09] 说……(具体观点)",
  "why": "两者具体如何关联(一句话,落到机制/结构层面,不要泛泛)"}}

NEW EPISODE: {this_title}
NEW EPISODE KEY CLAIMS:
\"\"\"
{this_claims}
\"\"\"

CANDIDATE PRIOR EPISODES (slug, title, tags, key claims):
\"\"\"
{candidates_block}
\"\"\"
"""


def build_mapping_prompt(
    reconstruction: str,
    plain_language: str,
    profile: str | None,
    output_lang: str,
) -> str:
    if profile:
        profile_block = f"""\
The listener has provided a personal profile describing their long-term
interests, current projects, writing direction, and existing views. Use it ONLY
to build the personal-mapping section. Do not flatter; if the episode does not
relate to something in the profile, do not force a connection.

LISTENER PROFILE:
\"\"\"
{profile}
\"\"\"
"""
        mapping_section = """\
## 个人映射
Connect the episode to this specific listener, based on their profile. Cover, as
relevant: how it relates to their long-term interests; how it connects to their
current projects; how it might enter their writing or product thinking; which
ideas are reusable as conceptual tools; which ideas CHALLENGE or update their
existing views; where it agrees with what they already believe.

CRITICAL: every mapping must point back to transcript evidence. Each mapped
point must cite the timestamp (or anchor phrase) in the episode it grows from.
Do not produce free-floating insight. If you cannot anchor it, drop it.
"""
    else:
        profile_block = (
            "No personal profile was provided. Skip the personal-mapping "
            "section entirely and produce only the evidence-grounded insights, "
            "concepts to save, and open questions."
        )
        mapping_section = ""

    return f"""\
You now have a faithful reconstruction and a plain-language re-telling of an
episode (below). This is the final layer. It runs LAST and only on top of the
verified earlier layers. Your job: extract evidence-grounded insight and, if a
profile is present, map the episode to this specific listener.

{_FIDELITY_RULES}

{profile_block}

{_lang(output_lang)}

Produce Markdown with EXACTLY these sections and headers, in this order
{"(include 个人映射)" if profile else "(skip 个人映射 -- no profile)"}:

## 证据锚定洞察
A list of the most important insights from the episode. For EACH:
- the insight, stated clearly
- a one-line plain-language explanation
- the supporting transcript segment / anchor (timestamp or short quote)
- confidence: 高 / 中 / 低
- whether it is 明确陈述 / 推断 / 猜测 (directly stated / inferred / speculative)
{mapping_section}
## 值得收藏的概念
A short list of concepts, frames, or mental models from this episode worth
saving into a personal knowledge system, each with a one-line description and
its anchor.

## 待追踪的问题
Open questions or threads worth tracking later -- things the episode raised but
did not resolve, or directions worth following up.

FAITHFUL RECONSTRUCTION:
\"\"\"
{reconstruction}
\"\"\"

PLAIN-LANGUAGE RE-TELLING:
\"\"\"
{plain_language}
\"\"\"
"""
