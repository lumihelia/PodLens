"""Core interpretation pipeline.

This module is deliberately decoupled from the CLI: it takes plain inputs and
returns a structured result, so a future web app or API can call `interpret()`
directly without touching any terminal code.

The pipeline runs three Gemini calls in order. Each later call is grounded in
the verified output of the earlier ones -- this is how PodLens enforces
"faithfulness before insight" at the architecture level, not just in prompt text.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from google import genai
from google.genai import types

from .config import Config
from .prompts import (
    build_connections_prompt,
    build_mapping_prompt,
    build_metadata_prompt,
    build_plain_language_prompt,
    build_reconstruction_prompt,
)
from .transcript import has_timestamps

# Temperatures rise with each stage: fidelity stays tight, mapping gets room.
_TEMP_RECONSTRUCTION = 0.2
_TEMP_PLAIN_LANGUAGE = 0.5
_TEMP_MAPPING = 0.6


@dataclass
class InterpretationResult:
    reconstruction: str
    plain_language: str
    mapping: str
    model: str
    had_timestamps: bool
    had_profile: bool
    tags: list[str] = field(default_factory=list)
    title: str = ""

    def to_markdown(self, title: str = "PodLens 解读") -> str:
        """Assemble the three stages into one ordered Markdown report."""
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        notes = []
        if not self.had_timestamps:
            notes.append("transcript 无时间戳,证据锚点改用原文短引用")
        if not self.had_profile:
            notes.append("未提供个人档案(profile.md),已跳过个人映射层")
        note_line = f"\n> 说明:{' ; '.join(notes)}\n" if notes else ""
        return (
            f"# {title}\n\n"
            f"> 由 PodLens 生成 · 模型 {self.model} · {stamp}\n"
            f"{note_line}\n"
            f"{self.reconstruction.strip()}\n\n"
            f"{self.plain_language.strip()}\n\n"
            f"{self.mapping.strip()}\n"
        )


def _make_client(config: Config) -> genai.Client:
    if not config.has_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your "
            "key, or get one free at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=config.api_key)


def _parse_json_list(text: str) -> list[str]:
    """Parse a JSON array of strings from a model response, tolerating fences."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t).rstrip("`").strip()
    start, end = t.find("["), t.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        data = json.loads(t[start : end + 1])
    except json.JSONDecodeError:
        return []
    return [str(x).strip() for x in data if str(x).strip()]


def _parse_json_obj(text: str) -> dict:
    """Parse a JSON object from a model response, tolerating code fences."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t).rstrip("`").strip()
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        return json.loads(t[start : end + 1])
    except json.JSONDecodeError:
        return {}


def _parse_json_objects(text: str) -> list[dict]:
    """Parse a JSON array of objects, tolerating code fences."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t).rstrip("`").strip()
    start, end = t.find("["), t.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        data = json.loads(t[start : end + 1])
    except json.JSONDecodeError:
        return []
    return [x for x in data if isinstance(x, dict)]


def find_connections(
    this_title: str,
    this_claims: str,
    candidates: list[dict],
    config: Config,
) -> list[dict]:
    """Find micro, evidence-grounded connections to prior episodes.

    `candidates` is a list of {slug, title, tags, claims}. Returns a list of
    connection dicts {slug, relation, this_point, that_point, why}, with slugs
    validated against the candidate set.
    """
    if not candidates or not this_claims.strip():
        return []
    blocks = []
    valid_slugs = set()
    for c in candidates:
        valid_slugs.add(c["slug"])
        tags = ", ".join(c.get("tags", []))
        blocks.append(
            f"--- slug: {c['slug']}\n标题: {c['title']}\n标签: {tags}\n"
            f"核心观点:\n{c.get('claims', '').strip()}\n"
        )
    candidates_block = "\n".join(blocks)

    client = _make_client(config)
    raw = _generate(
        client, config.model,
        build_connections_prompt(
            this_title, this_claims, candidates_block, config.output_lang
        ),
        _TEMP_MAPPING,
    )
    out = []
    for conn in _parse_json_objects(raw):
        slug = str(conn.get("slug", "")).strip()
        if slug in valid_slugs and conn.get("this_point") and conn.get("that_point"):
            out.append({
                "slug": slug,
                "relation": str(conn.get("relation", "关联")).strip(),
                "this_point": str(conn.get("this_point", "")).strip(),
                "that_point": str(conn.get("that_point", "")).strip(),
                "why": str(conn.get("why", "")).strip(),
            })
    return out


def extract_metadata(reconstruction: str, config: Config) -> dict:
    """Generate a title and 3-6 specific tags from the reconstruction.

    Returns {"title": str, "tags": list[str]}.
    """
    client = _make_client(config)
    raw = _generate(
        client, config.model,
        build_metadata_prompt(reconstruction, config.output_lang),
        _TEMP_RECONSTRUCTION,
    )
    obj = _parse_json_obj(raw)
    title = str(obj.get("title", "")).strip()
    tags = [str(t).strip() for t in obj.get("tags", []) if str(t).strip()][:6]
    return {"title": title, "tags": tags}


def _strip_preamble(text: str) -> str:
    """Drop any conversational preamble before the first Markdown heading.

    Models sometimes open a stage with chatter like "好的,我来..." before the
    first '## ' section. We assemble stages by concatenation, so that chatter
    would leak between sections. Keep only from the first heading onward.
    """
    idx = text.find("## ")
    if idx == -1:
        return text.strip()
    return text[idx:].strip()


def _generate(client: genai.Client, model: str, prompt: str, temperature: float) -> str:
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError(
            f"Model {model} returned an empty response. The transcript may be "
            "too short, or the request may have been blocked."
        )
    return _strip_preamble(text)


def build_prompts(
    transcript: str, profile: str | None, output_lang: str
) -> dict[str, str]:
    """Build all three stage prompts without calling the API (for --dry-run).

    Stage 2 and 3 prompts use placeholders for the not-yet-generated upstream
    outputs, so this shows prompt structure rather than the live chain.
    """
    recon = build_reconstruction_prompt(transcript, output_lang)
    plain = build_plain_language_prompt(
        transcript, "<STAGE 1 OUTPUT INSERTED AT RUNTIME>", output_lang
    )
    mapping = build_mapping_prompt(
        "<STAGE 1 OUTPUT INSERTED AT RUNTIME>",
        "<STAGE 2 OUTPUT INSERTED AT RUNTIME>",
        profile,
        output_lang,
    )
    return {"reconstruction": recon, "plain_language": plain, "mapping": mapping}


def interpret(
    transcript: str,
    profile: str | None,
    config: Config,
    on_stage: Callable[[str], None] | None = None,
) -> InterpretationResult:
    """Run the full three-stage interpretation.

    `on_stage` is an optional callback invoked with a human-readable stage name
    before each Gemini call, so callers can show progress.
    """
    client = _make_client(config)
    timestamps = has_timestamps(transcript)

    def note(stage: str) -> None:
        if on_stage:
            on_stage(stage)

    note("第 1/3 步:忠实还原 transcript")
    reconstruction = _generate(
        client,
        config.model,
        build_reconstruction_prompt(transcript, config.output_lang),
        _TEMP_RECONSTRUCTION,
    )

    note("第 2/3 步:大白话重讲")
    plain_language = _generate(
        client,
        config.model,
        build_plain_language_prompt(transcript, reconstruction, config.output_lang),
        _TEMP_PLAIN_LANGUAGE,
    )

    note("第 3/3 步:证据锚定洞察与个人映射")
    mapping = _generate(
        client,
        config.model,
        build_mapping_prompt(
            reconstruction, plain_language, profile, config.output_lang
        ),
        _TEMP_MAPPING,
    )

    note("生成标题与主题标签")
    meta = _parse_json_obj(
        _generate(
            client, config.model,
            build_metadata_prompt(reconstruction, config.output_lang),
            _TEMP_RECONSTRUCTION,
        )
    )
    gen_title = str(meta.get("title", "")).strip()
    gen_tags = [str(t).strip() for t in meta.get("tags", []) if str(t).strip()][:6]

    return InterpretationResult(
        reconstruction=reconstruction,
        plain_language=plain_language,
        mapping=mapping,
        model=config.model,
        had_timestamps=timestamps,
        had_profile=profile is not None,
        tags=gen_tags,
        title=gen_title,
    )
