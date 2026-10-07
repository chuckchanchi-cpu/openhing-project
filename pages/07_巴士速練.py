"""
🚌 巴士速練 — Mobile-First Quiz App
一開就做題，搭車 10 分鐘都做到 5 題
"""

import streamlit as st
import requests
import json
import random
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="🚌 巴士速練",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== Silra API =====
SILRA_API_URL = "https://api.silra.cn/v1/chat/completions"
SILRA_API_KEY = "sk-HfiuPr1xWenSQUsB5x0PPtHW3gVYN9MBUXTVQ67orNPED24y"
MODEL = "qwen3.8-flash"

# ===== CSS for mobile =====
st.markdown("""
<style>
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {display: none !important;}
    
    /* Big tap targets */
    .stButton > button {
        width: 100%;
        min-height: 60px;
        font-size: 20px !important;
        margin: 8px 0;
        border-radius: 12px;
    }
    
    /* Radio buttons bigger */
    .stRadio > div > label {
        font-size: 18px !important;
        padding: 12px 8px;
    }
    
    /* Question text bigger */
    .question-text {
        font-size: 22px;
        line-height: 1.6;
        padding: 16px;
        background: #1e1e2e;
        border-radius: 12px;
        margin: 12px 0;
    }
    
    /* Score display */
    .score-big {
        font-size: 48px;
        text-align: center;
        padding: 20px;
    }
    
    /* Progress */
    .progress-text {
        font-size: 16px;
        color: #888;
        text-align: center;
    }
    
    /* Answer feedback */
    .correct {
        background: #1a472a;
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        font-size: 18px;
    }
    .wrong {
        background: #471a1a;
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 16px;
        font-size: 18px;
    }
    
    /* Subject selector */
    .subject-btn {
        min-height: 80px !important;
        font-size: 24px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== Subject configs =====
SUBJECTS = {
    "🇨🇳 中文": {
        "emoji": "📝",
        "topics": ["詞語填充", "近義詞反義詞", "修辭手法", "閱讀理解", "成語運用"],
        "prompt": """你係香港小學六年級中文科老師。出一條選擇題（4個選項），廣東話題目。
格式：
題目：[問題]
A. [選項]
B. [選項]
C. [選項]
D. [選項]
答案：[A/B/C/D]
解釋：[一句話解釋]""",
    },
    "🇬🇧 英文": {
        "emoji": "🔤",
        "topics": ["Grammar", "Vocabulary", "Tenses", "Prepositions", "Comprehension"],
        "prompt": """You are a Hong Kong Primary 6 English teacher. Create one multiple choice question (4 options).
Format:
Q: [question]
A. [option]
B. [option]
C. [option]
D. [option]
Answer: [A/B/C/D]
Explanation: [one sentence, in Cantonese]""",
    },
    "🔢 數學": {
        "emoji": "➕",
        "topics": ["分數", "小數", "百分比", "面積體積", "應用題"],
        "prompt": """你係香港小學六年級數學老師。出一條數學選擇題（4個選項），廣東話題目。
格式：
題目：[問題]
A. [選項]
B. [選項]
C. [選項]
D. [選項]
答案：[A/B/C/D]
解釋：[解題步驟，用廣東話]""",
    },
    "🌍 常識": {
        "emoji": "🧪",
        "topics": ["生物分類", "能源", "地球與太空", "健康與疾病", "環境"],
        "prompt": """你係香港小學六年級常識科老師。出一條選擇題（4個選項），廣東話題目。
格式：
題目：[問題]
A. [選項]
B. [選項]
C. [選項]
D. [選項]
答案：[A/B/C/D]
解釋：[一句話解釋]""",
    }
}

# ===== Helper functions =====
def generate_question(subject, topic=None):
    """Generate a question via Silra API"""
    config = SUBJECTS[subject]
    topic_hint = f"，主題係{topic}" if topic else ""
    
    try:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": config["prompt"]},
                {"role": "user", "content": f"出題{topic_hint}。要適合小六學生程度，唔好太難。"}
            ],
            "max_tokens": 500,
            "temperature": 0.8
        }
        headers = {
            "Authorization": f"Bearer {SILRA_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        return None
    except Exception as e:
        return None

def parse_question(text):
    """Parse generated question into structured format"""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    question = ""
    options = []
    answer = ""
    explanation = ""
    
    for line in lines:
        if line.startswith('題目:') or line.startswith('題目：') or line.startswith('Q:') or line.startswith('Q：'):
            question = line.split(':', 1)[-1].split('：', 1)[-1].strip()
        elif line.startswith('A.') or line.startswith('A、'):
            options.append(line[2:].strip())
        elif line.startswith('B.') or line.startswith('B、'):
            options.append(line[2:].strip())
        elif line.startswith('C.') or line.startswith('C、'):
            options.append(line[2:].strip())
        elif line.startswith('D.') or line.startswith('D、'):
            options.append(line[2:].strip())
        elif line.startswith('答案:') or line.startswith('答案：') or line.startswith('Answer:') or line.startswith('Answer：'):
            answer = line.split(':', 1)[-1].split('：', 1)[-1].strip()
        elif line.startswith('解釋:') or line.startswith('解釋：') or line.startswith('Explanation:') or line.startswith('Explanation：'):
            explanation = line.split(':', 1)[-1].split('：', 1)[-1].strip()
    
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation
    }

# ===== Session state init =====
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'  # home, quiz, result
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'loading' not in st.session_state:
    st.session_state.loading = False

# ===== HOME SCREEN =====
if st.session_state.screen == 'home':
    st.markdown("# 🚌 巴士速練")
    st.markdown("**搭車 10 分鐘，做多 5 題**")
    st.markdown("")
    
    # Subject selection - big buttons
    cols = st.columns(2)
    subjects = list(SUBJECTS.keys())
    for i, subj in enumerate(subjects):
        with cols[i % 2]:
            config = SUBJECTS[subj]
            if st.button(
                f"{config['emoji']}\n{subj}",
                key=f"subj_{i}",
                use_container_width=True
            ):
                st.session_state.selected_subject = subj
                st.session_state.screen = 'quiz'
                st.session_state.score = 0
                st.session_state.total = 0
                st.session_state.history = []
                st.session_state.answered = False
                st.rerun()
    
    st.markdown("---")
    
    # Quick stats
    if st.session_state.history:
        total_today = len(st.session_state.history)
        correct_today = sum(1 for h in st.session_state.history if h['correct'])
        st.markdown(f"📊 今日進度：**{correct_today}/{total_today}** 題啱咗")

# ===== QUIZ SCREEN =====
elif st.session_state.screen == 'quiz':
    subj = st.session_state.selected_subject
    config = SUBJECTS[subj]
    
    # Top bar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠", use_container_width=True):
            st.session_state.screen = 'home'
            st.rerun()
    with col2:
        st.markdown(f"<div class='progress-text'>{config['emoji']} {subj} · 第 {st.session_state.total + 1} 題</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='progress-text'>✅ {st.session_state.score}/{st.session_state.total}</div>", unsafe_allow_html=True)
    
    # Generate question if needed
    if st.session_state.current_q is None and not st.session_state.loading:
        st.session_state.loading = True
        with st.spinner("出緊題..."):
            topic = random.choice(config["topics"])
            raw = generate_question(subj, topic)
            if raw:
                st.session_state.current_q = parse_question(raw)
                st.session_state.current_q['raw'] = raw
                st.session_state.current_q['topic'] = topic
            else:
                st.error("出題失敗，試多次")
        st.session_state.loading = False
        st.rerun()
    
    # Display question
    if st.session_state.current_q:
        q = st.session_state.current_q
        
        # Question
        st.markdown(f"<div class='question-text'>{q['question']}</div>", unsafe_allow_html=True)
        
        # Options
        if not st.session_state.answered:
            options = q['options']
            option_labels = ['A', 'B', 'C', 'D']
            
            for i, opt in enumerate(options):
                if i < len(option_labels):
                    if st.button(
                        f"{option_labels[i]}. {opt}",
                        key=f"opt_{i}",
                        use_container_width=True
                    ):
                        st.session_state.answered = True
                        st.session_state.user_answer = option_labels[i]
                        if option_labels[i] == q['answer']:
                            st.session_state.score += 1
                        st.session_state.total += 1
                        st.session_state.history.append({
                            'subject': subj,
                            'question': q['question'],
                            'correct': option_labels[i] == q['answer'],
                            'user': option_labels[i],
                            'answer': q['answer']
                        })
                        st.rerun()
        
        # Show answer
        if st.session_state.answered:
            user = st.session_state.user_answer
            correct = q['answer']
            is_correct = user == correct
            
            if is_correct:
                st.markdown(f"<div class='correct'>✅ <b>啱咗！</b> 答案係 {correct}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='wrong'>❌ <b>錯咗</b>！你揀 {user}，答案係 {correct}</div>", unsafe_allow_html=True)
            
            if q.get('explanation'):
                st.markdown(f"💡 {q['explanation']}")
            
            st.markdown("")
            
            # Next question button
            if st.button("➡️ 下一題", use_container_width=True):
                st.session_state.current_q = None
                st.session_state.answered = False
                st.rerun()
            
            # End session
            if st.button("📊 睇成績", use_container_width=True):
                st.session_state.screen = 'result'
                st.rerun()

# ===== RESULT SCREEN =====
elif st.session_state.screen == 'result':
    st.markdown("# 📊 成績報告")
    
    score = st.session_state.score
    total = st.session_state.total
    
    if total > 0:
        pct = int(score / total * 100)
        
        st.markdown(f"<div class='score-big'>{score}/{total}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='progress-text'>正確率 {pct}%</div>", unsafe_allow_html=True)
        
        # Emoji feedback
        if pct >= 90:
            st.markdown("🌟 太犀利啦！Keep it up!")
        elif pct >= 70:
            st.markdown("👍 不錯！繼續努力！")
        elif pct >= 50:
            st.markdown("💪 有進步空間，再練多啲！")
        else:
            st.markdown("📚 唔緊要，下次會更好！")
        
        # History
        st.markdown("---")
        st.markdown("### 回顧")
        for i, h in enumerate(st.session_state.history):
            icon = "✅" if h['correct'] else "❌"
            st.markdown(f"{icon} **{h['subject']}** — {h['question'][:50]}...")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 再來一科", use_container_width=True):
            st.session_state.screen = 'home'
            st.session_state.current_q = None
            st.session_state.answered = False
            st.rerun()
    with col2:
        if st.button(f"🔁 繼續 {st.session_state.selected_subject}", use_container_width=True):
            st.session_state.screen = 'quiz'
            st.session_state.current_q = None
            st.session_state.answered = False
            st.session_state.score = 0
            st.session_state.total = 0
            st.rerun()