# 🧬 AgentGit v1.0.0

**Lightweight Source Control Engine for AI Coding Agents** — 零依赖、本地优先的 AI 编码代理源码控制引擎。

Track every change your AI coding agents make. Snapshot · Diff · Revert · Audit.

## ✨ What's New

This is the first stable release of AgentGit.

### Core Features
- 🧠 **Snapshot the working tree** — capture the full project state in one command, with message and agent attribution
- 🤖 **Agent attribution** — auto-detect running agents (Claude Code, Codex, Cursor, Gemini CLI, Aider, Windsurf, Copilot, and more) and tag each snapshot
- 🔍 **Diff at any point in time** — compare a snapshot against the current tree or another snapshot
- ↩️ **One-command revert** — restore the working tree to any snapshot, with safe `--dry-run` preview
- 👀 **Live status** — see exactly what changed since the last snapshot
- ⏱️ **Auto-watch mode** — auto-snapshot the moment files change
- 🖥️ **Local web dashboard** — polished zero-dependency dashboard (timeline, diff viewer, agent management)
- 🔒 **Privacy-first** — everything runs locally, no cloud, no telemetry, no accounts
- 🪶 **Zero dependencies** — pure Python standard library, Windows / macOS / Linux

### Commands
`init` · `snapshot` · `log` · `status` · `diff` · `revert` · `agents` · `watch` · `serve`

## 📦 Install

```bash
pip install agentgit-1.0.0-py3-none-any.whl
# or
pip install .
```

## 🧪 Verified

- 9/9 unit tests passing
- CLI end-to-end verified (init → snapshot → status → diff → revert → watch)
- Web dashboard + JSON API verified
- Wheel build verified

## 🔐 Checksum

```
SHA256 (agentgit-1.0.0-py3-none-any.whl) = 31e2b1dc90e5890068767ecc94ba7d34a7183d794e3482b4708c637051e6a6b9
```

## 📄 License

MIT © AgentGit Contributors
