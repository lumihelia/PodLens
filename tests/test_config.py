import os
import unittest
from unittest.mock import patch

from podlens.config import load_config


class ConfigTests(unittest.TestCase):
    def test_provider_default_model_is_used_when_override_is_blank(self) -> None:
        env = {
            "PODLENS_PROVIDER": "deepseek",
            "PODLENS_MODEL": "",
            "DEEPSEEK_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()

        self.assertEqual(config.provider, "deepseek")
        self.assertEqual(config.model, "deepseek-chat")

    def test_explicit_model_override_is_preserved(self) -> None:
        env = {
            "PODLENS_PROVIDER": "gemini",
            "PODLENS_MODEL": "gemini-2.5-flash",
            "GEMINI_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()

        self.assertEqual(config.model, "gemini-2.5-flash")


if __name__ == "__main__":
    unittest.main()
