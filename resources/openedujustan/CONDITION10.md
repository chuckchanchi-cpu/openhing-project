# Condition 10：情境式記憶（Memory-augmented / Semantic Memory）

> **定義：** 根據情境動態檢索與寫入記憶，Agent 越用越聰明。
> **適用場景：** 需要個人化、長期知識累積或持續學習的用途（如：個人助手、學習夥伴、研究助理）。

---

## 執行規則：每個任務前後都必須 Run Through

### 🔍 任務前（檢索）
1. **檢索記憶** — 搜尋相關紀錄：
   - 教材內容與進度（各科材料、已出練習）
   - Chuck 嘅偏好與規則（格式、語言、框架）
   - 成功框架與錯誤紀錄（避免重複犯錯）
2. **檢查 folder** — 確認 `Z:\` 各科 `materials\` 最新材料有冇未處理
3. **確認進行中項目** — 待確認事項、未完成訓練、pending 連結

### 📝 任務後（寫入）
1. **寫日誌** — 更新 `memory/YYYY-MM-DD.md`（今日發生咗咩）
2. **更新進度** — 完成咗咩、出咗咩 deliverable
3. **沉澱教訓** — 新框架、新錯誤、新偏好 → 寫入長期記憶（MEMORY.md / Guidance）

---

## 本項目點樣用（openedujustan）

| 記憶類型 | 存放位置 | 用途 |
|---|---|---|
| 每日日誌 | `memory/YYYY-MM-DD.md` | 每日發生嘅事、材料、deliverable |
| 長期記憶 | `MEMORY.md` | 規則、偏好、教訓、重要決定 |
| 成功框架 | `Z:\Guidance\` | Google Form 等可重用範本 |
| 材料歸檔 | `Z:\<科目>\materials\` | 每日上傳嘅課本/工作紙相片 |
| 進度追蹤 | 各科 `practice\` | worksheet、遊戲、答案 |

**效果：** 唔使重複解釋、唔會重複犯錯、材料/偏好/進度全部記得 — Agent 越用越聰明 💪

---

*建立日期：2026-09-13 ｜ 依據 Chuck 指示「write it on the top of the folder, and run through it before going on any task」*
