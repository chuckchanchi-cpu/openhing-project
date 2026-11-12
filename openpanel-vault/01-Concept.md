# 01 — OpenPanel 理念

## 核心主張
重大決策**唔應該由單一視角**決定。OpenPanel 用多個 AI agent（唔同 model / 唔同專業立場）審視同一議題，然後喺關鍵節點**停低等人類拍板**。

## 三個支柱

### 1. 多視角（Prospectives）
- 同一份數據 brief，多個席位獨立分析
- 席位之間可以**互相挑戰**（cross-examination），唔係各說各話
- 關鍵設計：**同一份數據**，避免各人搵料各說各話；**唔同 brain**（唔同 model），避免共同偏見

### 2. Human Stops（人類停靠點）
Agent 討論到以下節點必須停低：
1. 確認議題範圍 / 視角組合
2. 審視初步結論
3. 最終拍板前 sanity check
> 冇人類開聲，唔好自己衝落去

### 3. 可審計（Auditability）
- 每個結論要追得返：數據來源 → 邏輯鏈 → 機率判斷
- 呢個 Obsidian 庫就係審計工具
- 席位要有「乜嘢會令我改變睇法」嘅 falsifiability

## 成立經過
2026-11-12 Chuck 指定建立，Trial #1 同日完成試跑。
相關：[[02-Architecture]] ｜ [[03-Logic-Flow]]
