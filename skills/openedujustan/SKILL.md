---
name: openedujustan
description: OpenEduJustan 小學插班生練習平台 — 四科教材包（Chinese/English/Maths/General_Studies）+ 附科（Arts/Music/Putonghua/Sports/Guidance）。出題、批改、生成練習、分析功課時使用。觸發詞：出題、練習、功課、批改、教材、插班、練習平台、question、practice、homework。
---

# OpenEduJustan 教材包（Skill Pack）

小學插班生練習平台嘅教材同出題系統。呢個 skill 指引你使用 workspace 內嘅教材包。

## 教材包結構

| 科目 | 資料夾 | 內容 |
|------|--------|------|
| 中文 | `Chinese/` | 課文 MD、成語、閱讀理解、`practice/`、`materials/` |
| 英文 | `English/` | 單元閱讀、文法、作文、`practice/`、`materials/` |
| 數學 | `Maths/` | 分數、運算、應用題、`practice/`、`materials/` |
| 常識 | `General_Studies/` | 香港地理、生物、氣候、`practice/`、`materials/` |
| 附科 | `Arts/` `Music/` `Putonghua/` `Sports/` `Guidance/` | 各科練習 |

平台入口：`app.py`（Streamlit 主頁）、`practice_platform.py`（四科批改）、`ai_question_generator.py`（AI 出題器）、`pages/`（專項練習頁）。

## 檔案命名規則

所有新增檔案必須加日期：`YYYY-MM-DD_科目_內容.md`
- 例：`2026-10-06_英文_LookAndWrite.md`
- 功課記錄存入 `<科目>/YYYY-MM-DD_科目_內容.md`，原圖放 `<科目>/materials/YYYY-MM-DD/`

## 出題語言規則（必須遵守）

**所有出題一律用書面語，唔用口語**（準備學校重要考試）：
- 中文：正式書面語（例：「請解釋」唔係「講下」）
- 英文：正式英文（例："Please explain" 唔係 "tell me"）

## 訓練內容優先級

**主要訓練用香港相關資料優先**：
- 常識/各科出題同教材：香港例子、香港物種、香港情境優先（例：黑臉琵鷺米埗、綠海龜南丫島、颱風樺加沙、香港氣候）
- 非香港內容作補充；AI 生成嘅 prompt 都要偏向香港情境

## 批改注意

- 工作紙/書本**印刷部分**係重點 → 記錄 + 分析
- 手寫部分係**學生作答，可能出錯，僅供參考**，唔好當標準答案
- 正確答案先入題庫

## 語言

同用戶溝通：廣東話。出題內容：見「出題語言規則」。
