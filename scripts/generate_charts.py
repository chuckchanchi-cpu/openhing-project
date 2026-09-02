"""
Openhing 圖表生成器 — 為研究報告生成專業圖表
用法: python3 scripts/generate_charts.py
輸出: charts/ 資料夾內的 PNG 圖表
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# === 設定中文顯示 ===
os.makedirs('charts', exist_ok=True)

# 尋找可用中文字型
zh_fonts = []
for f in fm.findSystemFonts():
    if any(k in f.lower() for k in ['noto', 'cjk', 'wqy', 'droid', 'source han', 'simhei', 'pingfang', 'heiti']):
        zh_fonts.append(f)

# 加入常用中文字型路徑
extra_paths = [
    os.path.expanduser('~/.fonts/NotoSansCJKsc-Regular.otf'),
    os.path.expanduser('~/.fonts/NotoSansCJKsc-Bold.otf'),
]
for p in extra_paths:
    if os.path.exists(p) and p not in zh_fonts:
        zh_fonts.append(p)

zh = None
for f in zh_fonts:
    try:
        fm.fontManager.addfont(f)
        zh = fm.FontProperties(fname=f)
        break
    except:
        continue

if zh is None:
    # 備用：用 sans-serif
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    print("⚠️ 未找到中文字型，圖表可能顯示為方塊")
else:
    plt.rcParams['font.sans-serif'] = [zh.get_name()]
    plt.rcParams['font.family'] = 'sans-serif'
    print(f"✅ 使用中文字型: {zh.get_name()}")

plt.rcParams['axes.unicode_minus'] = False

# 色彩方案
C1, C2, C3, C4, C5 = '#2563EB', '#7C3AED', '#059669', '#DC2626', '#D97706'

# ============================================================
# 圖表 1: AI Agent 市場規模成長預測（柱狀圖）
# ============================================================
years = [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2033]
values = [5.1, 18.6, 109, 156, 224, 321, 460, 1829]
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(len(years)), values, color=[C1]*5 + [C2, C2, C4], width=0.6)
ax.set_xticks(range(len(years)))
ax.set_xticklabels([str(y) for y in years])
ax.set_ylabel('市場規模（億美元）', fontsize=12)
ax.set_title('全球 AI Agent 市場規模成長預測（2024-2033）', fontsize=15, fontweight='bold', pad=15)
ax.set_yscale('log')  # log scale 因為成長太快
for i, v in enumerate(values):
    ax.text(i, v*1.15, f'${v}B', ha='center', fontsize=9, fontweight='bold')
ax.annotate('爆發期 2026\n(109億美元)', xy=(2, 109), xytext=(4.2, 300),
            fontsize=11, color=C4, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=C4, lw=2))
ax.grid(axis='y', alpha=0.3)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/market_growth.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ 圖表 1: 市場規模成長 (market_growth.png)")

# ============================================================
# 圖表 2: 活躍 Agent 數量爆炸式成長
# ============================================================
y2 = [2025, 2026, 2027, 2028, 2029, 2030]
agents = [0.286, 0.8, 2.1, 5.4, 12.8, 22.16]
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y2, agents, marker='o', markersize=8, linewidth=3, color=C2)
ax.fill_between(y2, agents, alpha=0.15, color=C2)
for i, v in enumerate(agents):
    ax.annotate(f'{v}億', (y2[i], v), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='bold', fontsize=11)
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('活躍 AI Agent 數量（億）', fontsize=12)
ax.set_title('數位勞動力爆炸式成長：活躍 Agent 數量（2025-2030）', fontsize=15, fontweight='bold', pad=15)
ax.annotate('80倍成長\n(CAGR 139%)', xy=(2029, 12.8), xytext=(2025.3, 15),
            fontsize=12, color=C4, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=C4, lw=2))
ax.grid(alpha=0.3)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/agent_growth.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ 圖表 2: Agent 數量成長 (agent_growth.png)")

# ============================================================
# 圖表 3: 企業採用率 vs 成熟度（水平條形圖）
# ============================================================
metrics = ['已在生產環境運行\nAI Agent (Google)', '已正式部署\n(Google)', '大型企業規模化\n部署 (McKinsey)', '視AI為競爭優勢\n(Deloitte)', '達到「成熟」等級\n(Deloitte)', '真正「Agent-First」\n(BCG)']
rates = [70, 52, 40, 88, 1, 5]
colors = [C1, C1, C1, C3, C4, C4]
fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(range(len(metrics)), rates, color=colors, height=0.6)
ax.set_yticks(range(len(metrics)))
ax.set_yticklabels(metrics, fontsize=10)
ax.set_xlabel('百分比 (%)', fontsize=12)
ax.set_title('企業 AI Agent 採用率 vs 成熟度：巨大的鴻溝', fontsize=15, fontweight='bold', pad=15)
for i, (v, c) in enumerate(zip(rates, colors)):
    ax.text(v + 1, i, f'{v}%', va='center', fontweight='bold', fontsize=11, color=c)
ax.set_xlim(0, 105)
ax.grid(axis='x', alpha=0.3)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/adoption_vs_maturity.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ 圖表 3: 採用率 vs 成熟度 (adoption_vs_maturity.png)")

# ============================================================
# 圖表 4: 治理挑戰數據（甜甜圈圖）
# ============================================================
labels = ['未通過完整資安審查', '通過資安審查']
sizes = [85.6, 14.4]
colors4 = [C4, C1]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
# 左：資安審查
wedges1, _ = ax1.pie(sizes, colors=colors4, startangle=90, wedgeprops=dict(width=0.35, edgecolor='w'))
ax1.text(0, 0, '14.4%\n通過\n審查', ha='center', va='center', fontsize=13, fontweight='bold')
ax1.set_title('僅 14.4% Agent\n上線前通過資安審查', fontsize=13, fontweight='bold')
# 右：監控覆蓋率
labels2 = ['已監控 52%', '未監控 48%']
sizes2 = [52, 48]
wedges2, _ = ax2.pie(sizes2, colors=[C3, '#9CA3AF'], startangle=90, wedgeprops=dict(width=0.35, edgecolor='w'))
ax2.text(0, 0, '48%\n未受\n監控', ha='center', va='center', fontsize=13, fontweight='bold', color=C4)
ax2.set_title('平均監控覆蓋率僅 52%', fontsize=13, fontweight='bold')
plt.suptitle('AI Agent 治理危機：安全審查與監控缺口（Gravitee 2026）', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('charts/governance_gap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ 圖表 4: 治理缺口 (governance_gap.png)")

print("\n🎉 全部圖表生成完成！存放於 charts/ 資料夾")
