#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - 香港人口數據視覺化
生成互動圖表用於研究報告

功能：
1. 香港 2026 人口金字塔 (對比 2046 預測)
2. 青年就業趨勢示意圖
3. 5大關鍵方向能量圖
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

OUTPUT_DIR = "/Users/fring1117/Desktop/openhing/resources/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_population_pyramid():
    age_groups = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95-99", "100+"]
    
    male_2026 = [1.4, 1.7, 2.0, 2.0, 1.7, 2.3, 3.0, 3.1, 3.1, 3.1, 3.2, 3.2, 3.7, 3.8, 3.1, 2.2, 1.1, 0.8, 0.4, 0.1, 0.0]
    female_2026 = [1.3, 1.6, 2.0, 1.9, 2.3, 2.3, 3.5, 4.2, 4.9, 4.8, 4.6, 4.4, 4.6, 4.1, 3.4, 2.4, 1.2, 1.0, 0.7, 0.3, 0.1]
    male_2046 = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 4.8, 5.0, 5.2, 5.5]
    female_2046 = [0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.6, 5.8]
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("2026 (實際)", "2046 (預測)"))
    fig.add_trace(go.Bar(x=[-x for x in male_2026], y=age_groups, orientation='h', name='男性', marker_color='#4e79a7'), row=1, col=1)
    fig.add_trace(go.Bar(x=female_2026, y=age_groups, orientation='h', name='女性', marker_color='#f28eb1'), row=1, col=1)
    fig.add_trace(go.Bar(x=[-x for x in male_2046], y=age_groups, orientation='h', name='男性', marker_color='#4e79a7', opacity=0.6), row=1, col=2)
    fig.add_trace(go.Bar(x=female_2046, y=age_groups, orientation='h', name='女性', marker_color='#f28eb1', opacity=0.6), row=1, col=2)
    fig.update_layout(title_text="香港人口金字塔對比 (2026 vs 2046)", barmode='stack', width=800, height=600, showlegend=False)
    fig.write_html(os.path.join(OUTPUT_DIR, "population_pyramid.html"), include_plotlyjs=False)
    print("✅ population_pyramid.html")


def create_youth_employment_trends():
    years = list(range(2026, 2046))
    ai_related = [5, 8, 12, 18, 25, 32, 40, 48, 55, 62, 68, 72, 75, 78, 80, 82, 84, 85, 86, 87]
    traditional = [85, 82, 78, 72, 65, 58, 50, 42, 35, 28, 22, 18, 15, 12, 10, 8, 7, 6, 5, 4]
    cross_domain = [10, 15, 22, 30, 40, 50, 60, 68, 75, 80, 85, 88, 90, 92, 93, 94, 95, 95, 96, 96]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=ai_related, mode='lines+markers', name='AI 相關職位', line=dict(color='#ff6b6b', width=3)))
    fig.add_trace(go.Scatter(x=years, y=traditional, mode='lines+markers', name='傳統職業', line=dict(color='#4e79a7', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cross_domain, mode='lines+markers', name='跨領域技能', line=dict(color='#51cf66', width=3)))
    fig.update_layout(title="香港青年就業趨勢預測 (2026-2046)", xaxis_title="年份", yaxis_title="需求 (%)", legend=dict(x=0.02, y=0.98), hovermode='x unified', width=800, height=600)
    fig.write_html(os.path.join(OUTPUT_DIR, "youth_employment_trends.html"), include_plotlyjs=False)
    print("✅ youth_employment_trends.html")


def create_direction_energy_chart():
    directions = ['AI Collaboration', 'Digital Ethics', 'Cross-domain Integration', 'Mental Health Balance', 'Employment Transition']
    importance = [95, 85, 98, 80, 92]
    growth = [90, 75, 88, 70, 85]
    demand = [92, 82, 95, 78, 90]
    colors = ['#ff6b6b', '#4e79a7', '#51cf66', '#f08c5d', '#9b59b6']
    
    fig = go.Figure()
    for i in range(3):
        r_values = [importance[i//2] if i==0 else (growth[i-1] if i==1 else demand[i-2])]
    
    # 直接用 graph_objects
    fig.add_trace(go.Scatterpolar(r=importance, theta=directions, fill='toself', name='重要性', line_color='#ff6b6b'))
    fig.add_trace(go.Scatterpolar(r=growth, theta=directions, fill='toself', name='增長潛力', line_color='#4e79a7'))
    fig.add_trace(go.Scatterpolar(r=demand, theta=directions, fill='toself', name='市場需求', line_color='#51cf66'))
    
    fig.update_layout(title="5 Major Directions Energy Analysis", font=dict(family="Arial", size=14), width=600, height=600)
    fig.write_html(os.path.join(OUTPUT_DIR, "direction_energy.html"), include_plotlyjs=False)
    print("✅ direction_energy.html")


if __name__ == "__main__":
    print("🦀 開始生成圖表...")
    print("=" * 50)
    create_population_pyramid()
    create_youth_employment_trends()
    create_direction_energy_chart()
    print("=" * 50)
    print(f"✅ 所有圖表已生成到: {OUTPUT_DIR}")
