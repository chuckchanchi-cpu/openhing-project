import streamlit as st
import json
import os

st.set_page_config(page_title="📝 中文成語練習", page_icon="📝", layout="wide")

# 成語數據（從本地文件加載）
CHENG_YU_DATA = [
    {"idiom": "曇花一現", "pinyin": "tán huā yī xiàn", "meaning": "比喻美好事物短暫出現就消失", "example": "這朵曇花只開了三小時就凋謝了，真是曇花一現。"},
    {"idiom": "車水馬龍", "pinyin": "chē shuǐ mǎ lóng", "meaning": "形容車輛很多，來往不斷", "example": "節日的維多利亞公園車水馬龍，非常熱鬧。"},
    {"idiom": "魚貫而入", "pinyin": "yú guàn ér rù", "meaning": "像魚一樣一個接一個地進入", "example": "觀眾魚貫而入，找座位坐下。"},
    {"idiom": "日新月異", "pinyin": "rì xīn yuè yì", "meaning": "每天每月都有新變化，形容發展迅速", "example": "科技日新月異，我們要不断学习才能跟得上。"},
    {"idiom": "消聲匿跡", "pinyin": "xiāo shēng nì jì", "meaning": "隱蔽起來，不露痕跡", "example": "那個人做完壞事後就消聲匿跡了。"},
    {"idiom": "別樹一幟", "pinyin": "bié shù yī zhì", "meaning": "獨創一格，與眾不同", "example": "他的畫作別樹一幟，令人耳目一新。"},
    {"idiom": "雨後春筍", "pinyin": "yǔ hòu chūn sǔn", "meaning": "比喻新生事物大量湧現", "example": "政策放寬後，小型企業如雨後春筍般涌現。"},
    {"idiom": "碩果僅存", "pinyin": "shuò guǒ jǐn cún", "meaning": "大而豐厚的成果只剩很少", "example": "經過戰爭，這座古城的歷史建築碩果僅存。"},
    {"idiom": "奇貨可居", "pinyin": "qí huò kě jū", "meaning": "把珍貴的東西囤積起來，等待高價出售", "example": "他收藏了許多稀有古董，以為奇貨可居。"},
    {"idiom": "搖搖欲墜", "pinyin": "yáo yáo yù zhuì", "meaning": "形勢危險，快要倒塌或垮台", "example": "這座老房子年久失修，搖搖欲墜。"},
    {"idiom": "門可羅雀", "pinyin": "mén kě luó què", "meaning": "門前可以張網捕雀，形容十分冷落", "example": "店鋪倒閉後，門可羅雀，無人光顧。"},
    {"idiom": "座無虛席", "pinyin": "zuò wú xū xí", "meaning": "座位都坐滿了，形容參加的人很多", "example": "音樂會場內座無虛席，氣氛熱烈。"},
    {"idiom": "捉襟見肘", "pinyin": "zhuō jīn jiàn zhǒu", "meaning": "形容貧困或處境困難，應付不過來", "example": "他收入微薄，捉襟見肘，難以養家餬口。"},
    {"idiom": "大煞風景", "pinyin": "dà shā fēng jǐng", "meaning": "破壞美好的景色或氣氛", "example": "在安靜的圖書館裡大聲說話，實在大煞風景。"}
]

st.title("📝 中文成語練習")
st.markdown("### 單元一：14個核心成語")

# 選擇練習模式
mode = st.radio("選擇練習模式：", ["學習成語", "填充練習", "造句練習"])

if mode == "學習成語":
    st.subheader("📚 成語詞典")
    for i, cy in enumerate(CHENG_YU_DATA):
        with st.expander(f"{i+1}. {cy['idiom']} ({cy['pinyin']})"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("**意思：**")
                st.write(cy['meaning'])
            with col2:
                st.write("**例句：**")
                st.write(cy['example'])

elif mode == "填充練習":
    st.subheader("✏️ 填充練習")
    questions = [
        ("這座古寺歷經百年風霜，如今已________，只剩下幾根殘柱。", "碩果僅存"),
        ("節假日的尖沙咀________，遊客絡繹不絕。", "車水馬龍"),
        ("演出開始後，觀眾________，場面秩序井然。", "魚貫而入"),
        ("人工智能技術________，每年都有重大突破。", "日新月異"),
        ("犯罪份子作案後立即________，警方苦無線索。", "消聲匿跡"),
        ("這位年輕設計師的作品________，在展覽中格外搶眼。", "別樹一幟"),
        ("經濟復甦後，創新企業如________般大量出現。", "雨後春筍"),
        ("他的收藏品價值連城，一向自恃________，不肯輕易出手。", "奇貨可居"),
        ("這座危樓年久失修，隨時可能倒塌，真是________。", "搖搖欲墜"),
        ("該區人口稀疏，商店寥寥無幾，幾乎是________。", "門可羅雀"),
        ("演唱會現場________，歌迷熱情高涨。", "座無虛席"),
        ("他家境貧寒，每月收入只夠糊口，常常________。", "捉襟見肘"),
        ("在莊嚴的紀念儀式上，有人嬉笑打鬧，實在是________。", "大煞風景"),
        ("這朵昙花开放时间極短，只是________，令人惋惜。", "曇花一現")
    ]
    
    score = 0
    for i, (question, answer) in enumerate(questions):
        st.write(f"**Q{i+1}.** {question}")
        user_answer = st.text_input(f"Q{i+1} 答案", key=f"q{i}")
        if st.button(f"檢查 Q{i+1}", key=f"check{i}"):
            if user_answer.strip() == answer:
                st.success("✅ 正確！")
                score += 1
            else:
                st.error(f"❌ 錯誤！正確答案是：{answer}")
    
    st.write(f"\n**總分：{score}/{len(questions)}**")

elif mode == "造句練習":
    st.subheader("✍️ 造句練習")
    st.write("請用以下成語各造一個句子：")
    
    selected_idioms = st.multiselect("選擇要練習的成語：", [cy['idiom'] for cy in CHENG_YU_DATA])
    
    if selected_idioms:
        for idiom in selected_idioms:
            st.write(f"**{idiom}**")
            sentence = st.text_area(f"用「{idiom」造句", key=f"sentence_{idiom}")
            if st.button(f"提交 {idiom} 造句", key=f"submit_{idiom}"):
                if len(sentence) > 10:
                    st.success("✅ 句子已提交！")
                else:
                    st.warning("⚠️ 句子太短，請再詳細一點。")

st.markdown("---")
st.markdown("💡 **提示：** 每日練習10-15分鐘，堅持一個月效果顯著！")
