"""Unit tests for AgentGit core functionality.

Run with:  python -m unittest discover -s tests -v
or:        python tests/test_core.py
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentgit.storage import AgentGitRepo, scan_files  # noqa: E402


class TestAgentGitCore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="agentgit_test_")
        self.repo_path = Path(self.tmp) / "work"
        self.repo_path.mkdir()
        (self.repo_path / "hello.txt").write_text("hello world\n", encoding="utf-8")
        (self.repo_path / "app.py").write_text("print('hi')\n", encoding="utf-8")
        self.repo = AgentGitRepo(self.repo_path)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_init(self):
        self.assertTrue(self.repo.init())
        self.assertFalse(self.repo.init())  # second init is a no-op
        self.assertTrue((self.repo.agentgit_dir / "index.json").exists())

    def test_scan_files(self):
        files = scan_files(self.repo_path)
        self.assertIn("hello.txt", files)
        self.assertIn("app.py", files)
        # .agentgit should be ignored
        self.repo.init()
        files = scan_files(self.repo_path)
        self.assertNotIn(".agentgit/index.json", files)

    def test_snapshot_and_log(self):
        self.repo.init()
        m = self.repo.create_snapshot(agent="Claude Code", message="first")
        self.assertEqual(m["agent"], "Claude Code")
        snaps = self.repo.list_snapshots()
        self.assertEqual(len(snaps), 1)
        self.assertEqual(snaps[0]["id"], m["id"])

    def test_status_clean_then_dirty(self):
        self.repo.init()
        self.repo.create_snapshot(agent="Codex", message="baseline")
        st = self.repo.status()
        self.assertTrue(st["clean"])
        # modify a file
        (self.repo_path / "hello.txt").write_text("changed!\n", encoding="utf-8")
        st = self.repo.status()
        self.assertFalse(st["clean"])
        self.assertIn("hello.txt", st["modified"])

    def test_diff(self):
        self.repo.init()
        self.repo.create_snapshot(agent="Codex", message="baseline")
        (self.repo_path / "new.txt").write_text("new\n", encoding="utf-8")
        (self.repo_path / "hello.txt").write_text("changed!\n", encoding="utf-8")
        snaps = self.repo.list_snapshots()
        d = self.repo.diff(snaps[0]["id"])
        self.assertIn("new.txt", d["added"])
        self.assertIn("hello.txt", d["modified"])

    def test_revert(self):
        self.repo.init()
        self.repo.create_snapshot(agent="Cursor", message="baseline")
        (self.repo_path / "hello.txt").write_text("changed!\n", encoding="utf-8")
        (self.repo_path / "extra.txt").write_text("extra\n", encoding="utf-8")
        snaps = self.repo.list_snapshots()
        result = self.repo.revert(snaps[0]["id"])
        self.assertIn("hello.txt", result["restored"])
        self.assertIn("extra.txt", result["removed"])
        self.assertEqual(
            (self.repo_path / "hello.txt").read_text(encoding="utf-8"),
            "hello world\n",
        )
        self.assertFalse((self.repo_path / "extra.txt").exists())

    def test_revert_dry_run(self):
        self.repo.init()
        self.repo.create_snapshot(agent="Gemini CLI", message="baseline")
        (self.repo_path / "hello.txt").write_text("changed!\n", encoding="utf-8")
        snaps = self.repo.list_snapshots()
        result = self.repo.revert(snaps[0]["id"], dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertIn("hello.txt", result["restored"])
        # file must NOT change on dry run
        self.assertEqual(
            (self.repo_path / "hello.txt").read_text(encoding="utf-8"),
            "changed!\n",
        )

    def test_agent_registry(self):
        self.repo.init()
        self.repo.create_snapshot(agent="Claude Code", message="a")
        self.repo.create_snapshot(agent="Codex", message="b")
        agents = self.repo.load_agents()["agents"]
        self.assertEqual(agents["Claude Code"]["count"], 1)
        self.assertEqual(agents["Codex"]["count"], 1)


class TestIgnore(unittest.TestCase):
    def test_is_ignored(self):
        from agentgit.storage import is_ignored

        ignores = {".agentgit", ".git", "node_modules", "*.pyc", "dist"}
        self.assertTrue(is_ignored(".agentgit/index.json", ignores))
        self.assertTrue(is_ignored("node_modules/pkg/index.js", ignores))
        self.assertTrue(is_ignored("src/foo.pyc", ignores))
        self.assertTrue(is_ignored("dist/bundle.js", ignores))
        self.assertFalse(is_ignored("src/app.py", ignores))


if __name__ == "__main__":
    unittest.main(verbosity=2)
