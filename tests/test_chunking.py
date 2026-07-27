import unittest

from podlens.chunking import estimate_tokens, needs_chunking, split_transcript


class ChunkingTests(unittest.TestCase):
    def test_gemini_never_chunks(self) -> None:
        transcript = ("[00:01] long line\n" * 100_000).strip()
        self.assertFalse(needs_chunking(transcript, "gemini"))
        self.assertEqual(split_transcript(transcript, "gemini"), [transcript])

    def test_deepseek_chunks_and_reassembles_without_loss(self) -> None:
        transcript = "\n".join(
            f"[{i // 60:02d}:{i % 60:02d}] " + ("evidence " * 40)
            for i in range(400)
        )
        chunks = split_transcript(transcript, "deepseek")

        self.assertGreater(len(chunks), 1)
        self.assertEqual("\n".join(chunks), transcript)
        self.assertTrue(all(estimate_tokens(chunk) < 50_000 for chunk in chunks))

    def test_long_single_line_falls_back_to_word_splitting(self) -> None:
        transcript = " ".join(f"word{i}" for i in range(30_000))
        chunks = split_transcript(transcript, "deepseek")

        self.assertGreater(len(chunks), 1)
        self.assertEqual(" ".join(chunks), transcript)


if __name__ == "__main__":
    unittest.main()
