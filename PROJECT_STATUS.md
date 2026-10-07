# 📚 OpenEduJustan 項目狀態快照

**最後更新**: 2026-10-07 14:44 HKT
**負責人**: Claw (🦀)

---

## 項目概述

- **名稱**: OpenEduJustan（小學插班生練習平台）
- **GitHub**: `chuckchanchi-cpu/openhing-project` (branch: main)
- **技術棧**: Streamlit + Silra API (qwen3.8-flash)
- **用途**: 幫香港小學插班生做練習（中文、英文、數學、常識）

---

## 啟動方法

```bash
cd ~/Desktop/openedujustan
streamlit run app.py --server.headless true
```

- **Port**: 8502（自動 fallback，8501 可能被佔）
- **本地**: http://localhost:8502
- **網絡**: http://192.168.111.248:8502
- **外部**: http://161.81.241.58:8502

---

## API 配置

| 項目 | 值 |
|------|-----|
| **Silra API URL** | `https://api.silra.cn/v1/chat/completions` |
| **Silra API Key** | `sk-HfiuPr1xWenSQUsB5x0PPtHW3gVYN9MBUXTVQ67orNPED24y` |
| **Model** | `qwen3.8-flash` |
| **存儲方式** | 硬編碼喺各 .py 文件（冇 .streamlit/secrets.toml） |

---

## 頁面結構

```
openedujustan/
├── app.py                          # 主頁（申請系統 + AI 寫作輔助）
├── practice_platform.py            # 練習平台（四科批改）
├── ai_question_generator.py        # AI 出題器
├── 05_AI_題目生成器.py              # 舊版出題器
├── pages/
│   ├── 03_English_Grammar.py       # 英文文法練習
│   ├── 04_成語練習.py               # 中文成語
│   ├── 05_Badminton_Trainer_Final.py # 羽毛球教練
│   ├── 06_分數乘法.py               # 數學分數乘法
│   └── 07_巴士速練.py               # 🚌 Mobile-first 速練
├── python-quest/                   # Python 學習遊戲
│   ├── app.py
│   └── pages/
│       ├── 01_Python_Quest.py
│       ├── 02_Chinese_練習.py
│       └── 03_English_Adverbs.py
└── requirements.txt                # streamlit>=1.30.0
```

---

## 四科教材

| 科目 | 資料夾 | 內容 |
|------|--------|------|
| 中文 | `Chinese/` | ~20 個 MD + practice/ + materials/ + vocab/ |
| 英文 | `English/` | ~10 個 MD + practice/ + materials/ + vocab/ |
| 數學 | `Maths/` | ~15 個 MD + practice/ + materials/ |
| 常識 | `General_Studies/` | ~10 個 MD + practice/ + materials/ |

---

## Google Form 整合

- **Apps Script**: `google_form_apps_script_fixed.js`
- **設定指南**: `google_form_guidance.md`
- **CSV 模板**: `google_form_30min_training.csv`
- **30 分鐘車程訓練表單**: https://docs.google.com/forms/d/e/1FAIpQLSfa58z_6o367Xqh_rYNV9055mNhNDWeY17HwYrpnFVnZEbZvA/viewform

---

## 依賴

```
streamlit>=1.30.0
```

Python packages（系統已裝）:
- streamlit 1.50.0
- requests 2.32.5
- pandas 2.3.3
- openai 1.109.1

---

## .streamlit 配置

**❌ 不存在** — 冇 secrets.toml 或 config.toml。API key 全部硬編碼喺 .py 文件。

---

## 備註

- Silra API key 如果變咗，要逐個 .py 文件改
- Streamlit port 如果 8501 被佔會自動跳去 8502
- `python-quest/` 有獨立嘅 git repo
- 教材 materials/ 資料夾被 .gitignore 排除