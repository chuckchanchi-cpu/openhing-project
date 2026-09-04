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
from datetime import datetime

# 配置
st.set_page_config(
    page_title="🦀 Openhing Research Assistant",
    page_icon="🦀",
    layout="wide"
)

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

# 檢查 chart files 是否存在
chart_dir = os.path.join(os.path.dirname(__file__), "resources", "charts")
has_charts = os.path.exists(chart_dir)


def load_plotly_figure(html_path):
    """從 Plotly HTML 提取 figure（用 raw_decode 處理巢狀 JSON）"""
    import json
    import re
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


if has_charts:
    col1, col2, col3 = st.columns(3)

    charts = [
        ("population_pyramid.html", "人口金字塔"),
        ("youth_employment_trends.html", "就業趨勢"),
        ("direction_energy.html", "能量分析")
    ]

    for i, (chart_file, title) in enumerate(charts):
        chart_path = os.path.join(chart_dir, chart_file)
        with [col1, col2, col3][i]:
            if os.path.exists(chart_path):
                try:
                    fig_data = load_plotly_figure(chart_path)
                    if fig_data:
                        import plotly.graph_objects as go
                        data, layout = fig_data
                        fig = go.Figure(data=data, layout=layout)
                        st.plotly_chart(fig, use_container_width=True, key=f"chart_{chart_file}")
                    else:
                        st.info(f"{title}: 無法提取圖表數據")
                except Exception as e:
                    st.error(f"Error loading {title}: {str(e)}")
            else:
                st.info(f"{title} chart not found")
else:
    st.info("Chart directory not found. Charts will be available after deployment.")

# 底部
st.divider()
st.caption("Powered by CrewAI 1.15 + DeepSeek V3.2 | https://github.com/chuckchanchi-cpu/openhing-project")


def run_crewai(topic, depth):
    """調用 CrewAI API 生成報告"""
    
    # 使用簡化版腳本（可靠）
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "research_agent_simple.py")
    
    # 修改腳本中的 topic
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_topic = topic.replace('"', "'")
    # 用 regex 匹配任何預設主題（穩陣過 hardcode 特定字串）
    import re
    content = re.sub(
        r'topic = ".*?"',
        lambda m: f'topic = "{new_topic}"',
        content,
        count=1
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
            ['python3', temp_script],
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
