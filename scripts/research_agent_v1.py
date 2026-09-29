#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - CrewAI Hello World Demo
文獻搜索 Agent (最簡單版本)

功能：用戶輸入研究主題 → Agent 搜索並返回摘要
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 載入環境變量
load_dotenv()

# 初始化 LLM (Silra Platform - DeepSeek V3.2)
llm = ChatOpenAI(
    base_url="https://api.silra.cn/v1",
    api_key="sk-2YmYfA9Rlar5aIzcjpf56T101fKaSFUkLaceH2zPW7TPCSB7",
    model="deepseek-v3.2",
    temperature=0.3,
    max_tokens=2000
)

# 定義搜索 Agent
search_agent = Agent(
    role="學術研究助手",
    goal="幫用戶快速搵到相關嘅學術文獻並提供摘要",
    backstory="""你係一個專業嘅學術研究助手，擅長快速搜索同理解學術文獻。
你會用簡潔嘅廣東話同用戶溝通，提供準確嘅信息。""",
    verbose=True,
    allow_delegation=False,
    llm=llm  # 啟用 LLM
)

# 定義搜索任務
search_task = Task(
    description="""
    用戶研究主題：{topic}
    
    請執行以下步驟：
    1. 理解用戶嘅研究主題
    2. 提供 3-5 個相關嘅研究方向建議
    3. 對於每個方向，簡要說明：
       - 核心概念
       - 關鍵學者/論文
       - 最新發展趨勢
    
    請用廣東話回覆，保持簡潔清晰。
    """,
    expected_output="包含 3-5 個研究方向建議嘅結構化報告",
    agent=search_agent,
)

# 創建 Crew
crew = Crew(
    agents=[search_agent],
    tasks=[search_task],
    verbose=True,
)

# 執行
if __name__ == "__main__":
    print("🦀 Openhing - CrewAI Hello World Demo")
    print("=" * 50)
    
    # 用戶輸入
    topic = input("\n請輸入研究主題：")
    
    print(f"\n🔍 正在搜索 '{topic}' 相關文獻...\n")
    
    # 執行任務
    result = crew.kickoff(inputs={"topic": topic})
    
    print("\n" + "=" * 50)
    print("✅ 搜索完成！")
    print("\n" + result)
