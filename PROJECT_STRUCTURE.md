# 📁 OpenEduJustan 專案結構摘要

**專案名稱：** OpenEduJustan  
**用途：** AI 題目生成平台 / 學習應用程式  
**技術：** Streamlit (Python) + Google Forms API  
**托管：** Streamlit Cloud  
**GitHub：** github.com/chuckchanchi-cpu/openhing-project

---

## 🗂️ 資料夾結構

```
openedujustan/
├── 📄 根目錄檔案
│   ├── app.py                    # 主應用程式 (入學申請系統)
│   ├── practice_platform.py       # 練習平台
│   ├── ai_question_generator.py # AI 題目生成器
│   ├── 05_AI_題目生成器.py       # AI 題目生成頁面
│   ├── requirements.txt         # Python 依賴
│   └── OPENCLAW_SETUP.md        # OpenClaw 設定記錄
│
├── 📂 pages/                     # Streamlit 多頁面
│   ├── 03_English_Grammar.py    # 英文文法練習
│   ├── 04_成語練習.py            # 中文成語練習
│   ├── 05_Badminton_Trainer_Final.py  # 羽毛球訓練
│   └── 06_分數乘法.py            # 數學分數乘法練習
│
├── 📂 Chinese/                   # 中文科
│   ├── 2026-09-27_中文_第1課諾貝爾填充詞語.md
│   ├── 2026-09-28_中文_閱讀理解_假蘋果.md
│   ├── 2026-10-04_中文課文填空與副詞辨析練習.md
│   ├── 2026-10-06_中文_最後的姿態填空練習.md
│   ├── practice/                # 練習教材
│   │   ├── 詞語填充訓練_17詞.md
│   │   ├── 近義詞學習與訓練.md
│   │   └── 多重複句學習與訓練.md
│   └── vocab/                   # 詞彙表
│
├── 📂 English/                   # 英文科
│   ├── 2026-10-06_英文_Adverbs_副詞.md
│   ├── practice/
│   └── vocab/
│
├── 📂 Maths/                     # 數學科
│   ├── 2026-09-26_數學_奶茶小數四則混合.md
│   ├── 2026-09-27_數學_小數與分數互化.md
│   ├── 2026-10-04_數學_小數分數互化.md
│   ├── 2026-10-06_數學_分數乘法.md
│   ├── practice/                 # 練習遊戲
│   │   └── game_數學.html
│   └── materials/
│
├── 📂 General_Studies/           # 常識科
│   ├── Unit_1_BiologicalClassification_Notes_20260913.md
│   ├── Unit_2_Plants_and_Environment_20260917.md
│   ├── Unit_3_Animals_and_Environment_20260924.md
│   ├── 2026-10-04_常識_動物與環境練習.md
│   ├── practice/
│   └── materials/
│
├── 📂 Guidance/                  # 升學輔導
│   ├── google_form_guidance.md
│   ├── google_form_math_framework.js
│   └── google_form_*.js         # Google Forms 自動化腳本
│
├── 📂 綜合挑戰/                   # 綜合挑戰題目
│
└── 📂 .github/workflows/         # CI/CD
```

---

## 🎯 主要功能

### 1. 主頁 (app.py)
- 入學申請系統
- AI 寫作助手（廣東話）
- 自推薦信、各部分輔導

### 2. 練習平台 (practice_platform.py)
- 各科練習整合

### 3. AI 題目生成器
- 根據輸入內容自動生成練習題
- 支援選擇題、填充題、問答題

---

## 📱 已部署的 Streamlit Apps

| App | URL | 描述 |
|-----|-----|------|
| OpenEduJustan | openhing-project.streamlit.app | 主學習平台 |
| Python Quest | python-quest.streamlit.app | Python 學習遊戲 |

---

## 🔧 AI 模型配置

- **預設模型：** MiniMax-M2.5
- **API：** Silra API (https://api.silra.cn/v1/)
- **可用模型：** qwen3.6-plus, qwen3.8-flash, deepseek-chat

---

## 📝 最近的更新記錄

- **2026-10-07:** 分數乘法練習頁面
- **2026-10-06:** 襯托手法（中文）、Adverbs（英文）
- **2026-10-05:** OpenClaw 設定完成

---

## 🚀 部署流程

1. 推送更新到 GitHub：`git push origin main`
2. Streamlit Cloud 自動部署（約 30 秒）
3. 訪問對應 URL 即可使用
