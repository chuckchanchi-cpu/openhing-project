#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 圖表詳情頁面 (Streamlit Multi-Page)

功能：
1. 選擇要查看嘅圖表
2. 全屏查看 + 互動式操作
3. 下載圖表為 PNG/PDF
"""

import streamlit as st
import os
import json
import re
from datetime import datetime

st.set_page_config(
    page_title="📊 數據視覺化",
    page_icon="📊",
    layout="wide"
)

# 標題
st.title("📊 數據視覺化 - 詳細查看")
st.caption("點擊左側菜單返回主頁")

# 導航回主頁
st.markdown("""
[🏠 返回研究助手](https://openhing-project-iyhfozjplwp6qdw3chkesk.streamlit.app)
""")

st.divider()

# 圖表目錄
chart_dir = os.path.join(os.path.dirname(__file__), "resources", "charts")

# 圖表列表
charts = [
    ("population_pyramid.html", "人口金字塔", "👥"),
    ("youth_employment_trends.html", "就業趨勢", "💼"),
    ("direction_energy.html", "能量分析", "⚡")
]

# 側邊欄選擇圖表
with st.sidebar:
    st.header("📋 選擇圖表")
    selected_chart = st.selectbox(
        "選擇要查看嘅圖表",
        options=[c[0] for c in charts],
        format_func=lambda x: f"{[c[2] for c in charts][[c[0] for c in charts].index(x)]} {[c[1] for c in charts][[c[0] for c in charts].index(x)]}"
    )
    
    chart_info = [c for c in charts if c[0] == selected_chart][0]
    icon, title = chart_info[2], chart_info[1]
    
    st.markdown(f"### {icon} {title}")
    
    # 下載按鈕
    if st.button("💾 下載為 PNG"):
        chart_path = os.path.join(chart_dir, selected_chart)
        if os.path.exists(chart_path):
            st.success("準備就緒！請右鍵另存圖片。")
            st.info("提示：Plotly 圖表可以右鍵 → Save Image as PNG")

# 檢查文件是否存在
chart_path = os.path.join(chart_dir, selected_chart)

if not os.path.exists(chart_path):
    st.error(f"❌ 找不到文件：{selected_chart}")
    st.info("💡 請確保 `resources/charts/` 文件夾存在並包含圖表文件。")
else:
    # 加載 Plotly 圖表
    def load_plotly_figure(html_path):
        """從 Plotly HTML 提取 figure"""
        with open(html_path, encoding='utf-8') as f:
            c = f.read()
        start = c.find('Plotly.newPlot(')
        if start == -1:
            return None
        seg = c[start + len('Plotly.newPlot('):]
        m1 = re.match(r'\s*"(.*?)"', seg)
        if not m1:
            return None
        dec = json.JSONDecoder()
        idx = m1.end()
        while seg[idx] in ' ,\n\r\t':
            idx += 1
        data, end = dec.raw_decode(seg, idx)
        idx2 = end
        while seg[idx2] in ' ,\n\r\t':
            idx2 += 1
        layout, _ = dec.raw_decode(seg, idx2)
        # 移除固定尺寸，令圖表自適應
        layout.pop('width', None)
        layout.pop('height', None)
        layout['autosize'] = True
        return data, layout
    
    try:
        fig_data = load_plotly_figure(chart_path)
        if fig_data:
            import plotly.graph_objects as go
            data, layout = fig_data
            fig = go.Figure(data=data, layout=layout)
            
            # 全屏顯示圖表
            st.plotly_chart(fig, use_container_width=True, key=f"full_{selected_chart}")
            
            # 操作提示
            st.divider()
            st.subheader("💡 操作指南")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("🔍 **縮放**\n用滑鼠拖曳選取區域放大")
            with col2:
                st.info("📦 **平移**\n按住滑鼠左鍵拖曳移動")
            with col3:
                st.info("💾 **下載**\n右上角 ⬇️ 按鈕下載 PNG/SVG")
            
        else:
            st.warning("⚠️ 無法提取圖表數據")
            st.info("💡 請檢查 HTML 文件格式是否正確。")
    except Exception as e:
        st.error(f"❌ 加載失敗：{str(e)}")
        st.exception(e)
