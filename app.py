#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Research Assistant (Streamlit multipage router)

用 st.navigation 自訂 page 名稱（頁面檔名全部 ASCII，避免 Streamlit 對
中文/emoji 檔名嘅 page scan 問題 — 2026-09-16 教訓）
"""

import os
import streamlit as st
from streamlit.navigation import Page

# 將 Streamlit Secrets 注入環境變數（令 subprocess 繼承）
# 本地開發時 secrets 唔存在，會用 .env / 預設值
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k, v in st.secrets.items():
        os.environ[k] = str(v)

pages = [
    Page("pages/01_Research_Assistant.py", title="🦀 Research Assistant", icon="🦀", default=True),
    Page("pages/02_Chart_Detail.py", title="📊 Chart Detail", icon="📊"),
    Page("pages/03_AI_Essay_Grader.py", title="📝 AI 作文批改", icon="📝"),
    Page("pages/04_AI_Practice.py", title="🏋️ AI 練習平台", icon="🏋️"),
    Page("pages/05_AI_Question_Generator.py", title="🛠️ AI 題目生成器", icon="🛠️"),
]

pg = st.navigation(pages)
pg.run()
