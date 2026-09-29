#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - CrewAI 完整版本 Demo (v2)
未來20年年青人努力方向 - 完整分析報告

功能：用戶輸入研究主題 → Agent 生成完整結構化報告
"""

from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv

# 載入環境變量
load_dotenv()

# 初始化 LLM (Silra Platform - DeepSeek V3.2)
LLM_CONFIG = {
    "model": "deepseek-v3.2",
    "openai_api_key": "sk-2YmYfA9Rlar5aIzcjpf56T101fKaSFUkLaceH2zPW7TPCSB7",
    "openai_api_base": "https://api.silra.cn/v1",
}

# 定義搜索 Agent
search_agent = Agent(
    role="學術研究助手",
    goal="幫用戶生成完整深入嘅分析報告",
    backstory="""你係一個專業嘅學術研究助手，擅長全面分析同提供結構化報告。
你會用廣東話回覆，內容深入有條理。""",
    verbose=True,
    allow_delegation=False,
    llm=LLM_CONFIG["model"],
    max_iter=10,
)

# 定義搜索任務
prompt_text = (
    "用戶研究主題：{topic}\n\n"
    "請提供一份**完整深入嘅分析報告**，包括以下所有部分：\n\n"
    "## 第一部分：5 大關鍵方向\n"
    "列出 5 個最適合年青人投入嘅努力方向，每個方向包括：\n"
    "- 方向名稱\n"
    "- 核心概念 (1-2 句解釋)\n"
    "- 為什麼重要 (3 個理由)\n"
    "- 需要什麼技能\n"
    "- 預期就業前景\n\n"
    "## 第二部分：時間軸規劃\n"
    "- 短期 (1-5年)：應該做什麼準備\n"
    "- 中期 (5-10年)：應該專注發展什麼能力\n"
    "- 長期 (10-20年)：應該追求什麼目標\n\n"
    "## 第三部分：關鍵資源與工具\n"
    "- 推薦學習平台 (免費 + 付費)\n"
    "- 必讀書籍/文章\n"
    "- 實用工具/App\n"
    "- 相關社區/組織\n\n"
    "## 第四部分：風險與挑戰\n"
    "- AI 時代最大嘅職業威脅\n"
    "- 如何應對自動化取代\n"
    "- 心理適應建議\n\n"
    "## 第五部分：行動清單\n"
    "- 今個月可以開始做嘅 5 件事\n"
    "- 今年內要完成嘅 3 個里程碑\n"
    "- 未來 5 年嘅成功指標\n\n"
    "請用廣東話回覆，保持深入同有條理。"
)

search_task = Task(
    description=prompt_text,
    expected_output="包含 5 大部分嘅完整結構化報告",
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
    print("🦀 Openhing - CrewAI 完整版本 Demo")
    print("=" * 60)
    print(f"🤖 Model: {LLM_CONFIG['model']}")
    print(f"🔗 API: {LLM_CONFIG['openai_api_base']}")
    print("=" * 60)

    # 用戶輸入 (測試模式)
    topic = "未來20年年青人努力方向"
    print(f"\n📚 研究主題：{topic}\n")

    print(f"🔍 正在分析 '{topic}'...\n")

    # 執行任務
    result = crew.kickoff(inputs={"topic": topic})

    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)
    print(str(result))
