"""Polling file watcher for AgentGit auto-snapshots.

Zero-dependency watcher that monitors the working tree and creates
automatic snapshots when changes are detected.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Dict, Optional

from .storage import AgentGitRepo, scan_files


class AgentGitWatcher:
    """Poll-based watcher that triggers auto-snapshots on file changes."""

    def __init__(
        self,
        repo: AgentGitRepo,
        interval: float = 3.0,
        on_change: Optional[Callable[[Dict], None]] = None,
        agent: Optional[str] = None,
        quiet: bool = False,
    ):
        self.repo = repo
        self.interval = max(0.5, float(interval))
        self.on_change = on_change
        self.agent = agent
        self.quiet = quiet
        self._last_state: Optional[Dict[str, str]] = None
        self._last_change = 0.0
        self._debounce = 1.0

    def _log(self, msg: str) -> None:
        if not self.quiet:
            print(f"[agentgit] {msg}")

    def run(self, max_iterations: Optional[int] = None) -> None:
        """Watch until interrupted (or until max_iterations for testing)."""
        self._log(f"Watching {self.repo.path} every {self.interval}s (Ctrl+C to stop)")
        iterations = 0
        try:
            while max_iterations is None or iterations < max_iterations:
                current = scan_files(self.repo.path)
                if self._last_state is not None and current != self._last_state:
                    now = time.time()
                    if now - self._last_change >= self._debounce:
                        self._last_change = now
                        self._snapshot()
                self._last_state = current
                iterations += 1
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self._log("Stopped by user.")

    def _snapshot(self) -> None:
        try:
            manifest = self.repo.create_snapshot(agent=self.agent, message="auto-snapshot")
            self._log(
                f"Auto-snapshot {manifest['id']} created "
                f"({manifest['file_count']} files tracked)"
            )
            if self.on_change:
                self.on_change(manifest)
        except Exception as exc:  # pragma: no cover - defensive
            self._log(f"Auto-snapshot failed: {exc}")
