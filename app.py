#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Research Assistant (Streamlit multipage home)

頁面檔名全部 ASCII（避免 Streamlit 對中文/emoji 檔名 page scan 問題）。
Pages 自動 scan 模式 — sidebar 顯示 pages/ 入面所有頁面。
"""

import os
import streamlit as st

# 將 Streamlit Secrets 注入環境變數（令 subprocess 繼承）
# 本地開發時 secrets 唔存在，會用 .env / 預設值
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k, v in st.secrets.items():
        os.environ[k] = str(v)

st.set_page_config(
    page_title="🦀 Openhing",
    page_icon="🦀",
    layout="wide"
)

st.title("🦀 Openhing - AI Research Assistant")
st.caption("Enhancing Human Intelligence through AI Agents")

st.markdown("""
### 👋 歡迎！揀左邊 sidebar 開始：

| 頁面 | 用途 |
|------|------|
| 🦀 **01_Research_Assistant** | AI 研究報告生成（CrewAI） |
| 📊 **02_Chart_Detail** | 互動圖表（人口/就業/能源） |
| 📝 **03_AI_Essay_Grader** | AI 作文批改（上傳 CSV / 直接貼文） |
| 🏋️ **04_AI_Practice** | AI 練習平台（學生作答 + 即時批改） |
| 🛠️ **05_AI_Question_Generator** | AI 題目生成器（生成 → review → 發布） |

> 💡 **練習流程：** 05 生成題目 → 發布 → 04 練習平台 → 揀「🆕 老師新生成」
""")
