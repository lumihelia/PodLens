import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PRIVATE_HEADINGS = (
    "证据锚定洞察",
    "个人映射",
    "值得收藏的概念",
    "待追踪的问题",
)


class StaticSiteTests(unittest.TestCase):
    def test_feeds_and_sitemap_are_valid_xml(self) -> None:
        for relative in ("feed.xml", "zh/feed.xml", "sitemap.xml"):
            with self.subTest(relative=relative):
                ET.parse(DOCS / relative)

    def test_manifest_items_have_bilingual_pages_and_sources(self) -> None:
        items = json.loads((DOCS / "manifest.json").read_text(encoding="utf-8"))["items"]
        self.assertGreater(len(items), 0)

        for item in items:
            section = "papers" if item.get("kind") == "paper" else "episodes"
            self.assertTrue(item.get("source_url"), item["slug"])
            self.assertTrue((DOCS / section / f"{item['slug']}.html").is_file())
            self.assertTrue((DOCS / "zh" / section / f"{item['slug']}.html").is_file())

    def test_private_layer_headings_are_not_published(self) -> None:
        public_files = list(DOCS.rglob("*.html"))
        public_files += list(DOCS.rglob("*.xml"))
        public_files += list(DOCS.rglob("*.json"))

        for path in public_files:
            text = path.read_text(encoding="utf-8")
            for heading in PRIVATE_HEADINGS:
                self.assertNotIn(heading, text, f"{heading} leaked into {path}")

    def test_merged_episode_keeps_legacy_redirects(self) -> None:
        old_slug = "alexei-efros-surface-deep-data-curious-robot"
        target = "https://lens.lumihelia.com/episodes/alexei-efros-surface-data-deep-data.html"
        for path in (
            DOCS / "episodes" / f"{old_slug}.html",
            DOCS / "en" / "episodes" / f"{old_slug}.html",
        ):
            with self.subTest(path=path):
                page = path.read_text(encoding="utf-8")
                self.assertIn(f'<meta http-equiv="refresh" content="0; url={target}">', page)
                self.assertIn(f'<link rel="canonical" href="{target}">', page)


if __name__ == "__main__":
    unittest.main()
