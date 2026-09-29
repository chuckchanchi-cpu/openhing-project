# 🦀 Openhing - Ethical AI Research Assistant

**成立日期**: 2026-08-27  
**發起人**: Chuck (@chuck)  
**項目領隊**: @fring1118 (Claw)  
**當前階段**: 第 1 週 - 基礎建設 (9 月 1-7 日)  
**整體進度**: 50%

---

## 🎯 項目願景

探索同開發「增強人類」嘅 AI Agent 系統，專注於 **多智能體協作 (MAS)** 同 **工作流自動化**，確保 AI 係幫助人類而非取代。

**回應 Bill Gates 2026-08-27 AI 裁員警告**：我哋設計嘅 Agent 必須 **增強人類能力**，而唔係 **取代人類工作**。

---

## 👥 團隊成員

| 成員 | 角色 | 職責 | 狀態 | 最後活躍 |
|------|------|------|------|----------|
| **@fring1118 (Claw)** | 項目領隊 | 應用場景分析 + 情報收集 + Dashboard + MVP 開發 | ✅ 按時推進 | 2026-09-01 23:40 |
| **@chuck** | 發起人/顧問 | 項目發起 + 戰略指導 + GitHub Repo | ✅ 支援中 | 2026-09-01 23:37 |
| **@fring1119** | 技術開發 (招募中) | 技術框架調研 + 開發環境 | 🔴 未回覆 | 2026-08-31 10:43 |
| **@Openclaw#3993** | 技術開發 (招募中) | 技術框架調研 / GitHub Repo | 🔴 未回覆 | 未見活躍 |

> **註**: @fring1119 和 @Openclaw#3993 由 9 月 1 日 09:00 開始多次被 @，但截至 23:40 仍未確認任務。如果 9 月 2 日 09:00 前未回覆，將改為開放招募。

---

## 📊 當前進度

### ✅ 已完成 (50%)

| 任務 | 負責人 | 完成日期 | 文件連結 |
|------|--------|----------|----------|
| 應用場景分析 | @fring1118 | 2026-09-01 | [docs/應用場景分析.md](docs/應用場景分析.md) |
| 道德設計原則 | @fring1118 | 2026-09-01 | [docs/道德設計原則.md](docs/道德設計原則.md) |
| Dashboard (Markdown) | @fring1118 | 2026-09-01 | [docs/項目_Dashboard.md](docs/項目_Dashboard.md) |
| Dashboard (HTML) | @fring1118 | 2026-09-01 | [docs/項目_Dashboard.html](docs/項目_Dashboard.html) |
| README.md | @fring1118 | 2026-09-01 | [README.md](README.md) |
| Mac 文件夾同步 | @fring1118 | 2026-09-01 | `~/Desktop/openhing/` |
| GitHub Repo 建立 | @chuck | 2026-09-01 | [GitHub Repo](https://github.com/chuckchanchi-cpu/openhing-project) |

### ⏳ 進行中

| 任務 | 負責人 | Deadline | 進度 |
|------|--------|----------|------|
| CrewAI MVP Demo | @fring1118 | 2026-09-02 | 10% |
| 技術框架調研 | 招募中 | 2026-09-07 | 0% |
| 團隊招募 | @fring1118 | 2026-09-02 | 0% |

### 📅 下一步

- **今日 (9 月 1 日)**: 準備 GitHub 文件 Upload
- **聽日 (9 月 2 日)**: CrewAI Demo 開發 + 團隊招募
- **本週 (9 月 1-7 日)**: 完成技術框架調研 + 準備 9/7 會議

---

## 🎯 首選應用場景：研究助手

**推薦指數**: ⭐⭐⭐⭐⭐ (5/5)  
**道德評分**: ⭐⭐⭐⭐ (4/5)

### 核心功能流程

```
用戶輸入研究主題
    ↓
[搜索 Agent] → 搜索文獻/資料
    ↓
[分析 Agent] → 閱讀、摘要、提取關鍵信息
    ↓
[整合 Agent] → 合併多個來源
    ↓
[寫作 Agent] → 撰寫結構化報告
    ↓
用戶審閱 + 修改 ← 人類確認步驟
```

### 技術需求
- **框架**: CrewAI (推薦) / AutoGen / LangChain
- **LLM**: 長上下文 (128K+) 處理完整論文
- **APIs**: Serper API、學術數據庫 API
- **存儲**: 文獻數據庫、引用管理

---

## 📂 文件結構

```
openhing/
├── README.md                          # 項目總覽 (本文件)
├── LICENSE                            # 開源許可證 (待添加)
├── .gitignore                         # Git 忽略文件
├── requirements.txt                   # Python 依賴
│
├── docs/                              # 正式文檔
│   ├── 應用場景分析.md                # ✅ 3 個場景詳細分析
│   ├── 道德設計原則.md                # ✅ 5 大原則
│   ├── 項目_Dashboard.md              # ✅ Markdown 版 Dashboard
│   └── 大學圖書館研究準備指南.md      # ✅ 研究指南
│
├── notes/                             # 會議筆記
│   ├── 00-項目啟動筆記.md             # ✅ 啟動會議記錄
│   └── 01-進度匯報_2026-09-01.md      # ✅ 今日進度
│
├── resources/                         # 參考資料
│   ├── bill-gates-ai-layoffs-analysis.md       # ✅ 蓋茨警告分析
│   ├── bill-gates-ai-layoffs-prediction.jpg    # ✅ 蓋茨文章截圖
│   └── 2026-08-27-Qwen3.8-Flash-發布分析.md    # ✅ 模型分析
│
├── scripts/                           # 腳本 (待開發)
│   ├── research_assistant.py          # ⏳ CrewAI Demo
│   └── setup_env.sh                   # ⏳ 環境設置
│
└── templates/                         # 模板 (待開發)
```

---

## 🚦 8 週行動計劃

| 週數 | 日期 | 階段 | 主要任務 | 負責人 |
|------|------|------|----------|--------|
| **第 1 週** | 9 月 1-7 日 | 基礎建設 | 技術調研 + 應用場景選擇 + 道德指引 | @fring1118 |
| **第 2 週** | 9 月 8-14 日 | 環境設置 | 開發環境 + Agent 架構設計 | 招募中 |
| **第 3 週** | 9 月 15-21 日 | 架構設計 | 詳細系統設計 | 招募中 |
| **第 4-5 週** | 9 月 22 日 -10 月 5 日 | 核心開發 | MVP 開發 | 全體 |
| **第 6 週** | 10 月 6-12 日 | 測試改進 | 測試 + 用戶反饋 | 全體 |
| **第 7-8 週** | 10 月 13-26 日 | 文檔分享 | 技術博客 + 社區分享 | 全體 |

---

## ⚠️ 風險與緩解

| 風險 | 等級 | 影響 | 緩解方案 | 狀態 |
|------|------|------|----------|------|
| 技術夥伴未回覆 | 🔴 高 | 項目延誤 | **已執行**: 領隊單人推進 MVP | ✅ 已緩解 |
| 領隊工作量過大 | 🟡 中 | 可能疲勞 | 縮小 MVP 範圍，專注核心功能 | ✅ 已識別 |
| 缺乏技術反饋 | 🟡 中 | 可能走錯方向 | 9 月 2 日發招募帖，吸引技術顧問 | ⏳ 待執行 |
| 競爭激烈 | 🟡 中 | 市場接受度 | 差異化：道德設計 + 廣東話支援 | ✅ 已識別 |

---

## 📞 溝通機制

- **每週會議**: 週一 10:00 (香港時間) - Discord
- **日常溝通**: Discord Channel `#general`
- **文件共享**: GitHub + Discord
- **Dashboard 更新**: 每次有新進度時更新

---

## 🎯 招募計劃

### 招募對象

1. **技術開發夥伴** (1-2 人)
   - 技能：Python、AI/ML 經驗
   - 職責：技術框架調研、代碼開發
   - 時間承諾：每週 5-10 小時

2. **行業顧問** (1 人)
   - 背景：學術研究/圖書館/教育科技
   - 職責：提供行業洞察、用戶反饋
   - 時間承諾：每週 1-2 小時

### 有興趣？

喺 Discord 聯絡 @fring1118 (Claw) 或者 @chuck！

---

## 📚 參考資料

1. Bill Gates. "A Turbulent AI Era and Critical Choices to Make". GatesNotes, 2026-08-27.
2. IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems.
3. EU AI Act (2024).
4. OECD AI Principles.

---

*最後更新：2026-09-01 23:40*  
*作者：Claw (fring1118)*  
*GitHub: https://github.com/chuckchanchi-cpu/openhing-project*
