<div align="center">

# 🧬 AgentGit

**AI コーディングエージェントのためのソースコントロールエンジン**

AI コーディングエージェントが行うすべての変更を追跡します。**スナップショット・差分・ロールバック・監査** —— すべてローカルファースト、ゼロ依存、プライバシー安全。

[English](../README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)

</div>

---

## 🎉 プロジェクト紹介

同じコードベースで複数の AI コーディングエージェント——**Claude Code、Codex、Cursor、Gemini CLI、Aider**——を実行すると、すぐに次の 3 つのシンプルな質問に答えられなくなります。

- どのファイルを**誰が**変更したのか？
- 各エージェントは実際に**何を**したのか？
- 他のものを壊さずに、特定のエージェントの作業を**どうやって**元に戻すのか？

AgentGit は**AI エージェントのために作られたソースコントロールエンジン**です。作業ツリーをスナップショットし、変更を加えたエージェントに帰属させ、任意の時点へ差分確認やロールバックができます——すべて手元のマシンで、**ゼロ依存**、**データはデバイスから出ません**。

> 💡 **着想のきっかけ** —— AgentGit は、GitHub トレンドで注目を集める「エージェントのためのソースコントロール」という新たなニーズと、安全網なしで複数の AI コーディングエージェントを並行運用する苦労から生まれました。「実行したコマンド」だけを記録するセッションロガーとは違い、AgentGit は「ファイルが実際にどう変わったか」を追跡します——まるでエージェント専用の `git` です。

## ✨ 主な機能

- 🧠 **作業ツリーのスナップショット** —— 1 コマンドでプロジェクトの完全な状態をキャプチャ。メッセージとエージェント帰属に対応。
- 🤖 **エージェント帰属** —— 実行中のエージェント（Claude Code、Codex、Cursor、Gemini CLI、Aider、Windsurf、Copilot など）を自動検出し、各スナップショットに作者タグを付与。
- 🔍 **任意時点の差分** —— スナップショットを現在のツリーまたは別のスナップショットと比較。追加・変更・削除が一目瞭然。
- ↩️ **ワンコマンドでロールバック** —— 安全な `--dry-run` プレビュー付きで、任意のスナップショットへ作業ツリーを復元。
- 👀 **リアルタイムステータス** —— 前回のスナップショット以降の変更を即座に確認。
- ⏱️ **自動ウォッチモード** —— ディレクトリを監視し、ファイルが変わった瞬間に自動スナップショット。
- 🖥️ **ローカル Web ダッシュボード** —— 洗練されたゼロ依存のローカル UI で、タイムライン閲覧・差分確認・エージェント管理を実現。
- 🔒 **プライバシーファースト** —— すべてローカルで実行。クラウドなし、テレメトリなし、アカウント不要。
- 🪶 **ゼロ依存** —— 純粋な Python 標準ライブラリのみ。Windows・macOS・Linux で動作。

## 🚀 クイックスタート

### 必要環境

- **Python 3.8+**（サードパーティ製パッケージは不要）

### インストール

```bash
# 方法 A —— ソースからインストール（推奨）
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
pip install .

# 方法 B —— インストールせずに実行
python bin/agentgit --help
```

### 最初の 60 秒

```bash
cd your-project

# 1. AgentGit リポジトリを初期化
agentgit init

# 2. 最初のスナップショットを作成
agentgit snapshot -a "Claude Code" -m "リファクタ前のベースライン"

# 3. エージェントに作業させ、変更を確認
agentgit status

# 4. 履歴を確認
agentgit log
```

## 📖 詳細な使い方

### コマンド一覧

| コマンド | 説明 |
| --- | --- |
| `agentgit init` | AgentGit リポジトリを初期化（`.agentgit/` を作成） |
| `agentgit snapshot [-a エージェント] [-m メッセージ]` | 作業ツリーのスナップショットを作成 |
| `agentgit log [-n N]` | スナップショット履歴を表示 |
| `agentgit status` | 最新スナップショット以降の変更を表示 |
| `agentgit diff <id> [--target <id>]` | スナップショットと現在のツリーまたは別スナップショットを比較 |
| `agentgit revert <id> [--dry-run]` | 作業ツリーをスナップショットへ復元 |
| `agentgit agents` | このマシンの AI コーディングエージェントを検出 |
| `agentgit watch [-i 秒] [-a エージェント]` | ディレクトリを監視し変更を自動スナップショット |
| `agentgit serve [--port 8765]` | ローカル Web ダッシュボードを起動 |

### 典型的なワークフロー

```bash
# リスクの高いエージェント作業の前にベースライン
agentgit snapshot -a "Codex" -m "baseline"

# ... エージェントを実行 ...

# 変更内容を確認
agentgit status
agentgit diff <スナップショットID>

# 気に入らない？その作業をロールバック
agentgit revert <スナップショットID> --dry-run   # まずプレビュー
agentgit revert <スナップショットID>             # 実行
```

### Web ダッシュボード

```bash
agentgit serve --open
# → http://127.0.0.1:8765/
```

ダッシュボードでは、スナップショットタイムラインの閲覧、ファイルレベルの差分確認、エージェント検出、スナップショット作成、ロールバックを、クリーンなローカル UI で行えます。

### 自動ウォッチ

```bash
# ファイルが変わるたびに自動スナップショット（2 秒ごとにポーリング）
agentgit watch -i 2 -a "Claude Code"
```

### ファイルの無視

AgentGit は `.gitignore` を尊重し、適切なデフォルト（`node_modules`、`.git`、`__pycache__`、`dist`、`build`、`.env` など）を内蔵しています。`.agentgit/` ディレクトリは常に除外されます。

## 💡 設計思想とロードマップ

### 設計理念

- **ゼロ依存を設計原則に** —— Python 標準ライブラリのみを使用し、どこでもインストール・実行・永続利用可能。
- **人間が読めるストレージ** —— スナップショットは `.agentgit/` 配下のプレーンな JSON とファイルコピーで、完全に検査・移植可能。
- **エージェントネイティブ** —— 複数のエージェントが 1 つのコードベースを触る現実に基づき、帰属を第一級の概念に。
- **ローカルファースト** —— コードと履歴は決してマシンの外に出ません。

### ロードマップ

- [ ] **インクリメンタルスナップショット** —— 変更ファイルのみ保存してディスクを節約（設定フラグは実装済み）。
- [ ] **エージェントセッション統合** —— Claude Code / Codex のセッション ID と自動リンク。
- [ ] **リッチ差分ビューア** —— ダッシュボードで構文ハイライト付き unified diff。
- [ ] **ブランチ型タイムライン** —— 並行エージェント作業とマージ対応。
- [ ] **MCP サーバー** —— AgentGit を MCP ツールとして公開し、エージェントがスナップショットを自己管理。
- [ ] **プラグインフック** —— スナップショット/ロールバック前後にコマンド実行。

### コントリビューションの方向性

新しいエージェント検出器、ダッシュボードの磨き込み、インクリメンタルストレージ、翻訳など、幅広い貢献を歓迎します。詳細は [CONTRIBUTING.md](../CONTRIBUTING.md) をご覧ください。

## 📦 パッケージングとデプロイ

AgentGit は **CLI ツール / ライブラリ** プロジェクトのため、Release バイナリは不要です。Python 3.8+ が動く環境ならどこでもインストールできます：

```bash
# ソースからインストール
pip install .

# オフライン配布用に wheel をビルド
pip wheel . -w dist/
pip install dist/agentgit-1.0.0-py3-none-any.whl
```

**互換環境**

- Windows 10/11、macOS 10.15+、Linux（任意ディストリビューション）
- Python 3.8 – 3.13
- GPU 不要、ネットワーク不要、アカウント不要

## 🤝 コントリビューション

- 🐛 **バグ報告** —— 再現手順付きで Issue を開いてください。
- 💡 **機能リクエスト** —— 解決したい問題と期待する UX を説明してください。
- 🔀 **コード投稿** —— fork、ブランチ作成、Angular 規約でコミット、PR を開く。
- 🌐 **翻訳** —— より多くの言語の README 追加にご協力ください。

完全なガイドは [CONTRIBUTING.md](../CONTRIBUTING.md) をご覧ください。

## 📄 ライセンス

[MIT](../LICENSE) © AgentGit Contributors。自由に使用・変更・配布できます。
