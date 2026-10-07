import streamlit as st
import requests
import json
import os
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="🎓 OpenEduJustan 練習平台", page_icon="🎓", layout="wide")

# Silra API Configuration
SILRA_API_URL = "https://api.silra.cn/v1/chat/completions"
SILRA_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-HfiuPr1xWenSQUsB5x0PPtHW3gVYN9MBUXTVQ67orNPED24y")
MODEL = "qwen3.8-flash"

# Mac mini folder paths
BASE_DIR = Path.home() / "Desktop" / "openedujustan"
SUBJECT_FOLDERS = {
    "中文": BASE_DIR / "Chinese",
    "常識": BASE_DIR / "General_Studies",
    "英文": BASE_DIR / "English",
    "數學": BASE_DIR / "Maths"
}

def get_ai_feedback(question, answer, subject, grade):
    """Get AI feedback for student answer"""
    try:
        prompts = {
            "中文": f"你係一位經驗豐富嘅小學中文老師。請批改以下{grade}學生嘅作文/文章。\n\n**評分標準：**\n1. 內容完整性 (40%)\n2. 語法同拼寫 (30%)\n3. 表達清晰度 (20%)\n4. 創意同深度 (10%)\n\n**問題**: {question}\n**學生答案**: {answer}\n\n請提供：總評、優點、需要改進嘅地方、具體修改建議。用廣東話回覆。",
            
            "常識": f"你係一位經驗豐富嘅小學常識科老師。請批改以下{grade}學生嘅開放式問題答案。\n\n**評分標準：**\n1. 答案完整性 (40%) - 有冇答晒所有部分？\n2. 知識準確性 (30%) - 科學概念正確嗎？\n3. 邏輯清晰度 (20%) - 論述有條理嗎？\n4. 例子運用 (10%) - 有冇具體例子支持？\n\n**問題**: {question}\n**學生答案**: {answer}\n\n請提供：總評、知識點檢查、改進建議。用廣東話回覆。",
            
            "英文": f"You are an experienced primary school English teacher. Please grade this {grade} student's writing.\n\n**Grading Criteria:**\n1. Content & Relevance (40%)\n2. Grammar & Spelling (30%)\n3. Clarity & Coherence (20%)\n4. Vocabulary (10%)\n\n**Question**: {question}\n**Student Answer**: {answer}\n\nPlease provide: Overall assessment, strengths, areas for improvement, specific suggestions. Reply in Cantonese.",
            
            "數學": f"你係一位經驗豐富嘅小學數學老師。請批改以下{grade}學生嘅應用題解答。\n\n**評分標準：**\n1. 方法正確性 (40%)\n2. 計算準確性 (30%)\n3. 步驟完整性 (20%)\n4. 答案合理性 (10%)\n\n**問題**: {question}\n**學生答案**: {answer}\n\n請提供：方法評估、計算檢查、錯誤定位、改進建議。用廣東話回覆。"
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": prompts.get(subject, prompts["中文"])},
                {"role": "user", "content": f"請批改以下答案：\n\n{answer}"}
            ],
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {SILRA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"AI 服務暫時不可用 (錯誤碼: {response.status_code})"
    except Exception as e:
        return f"AI 錯誤: {str(e)}"

def load_questions_from_folder(folder_path):
    """Load questions from markdown files in the folder"""
    questions = []
    
    if not folder_path.exists():
        return questions
    
    # Scan all .md files recursively
    for md_file in sorted(folder_path.rglob("*.md")):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract title (first line starting with #)
            title = ""
            question_text = ""
            lines = content.split("\n")
            
            for i, line in enumerate(lines):
                if line.startswith("# ") and not title:
                    title = line[2:].strip()
                elif line.startswith("## ") or line.startswith("### "):
                    # This might be a sub-question
                    pass
            
            # If we have a title, add it
            if title:
                # Try to extract a practice question from the content
                # Look for sections that look like exercises/practice
                practice_section = ""
                in_practice = False
                
                for line in lines:
                    if "練習" in line or "訓練" in line or "做題" in line or "Homework" in line.lower():
                        in_practice = True
                    if in_practice and line.strip() and not line.startswith("#"):
                        practice_section += line + "\n"
                
                if practice_section:
                    questions.append({
                        "id": len(questions) + 1,
                        "title": title,
                        "question": practice_section[:500],  # Truncate for display
                        "full_content": content,
                        "file_path": str(md_file),
                        "tip": "💡 提示：仔細閱讀題目，結合所學知識作答。"
                    })
        except Exception as e:
            st.warning(f"⚠️ 讀取文件出錯: {md_file.name} - {str(e)}")
    
    return questions

# Session state management
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = "中文"
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_grade' not in st.session_state:
    st.session_state.student_grade = "小六"
if 'practice_history' not in st.session_state:
    st.session_state.practice_history = []

# Title
st.title("🎓 OpenEduJustan 互動練習平台")
st.markdown("選擇科目 → 讀取本地題目 → 輸入答案 → 獲得 AI 即時反饋")

# Sidebar: Student Info
with st.sidebar:
    st.header("👤 學生資料")
    
    name = st.text_input("學生姓名", value=st.session_state.student_name, placeholder="輸入姓名")
    grade = st.selectbox("年級", ["小一", "小二", "小三", "小四", "小五", "小六"], 
                         index=["小一", "小二", "小三", "小四", "小五", "小六"].index(st.session_state.student_grade) if st.session_state.student_grade in ["小一", "小二", "小三", "小四", "小五", "小六"] else 5)
    
    st.divider()
    
    st.header("📚 選擇科目")
    subjects = ["中文", "常識", "英文", "數學"]
    subject = st.radio("", subjects, index=subjects.index(st.session_state.current_subject), label_visibility="collapsed")
    
    st.session_state.current_subject = subject
    st.session_state.student_name = name
    st.session_state.student_grade = grade
    
    st.divider()
    
    # Stats
    st.header("📊 練習統計")
    total_practices = len(st.session_state.practice_history)
    st.metric("已完成練習", total_practices)
    
    if total_practices > 0:
        avg_score = sum(p.get('score', 0) for p in st.session_state.practice_history if 'score' in p) / total_practices
        st.metric("平均評分", f"{avg_score:.1f}/100")

# Main content area
st.header(f"📝 {subject}練習")

# Load questions from Mac mini folder
folder_path = SUBJECT_FOLDERS.get(subject, BASE_DIR)
local_questions = load_questions_from_folder(folder_path)

# Define fallback default questions (in case no local files found)
DEFAULT_QUESTIONS = {
    "中文": [
        {
            "id": 1,
            "title": "敘事文：一次難忘的經歷",
            "question": "請以「一次難忘的經歷」為題，寫一篇不少于400字的记叙文。要求內容具體，感情真摯，有開頭、發展、高潮和結尾。",
            "tip": "💡 提示：選擇一件真正令你印象深刻的事，詳細描述當時的情景同感受。",
            "min_words": 400
        }
    ],
    "常識": [
        {
            "id": 1,
            "title": "水的循環",
            "question": "請詳細解釋水的循環過程。包括：\n1. 水循環有哪幾個主要階段？\n2. 每個階段發生什麼變化？\n3. 太陽在水循環中扮演什麼角色？\n4. 舉出一個日常生活中觀察到的水循環例子。",
            "tip": "💡 提示：使用「蒸發」、「凝結」、「降水」、「匯集」等科學術語。",
            "min_words": 200
        }
    ],
    "英文": [
        {
            "id": 1,
            "title": "My Best Friend",
            "question": "Write a paragraph (at least 80 words) about your best friend. Include:\n- What does your friend look like?\n- What is his/her personality like?\n- Why do you like him/her?\n- Share one special memory you have together.",
            "tip": "💡 Tip: Use descriptive adjectives and specific examples.",
            "min_words": 80
        }
    ],
    "數學": [
        {
            "id": 1,
            "title": "應用題：購物問題",
            "question": "小明去商店買文具。一支筆售價$15，一本筆記本售價$25。他買了3支筆和2本筆記本，付給店員$100。\n\n請問：\n1. 小明一共花了多少錢？\n2. 店員應該找給他多少錢？\n3. 如果他想用餘額再買$10的橡皮擦，夠嗎？",
            "tip": "💡 提示：列出算式，逐步計算，注意單位。",
            "min_words": 50
        }
    ]
}

# Use local questions if available, otherwise use defaults
current_questions = local_questions if local_questions else DEFAULT_QUESTIONS.get(subject, [])

# Display source info
if local_questions:
    st.success(f"✅ 已載入 {len(local_questions)} 個本地題目 (來自 {folder_path})")
else:
    st.info(f"ℹ️ 未找到本地題目，使用默認題目庫")

if not current_questions:
    st.warning("⚠️ 暫無練習題目")
else:
    # Question selector
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 題目列表")
        question_id = st.selectbox(
            "選擇題目",
            options=[f"#{q['id']} {q['title']}" for q in current_questions],
            index=0
        )
        
        # Extract question ID from selection
        selected_idx = [f"#{q['id']} {q['title']}" for q in current_questions].index(question_id)
        current_q = current_questions[selected_idx]
    
    with col2:
        st.markdown(f"### {current_q['title']}")
        st.info(current_q.get('tip', '💡 提示：仔細閱讀題目，結合所學知識作答。'))
        
        st.markdown("**問題：**")
        st.write(current_q['question'])
    
    # Answer input area
    st.markdown("---")
    st.markdown("### ✍️ 請在此輸入你的答案")
    
    answer = st.text_area(
        "你的答案",
        height=300,
        placeholder="請仔細閱讀題目，然後在下方輸入你的答案..."
    )
    
    char_count = len(answer)
    st.caption(f"字數: {char_count}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        submit_btn = st.button("🤖 提交批改", type="primary", use_container_width=True, disabled=char_count < 10)
    
    with col2:
        save_btn = st.button("💾 保存草稿", use_container_width=True, disabled=char_count < 10)
    
    with col3:
        clear_btn = st.button("🗑️ 清空答案", use_container_width=True)
    
    # Handle clear
    if clear_btn:
        answer = ""
        st.rerun()
    
    # Handle save draft
    if save_btn:
        draft_data = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "question_id": current_q['id'],
            "question_title": current_q['title'],
            "answer": answer,
            "student_name": name,
            "grade": grade
        }
        st.session_state.practice_history.append(draft_data)
        st.success("✅ 草稿已保存！")
    
    # Handle submission
    if submit_btn and answer:
        with st.spinner("🤖 AI 正在批改你的答案..."):
            feedback = get_ai_feedback(current_q['question'], answer, subject, grade)
        
        # Display feedback
        st.markdown("---")
        st.markdown("### 🤖 AI 反饋")
        st.info(feedback)
        
        # Save result
        result_data = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "question_id": current_q['id'],
            "question_title": current_q['title'],
            "answer": answer,
            "feedback": feedback,
            "student_name": name,
            "grade": grade
        }
        st.session_state.practice_history.append(result_data)
        
        # Download button
        if st.button("💾 下載結果 (Markdown)", use_container_width=True):
            filename = f"{name or 'Student'}_{subject}_{current_q['title']}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {name or 'Student'} - {subject}練習反饋\n\n")
                f.write(f"**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
                f.write(f"**年級**: {grade}  \n")
                f.write(f"**題目**: {current_q['title']}  \n\n")
                f.write(f"## 問題\n\n{current_q['question']}  \n\n")
                f.write(f"## 你的答案\n\n{answer}  \n\n")
                f.write(f"## AI 反饋\n\n{feedback}\n")
            st.success(f"✅ 已下載至 {filename}")
        
        st.balloons()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | 互動練習平台</div>", unsafe_allow_html=True)
