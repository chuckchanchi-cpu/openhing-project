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

請根據教材生成 {count} 條練習題目。**呢個係「每日溫習」**：目的係吸引學生回顧學校今日所學，題目要親切、有鼓勵性，**唔好出太深太偏嘅嘢嚇怕學生，亦唔好教教材以外嘅新知識**。

**🔒 鐵律（最重要，必須跟足）：**
1. **只准用教材內容出題** — 題目所需嘅知識、詞彙、概念、例子，必須全部喺上面教材內容入面出現過
2. **嚴禁教材以外嘅知識** — 唔可以用互聯網/課外常識/教科書以外嘅事實出題
3. **難度升級只可以「基於教材延伸」** — 想加深難度時，只可以喺教材內容基礎上：換數字、換情境、換角度、反問、綜合比較教材入面嘅概念；**絕對唔可以引入教材冇嘅新知識**
4. **出完題自檢** — 生成完之後逐題檢查：如果某一題需要教材內容以外嘅知識先答到 → 必須改寫嗰題，直至「淨係睇教材就答到」

**題型要求（{count} 條題目必須混合題型，至少包含：1 條 MC、1 條 T/F、1 條 short、1 條 long）：**
- "MC"：選擇題 — 4 個選項，只有 1 個正確；錯嘅選項要係學生常見錯誤（好似真測驗咁）
- "T/F"：判斷題 — 答案明確係「對」或「錯」
- "short"：短答題 — 一個詞、一個數字或一句句子
- "long"：長答題 — 要解釋原因/寫步驟/發表看法（2-3 句以上）

**難度階梯（必須跟足，第 1 題最簡單）：**
- 第 1 題（⭐）：最簡單 — MC 選擇題，直接從教材搵到答案（記憶/辨認）
- 第 2 題（⭐⭐）：簡單 — T/F 判斷題，基礎理解
- 第 3 題（⭐⭐⭐）：中等 — 短答題，簡單應用（一步計算/填充/改寫）
- 第 4 題（⭐⭐⭐⭐）：較難 — MC 或短答，多步驟/比較/分析
- 第 5 題（⭐⭐⭐⭐⭐）：最難 — 長答題，要解釋原因/綜合教材概念

**同學名字（題目要自然融入，令學生覺得親切熟悉）：**
- 中文科/數學科/常識科用：皓一、仲庭、仲希、少軍、心謐、信一、依純
- 英文科用：Hugo、Jay、Ethan
- 例如：「皓一有 28.4 元，佢想買每枝 7.8 元嘅雪條，佢最多可以買幾多枝？」

**每條題目包含：**
- "question": 題目內容
- "type": "MC" / "T/F" / "short" / "long"
- "options": 只有 MC 先有（4 個選項 array）
- "answer": 正確答案（MC 寫正確選項嘅內容；T/F 寫「對」或「錯」；short/long 寫參考答案要點）
- "difficulty": 難度級數（"⭐"/"⭐⭐"/"⭐⭐⭐"/"⭐⭐⭐⭐"/"⭐⭐⭐⭐⭐"）
- "tip": 提示（引導學生思考，唔好直接俾答案）
- "rubric": 評分準則（4 項，每項 0-10 分，用廣東話/英文視乎科目）

**輸出格式（只輸出 JSON array，唔好有其他文字）：**
[
  {{"question": "...", "type": "MC", "options": ["...", "...", "...", "..."], "answer": "...", "difficulty": "⭐", "tip": "...", "rubric": "..."}},
  ...
]"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"請根據教材生成 {count} 條每日溫習題目：混合題型（MC/判斷/短答/長答）、由淺入深、自然融入同學名、全部用教材內容！"}
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
                    q.setdefault("difficulty", "")
                    q.setdefault("type", "short")
                    q.setdefault("options", [])
                    q.setdefault("answer", "")
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
題型：{q.get('type', 'short')}
題目：{q['q']}
正確答案（選擇/判斷題適用）：{q.get('answer', '冇提供')}
評分準則（每項 0-10 分）：
{q['rubric']}
學生答案：
\"\"\"
{a}
\"\"\"

"""

    prompt = f"""你係一個專業同友善嘅小學老師。根據每題嘅評分準則，逐題批改學生嘅答案，全部用廣東話寫評語（英文科題目可用英文）。
選擇題/判斷題：直接對「正確答案」判斷對錯（揀啱就滿分，揀錯就 0 分）；短答/長答：按評分準則評分。評語要鼓勵為主，唔好嚇怕學生。

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
st.subheader(f"📝 每日溫習（{len(questions)} 條題目）")
st.caption("🎯 混合題型 + 由淺入深：第 1 題最簡單，越後越有挑戰性 — 加油！")
TYPE_BADGE = {"MC": "🔘 選擇題", "T/F": "⚖️ 判斷題", "short": "✏️ 短答", "long": "📝 長答"}
for i, q in enumerate(questions):
    diff = q.get("difficulty", "")
    qtype = q.get("type", "short")
    badge = TYPE_BADGE.get(qtype, "")
    st.markdown(f"### {i+1}. {q_text(q)}　{diff}　{badge}")
    with st.expander("💡 提示（撳開睇）"):
        st.markdown(q.get("tip", ""))
    if qtype == "MC":
        options = q.get("options") or []
        if options:
            answers[i] = st.radio(f"第 {i+1} 題作答（揀一個答案）", options, key=f"ans_{i}")
        else:
            answers[i] = st.text_input(f"✍️ 第 {i+1} 題作答", key=f"ans_{i}", label_visibility="collapsed")
    elif qtype == "T/F":
        answers[i] = st.radio(f"第 {i+1} 題作答（對 / 錯）", ["對", "錯"], key=f"ans_{i}")
    elif qtype == "short":
        answers[i] = st.text_input(f"✍️ 第 {i+1} 題作答（短答）", key=f"ans_{i}", placeholder="寫低你嘅答案⋯", label_visibility="collapsed")
    else:
        answers[i] = st.text_area(f"✍️ 第 {i+1} 題作答（長答）", key=f"ans_{i}", height=110, placeholder="寫低你嘅答案⋯", label_visibility="collapsed")
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
    q_list = [{"q": q["q"], "type": q.get("type", "short"), "answer": q.get("answer", ""), "options": q.get("options", []), "rubric": q.get("rubric", RUBRIC_FALLBACK)} for q in questions]
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
