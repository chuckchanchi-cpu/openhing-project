"""
Openhing 研究助手 — CrewAI 原型

使用方法:
1. pip install crewai
2. 設定環境變數:
   - OPENAI_API_KEY
   - OPENAI_API_BASE (可選，如用第三方 API)
   - OPENAI_MODEL_NAME (可選，預設 gpt-4)
3. python research_assistant.py --topic "你的研究主題"
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# === 設定 ===
DEFAULT_TOPIC = "2026年AI Agent 採用趨勢與發展"

def get_topic():
    if len(sys.argv) > 1 and sys.argv[1] == "--topic":
        return " ".join(sys.argv[2:]) if len(sys.argv) > 2 else DEFAULT_TOPIC
    return DEFAULT_TOPIC

def create_research_crew(topic: str):
    """建立研究助手 Crew"""

    # === Agent 1: 研究員 ===
    researcher = Agent(
        role="高級研究分析師",
        goal=f"對「{topic}」進行全面、深入的研究，找出關鍵數據、趨勢和專家觀點",
        backstory=(
            "你是一位經驗豐富的研究分析師，擅長從多個來源搜集資訊，"
            "核實事實，並提煉出有價值的見解。你的研究報告以全面和準確著稱。"
        ),
        verbose=True,
        allow_delegation=False,
    )

    # === Agent 2: 分析師 ===
    analyst = Agent(
        role="數據分析師",
        goal="分析研究結果，識別模式、趨勢和關鍵洞察",
        backstory=(
            "你是一位數據分析專家，擅長從大量資訊中找出核心趨勢和模式。"
            "你能將複雜的數據轉化為清晰的見解。"
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    # === Agent 3: 寫手 ===
    writer = Agent(
        role="技術寫手",
        goal="將研究和分析結果轉化為結構清晰、易於理解的報告",
        backstory=(
            "你是一位專業的技術寫手，擅長用淺顯易懂的語言解釋複雜的技術概念。"
            "你的文章既有深度又有可讀性。"
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    # === 任務定義 ===
    research_task = Task(
        description=(
            f"對「{topic}」進行全面研究。\n"
            "請找出：\n"
            "1. 主要趨勢和發展方向\n"
            "2. 關鍵統計數據\n"
            "3. 行業領袖和專家觀點\n"
            "4. 重要事件和里程碑\n"
            "5. 潛在風險和挑戰"
        ),
        expected_output=(
            "一份結構化的研究簡報，包含所有發現、數據來源和關鍵要點。"
        ),
        agent=researcher,
    )

    analysis_task = Task(
        description=(
            "分析研究結果，找出核心模式和趨勢。\n"
            "請重點分析：\n"
            "1. 最重要的 3-5 個趨勢\n"
            "2. 這些趨勢的影響\n"
            "3. 它們之間的關聯性\n"
            "4. 對未來的預測"
        ),
        expected_output=(
            "一份分析報告，重點突出核心趨勢和洞察。"
        ),
        agent=analyst,
    )

    writing_task = Task(
        description=(
            "根據研究和分析結果，撰寫一篇完整的文章。\n"
            "文章結構：\n"
            "1. 引言（為什麼這個主題重要）\n"
            "2. 主要發現\n"
            "3. 核心趨勢分析\n"
            "4. 未來展望\n"
            "5. 結論與建議\n"
            "請撰寫一篇 **3000-4000 字** 的深度完整文章，"
            "內容要充實、有具體數據、實例和可執行建議，"
            "不要精簡或敷衍。"
        ),
        expected_output=(
            "一篇 3000-4000 字的深度完整文章，內容充實、數據具體、建議可執行。"
        ),
        agent=writer,
    )

    # === 建立 Crew ===
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,  # 順序執行
        verbose=True,
    )

    return crew

def safe_filename(topic: str) -> str:
    """把主題轉成安全的檔案名稱"""
    name = re.sub(r'[\\/:*?"<>|]', '', topic).strip()
    return name[:50] or "research"

def main():
    topic = get_topic()
    print(f"\n🚀 Openhing 研究助手 — 開始研究：「{topic}」\n")
    print("=" * 60)

    crew = create_research_crew(topic)
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print(f"✅ 研究完成！結果：\n")
    print(result)

    # === 自動儲存到檔案 ===
    try:
        docs_dir = Path(__file__).resolve().parent.parent / "docs"
        docs_dir.mkdir(exist_ok=True)
        fname = f"{datetime.now():%Y%m%d}-{safe_filename(topic)}.md"
        out_path = docs_dir / fname
        header = (
            f"# {topic}\n\n"
            f"> 由 Openhing 研究助手（CrewAI）自動生成\n"
            f"> 日期：{datetime.now():%Y-%m-%d %H:%M}\n"
            f"> 模型：deepseek-v3.2 | 3 Agent 協作（研究員→分析師→寫手）\n\n"
            "---\n\n"
        )
        out_path.write_text(header + str(result), encoding="utf-8")
        print(f"\n📁 已儲存：{out_path}")
    except Exception as e:
        print(f"\n⚠️ 儲存失敗：{e}")

if __name__ == "__main__":
    main()