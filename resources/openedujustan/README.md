# 📚 openedujustan 教材備份（MD 版）

> **用途：** Mac mini `openedujustan` 教材嘅 GitHub 備份 + 練習平台題目來源
> **同步策略：** Mac 係 source of truth → 定期將教材 copy 嚟呢度 → push → app 讀取
> **上次同步：** 2026-09-16

## 檔案清單

### 🌍 常識科
- `2026-09-07_常識_生物的分類學習與訓練.md` — Unit 1 生物分類（已轉題目 → `resources/questions/常識_生物分類.json`）

### 📕 英文
- `2026-09-07_Unit1_A_Helping_Hand_Practice.md` — Unit 1 練習
- `2026-09-15_英文默書1_職業詞語表.md` — 默書詞語
- `unit1_A_Helping_Hand_詞彙表.md` — 詞彙表

### 📗 中文
- `2026-09-07_多重複句學習與訓練.md`
- `2026-09-07_比喻修辭學習與訓練.md`
- `2026-09-07_蘇格拉底與麥穗_填充與運用練習.md`
- `2026-09-07_詞語填充訓練_17詞.md`
- `2026-09-07_詞語填充訓練_17詞_第二回.md`
- `2026-09-07_近義詞學習與訓練.md`
- `ch07_要挑最大的_詞語表.md`

### 🔢 數學
- `2026-09-07_數學_周界面積與大數訓練.md`
- `2026-09-08_數學_小數除法（一）學習與訓練.md`
- `2026-09-13_數學_小數除法（二）做題技巧.md`

### 📄 其他
- `CONDITION10.md`

## 流程

1. Mac 教材更新 → 話俾 Openclaw 知
2. Openclaw copy 新版本嚟呢度 + 整理題目 JSON（`resources/questions/`）
3. Push → Streamlit app 自動讀到新題目

## 注意

- 呢度只存 **MD 教材**（文字）；遊戲 HTML 唔放呢度（games/ 有自己版本）
- 原始檔案永遠以 Mac mini 為準
