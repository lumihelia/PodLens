"""Personal profile loading for the mapping layer."""

from pathlib import Path


def load_profile(path: str) -> str | None:
    """Load the user's personal profile text, or None if not present.

    The profile is only used in the final personal-mapping stage. If it is
    missing, PodLens still produces the faithful reconstruction and plain
    language layers, and skips personal mapping.
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
    text = p.read_text(encoding="utf-8").strip()
    return text or None


def save_profile(path: str, text: str) -> None:
    """Write the personal profile text to `path` (a LOCAL file only).

    The profile is never published; it only feeds the private personal-mapping
    stage. The next interpretation reads it fresh, so edits take effect at once.
    """
    content = text.strip()
    Path(path).write_text(content + "\n" if content else "", encoding="utf-8")
