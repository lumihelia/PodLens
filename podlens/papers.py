"""Paper ingestion: PDF -> clean, quotable plain text + light metadata.

This is the papers analogue of transcript.py. PodLens's core pipeline is
source-agnostic (it interprets *text*); this module turns a research-paper PDF
into the same kind of clean text the transcript path produces, so the existing
three-stage engine can interpret it.

Design notes (validated on "The Era of Experience", Silver & Sutton, 11 pp):
- Many papers are typeset with tight kerning, so pdfplumber's default word
  splitting glues words together ("Westandon..."). x_tolerance=2 restores word
  boundaries reliably without over-splitting.
- Justified text hyphenates across line breaks ("unprece-\ndented"); we rejoin.
- Bare page-number lines and obvious running heads are dropped.

We deliberately do NOT try to perfectly reconstruct two-column / figure-heavy
layouts here. If a paper extracts poorly, the caller can fall back to pasting
text directly, or (future) hand the PDF to Gemini multimodally.
"""

import re
from pathlib import Path

# A line that is just a page number (optionally with surrounding whitespace).
_PAGE_NUM_RE = re.compile(r"^\s*\d{1,3}\s*$")
# Hyphen at a line break: "unprece-\ndented" -> "unprecedented".
_HYPHEN_BREAK_RE = re.compile(r"(\w)-\s*\n\s*(\w)")
# In-line wrapped hyphen joined with a space: "unprece- dented".
_HYPHEN_SPACE_RE = re.compile(r"(\w)-\s+(\w)")

_WORD_X_TOLERANCE = 2  # restores spaces on tight-kerned papers (see module doc)


def extract_pdf_text(path: str) -> str:
    """Extract clean, quotable plain text from a paper PDF.

    Raises RuntimeError with a readable message if pdfplumber is unavailable or
    the file cannot be read, so callers can surface it instead of a stack trace.
    """
    try:
        import pdfplumber
    except ImportError as exc:  # pragma: no cover - environment guard
        raise RuntimeError(
            "pdfplumber is required to read PDFs. Install it with "
            "'pip install pdfplumber'."
        ) from exc

    p = Path(path)
    if not p.is_file():
        raise RuntimeError(f"PDF not found: {path}")

    pages: list[str] = []
    try:
        with pdfplumber.open(str(p)) as pdf:
            for page in pdf.pages:
                pages.append(_clean_page(page.extract_text(x_tolerance=_WORD_X_TOLERANCE) or ""))
    except Exception as exc:  # pdfplumber raises various errors on odd PDFs
        raise RuntimeError(f"could not read the PDF ({type(exc).__name__}: {exc})") from exc

    text = "\n".join(pages)
    text = _HYPHEN_BREAK_RE.sub(r"\1\2", text)
    text = _HYPHEN_SPACE_RE.sub(_rejoin_short_hyphen, text)
    return _collapse_blank_lines(text).strip()


def _clean_page(text: str) -> str:
    """Drop bare page-number lines from a single page's extracted text."""
    return "\n".join(
        line for line in text.split("\n") if not _PAGE_NUM_RE.match(line)
    )


def _rejoin_short_hyphen(match: re.Match) -> str:
    """Rejoin a wrapped hyphenated word, but leave real hyphenated compounds.

    A genuine wrap ("unprece- dented") is short; a real compound on its own line
    ("state-of-the-art") would be long, so only rejoin short spans.
    """
    whole = match.group(0)
    if len(whole) < 40:
        return match.group(1) + match.group(2)
    return whole


def _collapse_blank_lines(text: str) -> str:
    """Collapse 3+ blank lines into one, matching transcript.clean_transcript."""
    out: list[str] = []
    blank = 0
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if line.strip() == "":
            blank += 1
            if blank <= 1:
                out.append("")
        else:
            blank = 0
            out.append(line.rstrip())
    return "\n".join(out)


def load_paper(source: str) -> str:
    """Load paper text from a PDF path, a .txt/.md path, or raw pasted text.

    The escape hatch the plan promises: if extraction is poor, the user can pass
    already-clean text (a path to .txt/.md, or the raw string) and it is used
    as-is. PDFs go through extract_pdf_text.
    """
    p = None
    try:
        p = Path(source)
        is_file = p.is_file()
    except OSError:
        is_file = False

    if is_file and p.suffix.lower() == ".pdf":
        return extract_pdf_text(source)
    if is_file:
        return _collapse_blank_lines(p.read_text(encoding="utf-8")).strip()
    return _collapse_blank_lines(source).strip()


def _norm(s: str) -> str:
    """Normalize for quote matching: unify smart punctuation + whitespace."""
    s = (s.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"'))
    return re.sub(r"\s+", " ", s).strip().lower()


def quote_is_present(quote: str, source_text: str) -> bool:
    """Whether a verbatim quote anchor actually occurs in the source paper.

    The traceability guarantee: every anchor must be findable in the original.
    Normalizes smart quotes + whitespace so line-wrapped quotes still match, and
    tolerates footnote digits glued onto words in the source ("algorithm1" so a
    quote of "algorithm subsequently" still matches). Used as a deterministic
    safety net to catch hallucinated or altered quotes.
    """
    q = _norm(quote)
    if len(q) < 8:
        return False
    src = _norm(source_text)
    if q in src:
        return True
    # Footnote markers glue digits to a word in the extracted text; drop them.
    if q in re.sub(r"([a-z])\d{1,2}\b", r"\1", src):
        return True
    # Extraction sometimes glues a whole sentence into one space-less run (tight
    # kerning). Compare with ALL whitespace removed so a correctly-spaced quote
    # still matches a glued source span. (This is why a real quote could look
    # "missing" — the fault was our PDF extraction, not the quote.)
    nospace = lambda s: re.sub(r"\s+", "", s)
    return len(q) >= 12 and nospace(q) in nospace(src)


# An anchor quote: an English run inside double quotes that sits right after the
# section separator " · " (optionally inside backticks), per our anchor format.
_ANCHOR_QUOTE_RE = re.compile(r'["“]([A-Za-z][^"“”]{6,}?)["”]')


def verify_anchors(report_md: str, source_text: str) -> tuple[str, int, int]:
    """Guarantee traceability: neutralize any anchor quote not found in source.

    Scans the report for English quote anchors (the "Section · \"quote\"" form),
    checks each against the source paper, and replaces any that cannot be found
    with a 释义 marker so PodLens never publishes a verbatim quote the reader
    cannot locate in the original. Content is untouched; only the false
    verbatim-quote claim is downgraded. Returns (clean_md, n_ok, n_fixed).
    """
    quotes = set(_ANCHOR_QUOTE_RE.findall(report_md))
    n_ok = 0
    n_fixed = 0
    clean = report_md
    for q in quotes:
        # Only treat it as an anchor if it actually appears after a section "· ".
        is_anchor = re.search(r"·\s*`?[\"“]" + re.escape(q) + r"[\"”]", clean)
        if not is_anchor:
            continue
        if quote_is_present(q, source_text):
            n_ok += 1
            continue
        for quoted in (f'"{q}"', f"“{q}”"):
            if quoted in clean:
                clean = clean.replace(quoted, "(释义,非逐字引用)")
                n_fixed += 1
    return clean, n_ok, n_fixed
