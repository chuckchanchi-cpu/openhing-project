#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Agent 情報搜索
快速搜索 CrewAI vs AutoGen vs LangChain 比較
"""

import requests
import json
from datetime import datetime

# Serper API 配置
SERPER_API_KEY = "996eb60ceca9384e16331134d56ba3e4acb4c1d9"
SEARCH_URL = "https://google.serper.dev/search"

# 搜索查詢列表
QUERIES = [
    "CrewAI vs AutoGen vs LangChain 2026 comparison",
    "best multi-agent framework 2026",
    "CrewAI review 2026",
    "AutoGen Microsoft framework review",
    "LangChain LangGraph multi-agent",
    "AI research assistant tools 2026",
    "academic AI agent frameworks comparison",
]

def search_serper(query, api_key):
    """執行 Serper 搜索"""
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": 5,
        "gl": "us",
        "hl": "en"
    }
    
    try:
        response = requests.post(SEARCH_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 搜索失敗：{e}")
        return None

def main():
    print("=" * 60)
    print("🦀 Openhing - AI Agent 情報搜索")
    print("=" * 60)
    print(f"📅 時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 搜索查詢：{len(QUERIES)} 個")
    print("=" * 60)
    
    results = []
    
    for i, query in enumerate(QUERIES, 1):
        print(f"\n[{i}/{len(QUERIES)}] 🔍 Searching: {query}")
        
        search_result = search_serper(query, SERPER_API_KEY)
        
        if search_result and "organic" in search_result:
            print(f"   ✅ 找到 {len(search_result['organic'])} 個結果")
            results.append({
                "query": query,
                "results": search_result["organic"][:3]  # 只保留頭 3 個
            })
            
            # 顯示頭 2 個結果
            for j, item in enumerate(search_result["organic"][:2], 1):
                print(f"   {j}. {item.get('title', 'N/A')}")
                print(f"      📅 {item.get('date', 'N/A')}")
                print(f"      🔗 {item.get('link', 'N/A')}")
        else:
            print("   ❌ 無結果")
    
    # 保存結果
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_file = f"/Users/fring1117/Desktop/openhing/resources/ai-agent-intel-{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ 搜索完成！")
    print(f"📄 報告保存去：{output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
