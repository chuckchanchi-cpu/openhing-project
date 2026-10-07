# 📚 OpenEduJustan — Project Structure

## 📋 Overview
- **Project:** OpenEduJustan — Primary 6 Learning Platform
- **School:** 光明學校 (Kwong Ming School)
- **Student:** Justan (6A)
- **Subjects:** Chinese, English, Maths, General Studies
- **Platform:** Streamlit + Google Forms + HTML Games

---

## 🗂️ Directory Structure

```
openedujustan/
├── 📄 app.py                          # Main Streamlit app (Practice Platform)
├── 📄 ai_question_generator.py        # AI question generator
├── 📄 practice_platform.py            # Practice platform base
├── 📄 05_AI_題目生成器.py              # AI question generator (Streamlit)
├── 📄 python_quest.py                 # Python learning game (standalone)
├── 📄 PROJECT_STRUCTURE.md            # This file
├── 📄 PROJECT_STATUS.md               # Project status tracker
├── 📄 requirements.txt                # Python dependencies
│
├── 📂 pages/                          # Streamlit multi-page apps
│   ├── 03_English_Grammar.py          # English grammar practice
│   ├── 04_成語練習.py                  # 成語 (idioms) practice
│   ├── 05_Badminton_Trainer_Final.py  # Badminton trainer
│   ├── 06_分數乘法.py                  # Fraction multiplication
│   └── 07_巴士速練.py                  # Bus speed practice
│
├── 📂 python-quest/                   # 🐍 Learning Hub (separate repo)
│   ├── app.py                         # Hub main page
│   ├── pages/
│   │   ├── 01_Python_Quest.py         # Python learning game
│   │   ├── 02_Chinese_練習.py         # Chinese 襯托手法 practice
│   │   └── 03_English_Adverbs.py      # English adverbs practice
│   ├── requirements.txt
│   └── README.md
│
├── 📂 Chinese/                        # 📝 中文 materials & notes
│   ├── 2026-09-26_中文_嫦娥篇近義詞與修辭.md
│   ├── 2026-09-27_中文_第1課諾貝爾填充詞語.md
│   ├── 2026-09-27_中文_第8課啟示的啟示填充詞語.md
│   ├── 2026-09-28_中文_閱讀理解_假蘋果.md
│   ├── 2026-10-04_中文成語單元一.md
│   ├── 2026-10-04_中文課文填空與副詞辨析練習.md
│   ├── 2026-10-04_光明學校_閱讀評估_6A.md
│   ├── 2026-10-06_中文_最後的姿態填空練習.md
│   ├── 2026-10-06_中文_襯托手法_林肯.md
│   ├── Topic_Exercises_Paragraph_Rhetoric_20260920.md
│   ├── Topic_NearSynonyms_Practice.md
│   ├── Unit_3_WisdomSeeds_Exam_20260910.md
│   ├── Unit_8_Paragraph3_Memorization_20260918.md
│   ├── Unit_8_Qishi_LanguageApplication_20260917.md
│   ├── chapter8_full_vocabulary_form_20260918.js
│   ├── chapter8_vocabulary_form_20260917.js
│   ├── chengyu_unit1_form_20261004.js
│   ├── chinese_cloze_15min_car_form_20260927.js
│   ├── chinese_cloze_all_topics_form_20260927.js
│   ├── chinese_cloze_master_form_20260927.js
│   ├── materials/                     # 📸 Original worksheets/photos
│   │   └── 2026-09-10/
│   ├── practice/                      # ✍️ Practice exercises
│   │   ├── 2026-09-07_多重複句學習與訓練.md
│   │   ├── 2026-09-07_比喻修辭學習與訓練.md
│   │   ├── 2026-09-07_蘇格拉底與麥穗_填充與運用練習.md
│   │   ├── 2026-09-07_詞語填充訓練_17詞.md
│   │   ├── 2026-09-07_詞語填充訓練_17詞_第二回.md
│   │   ├── 2026-09-07_近義詞學習與訓練.md
│   │   ├── 2026-10-07_最後的姿態_練習卷.md
│   │   ├── game_hub.html              # 🎮 HTML game hub
│   │   ├── game_比喻.html
│   │   ├── game_複句.html
│   │   ├── game_詞語填充.html
│   │   ├── game_近義詞.html
│   │   └── near_synonym_form.js
│   └── vocab/
│       └── ch07_要挑最大的_詞語表.md
│
├── 📂 English/                        # 📝 English materials & notes
│   ├── 2026-09-26_英文_MooncakeMaths_AHelpingHand.md
│   ├── 2026-09-28_英文_條件句_進行式_連接詞.md
│   ├── 2026-09-29_英文_Revision1_災害詞彙_連接詞.md
│   ├── 2026-10-06_英文_Adverbs_副詞.md
│   ├── Writing_Story_Techniques_20260924.md
│   ├── dictation_1_revision_20260916.md
│   ├── vocabulary_occupations_20260915.md
│   ├── vocabulary_occupations_form_20260917.js
│   ├── materials/                     # 📸 Original worksheets/photos
│   │   ├── 2026-09-10/
│   │   ├── 2026-09-14/
│   │   ├── 2026-09-15/
│   │   ├── 2026-09-16/
│   │   └── 2026-10-06/
│   ├── practice/                      # ✍️ Practice exercises
│   │   ├── 2026-09-07_Unit1_A_Helping_Hand_Practice.md
│   │   ├── 2026-09-15_英文默書1_職業詞語表.md
│   │   ├── 2026-09-16_英文_SimplePresent_PresentContinuous_學習與訓練.md
│   │   ├── 2026-09-16_英文_慈善閱讀_CharityWeek.md
│   │   ├── Assessment_Weaknesses_20260917.md
│   │   ├── Grammar_1_so_Grammar_2_who_which_20260920.md
│   │   ├── Justan_Weakness_VocabFromText_20260917.md
│   │   ├── P6_AHelpingHand_Prewriting1_20260914.md
│   │   ├── Unit_1_Grammar_Exam_20260910.md
│   │   ├── Unit_1_SentenceExpansion_20260910.md
│   │   ├── VocabFromText_TrainingFramework_20260918.md
│   │   ├── english_grammar_unit1_form.js
│   │   ├── game_文法.html
│   │   ├── game_文法15分鐘.html
│   │   ├── game_英文生字.html
│   │   └── vocab_from_text_training_20260918.js
│   └── vocab/
│       └── unit1_A_Helping_Hand_詞彙表.md
│
├── 📂 Maths/                          # 🔢 Maths materials & notes
│   ├── 2026-09-26_數學_奶茶小數四則混合.md
│   ├── 2026-09-27_數學_小數與分數互化.md
│   ├── 2026-09-29_數學_小數分數互化_工作紙12.md
│   ├── 2026-10-04_數學_小數分數互化.md
│   ├── Topic_1_DecimalDivision_I_20260920.md
│   ├── Topic_2_DecimalDivision_Exam_20260910.md
│   ├── Topic_3_DecimalDivisionII_20260913.md
│   ├── Topic_3_DecimalDivisionII_Exercise3_20260914.md
│   ├── Topic_3_DecimalDivisionII_form.js
│   ├── Topic_3_DecimalDivisionII_form_v2.js
│   ├── Topic_3_DecimalDivision_Combined_20260920.md
│   ├── Topic_3_DecimalDivision_WordsProblem_20260920.md
│   ├── Topic_4_DecimalMixedOperations_20260920.md
│   ├── Unit_Exercise_DecimalDivision_20260924.md
│   ├── materials/                     # 📸 Original worksheets/photos
│   │   ├── 2026-09-10/
│   │   ├── 2026-09-13/
│   │   └── 2026-09-14/
│   └── practice/                      # ✍️ Practice exercises
│       ├── 2026-09-07_數學_周界面積與大數訓練.md
│       ├── 2026-09-08_數學_小數除法（一）學習與訓練.md
│       ├── 2026-09-13_數學_小數除法（二）做題技巧.md
│       ├── game_小數除法.html
│       └── game_數學.html
│
├── 📂 General_Studies/                # 🌍 常識 materials & notes
│   ├── 2026-09-26_常識_動物適應環境_能源百科風.md
│   ├── 2026-10-04_常識_動物與環境練習.md
│   ├── Unit_1_BiologicalClassification_Chinese.md
│   ├── Unit_1_BiologicalClassification_Homework_20260913.md
│   ├── Unit_1_BiologicalClassification_Notes_20260913.md
│   ├── Unit_2_Plants_and_Environment_20260917.md
│   ├── Unit_2_Plants_and_Environment_Exercise_20260920.md
│   ├── Unit_3_Animals_and_Environment_20260924.md
│   ├── bio_classification_game.html
│   ├── science_biological_classification_form.js
│   ├── materials/                     # 📸 Original worksheets/photos
│   │   └── 2026-09-13/
│   └── practice/                      # ✍️ Practice exercises
│       ├── 2026-09-07_常識_生物的分類學習與訓練.md
│       ├── 2026-09-17_常識_植物怎樣適應環境_第2課.md
│       └── game_常識.html
│
├── 📂 Guidance/                       # 📖 How-to guides
│   ├── Google表單_建立與批改指引.md
│   ├── Google表單_數學小數除法_成功案例.md
│   ├── google_form_template.js
│   └── google_form_template_maths.js
│
├── 📂 綜合挑戰/                       # 🎮 Cross-subject challenges
│   └── game_綜合挑戰_車程版.html
│
└── 📄 Google Form Scripts (root)
    ├── google_form_apps_script.js
    ├── google_form_apps_script_fixed.js
    ├── google_form_correct_template.js
    ├── google_form_guidance.md
    ├── google_form_math_framework.js
    └── google_form_30min_training.csv
```

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| 📝 Chinese notes | 14 files |
| 📝 English notes | 10 files |
| 🔢 Maths notes | 10 files |
| 🌍 General Studies | 7 files |
| 🎮 HTML games | 10 files |
| 📝 Streamlit pages | 5 pages |
| 📸 Material photos | 25+ images |
| 📄 Total files | ~97 files |

---

## 🚀 Deployment

### Main App (openedujustan)
- **URL:** https://openedujustan.streamlit.app
- **Repo:** GitHub (to be set up)
- **Features:** Practice platform, AI question generator, multi-page

### Learning Hub (python-quest)
- **URL:** https://python-quest.streamlit.app
- **Repo:** https://github.com/chuckchanchi-cpu/python-quest
- **Features:** Python Quest, Chinese 襯托手法, English Adverbs

---

## 📅 Recent Updates

| Date | Subject | Content |
|------|---------|---------|
| 2026-10-07 | 中文 | 最後的姿態 填空練習 |
| 2026-10-06 | 中文 | 襯托手法 — 林肯 |
| 2026-10-06 | English | Adverbs (manner + frequency) |
| 2026-10-06 | Python | Python Quest + Learning Hub |
| 2026-10-04 | 中文 | 成語單元一 |
| 2026-10-04 | 中文 | 光明學校 閱讀評估 6A |
| 2026-10-04 | 數學 | 小數分數互化 |
| 2026-10-04 | 常識 | 動物與環境練習 |

---

## 🎯 Subject Coverage

### 📝 中文 (Chinese)
- 課文填充 (cloze)
- 成語 (idioms)
- 近義詞 (synonyms)
- 修辭手法 (rhetoric: 比喻, 襯托)
- 閱讀理解 (reading comprehension)
- 詞語運用 (vocabulary usage)

### 📝 English
- Grammar (Simple Present, Present Continuous)
- Conditionals
- Adverbs (manner + frequency)
- Vocabulary (occupations, disaster words)
- Story writing techniques
- Dictation practice

### 🔢 數學 (Maths)
- 小數除法 (decimal division)
- 小數分數互化 (decimal-fraction conversion)
- 四則混合 (mixed operations)
- 周界面積 (perimeter & area)

### 🌍 常識 (General Studies)
- 生物分類 (biological classification)
- 植物與環境 (plants & environment)
- 動物與環境 (animals & environment)
- 能源 (energy)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Python 3.9+
- **Forms:** Google Apps Script (JavaScript)
- **Games:** HTML/CSS/JavaScript
- **AI:** Silra API (qwen3.8-flash)
- **Hosting:** Streamlit Community Cloud
- **Version Control:** Git + GitHub

---

## 📝 Notes for Development

1. **File naming:** `{date}_{subject}_{topic}.md` format
2. **Practice folder:** Contains exercises, games, and forms
3. **Materials folder:** Contains original worksheet photos
4. **Games:** HTML games work offline, no server needed
5. **Streamlit pages:** Auto-show in sidebar navigation
6. **AI integration:** Uses Silra API for question generation and explanations

---

*Last updated: 2026-10-07*