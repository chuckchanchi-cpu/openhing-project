#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - Multi-Agent System with Serper API
多智能體系統：搜索 + 分析 + 寫作

功能：
1. Search Agent: 用 Serper API 搜索網絡
2. Analysis Agent: 分析搜索结果
3. Writing Agent: 生成完整報告
"""

from crewai import Agent, Task, Crew
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = "996eb60ceca9384e16331134d56ba3e4acb4c1d9"
SERPER_URL = "https://google.serper.dev/search"

LLM_CONFIG = {
    "model": "deepseek-v3.2",
    "openai_api_key": "sk-2YmYfA9Rlar5aIzcjpf56T101fKaSFUkLaceH2zPW7TPCSB7",
    "openai_api_base": "https://api.silra.cn/v1",
}


def search_topic(topic):
    """使用 Serper API 搜索主題"""
    url = SERPER_URL
    payload = json.dumps({"q": topic, "gl": "hk", "hl": "zh-HK", "num": 10})
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        results = response.json().get("organic", [])
        return results
    except Exception as e:
        return [f"搜索錯誤: {str(e)}"]


def format_search_results(results):
    """格式化搜索結果"""
    formatted = []
    for result in results:
        formatted.append(f"- **{result.get('title')}**\n  URL: {result.get('link')}\n  摘要: {result.get('snippet', '')}\n")
    return "\n".join(formatted)


# 定義 Search Agent (使用外部搜索工具)
search_agent = Agent(
    role="網絡搜索專家",
    goal="使用 Serper API 搜索相關資訊並返回結構化結果",
    backstory="你擅長使用 Serper API 進行高效搜索，能夠快速找到最相關的資訊。",
    verbose=True,
    llm=LLM_CONFIG["model"],
)

# 定義 Analysis Agent
analysis_agent = Agent(
    role="資訊分析專家",
    goal="分析搜索結果並提取關鍵資訊",
    backstory="你擅長從大量資訊中提取重點，組織成有條理的結構。",
    verbose=True,
    llm=LLM_CONFIG["model"],
)

# 定義 Writing Agent
writing_agent = Agent(
    role="研究報告撰寫者",
    goal="根據分析結果生成完整研究報告",
    backstory="你擅長將複雜資訊轉化為清晰、易讀的報告。",
    verbose=True,
    llm=LLM_CONFIG["model"],
)

# 創建任務
topic = "AI Agent 在學術研究的應用"

print(f"🔍 正在搜索: {topic}")
search_results = search_topic(topic)
formatted = format_search_results(search_results)
print(f"📊 找到 {len(search_results)} 個結果\n")

# 先運行 Search Agent
search_task = Task(
    description=f"使用以下搜索結果生成分析報告：\n\n{formatted}",
    expected_output="包含主要發現和趨勢的結構化分析",
    agent=search_agent,
)

# 運行 Crew
crew = Crew(
    agents=[search_agent],
    tasks=[search_task],
    verbose=True,
)

print("\n🚀 開始執行...")
result = crew.kickoff(inputs={})

print("\n✅ 完成！")
print(result)
