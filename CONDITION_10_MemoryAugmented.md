# Condition 10: 情境式記憶 (Memory-augmented / Semantic Memory)

## 🎯 核心原則
根據情境動態檢索與寫入記憶，讓 Agent 越用越聰明。

---

## ✅ 啟動前檢查清單（每次任務前必讀）

### 1️⃣ 記憶結構化
- [ ] 長期記憶：MEMORY.md + memory/YYYY-MM-DD.md
- [ ] 短期記憶：當前會話上下文
- [ ] 知識庫：skills/SKILL.md + TOOLS.md

### 2️⃣ 情境感知
- [ ] 識別當前場景（Discord/WhatsApp/TUI/Group Chat）
- [ ] 判斷是否需要調用特定技能（Skill）
- [ ] 確認用戶偏好（語言、格式、模型）

### 3️⃣ 記憶檢索
- [ ] memory_search 相關內容
- [ ] memory_get 精確提取
- [ ] 避免重複詢問已知資訊

### 4️⃣ 記憶寫入
- [ ] 重要決策 → MEMORY.md
- [ ] 日常互動 → memory/YYYY-MM-DD.md
- [ ] 工具設定 → TOOLS.md
- [ ] 技能更新 → skills/SKILL.md

### 5️⃣ 情境適配
- [ ] WhatsApp → 廣東話口語、短句、emoji
- [ ] Discord → 可適當使用 markdown
- [ ] 技術文檔 → Sepia 專業文體
- [ ] 代碼/Tickets → 簡潔、無廢話

---

## 📁 文件夾結構規範

```
~/Desktop/openedujustan/
├── Chinese/          # 中文練習
│   ├── Unit_3_WisdomSeeds_Exam_20260910.md
│   └── practice/
│       └── near_synonym_form.js
├── English/          # 英文練習
│   ├── practice/
│   │   ├── Unit_1_Grammar_Exam_20260910.md
│   │   ├── Unit_1_SentenceExpansion_20260910.md
│   │   └── english_grammar_unit1_form.js
│   └── vocab/
├── Maths/            # 數學練習
│   └── Topic_2_DecimalDivision_Exam_20260910.md
├── google_form_*     # Google Form 框架與腳本
└── memory/           # 每日記憶文件
    └── YYYY-MM-DD.md
```

---

## 🔧 執行流程（每次任務前）

1. **Read** → 讀取 MEMORY.md + 近期 daily notes
2. **Search** → memory_search 相關內容
3. **Adapt** → 根據情境調整回應風格
4. **Execute** → 執行任務
5. **Write** → 記錄結果到 appropriate file
6. **Update** → 更新 MEMORY.md 若涉及重大決策

---

## 💡 關鍵提醒

- ✅ 私有資訊只存在 main session 的 MEMORY.md
- ✅ Group chat 中不載入 MEMORY.md
- ✅ 所有項目文件必須存於 `~/Desktop/openedujustan/`
- ✅ 優先使用已驗證的框架（如 google_form_math_framework.js）
- ✅ 避免重複造輪子，先查已有文件

---

## 🚀 當前狀態確認

[ ] MEMORY.md 已讀取  
[ ] memory/2026-09-12.md 已讀取  
[ ] openedujustan 文件夾結構已確認  
[ ] Google Form 框架已熟悉  
[ ] 中文近義詞辨析技巧已掌握  
[ ] 英文擴寫句子技巧已掌握  

**準備開始任務！** 🦀
