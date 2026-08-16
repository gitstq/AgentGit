<div align="center">

# 🧬 AgentGit

**AI 编码代理源码控制引擎**

追踪你的 AI 编码代理做出的每一次改动。**快照 · 差异 · 回滚 · 审计** —— 全部本地优先、零依赖、隐私安全。

[English](../README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
[![Download](https://img.shields.io/badge/⬇%20Download-v1.0.0-2ea44f?style=for-the-badge)](https://github.com/gitstq/AgentGit/releases/tag/v1.0.0)

</div>

---

## 🎉 项目介绍

当你在同一个代码库上运行多个 AI 编码代理——**Claude Code、Codex、Cursor、Gemini CLI、Aider**——时，你很快就会回答不了三个简单的问题：

- **谁**改了哪些文件？
- 每个代理到底**做了什么**？
- 如何**撤销**某个代理的改动而不破坏其他东西？

AgentGit 就是**为 AI 代理打造的源码控制引擎**。它快照你的工作树、把改动归因到对应的代理，并让你随时 diff 或回滚到任意时间点——全部在你的机器上完成，**零依赖**、**数据不出设备**。

> 💡 **灵感来源** —— AgentGit 受 GitHub 热榜上"为 Agent 做源码控制"这一新兴需求的启发，也源于并行管理多个 AI 编码代理却缺乏安全网的痛点。与只记录"跑了什么命令"的会话日志工具不同，AgentGit 追踪的是"文件到底发生了什么变化"——就像 `git`，但专为你的代理而生。

## ✨ 核心特性

- 🧠 **工作树快照** —— 一条命令捕获项目完整状态，支持消息与代理归因。
- 🤖 **代理归因** —— 自动检测正在运行的代理（Claude Code、Codex、Cursor、Gemini CLI、Aider、Windsurf、Copilot 等），并为每个快照打上作者标签。
- 🔍 **任意时间点差异** —— 将快照与当前工作树或另一个快照对比，新增/修改/删除一目了然。
- ↩️ **一键回滚** —— 将工作树恢复到任意快照，支持安全的 `--dry-run` 预览。
- 👀 **实时状态** —— 一眼看清自上次快照以来发生了什么变化。
- ⏱️ **自动监听模式** —— 监听目录，文件一变就自动创建快照。
- 🖥️ **本地 Web 仪表盘** —— 精致、零依赖的本地仪表盘，浏览时间线、查看差异、管理代理。
- 🔒 **隐私优先** —— 一切都在本地运行，无云端、无遥测、无账号。
- 🪶 **零依赖** —— 纯 Python 标准库，Windows、macOS、Linux 全平台可用。

## 🚀 快速开始

### 环境要求

- **Python 3.8+**（无需任何第三方包）

### 安装步骤

```bash
# 方式 A —— 源码安装（推荐）
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
pip install .

# 方式 B —— 免安装直接运行
python bin/agentgit --help
```

### 60 秒上手

```bash
cd your-project

# 1. 初始化 AgentGit 仓库
agentgit init

# 2. 创建第一个快照
agentgit snapshot -a "Claude Code" -m "重构前基线"

# 3. 让代理干活，然后查看改了什么
agentgit status

# 4. 查看完整历史
agentgit log
```

## 📖 详细使用指南

### 命令一览

| 命令 | 说明 |
| --- | --- |
| `agentgit init` | 初始化 AgentGit 仓库（创建 `.agentgit/`） |
| `agentgit snapshot [-a 代理] [-m 消息]` | 创建工作树快照 |
| `agentgit log [-n N]` | 列出快照历史 |
| `agentgit status` | 显示自上次快照以来的改动 |
| `agentgit diff <id> [--target <id>]` | 对比快照与当前工作树或另一快照 |
| `agentgit revert <id> [--dry-run]` | 将工作树回滚到某快照 |
| `agentgit agents` | 检测本机上的 AI 编码代理 |
| `agentgit watch [-i 秒] [-a 代理]` | 监听目录，改动自动快照 |
| `agentgit serve [--port 8765]` | 启动本地 Web 仪表盘 |

### 典型工作流

```bash
# 高风险代理任务前先打基线
agentgit snapshot -a "Codex" -m "baseline"

# ... 运行你的代理 ...

# 检查它改了什么
agentgit status
agentgit diff <快照id>

# 不满意？回滚这部分改动
agentgit revert <快照id> --dry-run   # 先预览
agentgit revert <快照id>             # 再执行
```

### Web 仪表盘

```bash
agentgit serve --open
# → http://127.0.0.1:8765/
```

仪表盘支持浏览快照时间线、查看文件级差异、检测代理、创建快照与回滚——全部在一个干净的本地界面中完成。

### 自动监听

```bash
# 文件一变就自动快照（每 2 秒轮询）
agentgit watch -i 2 -a "Claude Code"
```

### 忽略文件

AgentGit 会读取你的 `.gitignore`，并内置合理的默认忽略规则（`node_modules`、`.git`、`__pycache__`、`dist`、`build`、`.env` 等）。`.agentgit/` 目录始终被排除。

## 💡 设计思路与迭代规划

### 设计理念

- **零依赖优先** —— 只用 Python 标准库，任何环境都能装、都能跑、永远可用。
- **存储可读** —— 快照是纯 JSON + 文件副本，存放在 `.agentgit/` 下，完全可检查、可迁移。
- **面向代理** —— 围绕"多个代理同时改动一个代码库"的现实设计，归因是一等公民。
- **本地优先** —— 你的代码与历史永远不会离开你的机器。

### 迭代规划

- [ ] **增量快照** —— 只存改动文件以节省磁盘（配置项已支持）。
- [ ] **代理会话集成** —— 自动关联 Claude Code / Codex 的会话 ID。
- [ ] **富差异查看器** —— 仪表盘内语法高亮的 unified diff。
- [ ] **分支式时间线** —— 并行代理工作流与合并支持。
- [ ] **MCP 服务** —— 将 AgentGit 暴露为 MCP 工具，让代理自主管理快照。
- [ ] **插件钩子** —— 快照/回滚前后执行自定义命令。

### 社区贡献方向

欢迎围绕新的代理检测器、仪表盘打磨、增量存储、多语言翻译等方向贡献。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📦 打包与部署指南

AgentGit 属于 **CLI 工具 / 库** 类项目，无需发布二进制 Release。在任意 Python 3.8+ 环境安装即可：

```bash
# 从源码安装
pip install .

# 或构建 wheel 用于离线分发
pip wheel . -w dist/
pip install dist/agentgit-1.0.0-py3-none-any.whl
```

**兼容环境**

- Windows 10/11、macOS 10.15+、Linux（任意发行版）
- Python 3.8 – 3.13
- 无需 GPU、无需联网、无需账号

## 🤝 贡献指南

- 🐛 **报告 Bug** —— 提交 Issue，附上复现步骤。
- 💡 **请求功能** —— 描述要解决的问题与期望的交互。
- 🔀 **提交代码** —— fork、建分支、按 Angular 规范提交，并开 PR。
- 🌐 **参与翻译** —— 帮我们补充更多语言的 README。

完整指南见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📄 开源协议说明

[MIT](../LICENSE) © AgentGit Contributors。可自由使用、修改与分发。
