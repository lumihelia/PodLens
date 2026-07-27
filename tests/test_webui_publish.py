import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from webui import server


def completed(returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess([], returncode, "", stderr)


class GitPublishTests(unittest.TestCase):
    @patch("webui.server._git")
    def test_publish_commit_is_scoped_and_excludes_ds_store(self, git) -> None:
        git.side_effect = [
            completed(),
            completed(returncode=1),
            completed(),
            completed(),
        ]

        pushed, message = server._git_publish("Test title")

        self.assertTrue(pushed)
        self.assertEqual(message, "已发布并推送上线。几分钟后 GitHub Pages 会更新。")
        add_args = git.call_args_list[0].args
        commit_args = git.call_args_list[2].args
        self.assertEqual(add_args[:3], ("add", "-A", "--"))
        self.assertIn(":(exclude)**/.DS_Store", add_args)
        self.assertIn("--", commit_args)
        self.assertIn("docs", commit_args)
        self.assertIn(".podlens", commit_args)
        self.assertIn(":(exclude)**/.DS_Store", commit_args)

    @patch("webui.server._git")
    def test_publish_stops_when_no_scoped_content_is_staged(self, git) -> None:
        git.side_effect = [completed(), completed()]

        pushed, message = server._git_publish("No changes")

        self.assertFalse(pushed)
        self.assertIn("没有新内容", message)
        self.assertEqual(git.call_count, 2)

    @patch("webui.server._git")
    def test_publish_reports_add_failure(self, git) -> None:
        git.return_value = completed(returncode=128, stderr="pathspec failed")

        pushed, message = server._git_publish("Broken")

        self.assertFalse(pushed)
        self.assertIn("git add 失败", message)

    def test_real_git_commit_preserves_unrelated_staged_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "remote.git"
            repo = root / "repo"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
            subprocess.run(["git", "init", "-b", "main", str(repo)], check=True, capture_output=True)

            def run(*args: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", *args], cwd=repo, check=True, capture_output=True, text=True
                )

            run("config", "user.name", "PodLens Test")
            run("config", "user.email", "podlens-test@example.invalid")
            run("remote", "add", "origin", str(remote))
            (repo / "docs").mkdir()
            (repo / ".podlens").mkdir()
            (repo / "docs" / "index.html").write_text("old", encoding="utf-8")
            (repo / "docs" / ".DS_Store").write_text("old", encoding="utf-8")
            (repo / ".podlens" / "item.md").write_text("old", encoding="utf-8")
            (repo / "unrelated.txt").write_text("old", encoding="utf-8")
            run("add", ".")
            run("commit", "-m", "initial")
            run("push", "-u", "origin", "main")

            (repo / "docs" / "index.html").write_text("new", encoding="utf-8")
            (repo / "docs" / ".DS_Store").write_text("changed", encoding="utf-8")
            (repo / ".podlens" / "item.md").write_text("new", encoding="utf-8")
            (repo / "unrelated.txt").write_text("staged", encoding="utf-8")
            run("add", "unrelated.txt")

            with patch.object(server, "ROOT", repo):
                pushed, _ = server._git_publish("Scoped")

            self.assertTrue(pushed)
            committed = run("show", "--format=", "--name-only", "HEAD").stdout.splitlines()
            self.assertEqual(set(committed), {".podlens/item.md", "docs/index.html"})
            staged = run("diff", "--cached", "--name-only").stdout.splitlines()
            self.assertEqual(staged, ["unrelated.txt"])
            unstaged = run("diff", "--name-only").stdout.splitlines()
            self.assertEqual(unstaged, ["docs/.DS_Store"])


if __name__ == "__main__":
    unittest.main()
