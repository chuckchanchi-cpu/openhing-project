#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 OpenEduJustan 互動練習平台（單一 App）
1. 揀科目 + 主題 → AI 生成 5 題
2. 學生喺同一頁作答
3. AI 即時批改 + 評分
"""

import streamlit as st
import os
import json
import glob
import requests
import pandas as pd
import io
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="🎓 OpenEduJustan", page_icon="🎓", layout="wide")

SILRA_API_URL = "https://api.silra.cn/v1/chat/completions"
SILRA_API_KEY = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
MODEL = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "deepseek-chat")

def get_api_base():
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    silra_url = os.environ.get("SILRA_API_URL", "")
    if silra_url:
        base = silra_url.replace("/chat/completions", "").rstrip("/")
    if not base:
        base = "https://api.deepseek.com"
    return base

api_base = get_api_base()

def load_local_questions():
    bank = {}
    edu_folder = Path.home() / "Desktop" / "openedujustan"
    if not edu_folder.exists():
        return bank
    subject_dirs = {"Chinese": "中文科", "General_Studies": "常識科", "English": "英文科", "Maths": "數學科"}
    for dir_name, display_name in subject_dirs.items():
        dir_path = edu_folder / dir_name
        if not dir_path.exists():
            continue
        practice_dir = dir_path / "practice"
        if not practice_dir.exists():
            practice_dir = dir_path
        for md_file in sorted(practice_dir.rglob("*.md")):
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()
                title = ""
                for line in content.split("\n"):
                    if line.startswith("# ") and not title:
                        title = line[2:].strip()
                        break
                if title:
                    preview = "\n".join(content.split("\n")[:15]).strip()
                    if display_name not in bank:
                        bank[display_name] = []
                    bank[display_name].append({"source_file": str(md_file), "title": title, "preview": preview[:300], "full_content": content})
            except Exception:
                pass
    return bank

local_bank = load_local_questions()

BUILTIN_QUESTIONS = {
    "中文科": [
        {"q": "請以「一次難忘的經歷」為題，寫一篇不少于400字的记叙文。", "hint": "選擇一件真正令你印象深刻的事，詳細描述當時的情景同感受。", "rubric": "- 內容完整性（40%）\n- 語法同拼寫（30%）\n- 表達清晰度（20%）\n- 創意同深度（10%）"},
        {"q": "現在很多學生家長認為學校作業太多，影響孩子休息同健康。你同意這個觀點嗎？請寫一篇議論文。", "hint": "先表明立場，然後列出至少2-3個理由。", "rubric": "- 論點清晰（40%）\n- 論據充分（30%）\n- 邏輯嚴密（20%）\n- 語言流暢（10%）"},
    ],
    "常識科": [
        {"q": "請詳細解釋水的循環過程。包括：蒸發、凝結、降水。", "hint": "使用「蒸發」、「凝結」、「降水」、「匯集」等科學術語。", "rubric": "- 內容準確性（40%）\n- 解釋清晰度（30%）\n- 關鍵詞運用（20%）\n- 完整性（10%）"},
        {"q": "植物生長需要哪些條件？請詳細說明每個條件的作用。", "hint": "考慮光、水、空氣、溫度、養分等因素。", "rubric": "- 內容準確性（40%）\n- 解釋清晰度（30%）\n- 關鍵詞運用（20%）\n- 完整性（10%）"},
    ],
    "英文科": [
        {"q": "Write about your best friend. Include: appearance, personality, why you like them, and one special memory. (80+ words)", "hint": "Use descriptive adjectives and specific examples.", "rubric": "- Content & Relevance (40%)\n- Grammar & Spelling (30%)\n- Clarity & Coherence (20%)\n- Vocabulary (10%)"},
    ],
    "數學科": [
        {"q": "小明去商店買文具。一支筆售價$15，一本筆記本售價$25。他買了3支筆和2本筆記本，付給店員$100。\n請問：(1)一共花了多少錢？(2)應該找給他多少錢？(3)餘額夠買$10的橡皮擦嗎？", "hint": "列出算式，逐步計算。", "rubric": "- 方法正確性（40%）\n- 計算準確性（30%）\n- 步驟完整性（20%）\n- 答案合理性（10%）"},
    ],
}

ALL_SUBJECTS = {}
for subj, qs in BUILTIN_QUESTIONS.items():
    ALL_SUBJECTS[subj] = [{"type": "builtin", **q} for q in qs]
for subj, items in local_bank.items():
    ALL_SUBJECTS.setdefault(subj, []).extend([{"type": "local", **item} for item in items])

def extract_json_from_text(text):
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        text = text[start:end+1]
    import re
    text = re.sub(r',\s*([\]\}])', r'\1', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

def generate_questions(subject, grade, topic, count=5):
    try:
        system_prompt = f"""你係一位經驗豐富嘅小學{subject}科老師，專門為{grade}學生設計練習題目。

請嚴格生成恰好 {count} 條練習題目。每條題目必須包含以下欄位：
- id: 數字 (由 1 開始連續)
- title: 題目標題 (簡短)
- question: 完整題目內容
- difficulty: "簡單" 或 "中等" 或 "挑戰"
- marks: 分數 (數字)
- reference_answer: 參考答案要点
- tip: 提示或解題技巧

輸出格式 (純 JSON Array，唔好有任何其他文字)：
[{{"id":1,"title":"標題","question":"題目內容","difficulty":"簡單","marks":10,"reference_answer":"答案","tip":"提示"}}]

注意：只返回 JSON Array，不要任何其他文字。"""
        user_message = f"科目: {subject}\n年級: {grade}\n主題: {topic if topic else '請根據課程標準自行選擇合適主題'}\n數量: 恰好 {count} 條"
        payload = {"model": MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}], "max_tokens": 4000, "temperature": 0.7}
        headers = {"Authorization": f"Bearer {SILRA_API_KEY}", "Content-Type": "application/json"}
        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=90)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            questions = extract_json_from_text(content)
            if questions and isinstance(questions, list) and len(questions) >= count:
                return questions[:count]
            elif questions and isinstance(questions, list):
                return questions
            else:
                return [{"id": 1, "title": f"{subject}練習 - {topic or '綜合'}", "question": content[:800] if content else "無內容", "difficulty": "中等", "marks": 10, "reference_answer": "參見 AI 生成內容", "tip": "💡 仔細閱讀題目，結合所學知識作答。"}]
        else:
            return []
    except Exception as e:
        st.error(f"❌ 生成出錯: {str(e)}")
        return []

def grade_answer(question, answer, rubric):
    if not SILRA_API_KEY:
        return None, "⚠️ 未設定 API Key — 請喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY"
    prompt = f"""你係一個專業同友善嘅老師。根據評分準則，批改學生嘅答案，用廣東話寫評語。

題目：
{question}

評分準則：
{rubric}

學生答案：
{answer}

請用以下 JSON 格式回覆（唔好加其他文字）：
{{"scores": {{"內容準確性": 8, "解釋清晰度": 7, "關鍵詞運用": 6, "完整性": 8}}, "total": 29, "comment": "整體評語（廣東話，2-3 句，鼓勵為主）", "strengths": ["優點1", "優點2"], "improvements": ["改善1", "改善2"]}}
"""
    try:
        r = requests.post(f"{api_base}/chat/completions", json={"model": MODEL, "messages": [{"role": "system", "content": "你係專業老師。直接輸出 JSON，唔好有任何其他文字。"}, {"role": "user", "content": prompt}], "max_tokens": 800, "temperature": 0.3, "response_format": {"type": "json_object"}}, headers={"Authorization": f"Bearer {SILRA_API_KEY}", "Content-Type": "application/json"}, timeout=120)
        if r.status_code != 200:
            return None, f"API Error {r.status_code}: {r.text[:200]}"
        content = r.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(content), None
    except Exception as e:
        return None, f"Error: {str(e)}"

if 'current_subject' not in st.session_state:
    st.session_state.current_subject = "中文科"
if 'generated_qs' not in st.session_state:
    st.session_state.generated_qs = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'results' not in st.session_state:
    st.session_state.results = []

st.title("🎓 OpenEduJustan 互動練習平台")
st.caption("揀科目 → AI 生成題目 → 學生作答 → AI 即時批改")

with st.sidebar:
    st.header("⚙️ 設定")
    st.info(f"Model: `{MODEL}`")
    if not SILRA_API_KEY:
        st.warning("⚠️ 未偵測到 API key")
    st.divider()
    st.header("👤 學生資料")
    student_name = st.text_input("你叫咩名？", key="sname")
    st.divider()
    st.header("📚 揀科目")
    subjects = list(ALL_SUBJECTS.keys())
    subject = st.selectbox("", subjects, index=subjects.index(st.session_state.current_subject) if st.session_state.current_subject in subjects else 0)
    st.session_state.current_subject = subject
    st.selectbox("年級", ["小六"])
    topic = st.text_input("主題 (可選)", placeholder="留空 = 隨機")
    num_qs = st.slider("題目數量", 1, 10, 5)
    st.divider()
    st.header("📊 統計")
    total_done = len(st.session_state.results)
    st.metric("已完成", total_done)
    if total_done > 0:
        avg_total = sum(r.get('total', 0) for r in st.session_state.results) / total_done
        st.metric("平均分", f"{avg_total:.1f}")

st.header(f"📝 {subject}")

if st.button("🎲 AI 生成題目", type="primary", use_container_width=True):
    with st.spinner("🤖 正在生成題目..."):
        new_qs = generate_questions(subject, "小六", topic, num_qs)
    if new_qs:
        st.session_state.generated_qs = new_qs
        st.session_state.answers = {}
        st.session_state.results = []
        st.success(f"✅ 成功生成 {len(new_qs)} 條題目！")
    else:
        st.error("❌ 生成失敗，請再試一次")

if st.session_state.generated_qs:
    st.markdown("---")
    st.subheader(f"📋 練習題目 ({len(st.session_state.generated_qs)} 條)")
    
    for i, q in enumerate(st.session_state.generated_qs):
        q_key = f"q_{i}"
        
        with st.expander(f"❓ 第 {i+1} 題: {q.get('title', q.get('question', '')[:40])}", expanded=(i == 0)):
            question_text = q.get('question') or q.get('title', '')
            st.markdown(question_text)
            
            if q.get('tip'):
                st.info(f"💡 {q['tip']}")
            
            st.markdown("**評分準則：**")
            rubric = q.get('rubric', "- 內容準確性\n- 解釋清晰度\n- 完整性")
            st.caption(rubric)
            
            if q_key not in st.session_state.answers:
                st.session_state.answers[q_key] = ""
            
            ans = st.text_area(f"✍️ 第 {i+1} 題答案", value=st.session_state.answers[q_key], height=150, key=f"answer_{i}", placeholder="寫低你嘅答案...")
            st.session_state.answers[q_key] = ans
            
            if st.button(f"🤖 批改第 {i+1} 題", key=f"grade_{i}", use_container_width=True):
                if not ans.strip():
                    st.warning("⚠️ 請先輸入答案")
                else:
                    with st.spinner("🤖 批改緊..."):
                        result, err = grade_answer(question_text, ans, rubric)
                    
                    if result:
                        scores = result.get("scores", {})
                        total = result.get("total", sum(scores.values()))
                        
                        st.success(f"✅ 總分：{total}/40")
                        
                        cols = st.columns(len(scores) if scores else 1)
                        for col, (k, v) in zip(cols, scores.items()):
                            col.metric(k, f"{v}/10")
                        
                        st.markdown(f"### 💬 評語")
                        st.markdown(f"> {result.get('comment', '')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("✅ **做得好**")
                            for s in result.get("strengths", []):
                                st.markdown(f"- {s}")
                        with col2:
                            st.markdown("🔧 **下次改善**")
                            for s in result.get("improvements", []):
                                st.markdown(f"- {s}")
                        
                        st.session_state.results.append({
                            "學生": student_name, "科目": subject, "題號": i + 1,
                            "題目": question_text[:80], "答案": ans, "總分": total,
                            "評語": result.get("comment", ""), "日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        })
                    else:
                        st.error(err)
    
    st.markdown("---")
    col_x, col_y = st.columns(2)
    
    with col_x:
        if st.button("🔄 重新生成所有題目", use_container_width=True):
            st.session_state.generated_qs = []
            st.session_state.answers = {}
            st.session_state.results = []
            st.rerun()
    
    with col_y:
        if st.session_state.results and st.button("⬇️ 下載結果 CSV", use_container_width=True):
            df = pd.DataFrame(st.session_state.results)
            csv_out = io.StringIO()
            df.to_csv(csv_out, index=False, encoding="utf-8-sig")
            st.download_button("⬇️ 下載 CSV", csv_out.getvalue(), f"results_{student_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv", use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | AI 互動練習平台</div>", unsafe_allow_html=True)
