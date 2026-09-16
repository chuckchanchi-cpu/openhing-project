import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="📝 OpenEduJustan 申請系統", page_icon="📝", layout="wide")

# Silra API Configuration
SILRA_API_URL = "https://api.silra.cn/v1/chat/completions"
SILRA_API_KEY = "sk-L4fIuygz7Y4ZR7TV24mG7btCldqcU13Mx0ykoPiF0JNlPyNq"
MODEL = "qwen3.5-plus"

def get_ai_suggestion(current_text, prompt_type):
    """Get AI suggestion for writing assistance"""
    try:
        # Define prompts for different sections
        prompts = {
            "self_intro": "你而家寫緊學生自我介紹。請根據以下文字，提供改進建議同埋可以加入嘅內容提示。保持廣東話口吻，自然真誠。只返回建議，唔好重写整段。\n\n現有文字:\n{text}",
            "interests": "你而家寫緊學生興趣同成就部分。請根據以下文字，提供改進建議同埋可以加入嘅具體例子。保持廣東話口吻。\n\n現有文字:\n{text}",
            "school_reason": "你而家寫緊選擇學校原因。請根據以下文字，提供改進建議，特別係點樣將個人特質同學校特色結合。保持廣東話口吻。\n\n現有文字:\n{text}",
            "summary": "你而家寫緊總結部分。請根據以下文字，提供改進建議，確保有力量同令人留下印象。保持廣東話口吻。\n\n現有文字:\n{text}"
        }
        
        system_prompt = "你係一位經驗豐富嘅升學顧問，專門幫助香港學生準備插班生申請。你嘅任務係提供具體、實用嘅寫作建議，幫助學生提升文章質量。用廣東話回覆。"
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompts.get(prompt_type, prompts["self_intro"]).format(text=current_text)}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {SILRA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"AI 服務暫時不可用 (錯誤碼: {response.status_code})"
    except Exception as e:
        return f"AI 錯誤: {str(e)}"

def check_spelling_grammar(text):
    """Check spelling and grammar"""
    if not text or len(text.strip()) < 10:
        return "請輸入更多文字以進行檢查"
    
    try:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "你係一位粵語語法專家。請檢查以下文字嘅拼寫、語法同流暢度。列出所有錯誤同改進建議。用廣東話回覆。"},
                {"role": "user", "content": f"請檢查以下文字嘅語法同拼寫：\n{text}"}
            ],
            "max_tokens": 300,
            "temperature": 0.3
        }
        
        headers = {
            "Authorization": f"Bearer {SILRA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(SILRA_API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return "語法檢查暫時不可用"
    except Exception:
        return "語法檢查暫時不可用"

# Session state management
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'application_data' not in st.session_state:
    st.session_state.application_data = {
        "name": "",
        "email": "",
        "current_school": "",
        "grade": "",
        "self_intro": "",
        "interests": "",
        "school_reason": "",
        "summary": ""
    }

# Page title
st.title("📝 OpenEduJustan 插班生申請系統")
st.markdown("### AI 輔助寫作 - 分段填寫，即時獲得專業建議")

# Progress bar
steps = ["基本資料", "自我介紹", "興趣成就", "學校原因", "總結", "提交"]
progress = (st.session_state.current_step + 1) / len(steps)
st.progress(progress)
st.markdown(f"**步驟 {st.session_state.current_step + 1}/{len(steps)}**: {steps[st.session_state.current_step]}")

# ==================== STEP 1: Basic Info ====================
if st.session_state.current_step == 0:
    st.header("📋 基本資料")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("學生姓名", value=st.session_state.application_data["name"])
        email = st.text_input("電郵地址", value=st.session_state.application_data["email"])
    with col2:
        current_school = st.text_input("現讀學校", value=st.session_state.application_data["current_school"])
        grade = st.selectbox("年級", ["小三", "小四", "小五", "小六", "中一", "中二", "中三", "中四", "中五", "中六"], 
                            index=["小三", "小四", "小五", "小六", "中一", "中二", "中三", "中四", "中五", "中六"].index(st.session_state.application_data["grade"]) if st.session_state.application_data["grade"] in ["小三", "小四", "小五", "小六", "中一", "中二", "中三", "中四", "中五", "中六"] else 0)
    
    if st.button("➡️ 下一步"):
        st.session_state.application_data.update({
            "name": name,
            "email": email,
            "current_school": current_school,
            "grade": grade
        })
        st.session_state.current_step = 1
        st.rerun()

# ==================== STEP 2: Self Introduction ====================
elif st.session_state.current_step == 1:
    st.header("✍️ 自我介紹")
    st.markdown("""
    **指導**: 用 200-300 字介紹自己，包括：
    - 性格特點
    - 學習態度
    - 家庭背景（可選）
    - 人生目標
    
    💡 **提示**: 保持真誠，用具體例子證明你的特質。
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        self_intro = st.text_area(
            "請在此撰寫自我介紹",
            value=st.session_state.application_data["self_intro"],
            height=300,
            placeholder="例如：我叫小明，今年12歲，就讀於...我係一個..."
        )
        
        # Character count
        char_count = len(self_intro)
        st.caption(f"字數: {char_count}/300 {'✅' if 200 <= char_count <= 300 else '⚠️ 建議控制在200-300字'}")
    
    with col2:
        st.markdown("### 🤖 AI 助手")
        
        if st.button("💡 獲取建議", use_container_width=True):
            with st.spinner("AI 正在分析..."):
                suggestion = get_ai_suggestion(self_intro or "暫無文字", "self_intro")
            st.info(suggestion)
        
        if st.button("🔍 檢查語法", use_container_width=True):
            with st.spinner("正在檢查..."):
                grammar_check = check_spelling_grammar(self_intro)
            st.success(grammar_check)
        
        st.markdown("---")
        st.markdown("**進度提示:**")
        st.metric("完成度", f"{min(char_count, 300)}/300 字")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 上一步", use_container_width=True):
            st.session_state.application_data["self_intro"] = self_intro
            st.session_state.current_step = 0
            st.rerun()
    with col2:
        if st.button("💾 保存草稿", use_container_width=True):
            st.session_state.application_data["self_intro"] = self_intro
            st.success("✅ 草稿已保存！")
    with col3:
        if st.button("➡️ 下一步", use_container_width=True):
            st.session_state.application_data["self_intro"] = self_intro
            st.session_state.current_step = 2
            st.rerun()

# ==================== STEP 3: Interests & Achievements ====================
elif st.session_state.current_step == 2:
    st.header("🏆 興趣同成就")
    st.markdown("""
    **指導**: 用 200-300 字描述：
    - 主要興趣同愛好
    - 相關成就或證書
    - 參與過嘅活動/比賽
    - 從中學到嘅技能
    
    💡 **提示**: 用具體數據同例子，避免空泛形容詞。
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        interests = st.text_area(
            "請在此撰寫興趣同成就",
            value=st.session_state.application_data["interests"],
            height=300,
            placeholder="例如：我從小就對音樂有興趣，已經考獲...我曾參加...呢個經歷令我學會了..."
        )
        
        char_count = len(interests)
        st.caption(f"字數: {char_count}/300 {'✅' if 200 <= char_count <= 300 else '⚠️ 建議控制在200-300字'}")
    
    with col2:
        st.markdown("### 🤖 AI 助手")
        
        if st.button("💡 獲取建議", use_container_width=True):
            with st.spinner("AI 正在分析..."):
                suggestion = get_ai_suggestion(interests or "暫無文字", "interests")
            st.info(suggestion)
        
        if st.button("🔍 檢查語法", use_container_width=True):
            with st.spinner("正在檢查..."):
                grammar_check = check_spelling_grammar(interests)
            st.success(grammar_check)
        
        st.markdown("---")
        st.markdown("**進度提示:**")
        st.metric("完成度", f"{min(char_count, 300)}/300 字")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 上一步", use_container_width=True):
            st.session_state.application_data["interests"] = interests
            st.session_state.current_step = 1
            st.rerun()
    with col2:
        if st.button("💾 保存草稿", use_container_width=True):
            st.session_state.application_data["interests"] = interests
            st.success("✅ 草稿已保存！")
    with col3:
        if st.button("➡️ 下一步", use_container_width=True):
            st.session_state.application_data["interests"] = interests
            st.session_state.current_step = 3
            st.rerun()

# ==================== STEP 4: School Reason ====================
elif st.session_state.current_step == 3:
    st.header("🎯 選擇學校原因")
    st.markdown("""
    **指導**: 用 200-300 字說明：
    - 為什麼想轉去這所學校？
    - 學校嘅哪些特色吸引你？
    - 你如何配合學校文化？
    - 未來計劃同學校資源嘅匹配
    
    💡 **提示**: 展示你做咗功課，了解學校特色。
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        school_reason = st.text_area(
            "請在此撰寫選擇學校原因",
            value=st.session_state.application_data["school_reason"],
            height=300,
            placeholder="例如：我一直關注貴校嘅...特別欣賞貴校嘅...我希望能夠..."
        )
        
        char_count = len(school_reason)
        st.caption(f"字數: {char_count}/300 {'✅' if 200 <= char_count <= 300 else '⚠️ 建議控制在200-300字'}")
    
    with col2:
        st.markdown("### 🤖 AI 助手")
        
        if st.button("💡 獲取建議", use_container_width=True):
            with st.spinner("AI 正在分析..."):
                suggestion = get_ai_suggestion(school_reason or "暫無文字", "school_reason")
            st.info(suggestion)
        
        if st.button("🔍 檢查語法", use_container_width=True):
            with st.spinner("正在檢查..."):
                grammar_check = check_spelling_grammar(school_reason)
            st.success(grammar_check)
        
        st.markdown("---")
        st.markdown("**進度提示:**")
        st.metric("完成度", f"{min(char_count, 300)}/300 字")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 上一步", use_container_width=True):
            st.session_state.application_data["school_reason"] = school_reason
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("💾 保存草稿", use_container_width=True):
            st.session_state.application_data["school_reason"] = school_reason
            st.success("✅ 草稿已保存！")
    with col3:
        if st.button("➡️ 下一步", use_container_width=True):
            st.session_state.application_data["school_reason"] = school_reason
            st.session_state.current_step = 4
            st.rerun()

# ==================== STEP 5: Summary ====================
elif st.session_state.current_step == 4:
    st.header("📝 總結")
    st.markdown("""
    **指導**: 用 100-200 字總結：
    - 重申申請意願
    - 表達對學校嘅期待
    - 感謝審閱老師
    
    💡 **提示**: 簡潔有力，令人留下正面印象。
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        summary = st.text_area(
            "請在此撰寫總結",
            value=st.session_state.application_data["summary"],
            height=200,
            placeholder="例如：感謝審閱老師撥冗閱讀我嘅申請。我相信...期望能夠成為..."
        )
        
        char_count = len(summary)
        st.caption(f"字數: {char_count}/200 {'✅' if 100 <= char_count <= 200 else '⚠️ 建議控制在100-200字'}")
    
    with col2:
        st.markdown("### 🤖 AI 助手")
        
        if st.button("💡 獲取建議", use_container_width=True):
            with st.spinner("AI 正在分析..."):
                suggestion = get_ai_suggestion(summary or "暫無文字", "summary")
            st.info(suggestion)
        
        if st.button("🔍 檢查語法", use_container_width=True):
            with st.spinner("正在檢查..."):
                grammar_check = check_spelling_grammar(summary)
            st.success(grammar_check)
        
        st.markdown("---")
        st.markdown("**總進度:**")
        total_chars = sum(len(v) for v in st.session_state.application_data.values() if isinstance(v, str))
        st.metric("總字數", f"{total_chars} 字")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 上一步", use_container_width=True):
            st.session_state.application_data["summary"] = summary
            st.session_state.current_step = 3
            st.rerun()
    with col2:
        if st.button("💾 保存草稿", use_container_width=True):
            st.session_state.application_data["summary"] = summary
            st.success("✅ 草稿已保存！")
    with col3:
        if st.button("🚀 提交申請", use_container_width=True):
            st.session_state.application_data["summary"] = summary
            st.session_state.current_step = 5
            st.rerun()

# ==================== STEP 6: Review & Submit ====================
elif st.session_state.current_step == 5:
    st.header("✅ 申請摘要")
    st.markdown("請檢查以下資料，確認無誤後即可提交。")
    
    data = st.session_state.application_data
    
    with st.expander("📋 基本資料", expanded=True):
        st.write(f"**姓名**: {data['name']}")
        st.write(f"**電郵**: {data['email']}")
        st.write(f"**現讀學校**: {data['current_school']}")
        st.write(f"**年級**: {data['grade']}")
    
    with st.expander("✍️ 自我介紹", expanded=True):
        st.write(data['self_intro'])
    
    with st.expander("🏆 興趣成就", expanded=True):
        st.write(data['interests'])
    
    with st.expander("🎯 學校原因", expanded=True):
        st.write(data['school_reason'])
    
    with st.expander("📝 總結", expanded=True):
        st.write(data['summary'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 修改", use_container_width=True):
            st.session_state.current_step = 4
            st.rerun()
    with col2:
        if st.button("🎉 確認提交", use_container_width=True, type="primary"):
            st.success("✅ 申請已成功提交！多謝你嘅時間。")
            st.balloons()
            
            # Reset form
            st.session_state.current_step = 0
            st.session_state.application_data = {
                "name": "",
                "email": "",
                "current_school": "",
                "grade": "",
                "self_intro": "",
                "interests": "",
                "school_reason": "",
                "summary": ""
            }

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | AI 輔助寫作系統</div>", unsafe_allow_html=True)
