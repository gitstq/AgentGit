<div align="center">

# 🧬 AgentGit

**Lightweight Source Control Engine for AI Coding Agents**

Track every change your AI coding agents make. **Snapshot · Diff · Revert · Audit** — all local-first, zero-dependency, privacy-safe.

[English](README.md) · [简体中文](docs/README.zh-CN.md) · [繁體中文](docs/README.zh-TW.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)

</div>

---

## 🎉 Introduction

When you run multiple AI coding agents — **Claude Code, Codex, Cursor, Gemini CLI, Aider** — on the same codebase, it quickly becomes impossible to answer three simple questions:

- **Who** changed which files?
- **What** did each agent actually do?
- **How** do I undo a single agent's work without breaking everything else?

AgentGit is a **source control engine built for AI agents**. It snapshots your working tree, attributes changes to the agent that made them, and lets you diff or revert any point in time — all on your machine, with **zero dependencies** and **zero data leaving your device**.

> 💡 **Inspiration** — AgentGit was inspired by the rising demand for "source control for agents" (a hot topic on GitHub Trending) and the pain of managing parallel AI coding agents without a safety net. Unlike session loggers that only record *what commands were run*, AgentGit tracks *what files actually changed* — like `git`, but for your agents.

## ✨ Core Features

- 🧠 **Snapshot the working tree** — capture the full state of your project in one command, with a message and agent attribution.
- 🤖 **Agent attribution** — automatically detect running agents (Claude Code, Codex, Cursor, Gemini CLI, Aider, Windsurf, Copilot, and more) and tag each snapshot with its author.
- 🔍 **Diff at any point in time** — compare a snapshot against the current tree or against another snapshot; see added / modified / deleted files at a glance.
- ↩️ **One-command revert** — restore the working tree to any snapshot, with a safe `--dry-run` preview first.
- 👀 **Live status** — see exactly what changed since the last snapshot.
- ⏱️ **Auto-watch mode** — watch the directory and create snapshots automatically the moment files change.
- 🖥️ **Local web dashboard** — a polished, zero-dependency dashboard to browse the timeline, inspect diffs and manage agents, served from your own machine.
- 🔒 **Privacy-first** — everything runs locally. No cloud, no telemetry, no accounts.
- 🪶 **Zero dependencies** — pure Python standard library. Runs on Windows, macOS and Linux.

## 🚀 Quick Start

### Requirements

- **Python 3.8+** (no third-party packages needed)

### Installation

```bash
# Option A — install from source (recommended)
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
pip install .

# Option B — run without installing
python bin/agentgit --help
```

### First 60 seconds

```bash
cd your-project

# 1. Initialise an AgentGit repository
agentgit init

# 2. Create your first snapshot
agentgit snapshot -a "Claude Code" -m "baseline before refactor"

# 3. Let an agent work, then check what changed
agentgit status

# 4. See the full history
agentgit log
```

## 📖 Detailed Usage Guide

### Commands overview

| Command | Description |
| --- | --- |
| `agentgit init` | Initialise an AgentGit repository (creates `.agentgit/`) |
| `agentgit snapshot [-a AGENT] [-m MSG]` | Create a snapshot of the working tree |
| `agentgit log [-n N]` | List snapshot history |
| `agentgit status` | Show changes since the latest snapshot |
| `agentgit diff <id> [--target <id>]` | Diff a snapshot against current tree or another snapshot |
| `agentgit revert <id> [--dry-run]` | Revert the working tree to a snapshot |
| `agentgit agents` | Detect AI coding agents on this machine |
| `agentgit watch [-i SEC] [-a AGENT]` | Watch the tree and auto-snapshot on changes |
| `agentgit serve [--port 8765]` | Start the local web dashboard |

### Typical workflow

```bash
# Baseline before a risky agent task
agentgit snapshot -a "Codex" -m "baseline"

# ... run your agent ...

# Inspect what it changed
agentgit status
agentgit diff <snapshot-id>

# Not happy? Revert just that work
agentgit revert <snapshot-id> --dry-run   # preview first
agentgit revert <snapshot-id>             # apply
```

### Web dashboard

```bash
agentgit serve --open
# → http://127.0.0.1:8765/
```

The dashboard lets you browse the snapshot timeline, inspect file-level diffs, detect agents, create snapshots and revert — all from a clean local UI.

### Auto-watch

```bash
# Auto-snapshot every time files change (poll every 2s)
agentgit watch -i 2 -a "Claude Code"
```

### Ignoring files

AgentGit respects your `.gitignore` and ships with sensible defaults (`node_modules`, `.git`, `__pycache__`, `dist`, `build`, `.env`, etc.). Files inside `.agentgit/` are always excluded.

## 💡 Design & Roadmap

### Design philosophy

- **Zero-dependency by design** — only the Python standard library, so it installs and runs anywhere, forever.
- **Human-readable storage** — snapshots are plain JSON + file copies under `.agentgit/`, fully inspectable and portable.
- **Agent-native** — built around the reality that multiple agents touch one codebase; attribution is a first-class concept.
- **Local-first** — your code and history never leave your machine.

### Roadmap

- [ ] **Incremental snapshots** — store only changed files to save disk space (config flag already supported).
- [ ] **Agent session integration** — auto-link snapshots to Claude Code / Codex session IDs.
- [ ] **Rich diff viewer** — syntax-highlighted unified diffs in the dashboard.
- [ ] **Branch-style timelines** — parallel agent workstreams with merge support.
- [ ] **MCP server** — expose AgentGit as an MCP tool so agents can self-manage snapshots.
- [ ] **Plugin hooks** — run commands before/after snapshots and reverts.

### Contributing directions

We welcome contributions around new agent detectors, dashboard polish, incremental storage, and translations. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📦 Packaging & Deployment

AgentGit is a **CLI tool / library** project — no Release binaries are required. Install it anywhere Python 3.8+ runs:

```bash
# Install from PyPI-style source
pip install .

# Or build a wheel for offline distribution
pip wheel . -w dist/
pip install dist/agentgit-1.0.0-py3-none-any.whl
```

**Compatibility**

- Windows 10/11, macOS 10.15+, Linux (any distro)
- Python 3.8 – 3.13
- No GPU, no network, no accounts required

## 🤝 Contributing

- 🐛 **Report bugs** — open an issue with reproduction steps.
- 💡 **Request features** — describe the problem and a proposed UX.
- 🔀 **Submit code** — fork, branch, commit (Angular convention), and open a PR.
- 🌐 **Translate** — help us add more README languages.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## 📄 License

[MIT](LICENSE) © AgentGit Contributors. Free to use, modify and distribute.
