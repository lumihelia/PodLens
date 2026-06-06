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


_LANG_NAME = {"zh": "Simplified Chinese", "en": "English"}


def build_translation_prompt(payload_json: str, target_lang: str) -> str:
    """Translate an already-written PUBLIC-layer bundle into target_lang.

    This is a TRANSLATION step (not re-interpretation): the interpretation was
    done faithfully in the source language; here we only carry it into the other
    language, preserving structure, timestamps, and names exactly.

    `payload_json` is a JSON object with: body (markdown str), title (str),
    tags (list[str]), editor_note (str), connections (list of objects with
    slug/relation/why/this_point/that_point). The model returns the SAME shape
    with every human-readable string translated and slugs left unchanged.
    """
    lang_name = _LANG_NAME.get(target_lang, target_lang)
    return f"""\
You are translating an already-written, faithful podcast interpretation into
{lang_name}. This is a TRANSLATION task: preserve the meaning exactly. Do not
add, remove, reinterpret, summarize, or editorialize. Keep the same structure.

STRICT RULES:
- Output {lang_name} only. Translate the prose AND the Markdown heading text.
- Keep EVERY timestamp EXACTLY as-is and in place: e.g. [12:34], [1:02:33], or
  ranges like [00:00-01:04]. Never alter, move, reorder, or drop a timestamp.
- Preserve all Markdown structure: heading levels (##, ###), list markers,
  numbering, line breaks, blank lines. Only the human-readable TEXT changes.
- Keep ALL personal names and proper nouns in their ORIGINAL form (e.g.
  "Jim Al-Khalili", "Dana Reyes"). Never transliterate or translate a name.
- Do not leave untranslated source-language words in the prose, except proper
  nouns / names.
- The input is a JSON object. Return the SAME JSON object with every string
  value translated. `tags` is a list of strings (translate each). `connections`
  is a list of objects: translate `relation`, `why`, `this_point`, `that_point`
  (keep the timestamps inside them intact) and leave `slug` UNCHANGED. Keep the
  connections in the SAME order.
- Return ONLY the JSON object. No code fences, no commentary.

INPUT JSON:
{payload_json}
"""


# --- Shared grounding rules --------------------------------------------------

_FIDELITY_RULES = """\
GROUNDING RULES (apply to every stage):
- Stay faithful to the transcript. Do not invent facts, names, numbers, or
  claims that are not supported by the text.
- When the transcript has timestamps, cite them (e.g. [12:34]) as evidence
  anchors. When it has none, quote a short verbatim phrase from the transcript
  as the anchor instead.
- Clearly separate what the speaker actually said from your own inference.
- Keep ALL personal names and proper nouns (people, hosts, guests, places,
  organizations) in their ORIGINAL form — for these English-language podcasts,
  the original English/Latin spelling (e.g. "Hakeem Oluseyi", "Jim Al-Khalili").
  Do NOT translate or transliterate a person's name into Chinese anywhere it
  appears; write the English name directly (no Chinese, no parentheses).
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

{_lang(output_lang)} (the title's topic phrase and the tags MUST be in this
language; keep proper names as-is.)

Return ONLY a JSON object, nothing else. Example{" (English)" if output_lang == "en" else ""}:
{('{"title": "The Nature of Time · Jim Al-Khalili", "tags": ["Quantum Decoherence", "Block Universe", "Arrow of Time"]}' if output_lang == "en" else '{"title": "时间的本质 · Jim Al-Khalili", "tags": ["量子退相干", "块状宇宙", "时间之箭"]}')}

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
    res_vocab = ("Corroborates / Extends / Parallel / Complements / Follows-on"
                 if output_lang == "en" else "印证 / 延伸 / 同构 / 补充 / 承接")
    ten_vocab = ("Refutes / Contradicts / Contrast / Tension"
                 if output_lang == "en" else "反驳 / 矛盾 / 对照 / 张力")
    return f"""\
You are linking a NEW item (a podcast/talk episode OR a research paper) to PRIOR
items in a personal knowledge base. The two may be of different kinds — a paper
can resonate with or contradict an episode, and vice versa; actively look for
those cross-kind links too.
Find only GENUINE, SPECIFIC, MICRO-level connections — of TWO kinds:

  • RESONANCE (`kind`: "resonance") — the two claims AGREE, corroborate, extend,
    or build on each other.
  • TENSION (`kind`: "tension") — the two claims genuinely CONFLICT: they make
    incompatible assertions about the SAME question. These are the most valuable
    links, but they are also the easiest to fake, so the bar is HIGHER (below).

IRON RULES (apply to BOTH kinds):
- A connection must point to a SPECIFIC claim in the new item (with its anchor)
  AND a SPECIFIC claim in a prior item (with its anchor), and state the precise
  relationship between those two specific claims. An anchor is a timestamp like
  [12:34] for an audio/video episode, OR a section name + a short verbatim source
  quote for a paper (papers have NO timestamps — never invent one; use the
  section + quote exactly as given in the claims).
- BANNED: vague macro links like "both discuss physics" / "both about science"
  / "same field". If the only link is the broad topic, do NOT create it.
- Only use prior episodes from the candidate list below. Cite a prior episode by
  its exact "slug".
- `relation`: one short word/phrase IN THE OUTPUT LANGUAGE.
  For resonance use: {res_vocab}. For tension use: {ten_vocab}.
- `this_point` and `that_point` must contain ONLY the anchor (a timestamp, or a
  section + short source quote) and the claim itself. Do NOT prefix them with
  "本期"/"那期"/"this episode"/"that episode" — the page adds the correct label
  depending on which page it shows on.

EXTRA RULES FOR TENSION (do not manufacture disagreement):
- The two claims must address the SAME underlying question or object. Two claims
  about DIFFERENT scopes, levels, definitions, or contexts are NOT a conflict
  (e.g. one about the quantum scale and one about the cosmological scale do NOT
  conflict just because both mention "scale"). If the only "conflict" is
  different topic / scope / emphasis, do NOT create it.
- `why` must explain EXACTLY what is incompatible between the two specific
  claims — not merely that they "differ".
- Set `conflict_type`:
    "genuine"  — the two claims, as stated, cannot both be true.
    "apparent" — they appear to conflict but actually differ in scope /
                 definition / context; in `why`, name that difference.
  When unsure, prefer "apparent".
- For resonance items, omit `conflict_type` (or set it to "").

- If there is no genuine specific connection of either kind, return [].
- {_lang(output_lang)}

Return ONLY a JSON array. Each item:
{{"slug": "<prior episode slug>", "kind": "tension", "relation": "{('Refutes' if output_lang=='en' else '反驳')}",
  "conflict_type": "genuine",
  "this_point": "[12:30] …(本集里的具体观点,不要写'本期')",
  "that_point": "[52:09] …(那一集里的具体观点,不要写'那期')",
  "why": "两者具体如何冲突/呼应(一句话,落到机制/结构层面,不要泛泛)"}}

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


# --- Paper prompts -----------------------------------------------------------
# Papers reuse PodLens's three-stage philosophy, but a paper is not a podcast:
# it has structure (problem/method/evidence/limits), no timestamps, and far more
# jargon for a non-academic reader. So the stages are paper-shaped and the anchor
# is "section + a short VERBATIM English source quote" (the reader can search it
# in the PDF) instead of a timestamp. Output is Chinese (the reader's language);
# the public layer is translated to English at publish time, like episodes.

_PAPER_ANCHOR_RULE = (
    "锚点规则(关键):每一处证据锚点都要给出「章节名 · \"英文原文短引用\"」。"
    "引用必须是论文里一字不差的英文原文(5-12 个单词),即使你的解读是中文,"
    "引用也保持英文原文不翻译——这样读者能直接在 PDF 里检索到那句话。"
    "若要标一整段,用「该段开头三个词 … 该段结尾三个词」的形式。不要编造或改写引用。"
)

_PAPER_FIDELITY = (
    "忠实规则:只依据下面给出的论文原文,不臆造事实、数据、结论或文中没有的说法。"
    "把论文实际说的,与你自己的推断,清楚分开。人名、机构名、专有名词一律保留英文原形,"
    "不要音译成中文。不堆砌口号和励志填充。除了要求的 Markdown 章节,不要写任何开场白或结语。"
    "用简体中文输出;正文不要夹杂未翻译的普通英文词(专有名词和上述英文引用除外)。"
)


def build_paper_reconstruction_prompt(paper: str) -> str:
    return (
        "你是一位严谨的研究者,正在为一篇学术论文做忠实还原。这是「保真层」:"
        "低解读、高忠实。先不要用大白话解释,也先不要做个人联系。\n\n"
        + _PAPER_FIDELITY + "\n\n" + _PAPER_ANCHOR_RULE + "\n\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变:\n\n"
        "## 这篇论文讲了什么\n"
        "几句话忠实概述:论文的主题、作者、它要回答的核心问题、它的中心主张、"
        "以及整体论证脉络。像高质量的读书笔记,不带个人解读。\n\n"
        "## 论文骨架\n"
        "拆出这篇论文的结构,逐条说明(每条尽量带锚点):它在解决什么问题;"
        "核心主张是什么;用什么方式来论证(实验/推理/案例/类比等,position paper 就说明它的论证链);"
        "拿出了哪些证据或例子;它自己承认的边界或局限在哪。\n\n"
        "## 核心论点清单\n"
        "编号列出这篇论文最关键的论点(把紧密相关的合并成一条,别把一个意思拆成多条;"
        "一般 6-10 条)。每一条给出:\n"
        "- 论点本身(忠实陈述)\n"
        "- 锚点(章节 · 英文原文短引用)\n"
        "- 类型,取其一:事实 / 主张 / 例子 / 预测 / 定义 / 反驳\n"
        "- 若有,作者表达的不确定或保留(一行)\n\n"
        "论文原文:\n\"\"\"\n" + paper + "\n\"\"\"\n"
    )


def build_paper_plain_language_prompt(paper: str, reconstruction: str) -> str:
    return (
        "你现在有了一篇论文的忠实还原(见下),以及论文原文。你的任务是「大白话层」:"
        "像一个聪明而诚实的朋友坐在读者旁边,把门槛降下来,但不简化掉内容、也不偏离原文。"
        "读者几乎没读过论文、且英文吃力,所以你要特别照顾零基础的人。\n\n"
        + _PAPER_FIDELITY + "\n\n" + _PAPER_ANCHOR_RULE + "\n\n"
        "这一层的额外要求:\n"
        "- 把术语翻成日常语言,必要时用贴切的比喻(但不能歪曲)。\n"
        "- 把复杂推理压成清晰的因果链。\n"
        "- 遇到反直觉的地方,直说它为什么反直觉。\n"
        "- 保留原文的论证顺序,不要重排逻辑。\n"
        "- 不要寒暄,不要对读者打招呼,直接进入内容。\n\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变:\n\n"
        "## 大白话重讲\n"
        "先用一两句点出「这篇在跟什么较劲、为什么值得在意」,再顺着论文把它讲清楚。"
        "是流动的重述,不是要点罗列,可以有声音和节奏,但每一步都贴着论文的真实内容。\n\n"
        "## 术语小词典\n"
        "挑出 5-10 个理解这篇论文绕不开的关键术语,每个用一句人话解释清楚,并带上锚点"
        "(它在论文哪里被用到)。这是给零基础读者的脚手架。\n\n"
        "## 这篇之前与之后\n"
        "帮没有领域背景的读者把这篇放回它所在的脉络:在这篇之前,这个领域大体默认/相信什么;"
        "这篇主张改变或挑战了什么。两段话即可,带锚点。\n\n"
        "## 最值得读原文的几段\n"
        "指出 3-5 处最值得读者亲自去读英文原文的地方:给出锚点,并说明为什么值得"
        "(信息密度高、是论证的关键转折、或措辞本身重要)。\n\n"
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n\n"
        "论文原文(用于核对与引用):\n\"\"\"\n" + paper + "\n\"\"\"\n"
    )


def build_paper_mapping_prompt(reconstruction: str, plain: str,
                               profile: str | None) -> str:
    if profile:
        profile_block = (
            "读者提供了个人档案,描述他长期的兴趣、当前的项目、写作方向和已有的看法。"
            "只用它来写「个人映射」一节。不要奉承;若这篇论文和档案里的东西没有真实关联,"
            "就不要硬扯。\n\n读者档案:\n\"\"\"\n" + profile + "\n\"\"\"\n"
        )
        mapping_section = (
            "## 个人映射\n"
            "把这篇论文连接到这位具体的读者(依据他的档案)。可涵盖:它和他长期兴趣的关系;"
            "和他当前项目的关系;可能如何进入他的写作或产品思考;哪些想法可作为可复用的概念工具;"
            "哪些想法挑战或更新了他已有的看法;哪里印证了他已经相信的东西。\n"
            "关键:每一条映射都必须回指论文证据,带上锚点(章节 · 英文原文引用)。"
            "锚不住的洞察就删掉,不要悬空。\n\n"
        )
    else:
        profile_block = (
            "读者没有提供个人档案。跳过「个人映射」一节,只产出证据锚定洞察、"
            "值得收藏的概念、待追踪的问题。\n"
        )
        mapping_section = ""

    return (
        "你现在有了一篇论文的忠实还原和大白话重讲(见下)。这是最后一层,只在前面已核验的层之上运行。"
        "你的任务:提炼有证据支撑的洞察;若有档案,则把论文映射到这位具体读者。\n\n"
        + _PAPER_FIDELITY + "\n\n" + _PAPER_ANCHOR_RULE + "\n\n" + profile_block + "\n"
        "产出 Markdown,严格使用以下章节和标题,顺序不变"
        + ("(包含「个人映射」):" if profile else "(无档案,跳过「个人映射」):") + "\n\n"
        "## 证据锚定洞察\n"
        "列出这篇论文最重要的几条洞察。每条给出:洞察本身;一行大白话解释;支撑的锚点"
        "(章节 · 英文原文引用);置信度 高/中/低;以及它是 明确陈述 / 推断 / 猜测。\n\n"
        + mapping_section +
        "## 值得收藏的概念\n"
        "几个值得收进个人知识体系的概念、框架或心智模型,每个一行描述加锚点。\n\n"
        "## 待追踪的问题\n"
        "论文提出但未解决、或值得后续跟进的开放问题与线索。\n\n"
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n\n"
        "大白话重讲:\n\"\"\"\n" + plain + "\n\"\"\"\n"
    )


def build_paper_metadata_prompt(reconstruction: str) -> str:
    return (
        "从下面的忠实还原中,产出一个标题和 3-6 个具体的主题标签。\n"
        "标题格式:一个精炼的主题短语,然后 \" · \",然后第一作者的英文原名"
        "(例:\"经验时代:超越人类数据的强化学习 · David Silver\")。人名保留英文原形,不要音译。\n"
        "标签:3-6 个论文真正讨论的具体概念/术语(中文),每个 2-6 字,不要标点,不要写宽泛学科名。\n"
        "只返回一个 JSON 对象,例如:"
        '{"title": "主题短语 · David Silver", "tags": ["经验流", "奖励接地", "世界模型"]}\n\n'
        "忠实还原:\n\"\"\"\n" + reconstruction + "\n\"\"\"\n"
    )
