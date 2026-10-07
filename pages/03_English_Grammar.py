import streamlit as st
import json

st.set_page_config(page_title="🔤 English Grammar Trainer", page_icon="🔤", layout="wide")

# ===== English Grammar Exercises Data =====

GRAMMAR_EXERCISES = {
    "Look and Write: 看圖寫作": {
        "description": "看圖片寫出完整句子，每句不少於5個字",
        "questions": [
            {
                "question": "Look at the classroom picture. Write a sentence using 'This is...'",
                "hint": "以 'This is' 開頭，描述圖片中的一件物品或一個人",
                "answer": "This is a teacher.",
                "explanation": "用 'This is' 描述單數事物。例如：This is a teacher. (呢個係一位老師。)"
            },
            {
                "question": "Look at the classroom picture. Write a sentence using 'These are...'",
                "hint": "以 'These are' 開頭，描述圖片中的多件物品或多個人",
                "answer": "These are students.",
                "explanation": "用 'These are' 描述複數事物。例如：These are students. (呢啲係學生。)"
            },
            {
                "question": "Write a sentence about yourself using 'I am...'",
                "hint": "用 'I am' 介紹自己，可以寫年齡、名字或感受",
                "answer": "I am a student.",
                "explanation": "用 'I am' 介紹自己。例如：I am a student. (我係一個學生。)"
            },
            {
                "question": "Write a sentence about something you like using 'I like...'",
                "hint": "使用 'I like' 表達喜歡的事物，可以是食物、活動或顏色",
                "answer": "I like pizza.",
                "explanation": "用 'I like' 表達喜好。例如：I like pizza. (我鍾意食 pizza。)"
            },
            {
                "question": "Look at the picture. Write 3 sentences about what you see.",
                "hint": "用 'This is', 'These are', 'I am', 'I like' 等句型",
                "answer": "This is a classroom. These are desks. I am a student.",
                "explanation": "結合多個句型描述圖片。每句至少5個字。"
            }
        ]
    },
    "Grammar 1: so (原因和結果)": {
        "description": "用 so 連接原因和結果句子",
        "questions": [
            {
                "question": "I want to help the homeless. I prepare meals for them sometimes.",
                "hint": "使用 so 連接兩個句子，前面加逗號",
                "answer": "I want to help the homeless, so I prepare meals for them sometimes.",
                "explanation": "原因：想幫助無家可歸者 → 結果：幫他們準備食物"
            },
            {
                "question": "Chris likes helping blind people. He will sell flags next month.",
                "hint": "使用 so 連接，注意逗號位置",
                "answer": "Chris likes helping blind people, so he will sell flags next month.",
                "explanation": "原因：喜歡幫助盲人 → 結果：賣旗籌款"
            },
            {
                "question": "Karen is good at cooking. She helps her mother prepare food for the party.",
                "hint": "使用 so 連接因果關係",
                "answer": "Karen is good at cooking, so she helps her mother prepare food for the party.",
                "explanation": "原因：擅長煮餸 → 結果：幫媽媽準備食物"
            },
            {
                "question": "The dog needs a home. We adopt it from the SPCA.",
                "hint": "使用 so 連接",
                "answer": "The dog needs a home, so we adopt it from the SPCA.",
                "explanation": "原因：狗狗需要家 → 結果：從 SPCA 領養"
            }
        ]
    },
    "Grammar 2: who / which (關係代詞)": {
        "description": "用 who 指人，用 which 指物/動物",
        "questions": [
            {
                "question": "We can support a food charity. It prepares food for people in need.",
                "hint": "charity 是機構，使用 which",
                "answer": "We can support a food charity which prepares food for people in need.",
                "explanation": "charity = 物 → 用 which"
            },
            {
                "question": "We can visit sick children. They are in hospital.",
                "hint": "children 是人，使用 who",
                "answer": "We can visit sick children who are in hospital.",
                "explanation": "children = 人 → 用 who"
            },
            {
                "question": "I know a boy. He collects money for blind people.",
                "hint": "boy 是人，使用 who",
                "answer": "I know a boy who collects money for blind people.",
                "explanation": "boy = 人 → 用 who"
            },
            {
                "question": "I have a pet cat. It was adopted from the SPCA.",
                "hint": "cat 是動物，使用 which",
                "answer": "I have a pet cat which was adopted from the SPCA.",
                "explanation": "cat = 動物 → 用 which"
            }
        ]
    },
    "Connectives: so / so that / because": {
        "description": "分辨 so (結果), so that (目的), because (原因)",
        "questions": [
            {
                "question": "It was my birthday yesterday ___ we had a big meal.",
                "options": ["so", "so that", "because"],
                "answer": "so",
                "explanation": "生日是原因，吃大餐是結果 → 用 so"
            },
            {
                "question": "I will help Mum ___ she will not be so busy.",
                "options": ["so", "so that", "because"],
                "answer": "so that",
                "explanation": "目的是讓媽媽不那麼忙 → 用 so that (後有 will)"
            },
            {
                "question": "He did not play ___ he was sick.",
                "options": ["so", "so that", "because"],
                "answer": "because",
                "explanation": "生病是原因，沒有比賽是結果 → 用 because"
            }
        ]
    }
}

st.title("🔤 English Grammar Trainer")
st.markdown("### Grammar Practice + Look and Write")

# 選擇練習模式
selected_topic = st.selectbox(
    "選擇練習主題：",
    list(GRAMMAR_EXERCISES.keys())
)

if selected_topic:
    topic_data = GRAMMAR_EXERCISES[selected_topic]
    st.subheader(f"📚 {selected_topic}")
    st.info(topic_data["description"])
    
    # 顯示題目
    for i, q in enumerate(topic_data["questions"]):
        with st.expander(f"Q{i+1}: {q['question']}", expanded=False):
            st.write("**Hint:**")
            st.warning(q.get("hint", ""))
            
            if "options" in q:
                user_answer = st.radio("Your answer:", q["options"], key=f"q{i}")
                if st.button(f"Check Q{i+1}", key=f"check{i}"):
                    if user_answer == q["answer"]:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! Correct answer: {q['answer']}")
            else:
                user_answer = st.text_area("Your answer:", key=f"q{i}")
                if st.button(f"Check Q{i+1}", key=f"check{i}"):
                    if user_answer.strip().lower() == q["answer"].strip().lower():
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! Correct answer:\n{q['answer']}")
            
            st.markdown("**Explanation:**")
            st.info(q["explanation"])

st.markdown("---")
st.markdown("💡 **Tips:**\n- **Look and Write**: 睇圖寫句，每句至少5個字，用 'This is/These are/I am/I like' 等句型\n- **so** = 所以（結果），前面加逗號\n- **so that** = 以便（目的），後常有 can/will\n- **because** = 因為（原因）")
