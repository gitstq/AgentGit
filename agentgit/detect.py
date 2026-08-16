"""Agent detection for AgentGit.

Detects running AI coding agents on the local machine using only the
Python standard library (no psutil). Works on Linux, macOS and Windows.
"""

from __future__ import annotations

import glob
import os
import re
import subprocess
import sys
from typing import Dict, List

# Known AI coding agents and the process names / command fragments that
# identify them. Keys are the canonical agent names.
AGENT_SIGNATURES: Dict[str, List[str]] = {
    "Claude Code": ["claude", "claude-code", "claude_code"],
    "Codex": ["codex"],
    "Cursor": ["cursor"],
    "Gemini CLI": ["gemini"],
    "Aider": ["aider"],
    "OpenCode": ["opencode"],
    "Windsurf": ["windsurf", "codeium"],
    "Copilot": ["copilot"],
    "Cline": ["cline"],
    "Roo Code": ["roo-code", "roo"],
    "Cody": ["cody"],
    "Continue": ["continue"],
    "Qwen Code": ["qwen-code", "qwen"],
    "Kimi CLI": ["kimi"],
    "Augment Code": ["augment"],
    "Trae": ["trae"],
}

# Session / history files that indicate an agent has been used.
SESSION_PATTERNS = {
    "Claude Code": [
        os.path.expanduser("~/.claude/projects"),
        os.path.expanduser("~/.claude.json"),
    ],
    "Codex": [
        os.path.expanduser("~/.codex/sessions"),
        os.path.expanduser("~/.codex/history.jsonl"),
    ],
    "Cursor": [
        os.path.expanduser("~/.cursor"),
    ],
    "Gemini CLI": [
        os.path.expanduser("~/.gemini"),
    ],
    "Aider": [
        os.path.expanduser("~/.aider"),
    ],
    "Windsurf": [
        os.path.expanduser("~/.codeium/windsurf"),
    ],
}


def _running_processes() -> List[str]:
    """Return a list of running process command lines (best effort)."""
    names: List[str] = []
    if sys.platform.startswith("linux"):
        for pid in os.listdir("/proc"):
            if not pid.isdigit():
                continue
            try:
                with open(f"/proc/{pid}/comm", "r", encoding="utf-8", errors="ignore") as fh:
                    comm = fh.read().strip()
                if comm:
                    names.append(comm.lower())
                with open(f"/proc/{pid}/cmdline", "rb") as fh:
                    raw = fh.read().replace(b"\x00", b" ").decode("utf-8", errors="ignore")
                if raw.strip():
                    names.append(raw.lower())
            except OSError:
                continue
    else:
        try:
            if sys.platform == "darwin":
                out = subprocess.run(
                    ["ps", "-axo", "comm=", "command="],
                    capture_output=True, text=True, timeout=5,
                ).stdout
            else:
                out = subprocess.run(
                    ["wmic", "process", "get", "commandline"],
                    capture_output=True, text=True, timeout=5,
                ).stdout
            for line in out.splitlines():
                names.append(line.strip().lower())
        except (OSError, subprocess.SubprocessError):
            pass
    return names


def detect_running_agents() -> Dict[str, Dict]:
    """Detect which agents are currently running on the machine."""
    procs = _running_processes()
    found: Dict[str, Dict] = {}
    for agent, sigs in AGENT_SIGNATURES.items():
        for sig in sigs:
            if any(sig in p for p in procs):
                found[agent] = {"status": "running", "signature": sig}
                break
    return found


def detect_used_agents() -> Dict[str, Dict]:
    """Detect agents that have been used based on session/history files."""
    found: Dict[str, Dict] = {}
    for agent, patterns in SESSION_PATTERNS.items():
        for pat in patterns:
            if glob.glob(pat):
                found[agent] = {"status": "used", "evidence": pat}
                break
    return found


def detect_all() -> Dict[str, Dict]:
    """Combine running + used agent detection."""
    agents: Dict[str, Dict] = {}
    for name, info in detect_running_agents().items():
        agents[name] = info
    for name, info in detect_used_agents().items():
        if name not in agents:
            agents[name] = info
    return agents


def normalize_agent_name(name: str) -> str:
    """Map a user-supplied agent name to a canonical one."""
    name = name.strip()
    if not name:
        return "unknown"
    lower = name.lower()
    for canonical, sigs in AGENT_SIGNATURES.items():
        if lower == canonical.lower() or any(lower == s for s in sigs):
            return canonical
    return name
