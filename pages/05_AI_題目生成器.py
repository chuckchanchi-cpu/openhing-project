#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing AI 練習室（單一頁面 — 教材出題 + 即場作答 + AI 批改）

第一原則（Chuck）：
  1. 用 Mac mini（openedujustan）教材做 context 生成題目
  2. 學生喺同一個 page 作答
  3. AI 即時批改 + 改善建議

流程：揀教材 → 🎲 生成 5 條題目 → 逐題作答 → 🚀 提交批改 → 睇分數/評語
"""

import streamlit as st
import os
import json
import glob
import io
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🦀 Openhing AI 練習室", page_icon="🦀", layout="wide")

# 將 Streamlit Secrets 注入環境變數（每個 page 獨立執行，要自己注入！）
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k, v in st.secrets.items():
        os.environ[k] = str(v)

# ===== API 配置（env-first，兼容 OPENAI_* / SILRA_* 舊設定名）=====
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

# ===== 科目 rubric 預設（AI 冇俾 rubric 時用）=====
RUBRIC_DEFAULT = {
    "中文": "- 內容（Content）：主題相關、有細節\n- 結構（Structure）：有開頭/中間/結尾\n- 用詞（Vocabulary）：用詞豐富\n- 標點（Punctuation）：標點正確",
    "常識": "- 內容準確性（Accuracy）：答案正確、冇事實錯誤\n- 解釋清晰度（Clarity）：解釋有邏輯、有因果關係\n- 關鍵詞運用（Keywords）：有用到教材關鍵詞\n- 完整性（Completeness）：有答齊所有部分",
    "英文": "- 內容（Content）：主題相關、有細節\n- 結構（Structure）：有開頭/中間/結尾\n- 文法（Grammar）：時態正確、句子完整\n- 創意（Creativity）：用詞豐富",
    "數學": "- 步驟（Steps）：解題步驟清晰\n- 準確性（Accuracy）：計算正確\n- 解釋（Explanation）：有解釋點解用呢個方法\n- 格式（Format）：答案有寫單位",
}
RUBRIC_FALLBACK = "- 內容準確性（Accuracy）：答案正確\n- 解釋清晰度（Clarity）：解釋清楚\n- 完整性（Completeness）：有答齊\n- 創意（Creativity）：有自己嘅諗法"

# ===== 教材路徑 =====
def material_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "openedujustan")

def list_materials():
    return sorted(glob.glob(os.path.join(material_dir(), "*.md")))

def detect_subject(filename):
    """由教材檔名估科目（英文/數學/常識，其他當中文）"""
    if "英文" in filename or "English" in filename:
        return "英文"
    if "數學" in filename or "数学" in filename or "Math" in filename:
        return "數學"
    if "常識" in filename or "常识" in filename or "GS" in filename:
        return "常識"
    return "中文"

def q_text(q):
    """攞題目文字 — AI 可能用唔同 key，全部 fallback"""
    return (q.get('question') or q.get('title') or q.get('content')
            or q.get('text') or q.get('question_text') or '').strip()

# ===== AI 生成題目（根據教材）=====
def generate_questions(material_path, subject, count=5):
    api_base, api_key, model = get_api_config()
    if not api_key:
        st.error("⚠️ 未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY")
        return []
    try:
        with open(material_path, encoding="utf-8") as f:
            material_ctx = f.read()[:5000]

        system_prompt = f"""你係一位經驗豐富嘅小學六年級{subject}科老師。

**教材內容（題目必須根據呢份教材嚟出，用返教材嘅詞彙、概念同例子）：**
{material_ctx}

請根據教材生成 {count} 條練習題目，要求：
1. 題目涵蓋教材嘅唔同重點（由淺入深）
2. 每條題目要獨立、清晰，適合小六學生
3. 每條題目包含：
   - "question": 題目內容
   - "tip": 提示（引導學生思考，唔好直接俾答案）
   - "rubric": 評分準則（4 項，每項 0-10 分，用廣東話/英文視乎科目）

**輸出格式（只輸出 JSON array，唔好有其他文字）：**
[
  {{"question": "...", "tip": "...", "rubric": "..."}},
  ...
]"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"請生成 {count} 條題目"}
            ],
            "max_tokens": 3000,
            "temperature": 0.8
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        response = requests.post(f"{api_base}/chat/completions", json=payload, headers=headers, timeout=180)
        if response.status_code != 200:
            st.error(f"❌ AI 生成失敗（錯誤碼 {response.status_code}）：{response.text[:200]}")
            return []

        content = response.json()["choices"][0]["message"]["content"]
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            questions = json.loads(content)
            # 淨係留有效題目 + 補 rubric
            valid = []
            for q in questions:
                text = q_text(q)
                if text:
                    q["question"] = text
                    q["q"] = text  # 雙保險：q 同 question 都有
                    q.setdefault("rubric", RUBRIC_DEFAULT.get(subject, RUBRIC_FALLBACK))
                    q.setdefault("tip", "💡 諗下教材入面講過嘅重點")
                    valid.append(q)
            return valid
        except json.JSONDecodeError:
            st.error("❌ AI 回覆格式唔啱（唔係 JSON）— 請再試一次")
            return []
    except Exception as e:
        st.error(f"❌ 生成出錯：{str(e)}")
        return []

# ===== AI 一次過批改 5 條 =====
def grade_all(questions, answers, api_base, api_key, model):
    """一次過批改所有題目，回傳 list of result dict"""
    if not api_key:
        return None, "未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY"

    qa_block = ""
    for i, (q, a) in enumerate(zip(questions, answers)):
        qa_block += f"""【題目 {i+1}】
題目：{q['q']}
評分準則（每項 0-10 分）：
{q['rubric']}
學生答案：
\"\"\"
{a}
\"\"\"

"""

    prompt = f"""你係一個專業同友善嘅小學老師。根據每題嘅評分準則，逐題批改學生嘅答案，全部用廣東話寫評語（英文科題目可用英文）。

{qa_block}
請用以下 JSON 格式回覆（唔好加其他文字）：
{{"results": [
  {{"q_idx": 1, "scores": {{"內容準確性": 8, "解釋清晰度": 7, "關鍵詞運用": 6, "完整性": 8}}, "total": 29, "comment": "整體評語（2-3 句，鼓勵為主）", "strengths": ["優點1", "優點2"], "improvements": ["改善1", "改善2"]}},
  ...
]}}
注意：q_idx 由 1 開始，同題目編號對應。scores 嘅 key 要同該題 rubric 嘅項目對應。"""

    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "你係專業老師。直接輸出 JSON，唔好有任何其他文字。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 3000,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            },
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=180
        )
        if r.status_code != 200:
            return None, f"API Error {r.status_code}: {r.text[:200]}"
        content = r.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        data = json.loads(content)
        results = data.get("results", [])
        if not results and isinstance(data, list):
            results = data
        return results, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== Session state =====
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []
if 'current_material' not in st.session_state:
    st.session_state.current_material = None
if 'grade_results' not in st.session_state:
    st.session_state.grade_results = None

# ===== Sidebar =====
with st.sidebar:
    st.header("📖 教材")
    materials = list_materials()
    material_names = [os.path.basename(m) for m in materials]
    material_choice = st.selectbox("揀教材（Mac mini 教材庫）", material_names)
    material_path = os.path.join(material_dir(), material_choice)
    subject = detect_subject(material_choice)
    st.caption(f"📚 科目：**{subject}**")

    st.divider()

    if st.button("🎲 生成 5 條題目", type="primary", use_container_width=True):
        with st.spinner(f"🤖 根據《{material_choice}》生成緊 5 條題目..."):
            qs = generate_questions(material_path, subject, 5)
        if qs:
            st.session_state.current_questions = qs
            st.session_state.current_material = material_choice
            st.session_state.grade_results = None
            st.success(f"✅ 生成咗 {len(qs)} 條題目！")
        else:
            st.error("❌ 生成失敗，請再試")

    if st.session_state.current_questions:
        if st.button("🔄 新一輪（重新生成）", use_container_width=True):
            with st.spinner("🤖 重新生成緊..."):
                qs = generate_questions(material_path, subject, 5)
            if qs:
                st.session_state.current_questions = qs
                st.session_state.current_material = material_choice
                st.session_state.grade_results = None
                st.success("✅ 新一輪題目準備好！")
            else:
                st.error("❌ 生成失敗，請再試")

    st.divider()

    st.header("📊 老師選項")
    if st.checkbox("顯示練習紀錄"):
        if st.session_state.get("practice_log"):
            df_log = pd.DataFrame(st.session_state.practice_log)
            csv_out = io.StringIO()
            df_log.to_csv(csv_out, index=False)
            st.download_button("⬇️ 下載練習紀錄 CSV", csv_out.getvalue(), "practice_results.csv", "text/csv")
        else:
            st.info("未有練習紀錄（學生做過練習先有）")

# ===== Main =====
st.title("🦀 Openhing AI 練習室")
st.caption("📖 教材出題 → ✍️ 即場作答 → 🤖 AI 批改改善")

if not st.session_state.current_questions:
    st.info("👆 左邊揀教材，然後撳「🎲 生成 5 條題目」開始！")
    st.stop()

# 顯示而家教材
st.markdown(f"**📖 教材：** `{st.session_state.current_material}`　**📚 科目：** {subject}")
st.divider()

questions = st.session_state.current_questions
answers = {}

# 顯示題目 + 作答區
st.subheader(f"📝 練習（{len(questions)} 條題目）")
for i, q in enumerate(questions):
    st.markdown(f"### {i+1}. {q_text(q)}")
    with st.expander("💡 提示（撳開睇）"):
        st.markdown(q.get("tip", ""))
    answers[i] = st.text_area(
        f"✍️ 第 {i+1} 題作答",
        key=f"ans_{i}",
        height=110,
        placeholder="寫低你嘅答案⋯",
        label_visibility="collapsed"
    )
    st.divider()

# 提交批改
col_btn, col_status = st.columns([1, 3])
with col_btn:
    submitted = st.button("🚀 提交批改", type="primary", use_container_width=True, disabled=not any(answers.values()))
with col_status:
    if not any(answers.values()):
        st.caption("答至少一題先可以提交")

if submitted:
    api_base, api_key, model = get_api_config()
    q_list = [{"q": q["q"], "rubric": q.get("rubric", RUBRIC_FALLBACK)} for q in questions]
    a_list = [answers[i].strip() for i in range(len(questions))]
    with st.spinner("🤖 AI 老師批改緊（約 10-20 秒）..."):
        results, err = grade_all(q_list, a_list, api_base, api_key, model)
    if err:
        st.error(err)
    else:
        st.session_state.grade_results = results
        st.rerun()

# 顯示批改結果
if st.session_state.grade_results:
    results = st.session_state.grade_results
    st.markdown("---")
    st.subheader("📊 批改結果")

    grand_total = 0
    grand_max = 0
    for r in results:
        idx = r.get("q_idx", 0) - 1
        if idx < 0 or idx >= len(questions):
            continue
        scores = r.get("scores", {})
        total = r.get("total", sum(scores.values()) if scores else 0)
        grand_total += total
        grand_max += len(scores) * 10 if scores else 40

        with st.expander(f"### 第 {idx+1} 題：{total} 分", expanded=True):
            cols = st.columns(len(scores) if scores else 1)
            for col, (k, v) in zip(cols, scores.items()):
                col.metric(k, f"{v}/10")
            st.markdown(f"**💬 評語：** {r.get('comment', '')}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ 做得好**")
                for s in r.get("strengths", []):
                    st.markdown(f"- {s}")
            with c2:
                st.markdown("**🔧 下次改善**")
                for s in r.get("improvements", []):
                    st.markdown(f"- {s}")

    st.markdown("---")
    st.success(f"🏆 總分：**{grand_total} / {grand_max}**")
    st.info("💡 想再試？改答案再撳「🚀 提交批改」，或者撳「🔄 新一輪」做新題目！")

    # 記錄練習
    if "practice_log" not in st.session_state:
        st.session_state.practice_log = []
    log_entry = {
        "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "教材": st.session_state.current_material,
        "總分": grand_total,
        "滿分": grand_max,
    }
    for i, q in enumerate(questions):
        log_entry[f"題{i+1}"] = q["q"][:30]
        log_entry[f"答{i+1}"] = answers.get(i, "")[:50]
    for r in results:
        idx = r.get("q_idx", 0) - 1
        if 0 <= idx < len(questions):
            log_entry[f"分{idx+1}"] = r.get("total", "")
    st.session_state.practice_log.append(log_entry)

    # 下載題目（老師保存）
    with st.expander("💾 保存呢一輪題目"):
        payload = json.dumps({
            "subject": f"🆕 {subject}（AI 生成）",
            "source": f"{st.session_state.current_material} — {datetime.now().strftime('%Y-%m-%d')}",
            "questions": [{"q": q["q"], "hint": q.get("tip", ""), "rubric": q.get("rubric", "")} for q in questions]
        }, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ 下載題目 JSON",
            payload,
            f"questions_{subject}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            "application/json"
        )
        st.caption("下載後 send 俾 Openclaw，佢會 commit 入題目庫做永久保存")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | AI 練習室</div>", unsafe_allow_html=True)
