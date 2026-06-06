"""Environment and configuration loading."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load the project .env by EXPLICIT path. Bare load_dotenv() relies on
# find_dotenv() walking the call stack, which fails under `python -c`, some test
# runners, and certain server launch contexts — silently leaving every setting
# at its default. An explicit path is robust everywhere (CLI, WebUI, scripts).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DEFAULT_MODEL = "gemini-2.5-pro"
DEFAULT_OUTPUT_LANG = "zh"
DEFAULT_PROFILE = "profile.md"


@dataclass
class Config:
    api_key: str
    model: str
    output_lang: str
    profile_path: str

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key and self.api_key != "your_key_here")


def load_config() -> Config:
    """Read configuration from environment variables (.env supported)."""
    return Config(
        api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        model=os.getenv("PODLENS_MODEL", DEFAULT_MODEL).strip(),
        output_lang=os.getenv("PODLENS_OUTPUT_LANG", DEFAULT_OUTPUT_LANG).strip(),
        profile_path=os.getenv("PODLENS_PROFILE", DEFAULT_PROFILE).strip(),
    )
