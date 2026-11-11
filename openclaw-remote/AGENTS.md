# OpenHing Project Context — VPN Computer (AI Worker)

> 你係 openhing 項目嘅 AI worker（跑喺 Windows VPN computer）。呢個檔案係項目脈絡。
> 正本喺 Mac mini：`~/Desktop/openhing/PROJECT_CONTEXT.md` — 有更新時兩邊同步。
> **重要**：`openedujustan` 係 openhing 嘅**其中一個 function**，唔係獨立項目。

## 🎯 項目

**openhing** = AI Agent 探索項目（2026-08-27 成立，發起人 Chuck，領隊 Claw @fring1118）
- 願景：「增強人類」嘅 AI Agent 系統 — 多智能體協作 (MAS) + 工作流自動化
- 首選應用場景：研究助手

## 🧩 功能模組

| 模組 | 內容 | 呢部機嘅位置 |
|------|------|------|
| **openedujustan**（教育）| 小學插班生練習平台：四科教材 + 附科、AI 出題、批改、AI 練習室 | `~/.openclaw/workspace/openedujustan/` + skill `openedujustan` |
| **games**（遊戲）| HK 主題 HTML games | （Mac mini `~/Desktop/openhing/games/`）|
| **docs / research**（研究）| AI 趨勢、道德設計、應用場景分析 | （Mac mini）|
| （持續加入新 function⋯）| | |

## 🖥️ 機器佈局

- **Mac mini**（ChuckdeMac-mini-4）：主開發機 + 主 agent — `~/Desktop/openhing/`、`~/Desktop/openedujustan/`
- **呢部機**（Windows 11, VNC 113.10.159.97:20090）：AI worker — OpenClaw 2026.11.3 + qwen3.8-flash (Silra API)；無 admin（UAC 可經 VNC 確認）
- **GitHub repo**：`chuckchanchi-cpu/openhing-project`（public）— 更新同步：mini push → 呢部機 download zip → `Expand-Archive` 解壓（⚠️ 內建 tar 會跳過中文檔名，唔好用）

## 📏 規則

- **溝通**：廣東話
- **出題**：一律書面語（中文/英文皆然）
- **訓練內容**：香港相關資料優先
- **檔案命名**：`YYYY-MM-DD_科目_內容.md`，原圖放 `materials/YYYY-MM-DD/`
- **批改**：印刷部分係重點；手寫係學生作答僅供參考

## 📌 維護

- 項目脈絡更新 → 同步更新 Mac mini 正本同呢個檔案
- Skill pack（教材包）更新 → repo push → 重新 download zip + 解壓 + 更新 `skills/openedujustan/`

---
*最後更新：2026-11-12（Claw @ Mac mini）*
