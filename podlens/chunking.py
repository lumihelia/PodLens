"""Transcript chunking for providers with small context windows.

Gemini's context window (1M+ tokens) means a typical podcast transcript always
fits in one call, so this module is a no-op for it. DeepSeek's window (~64K
tokens) does not, for multi-hour episodes. Splitting happens on LINE
boundaries (each transcript line is one subtitle cue / one "[mm:ss] text"
entry), so a timestamp is never separated from its text.

Used by `interpreter.py` for the map-reduce pattern: split -> interpret each
chunk independently -> one synthesis call merges the partial results.
"""

# Conservative token estimate: ~1.5 chars/token covers CJK (denser per token)
# without underestimating Latin text (which is even less token-dense per char).
_CHARS_PER_TOKEN = 1.5

# Total prompt-token budget per call, leaving room for the provider's output
# reservation and a safety margin under its real context window. Gemini has
# no entry here -- its window is large enough that chunking is never needed.
CONTEXT_BUDGET_TOKENS = {
    "deepseek": 50_000,  # vs a ~64K window; leaves ~14K for output + margin
}

# Tokens reserved for prompt instructions/headers (estimated generously).
_PROMPT_OVERHEAD_TOKENS = 2_000


def estimate_tokens(text: str) -> int:
    return max(1, int(len(text) / _CHARS_PER_TOKEN))


def needs_chunking(transcript: str, provider: str, extra_tokens: int = 0) -> bool:
    """Whether `transcript` plus any extra context (e.g. a reconstruction
    already in the prompt) would likely exceed `provider`'s budget in one call."""
    budget = CONTEXT_BUDGET_TOKENS.get(provider)
    if budget is None:
        return False
    available = budget - _PROMPT_OVERHEAD_TOKENS - extra_tokens
    return estimate_tokens(transcript) > available


def _split_long_line(line: str, max_tokens: int) -> list[str]:
    """Fallback for a single line that alone exceeds the budget (e.g. a giant
    paragraph in a plain .txt transcript with no line breaks). Splits on
    whitespace; loses nothing, just breaks one long line into several."""
    words = line.split(" ")
    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0
    for word in words:
        word_tokens = estimate_tokens(word) + 1
        if current and current_tokens + word_tokens > max_tokens:
            pieces.append(" ".join(current))
            current = []
            current_tokens = 0
        current.append(word)
        current_tokens += word_tokens
    if current:
        pieces.append(" ".join(current))
    return pieces or [line]


def split_transcript(transcript: str, provider: str, extra_tokens: int = 0) -> list[str]:
    """Split a transcript into chunks that fit `provider`'s context budget.

    Returns `[transcript]` unchanged if it already fits in one call (this is
    the common case -- short episodes, or any provider not in
    CONTEXT_BUDGET_TOKENS).
    """
    budget = CONTEXT_BUDGET_TOKENS.get(provider)
    if budget is None or not needs_chunking(transcript, provider, extra_tokens):
        return [transcript]

    max_tokens = budget - _PROMPT_OVERHEAD_TOKENS - extra_tokens
    lines: list[str] = []
    for line in transcript.split("\n"):
        if estimate_tokens(line) > max_tokens:
            lines.extend(_split_long_line(line, max_tokens))
        else:
            lines.append(line)

    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0
    for line in lines:
        line_tokens = estimate_tokens(line) + 1
        if current and current_tokens + line_tokens > max_tokens:
            chunks.append("\n".join(current))
            current = []
            current_tokens = 0
        current.append(line)
        current_tokens += line_tokens
    if current:
        chunks.append("\n".join(current))
    return chunks
