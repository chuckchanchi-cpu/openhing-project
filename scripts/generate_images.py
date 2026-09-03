#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - 生成 PNG 圖片用於 Markdown 報告

功能：
1. 人口金字塔 (2026 vs 2046)
2. 青年就業趨勢
3. 5大關鍵方向能量圖
"""

import plotly.graph_objects as go
import os

PNG_DIR = "/Users/fring1117/Desktop/openhing/resources/images"
os.makedirs(PNG_DIR, exist_ok=True)


def create_population_pyramid_png():
    age_groups = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95-99", "100+"]
    
    male_2026 = [1.4, 1.7, 2.0, 2.0, 1.7, 2.3, 3.0, 3.1, 3.1, 3.1, 3.2, 3.2, 3.7, 3.8, 3.1, 2.2, 1.1, 0.8, 0.4, 0.1, 0.0]
    female_2026 = [1.3, 1.6, 2.0, 1.9, 2.3, 2.3, 3.5, 4.2, 4.9, 4.8, 4.6, 4.4, 4.6, 4.1, 3.4, 2.4, 1.2, 1.0, 0.7, 0.3, 0.1]
    male_2046 = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 4.8, 5.0, 5.2, 5.5]
    female_2046 = [0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.6, 5.8]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[-x for x in male_2026], y=age_groups, orientation='h', name='Male 2026', marker_color='#4e79a7'))
    fig.add_trace(go.Bar(x=female_2026, y=age_groups, orientation='h', name='Female 2026', marker_color='#f28eb1'))
    fig.add_trace(go.Bar(x=[-x for x in male_2046], y=age_groups, orientation='h', name='Male 2046', marker_color='#4e79a7', opacity=0.5))
    fig.add_trace(go.Bar(x=female_2046, y=age_groups, orientation='h', name='Female 2046', marker_color='#f28eb1', opacity=0.5))
    fig.update_layout(title="Hong Kong Population Pyramid (2026 vs 2046)", barmode='overlay', width=800, height=600)
    fig.write_image(os.path.join(PNG_DIR, "population_pyramid.png"), width=800, height=600, scale=2)
    print("✅ population_pyramid.png")


def create_trends_png():
    years = list(range(2026, 2046))
    ai_related = [5, 8, 12, 18, 25, 32, 40, 48, 55, 62, 68, 72, 75, 78, 80, 82, 84, 85, 86, 87]
    traditional = [85, 82, 78, 72, 65, 58, 50, 42, 35, 28, 22, 18, 15, 12, 10, 8, 7, 6, 5, 4]
    cross_domain = [10, 15, 22, 30, 40, 50, 60, 68, 75, 80, 85, 88, 90, 92, 93, 94, 95, 95, 96, 96]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=ai_related, mode='lines+markers', name='AI Jobs', line=dict(color='#ff6b6b', width=3)))
    fig.add_trace(go.Scatter(x=years, y=traditional, mode='lines+markers', name='Traditional', line=dict(color='#4e79a7', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cross_domain, mode='lines+markers', name='Cross-domain', line=dict(color='#51cf66', width=3)))
    fig.update_layout(title="HK Youth Employment Trends (2026-2046)", xaxis_title="Year", yaxis_title="Demand (%)", width=800, height=600)
    fig.write_image(os.path.join(PNG_DIR, "youth_employment_trends.png"), width=800, height=600, scale=2)
    print("✅ youth_employment_trends.png")


def create_energy_png():
    directions = ['AI Collab', 'Digital Ethics', 'Cross-domain', 'Mental Health', 'Employment']
    importance = [95, 85, 98, 80, 92]
    growth = [90, 75, 88, 70, 85]
    demand = [92, 82, 95, 78, 90]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=importance, theta=directions, fill='toself', name='Importance', line_color='#ff6b6b'))
    fig.add_trace(go.Scatterpolar(r=growth, theta=directions, fill='toself', name='Growth', line_color='#4e79a7'))
    fig.add_trace(go.Scatterpolar(r=demand, theta=directions, fill='toself', name='Demand', line_color='#51cf66'))
    fig.update_layout(title="5 Major Directions Energy Analysis", width=600, height=600)
    fig.write_image(os.path.join(PNG_DIR, "direction_energy.png"), width=600, height=600, scale=2)
    print("✅ direction_energy.png")


if __name__ == "__main__":
    print("🦀 Generating PNG images...")
    print("=" * 50)
    create_population_pyramid_png()
    create_trends_png()
    create_energy_png()
    print("=" * 50)
    print(f"✅ All images saved to: {PNG_DIR}")
