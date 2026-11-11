# OpenHing 項目脈絡 (Project Context)

> **維護規則（2026-11-12 起）**：項目脈絡有更新時，Mac mini 同 VPN computer 兩邊同步更新。
> - **Mac mini**：`~/Desktop/openhing/PROJECT_CONTEXT.md`（正本）
> - **VPN computer**：`~/.openclaw/workspace/AGENTS.md`
>
> **重要**：`openedujustan` 係 openhing 嘅**其中一個 function**（功能模組），唔係獨立項目。

---

## 🎯 項目是什麼

**openhing** = AI Agent 探索項目（成立 2026-08-27）
- **發起人**：Chuck
- **項目領隊**：@fring1118 (Claw)
- **願景**：探索同開發「增強人類」嘅 AI Agent 系統 — 多智能體協作 (MAS) + 工作流自動化，AI 幫助人類而非取代
- **首選應用場景**：研究助手（推薦 ⭐⭐⭐⭐⭐）
- 8 週行動計劃（2026-09 ~ 2026-10）：基礎建設 → 環境設置 → 架構設計 → 核心開發 (MVP) → 測試改進 → 文檔分享

## 🧩 功能模組（Functions）

| 模組 | 內容 | 位置 |
|------|------|------|
| **openedujustan**（教育）| 小學插班生練習平台：四科教材（Chinese/English/Maths/General_Studies）+ 附科、AI 出題、批改、AI 練習室 | `~/Desktop/openedujustan/`（mini）、`~/.openclaw/workspace/openedujustan/`（VPN 機）|
| **games**（遊戲）| HK 主題 HTML games：hk_monopoly、cha_chaan_teng_delivery、octopus_ninja_commute、ai_barista_challenge 等 | `~/Desktop/openhing/games/` |
| **docs / research**（研究）| AI 趨勢分析、道德設計原則、應用場景分析、研究助手規劃 | `~/Desktop/openhing/docs/` |
| **dashboard / charts**（監控）| 項目 Dashboard、圖表 | `~/Desktop/openhing/` |
| （持續加入新 function⋯）| | |

## 👥 團隊

| 成員 | 角色 |
|------|------|
| @fring1118 (Claw) | 項目領隊 — 應用場景分析 + 情報收集 + Dashboard |
| @fring1119 | 技術開發 |
| @Openclaw#3993 | 技術開發 |

## 🖥️ 機器佈局

| 機器 | 角色 | 備註 |
|------|------|------|
| **Mac mini**（ChuckdeMac-mini-4）| 主開發機 + 主 agent | `~/Desktop/openhing/`（項目檔）、`~/Desktop/openedujustan/`（工作 clone）|
| **VPN computer**（Windows 11, VNC `113.10.159.97:20090`）| AI worker | OpenClaw 2026.11.3 + Node 24.16.0 + qwen3.8-flash (Silra)；VNC 密碼見 openhing 記錄檔；無 admin 權限（UAC 可經 VNC 確認）|

**GitHub repo**：`chuckchanchi-cpu/openhing-project`（public）— 教材/代碼更新經此同步：mini push → VPN 機 download zip → `Expand-Archive` 解壓（⚠️ Windows 內建 tar 會跳過中文檔名，唔好用）。

## 📏 規則（沿用）

- **溝通**：廣東話
- **出題**：一律書面語（中文/英文皆然）— 準備學校重要考試
- **訓練內容**：香港相關資料優先（香港例子、物種、情境）
- **檔案命名**：`YYYY-MM-DD_科目_內容.md`，原圖放 `materials/YYYY-MM-DD/`
- **批改**：印刷部分係重點；手寫係學生作答僅供參考，唔好當標準答案

## 📌 已知事項

- `~/Desktop/openhing` 同 `~/Desktop/openedujustan` 都 clone 自 `openhing-project` repo 但內容唔一致（openhing clone 嘅歷史可能過時 / repo 曾重寫）— 以 openedujustan clone + GitHub remote 為準
- `~/Desktop/openhing` 嘅 git remote URL 含明文 PAT — 建議之後清理（`git remote set-url` 改用無 token URL）
- 2026-11-12：openedujustan skill pack 已裝入 VPN 機 OpenClaw（`skills/openedujustan/SKILL.md`，✓ Ready）

---
*最後更新：2026-11-12（Claw）*
