"""Storage layer for AgentGit.

Manages the ``.agentgit`` working directory:
snapshots, index, agent registry and configuration.
All data is stored as plain JSON + file copies, so it is fully
human-readable and zero-dependency.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

AGENTGIT_DIR = ".agentgit"
INDEX_FILE = "index.json"
AGENTS_FILE = "agents.json"
CONFIG_FILE = "config.json"
SNAPSHOTS_DIR = "snapshots"
FILES_DIR = "files"

# Default ignore patterns applied on top of the user's .gitignore.
DEFAULT_IGNORES = {
    ".agentgit",
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".cache",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.log",
    ".env",
    ".env.local",
    "target",
    ".idea",
    ".vscode",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _gen_id() -> str:
    return uuid.uuid4().hex[:12]


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_ignored(rel_path: str, ignore_patterns: set) -> bool:
    """Check whether a relative path matches any ignore pattern."""
    parts = rel_path.replace("\\", "/").split("/")
    for pat in ignore_patterns:
        pat = pat.strip()
        if not pat:
            continue
        if pat.startswith("#") or pat.startswith("!"):
            continue
        pat = pat.rstrip("/")
        # Directory pattern (e.g. node_modules) matches any segment.
        if "/" not in pat and pat in parts:
            return True
        # Glob patterns.
        if pat.startswith("*.") and any(p.endswith(pat[1:]) for p in parts):
            return True
        # Full relative path match.
        if pat == rel_path.replace("\\", "/"):
            return True
        # Prefix directory match.
        if rel_path.replace("\\", "/").startswith(pat + "/"):
            return True
    return False


def load_gitignore(repo_path: Path) -> set:
    """Load patterns from .gitignore if present."""
    patterns = set()
    gitignore = repo_path / ".gitignore"
    if gitignore.exists():
        try:
            for line in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.add(line)
        except OSError:
            pass
    return patterns


def scan_files(repo_path: Path) -> Dict[str, str]:
    """Scan the repository and return {relative_path: sha256} for tracked files."""
    ignore = set(DEFAULT_IGNORES) | load_gitignore(repo_path)
    result: Dict[str, str] = {}
    for root, dirs, files in os.walk(repo_path):
        root_path = Path(root)
        # Prune ignored directories.
        dirs[:] = [
            d
            for d in dirs
            if not is_ignored(str((root_path / d).relative_to(repo_path)), ignore)
        ]
        for name in files:
            full = root_path / name
            rel = str(full.relative_to(repo_path)).replace("\\", "/")
            if is_ignored(rel, ignore):
                continue
            try:
                result[rel] = sha256_file(full)
            except OSError:
                continue
    return result


class AgentGitRepo:
    """High-level repository handle bound to a working directory."""

    def __init__(self, repo_path: str | os.PathLike):
        self.path = Path(repo_path).resolve()
        self.agentgit_dir = self.path / AGENTGIT_DIR

    # ------------------------------------------------------------------ #
    # init / layout
    # ------------------------------------------------------------------ #
    def init(self) -> bool:
        """Initialise the .agentgit directory. Returns True if newly created."""
        if self.agentgit_dir.exists():
            return False
        (self.agentgit_dir / SNAPSHOTS_DIR).mkdir(parents=True)
        self._write_json(INDEX_FILE, {"version": 1, "created_at": _now(), "snapshots": []})
        self._write_json(AGENTS_FILE, {"agents": {}})
        self._write_json(
            CONFIG_FILE,
            {
                "auto_watch": True,
                "watch_interval": 3,
                "max_snapshots": 100,
                "store_full_files": True,
            },
        )
        return True

    # ------------------------------------------------------------------ #
    # json helpers
    # ------------------------------------------------------------------ #
    def _json_path(self, name: str) -> Path:
        return self.agentgit_dir / name

    def _read_json(self, name: str, default: Any) -> Any:
        p = self._json_path(name)
        if not p.exists():
            return default
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default

    def _write_json(self, name: str, data: Any) -> None:
        p = self._json_path(name)
        p.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ------------------------------------------------------------------ #
    # index
    # ------------------------------------------------------------------ #
    def load_index(self) -> Dict[str, Any]:
        return self._read_json(INDEX_FILE, {"version": 1, "created_at": _now(), "snapshots": []})

    def save_index(self, index: Dict[str, Any]) -> None:
        self._write_json(INDEX_FILE, index)

    def list_snapshots(self) -> List[Dict[str, Any]]:
        index = self.load_index()
        return index.get("snapshots", [])

    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        for snap in self.list_snapshots():
            if snap["id"] == snapshot_id or snap["id"].startswith(snapshot_id):
                return snap
        return None

    # ------------------------------------------------------------------ #
    # agents
    # ------------------------------------------------------------------ #
    def load_agents(self) -> Dict[str, Any]:
        return self._read_json(AGENTS_FILE, {"agents": {}})

    def save_agents(self, data: Dict[str, Any]) -> None:
        self._write_json(AGENTS_FILE, data)

    def record_agent(self, agent: str, snapshot_id: str) -> None:
        data = self.load_agents()
        agents = data.setdefault("agents", {})
        entry = agents.setdefault(agent, {"first_seen": _now(), "snapshots": [], "count": 0})
        entry["last_seen"] = _now()
        entry["count"] = entry.get("count", 0) + 1
        entry["snapshots"].append(snapshot_id)
        self.save_agents(data)

    # ------------------------------------------------------------------ #
    # snapshots
    # ------------------------------------------------------------------ #
    def create_snapshot(
        self,
        agent: Optional[str] = None,
        message: Optional[str] = None,
        parent: Optional[str] = None,
        store_full: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Create a snapshot of the current working tree."""
        if not self.agentgit_dir.exists():
            raise RuntimeError("Not an AgentGit repository. Run `agentgit init` first.")

        config = self._read_json(CONFIG_FILE, {})
        if store_full is None:
            store_full = config.get("store_full_files", True)

        files = scan_files(self.path)
        snap_id = _gen_id()
        snap_dir = self.agentgit_dir / SNAPSHOTS_DIR / snap_id
        files_dir = snap_dir / FILES_DIR

        # Store file contents (full copies by default).
        stored_files: Dict[str, str] = {}
        if store_full:
            files_dir.mkdir(parents=True)
            for rel, digest in files.items():
                src = self.path / rel
                dst = files_dir / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                except OSError:
                    continue
                stored_files[rel] = digest
        else:
            # Store only changed files relative to parent snapshot.
            parent_manifest = None
            if parent:
                parent_snap = self.get_snapshot(parent)
                if parent_snap:
                    parent_manifest = self._load_manifest(parent_snap)
            changed = set(files.keys())
            if parent_manifest:
                parent_files = parent_manifest.get("files", {})
                changed = {
                    rel
                    for rel, digest in files.items()
                    if parent_files.get(rel) != digest
                }
                changed |= {rel for rel in parent_files if rel not in files}
            files_dir.mkdir(parents=True)
            for rel in changed:
                src = self.path / rel
                if not src.exists():
                    continue
                dst = files_dir / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                except OSError:
                    continue
            stored_files = {rel: files[rel] for rel in changed if rel in files}

        manifest = {
            "id": snap_id,
            "created_at": _now(),
            "agent": agent or "unknown",
            "message": message or "",
            "parent": parent,
            "file_count": len(files),
            "files": stored_files,
        }
        (snap_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        index = self.load_index()
        snapshots = index.setdefault("snapshots", [])
        snapshots.append(
            {
                "id": snap_id,
                "created_at": _now(),
                "agent": agent or "unknown",
                "message": message or "",
                "parent": parent,
                "file_count": len(files),
            }
        )
        max_snaps = config.get("max_snapshots", 100)
        if len(snapshots) > max_snaps:
            # Drop oldest snapshots (keep newest max_snaps).
            removed = snapshots[: len(snapshots) - max_snaps]
            snapshots[:] = snapshots[len(snapshots) - max_snaps :]
            for old in removed:
                old_dir = self.agentgit_dir / SNAPSHOTS_DIR / old["id"]
                if old_dir.exists():
                    shutil.rmtree(old_dir, ignore_errors=True)
        index["snapshots"] = snapshots
        self.save_index(index)

        if agent:
            self.record_agent(agent, snap_id)

        return manifest

    def _load_manifest(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        snap_dir = self.agentgit_dir / SNAPSHOTS_DIR / snapshot["id"]
        manifest_path = snap_dir / "manifest.json"
        if not manifest_path.exists():
            return {}
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def snapshot_files(self, snapshot: Dict[str, Any]) -> Dict[str, str]:
        """Return {relative_path: sha256} for the files captured in a snapshot."""
        manifest = self._load_manifest(snapshot)
        files = manifest.get("files", {})
        # For full snapshots, files dict holds every tracked file.
        return files

    # ------------------------------------------------------------------ #
    # diff / status
    # ------------------------------------------------------------------ #
    def status(self) -> Dict[str, Any]:
        """Report changes since the latest snapshot."""
        current = scan_files(self.path)
        snapshots = self.list_snapshots()
        if not snapshots:
            return {
                "tracked_files": len(current),
                "added": [],
                "modified": [],
                "deleted": [],
                "clean": True,
                "latest_snapshot": None,
            }
        latest = snapshots[-1]
        base = self.snapshot_files(latest)
        added, modified, deleted = self._compare(base, current)
        return {
            "tracked_files": len(current),
            "added": sorted(added),
            "modified": sorted(modified),
            "deleted": sorted(deleted),
            "clean": not (added or modified or deleted),
            "latest_snapshot": latest,
        }

    @staticmethod
    def _compare(base: Dict[str, str], current: Dict[str, str]):
        added = [rel for rel in current if rel not in base]
        deleted = [rel for rel in base if rel not in current]
        modified = [rel for rel in base if rel in current and base[rel] != current[rel]]
        return added, modified, deleted

    def diff(self, snapshot_id: str, target: Optional[str] = None) -> Dict[str, Any]:
        """Diff a snapshot against the current tree or another snapshot."""
        snap = self.get_snapshot(snapshot_id)
        if not snap:
            raise RuntimeError(f"Snapshot not found: {snapshot_id}")

        base = self.snapshot_files(snap)
        if target:
            target_snap = self.get_snapshot(target)
            if not target_snap:
                raise RuntimeError(f"Snapshot not found: {target}")
            current = self.snapshot_files(target_snap)
        else:
            current = scan_files(self.path)

        added, modified, deleted = self._compare(base, current)
        return {
            "snapshot": snap["id"],
            "created_at": snap["created_at"],
            "agent": snap["agent"],
            "message": snap["message"],
            "target": target,
            "added": sorted(added),
            "modified": sorted(modified),
            "deleted": sorted(deleted),
            "changed_count": len(added) + len(modified) + len(deleted),
        }

    def file_content(self, snapshot_id: str, rel_path: str) -> Optional[str]:
        """Read a file's content from a snapshot (for the diff viewer)."""
        snap = self.get_snapshot(snapshot_id)
        if not snap:
            return None
        snap_dir = self.agentgit_dir / SNAPSHOTS_DIR / snap["id"]
        f = snap_dir / FILES_DIR / rel_path
        if not f.exists():
            return None
        try:
            return f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    # ------------------------------------------------------------------ #
    # revert
    # ------------------------------------------------------------------ #
    def revert(self, snapshot_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Revert the working tree to a snapshot's state."""
        snap = self.get_snapshot(snapshot_id)
        if not snap:
            raise RuntimeError(f"Snapshot not found: {snapshot_id}")

        snap_dir = self.agentgit_dir / SNAPSHOTS_DIR / snap["id"]
        files_dir = snap_dir / FILES_DIR
        manifest = self._load_manifest(snap)
        snapshot_files = manifest.get("files", {})

        restored: List[str] = []
        removed: List[str] = []
        skipped: List[str] = []

        if files_dir.exists():
            for rel in snapshot_files:
                src = files_dir / rel
                dst = self.path / rel
                if not src.exists():
                    continue
                if dry_run:
                    restored.append(rel)
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                    restored.append(rel)
                except OSError:
                    skipped.append(rel)

        # Remove files that existed in the snapshot's parent context but not in it.
        current = scan_files(self.path)
        for rel in current:
            if rel in snapshot_files:
                continue
            if is_ignored(rel, DEFAULT_IGNORES):
                continue
            if dry_run:
                removed.append(rel)
                continue
            try:
                (self.path / rel).unlink()
                removed.append(rel)
            except OSError:
                skipped.append(rel)

        return {
            "snapshot": snap["id"],
            "dry_run": dry_run,
            "restored": sorted(restored),
            "removed": sorted(removed),
            "skipped": sorted(skipped),
        }
