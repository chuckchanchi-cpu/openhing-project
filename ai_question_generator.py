import streamlit as st
import requests
import json
import os
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="🎓 OpenEduJustan AI 出題平台", page_icon="🎓", layout="wide")

# Silra API Configuration
SILRA_API_URL = "https://api.silra.cn/v1/chat/completions"
SILRA_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-HfiuPr1xWenSQUsB5x0PPtHW3gVYN9MBUXTVQ67orNPED24y")
MODEL = "deepseek-chat"

def generate_questions(subject, grade, topic, count=5):
    """Generate practice questions using AI"""
    try:
        system_prompt = f"""你係一位經驗豐富嘅小學{subject}科老師，專門為{grade}學生設計練習題目。

請根據以下要求生成 {count} 條練習題目：

**要求：**
1. 題目要清晰、具體，適合{grade}學生水平
2. 涵蓋不同難易度 (簡單、中等、挑戰)
3. 每條題目包含：題目內容、評分標準、參考答案
4. 用{subject}語撰寫 (英文科用英文，其他用廣東話)
5. 格式要統一，方便學生作答

**輸出格式 (JSON)：**
```json
[
  {{
    "id": 1,
    "title": "題目標題",
    "question": "完整題目內容",
    "difficulty": "簡單/中等/挑戰",
    "marks": 10,
    "reference_answer": "參考答案要点",
    "tip": "提示或解題技巧"
  }}
]
```

只返回 JSON，唔好有其他文字。"""

        user_message = f"科目: {subject}\n年級: {grade}\n主題: {topic if topic else '請根據課程標準自行選擇合適主題'}\n數量: {count} 條"

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 3000,
            "temperature": 0.8
        }

        headers = {
            "Authorization": f"Bearer {SILRA_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Parse JSON from response
            try:
                # Try to extract JSON from markdown code block
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    json_str = content.split("```")[1].split("```")[0].strip()
                else:
                    json_str = content
                
                questions = json.loads(json_str)
                return questions
            except json.JSONDecodeError:
                # If JSON parsing fails, create a fallback question
                return [{
                    "id": 1,
                    "title": f"{subject}練習 - {topic or '綜合'}",
                    "question": content[:500],
                    "difficulty": "中等",
                    "marks": 10,
                    "reference_answer": "參見 AI 生成內容",
                    "tip": "💡 仔細閱讀題目，結合所學知識作答。"
                }]
        else:
            st.error(f"❌ AI 生成失敗 (錯誤碼: {response.status_code})")
            return []
    except Exception as e:
        st.error(f"❌ 生成出錯: {str(e)}")
        return []

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

# Session state management
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = "中文"
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_grade' not in st.session_state:
    st.session_state.student_grade = "小六"
if 'generated_questions' not in st.session_state:
    st.session_state.generated_questions = []
if 'reviewed_questions' not in st.session_state:
    st.session_state.reviewed_questions = []

# Title
st.title("🎓 OpenEduJustan AI 出題平台")
st.markdown("👨‍🏫 教師模式：AI 自動生成題目 → 教師審核 → 學生練習")

# Sidebar: Settings
with st.sidebar:
    st.header("⚙️ 出題設定")
    
    subject = st.selectbox("科目", ["中文", "常識", "英文", "數學"], 
                           index=["中文", "常識", "英文", "數學"].index(st.session_state.current_subject))
    grade = st.selectbox("年級", ["小一", "小二", "小三", "小四", "小五", "小六"],
                         index=["小一", "小二", "小三", "小四", "小五", "小六"].index(st.session_state.student_grade))
    topic = st.text_input("主題 (可選)", placeholder="例如：水的循環、近義詞、小數除法")
    question_count = st.slider("題目數量", 1, 10, 5)
    
    st.session_state.current_subject = subject
    st.session_state.student_grade = grade
    
    st.divider()
    
    # Stats
    st.header("📊 統計")
    total_generated = len(st.session_state.generated_questions)
    total_reviewed = len(st.session_state.reviewed_questions)
    st.metric("已生成", total_generated)
    st.metric("已審核", total_reviewed)
    
    st.divider()
    
    st.header("📚 快速主題")
    quick_topics = {
        "中文": ["敘事文", "議論文", "描寫文", "近義詞", "成語運用"],
        "常識": ["水的循環", "植物生長", "地球與太陽", "生物分類", "天氣現象"],
        "英文": ["My Family", "Animals", "Food", "Travel", "Daily Routine"],
        "數學": ["小數加法", "面積計算", "分数應用", "時間計算", "應用題"]
    }
    
    cols = st.columns(2)
    for i, t in enumerate(quick_topics.get(subject, [])[:4]):
        with cols[i % 2]:
            if st.button(t, use_container_width=True):
                topic = t

# Main content area
st.header(f"🤖 AI 自動出題 — {subject}")

# Generate questions button
col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🎲 生成題目", type="primary", use_container_width=True):
        with st.spinner(f"🤖 正在生成 {question_count} 條 {subject} 題目..."):
            new_questions = generate_questions(subject, grade, topic, question_count)
        
        if new_questions:
            st.session_state.generated_questions = new_questions
            st.success(f"✅ 成功生成 {len(new_questions)} 條題目！")
        else:
            st.error("❌ 生成失敗，請再試一次")

with col2:
    if st.session_state.generated_questions:
        st.info(f"💡 當前有 {len(st.session_state.generated_questions)} 條題目，可點擊「重新生成」獲得新題目")

# Display generated questions
if st.session_state.generated_questions:
    st.markdown("---")
    st.subheader("📋 生成嘅題目")
    
    for idx, q in enumerate(st.session_state.generated_questions):
        with st.expander(f"#{q.get('id', idx+1)} {q.get('title', '未命名')}", expanded=(idx == 0)):
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.markdown(f"**{q.get('question', '無內容')}**")
                
                st.markdown("**評分標準：**")
                st.write(f"- 難度: {q.get('difficulty', '中等')}")
                st.write(f"- 分數: {q.get('marks', 10)} 分")
                
                if q.get('tip'):
                    st.info(q['tip'])
            
            with col_b:
                st.markdown("**教師操作：**")
                
                # Review buttons
                if st.button("✅ 通過", key=f"approve_{idx}", use_container_width=True):
                    q['reviewed'] = True
                    q['reviewed_at'] = datetime.now().isoformat()
                    st.session_state.reviewed_questions.append(q)
                    st.success("✅ 已通過！")
                    st.rerun()
                
                if st.button("🔄 重出這題", key=f"regenerate_{idx}", use_container_width=True):
                    with st.spinner("🤖 正在重新生成..."):
                        # Get single replacement question
                        single_q = generate_questions(subject, grade, topic, 1)
                        if single_q:
                            st.session_state.generated_questions[idx] = single_q[0]
                            st.success("✅ 已替換！")
                            st.rerun()
                
                if st.button("❌ 刪除", key=f"delete_{idx}", use_container_width=True):
                    st.session_state.generated_questions.pop(idx)
                    st.success("❌ 已刪除！")
                    st.rerun()
    
    # Batch actions
    st.markdown("---")
    col_x, col_y, col_z = st.columns(3)
    
    with col_x:
        if st.button("🔄 全部重新生成", use_container_width=True):
            with st.spinner("🤖 正在重新生成所有題目..."):
                new_qs = generate_questions(subject, grade, topic, question_count)
            if new_qs:
                st.session_state.generated_questions = new_qs
                st.success(f"✅ 已生成 {len(new_qs)} 條新題目！")
            else:
                st.error("❌ 生成失敗")
    
    with col_y:
        if st.button("💾 保存到文件", use_container_width=True):
            filename = f"{subject}_{grade}_{topic or 'custom'}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {subject}練習題目\n\n")
                f.write(f"**年級**: {grade}  \n")
                f.write(f"**日期**: {datetime.now().strftime('%Y-%m-%d')}  \n")
                f.write(f"**主題**: {topic or '自訂'}  \n\n")
                
                for q in st.session_state.generated_questions:
                    f.write(f"## #{q.get('id', 'N/A')} {q.get('title', '未命名')}\n\n")
                    f.write(f"{q.get('question', '')}\n\n")
                    f.write(f"- 難度: {q.get('difficulty', '中等')}\n")
                    f.write(f"- 分數: {q.get('marks', 10)} 分\n")
                    if q.get('tip'):
                        f.write(f"- 提示: {q['tip']}\n")
                    if q.get('reference_answer'):
                        f.write(f"\n**參考答案**:\n{q['reference_answer']}\n")
                    f.write("\n---\n\n")
            
            st.success(f"✅ 已保存至 {filename}")
    
    with col_z:
        if st.button("📤 發布給學生", use_container_width=True, type="primary"):
            st.success("🎉 題目已發布！學生可以開始練習")
            st.balloons()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | AI 出題平台</div>", unsafe_allow_html=True)
