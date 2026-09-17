# Justan 英文薄弱項訓練框架 — 從文章中找詞填空

## 📋 訓練目標

**Justan 的主要薄弱點：**
- 無法從課文/文章中快速定位正確的詞彙或單字
- 填空題時不知道該從哪裡找答案
- 對詞彙在上下文中的用法理解不足

---

## 🎯 訓練設計原則

### 1️⃣ 文章選擇標準
- **長度**：150-300 字（適合小六學生）
- **主題**：日常生活、學校生活、動物、環保等
- **難度**：與課文 P.3 "Get ready to meet your new family member!" 相當
- **詞彙量**：包含 6-8 個目標詞彙

### 2️⃣ 題目設計要求
- **格式**：短文章 + 空格填空
- **提示**：每題提供 Word Bank（詞彙庫）
- **數量**：每篇文章 4-6 題
- **難度遞增**：從簡單到困難

### 3️⃣ 反饋機制
- **正確時**：顯示 "✅ Correct! Well done!"
- **錯誤時**：顯示 "❌ Wrong! The answer is: [正確答案]"
- **提示**：每題附 💡 提示說明如何找到答案

---

## 📝 文章範例模板

### 文章結構：
```markdown
Article: "[文章標題]"

[第一段：介紹主題]

[第二段：展開細節]

[第三段：總結或建議]

Word Bank: [詞彙選項]
```

### 題目格式：
```markdown
addShortAnswer(form, 'Article: "[文章標題]"\n\n[文章內容]\n\nWord Bank: [詞彙選項]', '[正確答案]', '💡 提示：[如何找到答案的說明]');
```

---

## 📚 推薦文章主題

| 主題 | 重點詞彙 | 相關課文 |
|------|----------|----------|
| **Pet Adoption** | adopt / animal shelter / stray pets / responsible for / abandon | P.3 Get ready to meet your new family member! |
| **Environmental Protection** | responsible / save / protect / waste / pollute | P.10 Protect Our Planet |
| **School Life** | favourite / interesting / boring / difficult / easy | P.15 My School Day |
| **Family & Friends** | love / care / support / help / understand | P.20 My Family |
| **Health & Fitness** | exercise / healthy / diet / rest / energy | P.25 Stay Healthy |

---

## 🔧 生成步驟（給 AI 應用）

### Step 1: 選擇文章主題
- 從上述主題中選擇一個
- 確保與 Justan 的學習進度相符

### Step 2: 撰寫文章
- 長度：150-300 字
- 包含 6-8 個目標詞彙
- 使用簡單句式和常見語法

### Step 3: 設計題目
- 將目標詞彙替換為空格
- 每個空格對應一道題
- 提供 Word Bank（包含正確答案和干擾項）

### Step 4: 添加提示
- 每題附 💡 提示
- 說明如何從上下文中找到線索
- 解釋詞彙的意思和用法

### Step 5: 測試與調整
- 自己先做一遍題目
- 確認答案正確無誤
- 檢查提示是否清晰易懂

---

## 📖 完整範例

### 文章：Pet Adoption

```markdown
Article: "Get Ready to Meet Your New Family Member!"

If you want a pet, you can save money and _____(1) one from an animal shelter. Animal shelters rescue stray pets from the streets. Once you have a pet, you must be _____(2) its care. You should never _____(3) it when it gets old or sick.

Puppies and kittens are lovely, but they might scratch the furniture or make a mess while you are out. An adult animal will be more _____(4) for you because they are calmer. Before adopting, you need to complete an _____(5).

After adopting, a vet will give your pet a health check. You also need to take your pet for _____(6) at the vet's clinic. Finally, you must apply for a dog licence within three months.
```

### 題目設計：

| 題號 | 空格 | 正確答案 | Word Bank | 提示 |
|------|------|----------|-----------|------|
| 1 | _____(1) | adopt | abandon / adopt / responsible for | save money and ___ one → 領養一個 |
| 2 | _____(2) | responsible for | abandon / adopt / responsible for | be ___ its care → 對它的照顧負責 |
| 3 | _____(3) | abandon | abandon / adopt / responsible for | never ___ it → 永遠不要拋棄它 |
| 4 | _____(4) | suitable | suitable / application form | more ___ for you → 更適合你 |
| 5 | _____(5) | application form | suitable / application form | complete an ___ → 完成申請表 |
| 6 | _____(6) | injections | injections / dog licence / health check | take your pet for ___ → 帶寵物打疫苗 |

---

## 💡 教學策略

### 1. 上下文線索識別
- 教 Justan 注意空格前後的詞
- 判斷需要什麼類型的詞（名詞？動詞？形容詞？）
- 尋找固定搭配（如 "make a mess", "responsible for"）

### 2. 快速定位技巧
- 讀懂題目要求
- 回到課文找到相關段落
- 根據語境選擇正確詞彙

### 3. 詞彙理解
- 理解詞彙在特定句子中的意思
- 區分同義詞的細微差別
- 掌握固定搭配和常用組合

---

## 📊 評估標準

| 能力指標 | 良好 | 需改進 |
|----------|------|--------|
| 快速定位詞彙 | 能在30秒內找到答案 | 超過1分鐘或找不到 |
| 詞彙理解準確度 | 90%以上正確 | 低於70%正確 |
| 固定搭配掌握 | 能正确使用 | 常混淆或誤用 |
| 上下文判斷 | 能根據線索推斷 | 需要提示才能回答 |

---

## 📁 儲存位置
此框架文件已保存至：  
`~/Desktop/openedujustan/English/practice/VocabFromText_TrainingFramework_20260918.md`

AI 應用可根據此框架生成更多針對性訓練材料！🦀
