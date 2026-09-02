#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - 簡化版研究助手 (唔使 CrewAI)
直接調用 Silra API (DeepSeek V3.2)

功能：用戶輸入研究主題 → 返回研究建議
"""

import requests
import json
from datetime import datetime

# API 配置
API_BASE = "https://api.silra.cn/v1"
API_KEY = "sk-2YmYfA9Rlar5aIzcjpf56T101fKaSFUkLaceH2zPW7TPCSB7"
MODEL = "deepseek-v3.2"

def call_llm(prompt):
    """調用 LLM API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你係一個專業嘅學術研究助手，擅長用廣東話幫用戶分析研究主題並提供建議。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ API 調用失敗：{e}"

def main():
    print("=" * 60)
    print("🦀 Openhing - 研究助手 Demo (簡化版)")
    print("=" * 60)
    print(f"📅 時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 模型：{MODEL}")
    print("=" * 60)
    
    # 用戶輸入 (測試項目)
    topic = "年青人在 AI 時代未來 20 年努力的方向"
    print(f"\n📚 研究主題：{topic}")
    
    print(f"\n🔍 正在分析 '{topic}'...\n")
    
    # 構建提示詞
    prompt = f"""
請幫我分析以下研究主題，並提供：

1. **3-5 個相關研究方向**
   - 每個方向簡要說明核心概念
   
2. **關鍵學者/論文** (如果知道)

3. **最新發展趨勢**

4. **建議下一步行動**

研究主題：{topic}

請用廣東話回覆，保持簡潔清晰。
"""
    
    # 調用 API
    result = call_llm(prompt)
    
    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)
    print(f"\n{result}\n")

if __name__ == "__main__":
    main()
