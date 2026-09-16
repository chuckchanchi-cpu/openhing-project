#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏋️ AI 練習平台（學生直接用）
學生：揀練習 → 睇題目 → 打字作答 → AI 即時批改（分數 + 評語 + 改善建議）
老師：可以下載全班結果 CSV
"""

import streamlit as st
import os
import json
import glob
import time
import requests
import pandas as pd
import io
from pathlib import Path

st.set_page_config(page_title="🏋️ AI 練習平台", page_icon="🏋️", layout="wide")

# 將 Streamlit Secrets 注入環境變數（multipage 每個 page 獨立執行，要各自注入！）
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k, v in st.secrets.items():
        os.environ[k] = str(v)

# ===== API 配置 =====
def get_api_config():
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "deepseek-chat")
    if not base:
        silra_url = os.environ.get("SILRA_API_URL", "")
        if silra_url:
            base = silra_url.replace("/chat/completions", "").rstrip("/")
    if not base:
        base = "https://api.deepseek.com"
    return base, key, model

# ===== 題目庫（讀 resources/questions/*.json + openedujustan folder + 內置 fallback）=====
def load_question_bank():
    """讀 repo 入面 resources/questions/ 嘅題目 JSON + openedujustan 文件夾，合併內置題目"""
    bank = {}
    # 內置題目（fallback）
    for k, v in QUESTION_BANK.items():
        bank[k] = [dict(q, **{"rubric": q.get("rubric", "")}) for q in v]
    
    # 讀 repo 入面 resources/questions/ 嘅題目檔案
    qdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "questions")
    if os.path.isdir(qdir):
        for fpath in sorted(glob.glob(os.path.join(qdir, "*.json"))):
            try:
                with open(fpath, encoding="utf-8") as f:
                    data = json.load(f)
                subject = data.get("subject", os.path.basename(fpath))
                source = data.get("source", "")
                qs = data.get("questions", [])
                for q in qs:
                    q["source"] = source
                if subject in bank:
                    bank[subject] = bank[subject] + qs
                else:
                    bank[subject] = qs
            except Exception as e:
                st.warning(f"讀題目檔案出錯 {fpath}: {e}")
    
    # 讀 Mac mini openedujustan folder (.md 練習文件)
    edu_folder = Path.home() / "Desktop" / "openedujustan"
    if edu_folder.exists():
        subject_dirs = {
            "Chinese": "📕 中文科",
            "General_Studies": "🌍 常識科",
            "English": "🔤 英文科",
            "Maths": "🔢 數學科",
        }
        for dir_name, display_name in subject_dirs.items():
            dir_path = edu_folder / dir_name
            if dir_path.exists():
                practice_dir = dir_path / "practice"
                if not practice_dir.exists():
                    practice_dir = dir_path
                for md_file in sorted(practice_dir.rglob("*.md")):
                    try:
                        with open(md_file, encoding="utf-8") as f:
                            content = f.read()
                        # Extract title (first line starting with #)
                        title = ""
                        lines = content.split("\n")
                        for line in lines:
                            if line.startswith("# ") and not title:
                                title = line[2:].strip()
                                break
                        if title:
                            # Use first 300 chars of content as the question
                            question_text = "\n".join(lines[:20]).strip()
                            if display_name not in bank:
                                bank[display_name] = []
                            bank[display_name].append({
                                "q": f"[{title}] {question_text[:200]}",
                                "hint": f"💡 提示：完整題目來自 {md_file.name}，請仔細閱讀並作答。",
                                "rubric": """- 內容準確性（Accuracy）：答案正確、冇事實錯誤
- 解釋清晰度（Clarity）：解釋有邏輯
- 關鍵詞運用（Keywords）：有用到教材關鍵詞
- 完整性（Completeness）：有答齊所有部分""",
                                "source": str(md_file),
                                "full_content": content,
                            })
                    except Exception as e:
                        pass  # Silently skip unreadable files
    
    return bank

QUESTION_BANK = {
    "🌍 常識科": [
        {
            "q": "點解我哋要節約用水？",
            "hint": "試下諗：水從邊度嚟？世界上嘅水夠唔夠？我哋可以點做？",
            "rubric": """- 內容準確性（Accuracy）：答案正確、冇事實錯誤
- 解釋清晰度（Clarity）：解釋有邏輯、有因果關係
- 關鍵詞運用（Keywords）：有用到「水資源」「短缺」「循環再用」等概念
- 完整性（Completeness）：有答齊原因 + 至少一個實際做法""",
        },
        {
            "q": "如果我哋冇咗樹木，世界會變成點？",
            "hint": "試下諗：樹木有咩作用？（空氣、動物、泥土、天氣）",
            "rubric": """- 內容準確性（Accuracy）：答案正確、冇事實錯誤
- 解釋清晰度（Clarity）：解釋有邏輯、有因果關係
- 關鍵詞運用（Keywords）：有用到「氧氣」「溫室效應」「水土流失」等概念
- 完整性（Completeness）：有提到至少 3 個樹木嘅作用""",
        },
        {
            "q": "點解我哋要做運動？",
            "hint": "試下諗：運動對身體有咩好處？（心臟、肌肉、情緒）",
            "rubric": """- 內容準確性（Accuracy）：答案正確、冇事實錯誤
- 解釋清晰度（Clarity）：解釋有邏輯
- 關鍵詞運用（Keywords）：有用到「健康」「血液循環」「強身健體」等概念
- 完整性（Completeness）：有提到至少 2 個好處 + 1 個例子""",
        },
    ],
    "📕 英文作文": [
        {
            "q": "Write about your favourite place. (50-80 words)",
            "hint": "Where is it? What can you see/hear there? Why do you like it? Use at least 3 adjectives.",
            "rubric": """- 內容（Content）：主題相關、有細節
- 結構（Structure）：有開頭/中間/結尾
- 文法（Grammar）：時態正確、句子完整
- 創意（Creativity）：用詞豐富""",
        },
        {
            "q": "Write about a memorable day. (50-80 words)",
            "hint": "When was it? What happened? How did you feel? Use past tense!",
            "rubric": """- 內容（Content）：主題相關、有細節
- 結構（Structure）：有開頭/中間/結尾
- 文法（Grammar）：過去式正確
- 創意（Creativity）：用詞豐富""",
        },
    ],
    "🔢 數學解題": [
        {
            "q": "小明有 12 粒糖，佢分俾 3 個朋友，每人拎到幾多粒？請解釋你點計。",
            "hint": "用除法。寫低你嘅步驟同答案。",
            "rubric": """- 步驟（Steps）：解題步驟清晰
- 準確性（Accuracy）：計算正確
- 解釋（Explanation）：有解釋點解用除法
- 格式（Format）：答案有寫單位「粒」""",
        },
    ],
}

# ===== 合併 resources/questions/ 嘅題目 JSON（openedujustan 教材）=====
QUESTION_BANK = load_question_bank()

# ===== 合併老師用生成器「採用」嘅題目（session 內）=====
if "pending_questions" in st.session_state and st.session_state.pending_questions:
    pending = [q for q in st.session_state.pending_questions if q.get("q")]
    if pending:
        QUESTION_BANK.setdefault("🆕 老師新生成", [])
        existing_q = {q.get("q") for q in QUESTION_BANK["🆕 老師新生成"]}
        for q in pending:
            if q.get("q") not in existing_q:
                QUESTION_BANK["🆕 老師新生成"].append(q)

# ===== AI 批改核心 =====
def grade_answer(question, answer, rubric, api_base, api_key, model):
    if not api_key:
        return None, "未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY"
    prompt = f"""你係一個專業同友善嘅老師。根據評分準則，批改學生嘅答案，用廣東話寫評語。

題目：
{question}

評分準則（每項 0-10 分）：
{rubric}

學生答案：
\"\"\"
{answer}
\"\"\"

請用以下 JSON 格式回覆（唔好加其他文字）：
{{"scores": {{"內容準確性": 8, "解釋清晰度": 7, "關鍵詞運用": 6, "完整性": 8}}, "total": 29, "comment": "整體評語（廣東話，2-3 句，鼓勵為主）", "strengths": ["優點1", "優點2"], "improvements": ["改善1", "改善2"]}}
"""
    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "你係專業老師。直接輸出 JSON，唔好有任何其他文字。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            },
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=120
        )
        if r.status_code != 200:
            return None, f"API Error {r.status_code}: {r.text[:200]}"
        content = r.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(content), None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== UI =====
st.title("🏋️ AI 練習平台")
st.caption("揀練習 → 作答 → AI 即時批改！答完即刻知道點改善 💪")

api_base, api_key, model = get_api_config()

# Sidebar
with st.sidebar:
    st.header("⚙️ 設定")
    st.info(f"API: `{api_base}`\n\nModel: `{model}`")
    if not api_key:
        st.warning("⚠️ 未偵測到 API key")

    st.header("👤 學生資料")
    student_name = st.text_input("你叫咩名？", key="sname")

    st.header("📊 老師選項")
    pending_count = len(st.session_state.get("pending_questions", []))
    if pending_count > 0:
        st.success(f"🆕 老師新生成：{pending_count} 條題目已加入（喺「揀題目」度揀「🆕 老師新生成」）")
    if st.checkbox("顯示老師工具"):
        if st.session_state.get("practice_log"):
            df_log = pd.DataFrame(st.session_state.practice_log)
            csv_out = io.StringIO()
            df_log.to_csv(csv_out, index=False)
            st.download_button("⬇️ 下載全班結果 CSV", csv_out.getvalue(), "practice_results.csv", "text/csv")

# 揀科目 + 題目
subject = st.selectbox("📚 揀科目", list(QUESTION_BANK.keys()))
questions = QUESTION_BANK[subject]
q_idx = st.radio("📝 揀題目", range(len(questions)), format_func=lambda i: questions[i]["q"][:40] + "...")

question = questions[q_idx]
st.divider()

# 題目顯示
st.subheader(f"❓ {question['q']}")
with st.expander("💡 提示（撳開睇）"):
    st.markdown(question["hint"])

# 作答
answer = st.text_area("✍️ 喺度打字作答：", height=180, placeholder="寫低你嘅答案⋯")

if st.button("🚀 提交批改", type="primary", disabled=not answer.strip()):
    if not student_name.strip():
        st.warning("請先喺側邊欄輸入你嘅名")
    else:
        with st.spinner("🤖 AI 老師批改緊..."):
            result, err = grade_answer(question["q"], answer.strip(), question["rubric"], api_base, api_key, model)
        if result:
            scores = result.get("scores", {})
            total = result.get("total", sum(scores.values()))
            
            st.success(f"✅ 批改完成！總分：{total}/40")
            
            # 分數卡
            cols = st.columns(len(scores) if scores else 1)
            for col, (k, v) in zip(cols, scores.items()):
                col.metric(k, f"{v}/10")
            
            # 評語
            st.markdown(f"### 💬 老師評語")
            st.markdown(f"> {result.get('comment', '')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### ✅ 做得好")
                for s in result.get("strengths", []):
                    st.markdown(f"- {s}")
            with col2:
                st.markdown("### 🔧 下次改善")
                for s in result.get("improvements", []):
                    st.markdown(f"- {s}")
            
            # 記錄
            if "practice_log" not in st.session_state:
                st.session_state.practice_log = []
            st.session_state.practice_log.append({
                "學生": student_name, "科目": subject, "題目": question["q"],
                "答案": answer.strip(), "總分": total, "評語": result.get("comment", "")
            })
            
            st.info("💡 想再試多次？改完答案再撳「提交批改」就得！")
        else:
            st.error(err)

st.divider()
st.caption("💪 練習多啲，進步快啲！AI 老師 24 小時喺度")
