<div align="center">

# 🧬 AgentGit

**AI 編碼代理原始碼控制引擎**

追蹤你的 AI 編碼代理所做的每一次變更。**快照 · 差異 · 回滾 · 稽核** —— 全部本地優先、零依賴、隱私安全。

[English](../README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
[![Download](https://img.shields.io/badge/⬇%20Download-v1.0.0-2ea44f?style=for-the-badge)](https://github.com/gitstq/AgentGit/releases/tag/v1.0.0)

</div>

---

## 🎉 專案介紹

當你在同一個程式碼庫上執行多個 AI 編碼代理——**Claude Code、Codex、Cursor、Gemini CLI、Aider**——時，很快就會回答不了三個簡單的問題：

- **誰**改了哪些檔案？
- 每個代理到底**做了什麼**？
- 如何**撤銷**某個代理的變更而不破壞其他東西？

AgentGit 就是**為 AI 代理打造的原始碼控制引擎**。它快照你的工作樹、把變更歸因到對應的代理，並讓你隨時 diff 或回滾到任意時間點——全部在你的機器上完成，**零依賴**、**資料不出裝置**。

> 💡 **靈感來源** —— AgentGit 受 GitHub 熱榜上「為 Agent 做原始碼控制」這一新興需求的啟發，也源於並行管理多個 AI 編碼代理卻缺乏安全網的痛點。與只記錄「跑了什麼指令」的會話日誌工具不同，AgentGit 追蹤的是「檔案到底發生了什麼變化」——就像 `git`，但專為你的代理而生。

## ✨ 核心特性

- 🧠 **工作樹快照** —— 一條指令捕獲專案完整狀態，支援訊息與代理歸因。
- 🤖 **代理歸因** —— 自動偵測正在執行的代理（Claude Code、Codex、Cursor、Gemini CLI、Aider、Windsurf、Copilot 等），並為每個快照打上作者標籤。
- 🔍 **任意時間點差異** —— 將快照與目前工作樹或另一個快照對比，新增/修改/刪除一目了然。
- ↩️ **一鍵回滾** —— 將工作樹還原到任意快照，支援安全的 `--dry-run` 預覽。
- 👀 **即時狀態** —— 一眼看清自上次快照以來的變化。
- ⏱️ **自動監聽模式** —— 監聽目錄，檔案一變就自動建立快照。
- 🖥️ **本地 Web 儀表板** —— 精緻、零依賴的本地儀表板，瀏覽時間軸、檢視差異、管理代理。
- 🔒 **隱私優先** —— 一切都在本地執行，無雲端、無遙測、無帳號。
- 🪶 **零依賴** —— 純 Python 標準程式庫，Windows、macOS、Linux 全平台可用。

## 🚀 快速開始

### 環境需求

- **Python 3.8+**（無需任何第三方套件）

### 安裝步驟

```bash
# 方式 A —— 原始碼安裝（推薦）
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
pip install .

# 方式 B —— 免安裝直接執行
python bin/agentgit --help
```

### 60 秒上手

```bash
cd your-project

# 1. 初始化 AgentGit 倉庫
agentgit init

# 2. 建立第一個快照
agentgit snapshot -a "Claude Code" -m "重構前基線"

# 3. 讓代理做事，然後查看改了什麼
agentgit status

# 4. 查看完整歷史
agentgit log
```

## 📖 詳細使用指南

### 指令一覽

| 指令 | 說明 |
| --- | --- |
| `agentgit init` | 初始化 AgentGit 倉庫（建立 `.agentgit/`） |
| `agentgit snapshot [-a 代理] [-m 訊息]` | 建立工作樹快照 |
| `agentgit log [-n N]` | 列出快照歷史 |
| `agentgit status` | 顯示自上次快照以來的變更 |
| `agentgit diff <id> [--target <id>]` | 對比快照與目前工作樹或另一快照 |
| `agentgit revert <id> [--dry-run]` | 將工作樹回滾到某快照 |
| `agentgit agents` | 偵測本機上的 AI 編碼代理 |
| `agentgit watch [-i 秒] [-a 代理]` | 監聽目錄，變更自動快照 |
| `agentgit serve [--port 8765]` | 啟動本地 Web 儀表板 |

### 典型工作流程

```bash
# 高風險代理任務前先打基線
agentgit snapshot -a "Codex" -m "baseline"

# ... 執行你的代理 ...

# 檢查它改了什麼
agentgit status
agentgit diff <快照id>

# 不滿意？回滾這部分變更
agentgit revert <快照id> --dry-run   # 先預覽
agentgit revert <快照id>             # 再執行
```

### Web 儀表板

```bash
agentgit serve --open
# → http://127.0.0.1:8765/
```

儀表板支援瀏覽快照時間軸、檢視檔案級差異、偵測代理、建立快照與回滾——全部在一個乾淨的本地介面中完成。

### 自動監聽

```bash
# 檔案一變就自動快照（每 2 秒輪詢）
agentgit watch -i 2 -a "Claude Code"
```

### 忽略檔案

AgentGit 會讀取你的 `.gitignore`，並內建合理的預設忽略規則（`node_modules`、`.git`、`__pycache__`、`dist`、`build`、`.env` 等）。`.agentgit/` 目錄始終被排除。

## 💡 設計思路與迭代規劃

### 設計理念

- **零依賴優先** —— 只用 Python 標準程式庫，任何環境都能裝、都能跑、永遠可用。
- **儲存可讀** —— 快照是純 JSON + 檔案副本，存放在 `.agentgit/` 下，完全可檢查、可遷移。
- **面向代理** —— 圍繞「多個代理同時變更一個程式碼庫」的現實設計，歸因是一等公民。
- **本地優先** —— 你的程式碼與歷史永遠不會離開你的機器。

### 迭代規劃

- [ ] **增量快照** —— 只存變更檔案以節省磁碟（設定項已支援）。
- [ ] **代理會話整合** —— 自動關聯 Claude Code / Codex 的會話 ID。
- [ ] **富差異檢視器** —— 儀表板內語法高亮的 unified diff。
- [ ] **分支式時間軸** —— 並行代理工作流與合併支援。
- [ ] **MCP 服務** —— 將 AgentGit 暴露為 MCP 工具，讓代理自主管理快照。
- [ ] **外掛鉤子** —— 快照/回滾前後執行自訂指令。

### 社群貢獻方向

歡迎圍繞新的代理偵測器、儀表板打磨、增量儲存、多語言翻譯等方向貢獻。詳見 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📦 打包與部署指南

AgentGit 屬於 **CLI 工具 / 函式庫** 類專案，無需發布二進位 Release。在任意 Python 3.8+ 環境安裝即可：

```bash
# 從原始碼安裝
pip install .

# 或建置 wheel 用於離線散佈
pip wheel . -w dist/
pip install dist/agentgit-1.0.0-py3-none-any.whl
```

**相容環境**

- Windows 10/11、macOS 10.15+、Linux（任意發行版）
- Python 3.8 – 3.13
- 無需 GPU、無需連網、無需帳號

## 🤝 貢獻指南

- 🐛 **回報 Bug** —— 提交 Issue，附上重現步驟。
- 💡 **請求功能** —— 描述要解決的問題與期望的互動。
- 🔀 **提交程式碼** —— fork、建分支、按 Angular 規範提交，並開 PR。
- 🌐 **參與翻譯** —— 幫我們補充更多語言的 README。

完整指南見 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📄 開源協議說明

[MIT](../LICENSE) © AgentGit Contributors。可自由使用、修改與散佈。
