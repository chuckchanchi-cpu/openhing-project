import streamlit as st

st.set_page_config(page_title="🏋️ AI 練習", page_icon="🏋️", layout="wide")

st.title("🏋️ AI 練習平台")
st.markdown("⚠️ 此頁面正在遷移至 [openedujustan](https://github.com/chuckchanchi-cpu/openedujustan) 項目")
st.markdown("---")
st.info("👉 請前往獨立部署嘅 OpenEduJustan 練習平台使用完整功能")

if st.button("🚀 前往獨立練習平台"):
    st.switch_page("pages/05_🛠️_AI_題目生成器.py")
