"""
📐 分數乘法練習 (Fraction Multiplication Practice)
=====================================
對象：小學六年級學生
主題：分數乘法的認識與應用
"""

import streamlit as st
import random
import math

st.set_page_config(page_title="📐 分數乘法", page_icon="📐", layout="wide")

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# CSS - High contrast styling
st.markdown("""
<style>
    .question-box {
        background-color: #1e1e2e;
        border: 2px solid #6366f1;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    .question-text {
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
    }
    .ai-box {
        background-color: #2d2d44;
        border-left: 4px solid #00d9ff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #ffffff;
    }
    .correct {
        background-color: #1b4332;
        border: 2px solid #00ff88;
        padding: 10px;
        border-radius: 5px;
        color: #00ff88;
    }
    .wrong {
        background-color: #4a1515;
        border: 2px solid #ff4444;
        padding: 10px;
        border-radius: 5px;
        color: #ff4444;
    }
</style>
""", unsafe_allow_html=True)

st.title("📐 分數乘法練習")
st.markdown("### 小學六年級 - 分數乘法的認識與應用")

# Sidebar - 學習內容
st.sidebar.title("📚 學習內容")

mode = st.sidebar.radio(
    "選擇模式：",
    ["📖 學習教學", "✏️ 練習題", "🎮 測驗遊戲"]
)

# ========== 學習教學模式 ==========
if mode == "📖 學習教學":
    st.header("📖 分數乘法教學")
    
    st.markdown("""
    ### 📝 什麼是分數乘法？
    
    分數乘法就是**把一個分數重複相加幾次**。
    
    例如：2/3 × 4 = 2/3 + 2/3 + 2/3 + 2/3 = 8/3
    """)
    
    st.markdown("---")
    st.markdown("### 🧮 計算方法")
    
    st.markdown("""
    **分數 × 整數** 的計算步驟：
    
    1. **分子 × 整數**
    2. **分母不變**
    3. **結果要化簡**（化成最簡分數）
    """)
    
    # 示例
    st.markdown("---")
    st.markdown("### 📌 例子")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **例題 1：3/4 × 2**
        
        步驟：
        1. 分子：3 × 2 = 6
        2. 分母：4（不變）
        3. 6/4 = 3/2（化簡）
        
        答案：3/2 或 1½
        """)
    
    with col2:
        st.markdown("""
        **例題 2：5/6 × 3**
        
        步驟：
        1. 分子：5 × 3 = 15
        2. 分母：6（不變）
        3. 15/6 = 5/2（化簡）
        
        答案：5/2 或 2½
        """)

# ========== 練習題模式 ==========
elif mode == "✏️ 練習題":
    st.header("✏️ 分數乘法練習題")
    
    # 題目庫
    questions = [
        {"question": "2/3 × 4 = ?", "answer": "8/3", "simplified": "2⅔"},
        {"question": "4/5 × 2 = ?", "answer": "8/5", "simplified": "1⅗"},
        {"question": "2/7 × 3 = ?", "answer": "6/7", "simplified": "6/7"},
        {"question": "3/4 × 2 = ?", "answer": "6/4", "simplified": "3/2"},
        {"question": "5/6 × 3 = ?", "answer": "15/6", "simplified": "5/2"},
        {"question": "1/2 × 5 = ?", "answer": "5/2", "simplified": "2½"},
        {"question": "2/3 × 3 = ?", "answer": "6/3", "simplified": "2"},
        {"question": "3/5 × 4 = ?", "answer": "12/5", "simplified": "2⅖"},
    ]
    
    # 顯示題目
    for i, q in enumerate(questions):
        st.markdown(f"**題目 {i+1}：** {q['question']}")
        
        with st.expander("查看答案"):
            st.markdown(f"未化簡答案：{q['answer']}")
            st.markdown(f"**化簡答案：{q['simplified']}**")
        st.markdown("---")

# ========== 測驗遊戲模式 ==========
elif mode == "🎮 測驗遊戲":
    st.header("🎮 分數乘法測驗")
    
    # 顯示分數
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ 正確", st.session_state.score)
    with col2:
        st.metric("📝 總題目", st.session_state.total)
    
    if st.session_state.total > 0:
        accuracy = (st.session_state.score / st.session_state.total) * 100
        st.progress(accuracy / 100)
        st.markdown(f"準確率：{accuracy:.1f}%")
    
    st.markdown("---")
    
    # 生成隨機題目
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    
    if st.button("🎲 開始新題目"):
        # 隨機生成題目
        numerator = random.randint(1, 6)
        denominator = random.randint(2, 9)
        multiplier = random.randint(2, 5)
        
        # 計算答案
        raw_answer = numerator * multiplier
        gcd = math.gcd(raw_answer, denominator)
        simplified_num = raw_answer // gcd
        simplified_den = denominator // gcd
        
        st.session_state.current_question = {
            "num": numerator,
            "den": denominator,
            "mult": multiplier,
            "answer_num": simplified_num,
            "answer_den": simplified_den,
            "raw_num": raw_answer
        }
        st.session_state.show_result = False
        st.session_state.user_answer = ""
    
    # 顯示當前題目
    if st.session_state.current_question:
        q = st.session_state.current_question
        st.markdown(f"""
        <div class="question-box">
            <div class="question-text">計算：<br><br>
            <span style="font-size:32px">{q['num']}/{q['den']} × {q['mult']} = ?</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 輸入答案
        col1, col2 = st.columns(2)
        with col1:
            answer_num = st.number_input("分子（Numerator）", min_value=1, max_value=50, key="ans_num")
        with col2:
            answer_den = st.number_input("分母（Denominator）", min_value=1, max_value=50, key="ans_den")
        
        if st.button("✅ 提交答案", type="primary"):
            st.session_state.total += 1
            
            if answer_num == q['answer_num'] and answer_den == q['answer_den']:
                st.session_state.score += 1
                st.markdown('<div class="correct">🎉 正確！太棒了！</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong">❌ 不正確，正確答案是 {q["answer_num"]}/{q["answer_den"]}</div>', unsafe_allow_html=True)
            
            st.session_state.show_result = True
    
    # 歷史記錄
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 答題歷史")
        for h in st.session_state.history[-5:]:
            st.write(h)

    # 重新開始
    if st.button("🔄 重新開始"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.history = []
        st.session_state.current_question = None
        st.rerun()

st.markdown("---")
st.markdown("💡 **溫馨提示：** 記得把答案化簡成最簡分數喔！")
