"""Environment and configuration loading."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

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
