#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Research Assistant Web App (Streamlit)

功能：
1. 用戶輸入研究主題
2. 選擇報告深度（簡化版 / 完整版）
3. 獲取結構化 Markdown 報告
4. 嵌入互動圖表
"""

import streamlit as st
import subprocess
import os
import json
from datetime import datetime

# 配置
st.set_page_config(
    page_title="🦀 Openhing Research Assistant",
    page_icon="🦀",
    layout="wide"
)

st.title("🦀 Openhing - AI Research Assistant")
st.caption("Enhancing Human Intelligence through AI Agents")

# 側邊欄
with st.sidebar:
    st.header("⚙️ 設置")
    topic = st.text_input("📚 研究主題", "AI Agent 在學術研究的應用")
    depth = st.selectbox("📊 報告深度", ["簡化版 (快速)", "完整版 (深入)"])
    
    if st.button("🚀 生成報告"):
        with st.spinner("正在分析..."):
            # 調用 CrewAI v2 API
            result = run_crewai(topic, depth)
            st.session_state.report = result

# 主內容區
st.title("🦀 Openhing - AI Research Assistant")
st.caption("Enhancing Human Intelligence through AI Agents | Powered by CrewAI + Serper API")

# 側邊欄
with st.sidebar:
    st.header("⚙️ 設置")
    topic = st.text_input("📚 研究主題", "AI Agent 在學術研究的應用")
    depth = st.selectbox("📊 報告深度", ["簡化版 (快速)", "完整版 (深入)"])
    
    if st.button("🚀 生成報告"):
        with st.spinner("正在分析..."):
            result = run_crewai(topic, depth)
            st.session_state.report = result

# 顯示報告
if 'report' in st.session_state:
    report = st.session_state.report
    
    st.subheader("📋 報告結果")
    st.caption(f"🕒 生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown(report, unsafe_allow_html=True)
    
    st.download_button(
        label="💾 下載報告 (Markdown)",
        data=report,
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

# 圖表展示區
st.divider()
st.subheader("📊 數據視覺化")

col1, col2, col3 = st.columns(3)

with col1:
    st.html_embed(open('/Users/fring1117/Desktop/openhing/resources/charts/population_pyramid.html').read(), width=600, height=400)

with col2:
    st.html_embed(open('/Users/fring1117/Desktop/openhing/resources/charts/youth_employment_trends.html').read(), width=600, height=400)

with col3:
    st.html_embed(open('/Users/fring1117/Desktop/openhing/resources/charts/direction_energy.html').read(), width=600, height=400)

# 底部
st.divider()
st.caption("Powered by CrewAI 1.15 + DeepSeek V3.2 | https://github.com/chuckchanchi-cpu/openhing-project")


def run_crewai(topic, depth):
    """調用 CrewAI API 生成報告"""
    
    # 使用簡化版腳本（可靠）
    script_path = "/Users/fring1117/Desktop/openhing/scripts/research_agent_simple.py"
    
    # 修改腳本中的 topic
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_topic = topic.replace('"', "'")
    content = content.replace(
        'topic = "AI Agent 喺學術研究應用"',
        f'topic = "{new_topic}"'
    )
    
    # 根據深度調整 max_tokens
    if depth == "完整版 (深入)":
        content = content.replace('max_tokens=2000', 'max_tokens=3000')
    
    # 寫入臨時文件
    temp_script = "/tmp/openhing_temp_report.py"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 執行
    try:
        result = subprocess.run(
            ['python3.11', temp_script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # 提取報告部分（去掉警告信息）
        output = result.stdout
        for line in output.split('\n'):
            if '✅ 分析完成!' in line or '### 1.' in line:
                return '\n'.join(output.split(line)[-1:])
        
        return output
    
    except Exception as e:
        return f"❌ 錯誤: {str(e)}\n\n請檢查 API 配置是否正確。"
