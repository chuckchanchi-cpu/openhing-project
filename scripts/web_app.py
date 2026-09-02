"""
Openhing 研究助手 — Web UI
用法: python3 scripts/web_app.py
然後開瀏覽器: http://localhost:5000
"""
import os
import sys
import json
import threading
import queue
import time
from pathlib import Path

# 確保可以 import research_assistant
sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_assistant import create_research_crew, safe_filename

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 任務狀態管理
tasks = {}  # task_id -> {status, topic, progress, output, error, created_at}

# === HTML 模板（單一檔案，無需額外檔案） ===
PAGE = r"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦞 Openhing 研究助手</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', 'PingFang TC', 'Microsoft JhengHei', sans-serif;
       background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
       color: #e2e8f0; min-height: 100vh; }
.container { max-width: 860px; margin: 0 auto; padding: 40px 20px; }
h1 { font-size: 2.2rem; text-align: center; margin-bottom: 8px;
     background: linear-gradient(90deg, #60a5fa, #a78bfa, #34d399);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { text-align: center; color: #94a3b8; margin-bottom: 32px; font-size: 0.95rem; }
.card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 24px; margin-bottom: 20px;
        backdrop-filter: blur(10px); }
label { display: block; font-weight: 600; margin-bottom: 8px; color: #cbd5e1; }
input[type=text] { width: 100%; padding: 14px 16px; border-radius: 10px;
       border: 1px solid #334155; background: #1e293b; color: #e2e8f0;
       font-size: 1rem; margin-bottom: 16px; }
input[type=text]:focus { outline: none; border-color: #60a5fa; }
button { width: 100%; padding: 14px; border: none; border-radius: 10px;
       background: linear-gradient(90deg, #2563eb, #7c3aed); color: white;
       font-size: 1.1rem; font-weight: 700; cursor: pointer; transition: all 0.2s; }
button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(99,102,241,0.4); }
button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
#progress { display: none; }
.agent-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px;
       border-radius: 8px; margin: 6px 0; background: rgba(255,255,255,0.03); }
.agent-item .status { margin-left: auto; font-size: 1.2rem; }
.agent-item.done { border-left: 3px solid #34d399; }
.agent-item.running { border-left: 3px solid #f59e0b; }
.agent-item.pending { border-left: 3px solid #64748b; opacity: 0.6; }
.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid #f59e0b;
       border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
#output { display: none; }
#article { white-space: pre-wrap; line-height: 1.8; font-size: 0.95rem;
       background: #0f172a; padding: 20px; border-radius: 12px;
       max-height: 600px; overflow-y: auto; }
#status-text { text-align: center; color: #94a3b8; margin-top: 16px; }
.pulse { animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
a { color: #60a5fa; }
.footer { text-align: center; color: #475569; font-size: 0.8rem; margin-top: 40px; }
</style>
</head>
<body>
<div class="container">
  <h1>🦞 Openhing 研究助手</h1>
  <p class="subtitle">CrewAI 多智能體協作 · 研究員 → 分析師 → 寫手</p>

  <div class="card">
    <label for="topic">研究主題</label>
    <input type="text" id="topic" placeholder="例如：2026年 AI Agent 最新趨勢與企業應用">
    <button id="start-btn" onclick="startResearch()">🚀 開始研究</button>
  </div>

  <div class="card" id="progress">
    <h3 style="margin-bottom:12px;color:#cbd5e1;">🔬 研究進行中...</h3>
    <div id="agent-list"></div>
    <div id="status-text" class="pulse">Agent 協作中，請稍候（約 3-5 分鐘）...</div>
  </div>

  <div class="card" id="output">
    <h3 style="margin-bottom:12px;color:#cbd5e1;">📄 研究結果</h3>
    <div id="article"></div>
    <p style="margin-top:12px;font-size:0.85rem;color:#94a3b8;">
      文章已自動儲存至 <code>docs/</code> 資料夾 📁</p>
  </div>

  <div class="footer">Openhing 項目 · CrewAI + DeepSeek · MVP 2.0</div>
</div>

<script>
let pollTimer = null;

function startResearch() {
  const topic = document.getElementById('topic').value.trim();
  if (!topic) { alert('請輸入研究主題！'); return; }

  document.getElementById('start-btn').disabled = true;
  document.getElementById('progress').style.display = 'block';
  document.getElementById('output').style.display = 'none';
  document.getElementById('agent-list').innerHTML = '';

  fetch('/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic: topic })
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) { alert('錯誤：' + data.error); return; }
    pollTimer = setInterval(() => pollStatus(data.task_id), 2000);
  });
}

function pollStatus(taskId) {
  fetch('/status/' + taskId)
  .then(r => r.json())
  .then(data => {
    renderAgents(data.agents);
    document.getElementById('status-text').textContent = data.status_text;

    if (data.status === 'done') {
      clearInterval(pollTimer);
      document.getElementById('article').textContent = data.output;
      document.getElementById('output').style.display = 'block';
      document.getElementById('status-text').textContent = '✅ 研究完成！';
      document.getElementById('start-btn').disabled = false;
      document.getElementById('start-btn').textContent = '🔄 再研究一次';
    } else if (data.status === 'error') {
      clearInterval(pollTimer);
      alert('發生錯誤：' + data.error);
      document.getElementById('start-btn').disabled = false;
      document.getElementById('start-btn').textContent = '🚀 開始研究';
    }
  });
}

function renderAgents(agents) {
  const list = document.getElementById('agent-list');
  list.innerHTML = '';
  for (const a of agents) {
    const div = document.createElement('div');
    div.className = 'agent-item ' + a.status;
    let statusIcon = '';
    if (a.status === 'done') statusIcon = '✅';
    else if (a.status === 'running') statusIcon = '<span class="spinner"></span>';
    else statusIcon = '⏳';
    div.innerHTML = `<strong>${a.icon}</strong> <span>${a.name}</span>
      <span class="status">${statusIcon}</span>`;
    list.appendChild(div);
  }
}
</script>
</body>
</html>
"""

# === 任務執行（背景線程） ===
AGENT_DEFS = [
    {"icon": "🔍", "name": "研究員（搜集資料）", "key": "researcher"},
    {"icon": "📊", "name": "分析師（分析趨勢）", "key": "analyst"},
    {"icon": "✍️", "name": "寫手（撰寫文章）", "key": "writer"},
]

def run_task(task_id: str, topic: str):
    """在背景執行完整研究流程"""
    task = tasks[task_id]
    task["status"] = "running"
    task["agents"] = [
        {"icon": a["icon"], "name": a["name"], "status": "pending"} for a in AGENT_DEFS
    ]

    try:
        crew = create_research_crew(topic)

        # 模擬逐步執行（CrewAI kickoff 一次過跑，我哋用時間估算更新狀態）
        # 實際執行：先標記研究員 running
        task["agents"][0]["status"] = "running"
        task["status_text"] = "研究員正在搜集資料..."

        # 啟動真正執行
        result = crew.kickoff()
        result_str = str(result)

        # 全部完成
        for a in task["agents"]:
            a["status"] = "done"
        task["status"] = "done"
        task["output"] = result_str
        task["status_text"] = "✅ 研究完成！"

        # 儲存文章
        try:
            docs_dir = Path(__file__).resolve().parent.parent / "docs"
            docs_dir.mkdir(exist_ok=True)
            from datetime import datetime
            fname = f"{datetime.now():%Y%m%d}-{safe_filename(topic)}.md"
            out_path = docs_dir / fname
            header = (
                f"# {topic}\n\n"
                f"> 由 Openhing 研究助手（CrewAI）自動生成\n"
                f"> 日期：{datetime.now():%Y-%m-%d %H:%M}\n"
                f"> 3 Agent 協作（研究員→分析師→寫手）\n\n---\n\n"
            )
            out_path.write_text(header + result_str, encoding="utf-8")
            task["file"] = str(out_path)
        except Exception as e:
            task["file_error"] = str(e)

    except Exception as e:
        task["status"] = "error"
        task["error"] = str(e)
        task["status_text"] = "❌ 發生錯誤"


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    topic = (data or {}).get("topic", "").strip()
    if not topic:
        return jsonify({"error": "請輸入主題"}), 400

    task_id = str(int(time.time() * 1000))
    tasks[task_id] = {
        "status": "queued",
        "topic": topic,
        "agents": [],
        "output": "",
        "error": "",
        "status_text": "排隊中...",
        "created_at": time.time(),
    }

    t = threading.Thread(target=run_task, args=(task_id, topic), daemon=True)
    t.start()
    return jsonify({"task_id": task_id, "ok": True})


@app.route("/status/<task_id>")
def status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"status": "error", "error": "任務不存在"})
    return jsonify({
        "status": task["status"],
        "status_text": task["status_text"],
        "agents": task["agents"],
        "output": task["output"],
        "error": task["error"],
        "file": task.get("file", ""),
    })


if __name__ == "__main__":
    print("\n🦞 Openhing 研究助手 Web UI")
    print("=" * 40)
    print("🌐 開啟瀏覽器: http://localhost:5000")
    print("（Ctrl+C 停止）\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
