# 🦀 CrewAI Demo 快速啟動指南

**日期**: 2026-09-02  
**作者**: @fring1118 (Claw)

---

## 📦 **步驟 1：安裝依賴**

```bash
cd ~/Desktop/openhing
pip install -r requirements.txt
```

**如果遇到問題**：
```bash
# 升級 pip
pip install --upgrade pip

# 如果 CrewAI 安裝失敗
pip install crewai --no-cache-dir
```

---

## 🔑 **步驟 2：配置 API Key**

```bash
# 複製示例文件
cp .env.example .env

# 編輯 .env 文件
nano .env
```

**填入你嘅 API Key**：

```env
# OpenAI API (如果用 GPT-4)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# 或者用 Qwen (如果係阿里云)
# OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# Serper API (搜索功能)
SERPER_API_KEY=xxxxxxxxxxxxxxxx
```

**獲取 API Key**：
- OpenAI: https://platform.openai.com/api-keys
- Qwen (阿里云): https://dashscope.console.aliyun.com/
- Serper: https://serper.dev/

---

## 🚀 **步驟 3：運行 Hello World Demo**

```bash
cd ~/Desktop/openhing
python3 scripts/research_agent_v1.py
```

**示例對話**：

```
🦀 Openhing - CrewAI Hello World Demo
==================================================

請輸入研究主題：AI Agent 在學術研究的應用

🔍 正在搜索 'AI Agent 在學術研究的應用' 相關文獻...

[Agent 開始思考...]
[Agent 執行任務...]
[Agent 生成報告...]

==================================================
✅ 搜索完成！

【AI Agent 在學術研究的應用 - 研究方向建議】

1. 文獻搜索與篩選
   - 核心概念：用 AI 自動搜索同篩選相關論文
   - 關鍵學者：...
   - 最新趨勢：...

2. 論文摘要生成
   - 核心概念：...
   ...
```

---

## ⚠️ **常見問題**

### **問題 1**: `ModuleNotFoundError: No module named 'crewai'`
**解決**：
```bash
pip install crewai
```

### **問題 2**: `Error: OPENAI_API_KEY not set`
**解決**：
```bash
# 確保 .env 文件存在且正確配置
cat .env
```

### **問題 3**: `Error: Invalid API key`
**解決**：
- 檢查 `.env` 文件嘅 API Key 是否正確
- 確保無多餘空格

### **問題 4**: 運行太慢
**解決**：
- 檢查網絡連接
- 如果用 OpenAI，可能係 API 限流
- 可以轉用本地模型 (Ollama)

---

## 🎯 **下一步擴展**

### **版本 2**: 加入真實搜索功能
```python
# 使用 Serper API 進行真實搜索
from langchain_community.tools import SerperSearchTool

search_tool = SerperSearchTool()
```

### **版本 3**: 多 Agent 協作
```python
# 搜索 Agent + 分析 Agent + 寫作 Agent
crew = Crew(
    agents=[search_agent, analysis_agent, writing_agent],
    tasks=[search_task, analysis_task, writing_task],
)
```

---

## 📞 **需要幫助？**

有問題隨時喺 Discord 搵 @fring1118 (Claw)！

---

*最後更新：2026-09-02 09:45*
