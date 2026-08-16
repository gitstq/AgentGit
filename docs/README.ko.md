<div align="center">

# 🧬 AgentGit

**AI 코딩 에이전트를 위한 소스 컨트롤 엔진**

AI 코딩 에이전트가 만든 모든 변경 사항을 추적하세요. **스냅샷 · 차이 · 롤백 · 감사** — 모두 로컬 우선, 제로 의존성, 프라이버시 안전.

[English](../README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
[![Download](https://img.shields.io/badge/⬇%20Download-v1.0.0-2ea44f?style=for-the-badge)](https://github.com/gitstq/AgentGit/releases/tag/v1.0.0)

</div>

---

## 🎉 프로젝트 소개

하나의 코드베이스에서 여러 AI 코딩 에이전트——**Claude Code, Codex, Cursor, Gemini CLI, Aider**——를 실행하다 보면, 곧 세 가지 간단한 질문에 답할 수 없게 됩니다.

- 어떤 파일을 **누가** 변경했는가?
- 각 에이전트가 실제로 **무엇을** 했는가?
- 다른 것을 망가뜨리지 않고 특정 에이전트의 작업을 **어떻게** 되돌릴 것인가?

AgentGit은 **AI 에이전트를 위해 만들어진 소스 컨트롤 엔진**입니다. 작업 트리를 스냅샷하고, 변경 사항을 만든 에이전트에 귀속시키며, 언제든지 diff하거나 롤백할 수 있습니다 — 전부 내 컴퓨터에서, **제로 의존성**, **데이터는 기기를 떠나지 않습니다**.

> 💡 **영감** — AgentGit은 GitHub 트렌드에서 주목받는 "에이전트를 위한 소스 컨트롤"이라는 새로운 수요와, 안전망 없이 여러 AI 코딩 에이전트를 병렬로 관리하는 고통에서 영감을 받았습니다. "어떤 명령을 실행했는지"만 기록하는 세션 로거와 달리, AgentGit은 "파일이 실제로 어떻게 바뀌었는지"를 추적합니다 — 에이전트를 위한 `git`과 같습니다.

## ✨ 핵심 기능

- 🧠 **작업 트리 스냅샷** — 한 명령으로 프로젝트의 전체 상태를 캡처. 메시지와 에이전트 귀속 지원.
- 🤖 **에이전트 귀속** — 실행 중인 에이전트(Claude Code, Codex, Cursor, Gemini CLI, Aider, Windsurf, Copilot 등)를 자동 감지하고 각 스냅샷에 작성자 태그를 부여.
- 🔍 **임의 시점 차이** — 스냅샷을 현재 트리 또는 다른 스냅샷과 비교. 추가/수정/삭제가 한눈에.
- ↩️ **원클릭 롤백** — 안전한 `--dry-run` 미리보기와 함께 작업 트리를 임의 스냅샷으로 복원.
- 👀 **실시간 상태** — 마지막 스냅샷 이후 무엇이 바뀌었는지 즉시 확인.
- ⏱️ **자동 감시 모드** — 디렉터리를 감시하고 파일이 바뀌는 순간 자동 스냅샷 생성.
- 🖥️ **로컬 웹 대시보드** — 깔끔한 제로 의존성 로컬 UI로 타임라인 탐색, 차이 확인, 에이전트 관리.
- 🔒 **프라이버시 우선** — 모든 것이 로컬에서 실행. 클라우드 없음, 텔레메트리 없음, 계정 불필요.
- 🪶 **제로 의존성** — 순수 Python 표준 라이브러리. Windows·macOS·Linux에서 동작.

## 🚀 빠른 시작

### 요구 사항

- **Python 3.8+** (서드파티 패키지 불필요)

### 설치

```bash
# 방법 A — 소스에서 설치 (권장)
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
pip install .

# 방법 B — 설치 없이 실행
python bin/agentgit --help
```

### 첫 60초

```bash
cd your-project

# 1. AgentGit 저장소 초기화
agentgit init

# 2. 첫 스냅샷 생성
agentgit snapshot -a "Claude Code" -m "리팩터링 전 베이스라인"

# 3. 에이전트가 작업하게 한 뒤 변경 사항 확인
agentgit status

# 4. 전체 이력 확인
agentgit log
```

## 📖 상세 사용 가이드

### 명령어 개요

| 명령어 | 설명 |
| --- | --- |
| `agentgit init` | AgentGit 저장소 초기화 (`.agentgit/` 생성) |
| `agentgit snapshot [-a 에이전트] [-m 메시지]` | 작업 트리 스냅샷 생성 |
| `agentgit log [-n N]` | 스냅샷 이력 표시 |
| `agentgit status` | 최신 스냅샷 이후 변경 사항 표시 |
| `agentgit diff <id> [--target <id>]` | 스냅샷과 현재 트리 또는 다른 스냅샷 비교 |
| `agentgit revert <id> [--dry-run]` | 작업 트리를 스냅샷으로 복원 |
| `agentgit agents` | 이 컴퓨터의 AI 코딩 에이전트 감지 |
| `agentgit watch [-i 초] [-a 에이전트]` | 디렉터리 감시, 변경 시 자동 스냅샷 |
| `agentgit serve [--port 8765]` | 로컬 웹 대시보드 시작 |

### 일반적인 워크플로

```bash
# 위험한 에이전트 작업 전에 베이스라인
agentgit snapshot -a "Codex" -m "baseline"

# ... 에이전트 실행 ...

# 변경 내용 확인
agentgit status
agentgit diff <스냅샷ID>

# 마음에 안 들면? 해당 작업 롤백
agentgit revert <스냅샷ID> --dry-run   # 먼저 미리보기
agentgit revert <스냅샷ID>             # 적용
```

### 웹 대시보드

```bash
agentgit serve --open
# → http://127.0.0.1:8765/
```

대시보드에서 스냅샷 타임라인 탐색, 파일 수준 차이 확인, 에이전트 감지, 스냅샷 생성, 롤백을 깔끔한 로컬 UI로 수행할 수 있습니다.

### 자동 감시

```bash
# 파일이 바뀔 때마다 자동 스냅샷 (2초마다 폴링)
agentgit watch -i 2 -a "Claude Code"
```

### 파일 무시

AgentGit은 `.gitignore`를 존중하며 합리적인 기본값(`node_modules`, `.git`, `__pycache__`, `dist`, `build`, `.env` 등)을 내장합니다. `.agentgit/` 디렉터리는 항상 제외됩니다.

## 💡 설계 사상과 로드맵

### 설계 철학

- **제로 의존성 설계** — Python 표준 라이브러리만 사용하여 어디서든 설치·실행·영구 사용 가능.
- **사람이 읽을 수 있는 저장소** — 스냅샷은 `.agentgit/` 아래의 순수 JSON과 파일 복사본으로, 완전히 검사·이식 가능.
- **에이전트 네이티브** — 여러 에이전트가 하나의 코드베이스를 건드리는 현실을 기반으로, 귀속을 일급 개념으로 설계.
- **로컬 우선** — 코드와 이력은 결코 기기를 떠나지 않습니다.

### 로드맵

- [ ] **증분 스냅샷** — 변경 파일만 저장하여 디스크 절약 (설정 플래그는 이미 지원).
- [ ] **에이전트 세션 통합** — Claude Code / Codex 세션 ID와 자동 연결.
- [ ] **리치 diff 뷰어** — 대시보드에서 구문 하이라이트 unified diff.
- [ ] **브랜치형 타임라인** — 병렬 에이전트 작업과 병합 지원.
- [ ] **MCP 서버** — AgentGit을 MCP 도구로 노출하여 에이전트가 스냅샷을 자율 관리.
- [ ] **플러그인 훅** — 스냅샷/롤백 전후에 명령 실행.

### 기여 방향

새로운 에이전트 감지기, 대시보드 개선, 증분 저장, 번역 등 다양한 기여를 환영합니다. 자세한 내용은 [CONTRIBUTING.md](../CONTRIBUTING.md)를 참조하세요.

## 📦 패키징과 배포

AgentGit은 **CLI 도구 / 라이브러리** 프로젝트이므로 Release 바이너리가 필요 없습니다. Python 3.8+가 실행되는 어디서든 설치할 수 있습니다:

```bash
# 소스에서 설치
pip install .

# 오프라인 배포용 wheel 빌드
pip wheel . -w dist/
pip install dist/agentgit-1.0.0-py3-none-any.whl
```

**호환 환경**

- Windows 10/11, macOS 10.15+, Linux (모든 배포판)
- Python 3.8 – 3.13
- GPU 불필요, 네트워크 불필요, 계정 불필요

## 🤝 기여 가이드

- 🐛 **버그 신고** — 재현 단계와 함께 Issue를 열어주세요.
- 💡 **기능 요청** — 해결하려는 문제와 원하는 UX를 설명해주세요.
- 🔀 **코드 기여** — fork, 브랜치 생성, Angular 규약으로 커밋, PR 열기.
- 🌐 **번역** — 더 많은 언어의 README 추가에 도움을 주세요.

전체 가이드는 [CONTRIBUTING.md](../CONTRIBUTING.md)를 참조하세요.

## 📄 라이선스

[MIT](../LICENSE) © AgentGit Contributors. 자유롭게 사용·수정·배포할 수 있습니다.
