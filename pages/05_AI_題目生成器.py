#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ AI 題目生成器（老師用）
流程：揀教材 → AI 生成 N 條開放式題目 → 老師 review → 重新生成 / 採用 → 練習平台
"""

import streamlit as st
import os
import json
import glob
import time
import requests

st.set_page_config(page_title="🛠️ AI 題目生成器", page_icon="🛠️", layout="wide")

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

# ===== 教材掃描 =====
TEXTBOOK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "openedujustan")

# 練習平台 page 實際路徑（檔名有 emoji，用 glob 攞真實名避免編碼 mismatch）
# 注意：switch_page/page_link 要「相對 main script」嘅路徑，唔可以用絕對路徑
PRACTICE_PAGE = None
for _f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "04*.py")):
    PRACTICE_PAGE = "pages/" + os.path.basename(_f)
    break

def list_textbooks():
    """掃描 resources/openedujustan/ 入面嘅 MD 教材"""
    files = []
    if os.path.isdir(TEXTBOOK_DIR):
        for f in sorted(glob.glob(os.path.join(TEXTBOOK_DIR, "*.md"))):
            if os.path.basename(f) == "README.md":
                continue
            files.append(os.path.basename(f))
    return files

def read_textbook(name, max_chars=8000):
    """讀教材內容（截斷避免 token 爆）"""
    path = os.path.join(TEXTBOOK_DIR, name)
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return content[:max_chars]
    except Exception as e:
        return f"讀取錯誤: {e}"

# ===== AI 生成題目 =====
def generate_questions(textbook_name, content, count, exclude, api_base, api_key, model):
    if not api_key:
        return None, "未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY"

    exclude_text = ""
    if exclude:
        prev = "\n".join(f"- {q.get('q', '')}" for q in exclude[-10:])
        exclude_text = f"\n\n⚠️ 以下題目已經生成過，唔好重複（可以相似但唔好一樣）：\n{prev}"

    prompt = f"""你係小學課程專家。根據以下教材內容，生成 {count} 條開放式問題（唔係選擇題），適合小學生練習。

要求：
1. 每條題目要基於教材嘅知識點，需要學生用文字解釋（唔係背誦）
2. 每條題目附 hint（提示，幫學生諗方向，用廣東話）
3. 每條題目附 rubric（評分準則，4 項，每項 0-10 分）
4. 每條題目附參考答案（老師用，簡短）
5. 題目多元化：有「點解」「比較」「舉例」「應用」「判斷」等唔同類型
{exclude_text}

教材內容：
\"\"\"
{content}
\"\"\"

請用以下 JSON 格式回覆（唔好加任何其他文字）：
{{"questions": [{{"q": "題目", "hint": "提示", "rubric": "- 內容準確性（Accuracy）：...\n- 解釋清晰度（Clarity）：...\n- 關鍵詞運用（Keywords）：...\n- 完整性（Completeness）：...", "answer": "參考答案"}}]}}"""
    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "你係小學課程專家。直接輸出 JSON，唔好有任何其他文字。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 3000,
                "temperature": 0.8,
                "response_format": {"type": "json_object"}
            },
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=180
        )
        if r.status_code != 200:
            return None, f"API Error {r.status_code}: {r.text[:200]}"
        content_out = r.json()["choices"][0]["message"]["content"].strip()
        if content_out.startswith("```"):
            content_out = content_out.split("\n", 1)[1].rsplit("```", 1)[0]
        data = json.loads(content_out)
        qs = data.get("questions", [])
        for q in qs:
            q["source"] = f"AI 生成（{textbook_name}）"
        return qs, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== UI =====
st.title("🛠️ AI 題目生成器")
st.caption("揀教材 → 生成 5 條新題目 → 老師 review → 採用 → 練習平台即刻用到")

api_base, api_key, model = get_api_config()

with st.sidebar:
    st.header("⚙️ 設定")
    st.info(f"API: `{api_base}`\n\nModel: `{model}`")
    if not api_key:
        st.warning("⚠️ 未偵測到 API key")

# 揀教材
textbooks = list_textbooks()
if not textbooks:
    st.warning("⚠️ 搵唔到教材 — 請確認 resources/openedujustan/ 有 MD 檔案")
    st.stop()

st.subheader("📚 1. 揀教材")
col1, col2 = st.columns([3, 1])
with col1:
    tb_name = st.selectbox("教材", textbooks)
with col2:
    q_count = st.number_input("題目數量", min_value=3, max_value=10, value=5, step=1)

# 預覽教材
with st.expander(f"📖 預覽教材內容（{tb_name}）"):
    preview = read_textbook(tb_name, 3000)
    st.markdown(preview)

# 生成
st.subheader("🎲 2. 生成題目")
if "gen_questions" not in st.session_state:
    st.session_state.gen_questions = None
if "gen_error" not in st.session_state:
    st.session_state.gen_error = None
if "gen_count" not in st.session_state:
    st.session_state.gen_count = 0

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("🎲 生成題目", type="primary", use_container_width=True):
        content = read_textbook(tb_name)
        with st.spinner("🤖 AI 出題中（約 30 秒）..."):
            qs, err = generate_questions(tb_name, content, int(q_count), [], api_base, api_key, model)
        if qs:
            st.session_state.gen_questions = qs
            st.session_state.gen_error = None
            st.session_state.gen_count = 1
        else:
            st.session_state.gen_questions = None
            st.session_state.gen_error = err
with c2:
    regen_disabled = st.session_state.gen_questions is None
    if st.button("🔄 重新生成", use_container_width=True, disabled=regen_disabled):
        content = read_textbook(tb_name)
        with st.spinner("🤖 再出過一批（避免重複）..."):
            qs, err = generate_questions(tb_name, content, int(q_count), st.session_state.gen_questions, api_base, api_key, model)
        if qs:
            st.session_state.gen_questions = qs
            st.session_state.gen_error = None
            st.session_state.gen_count += 1
        else:
            st.session_state.gen_error = err

if st.session_state.gen_error:
    st.error(st.session_state.gen_error)

# 顯示生成結果
if st.session_state.gen_questions:
    qs = st.session_state.gen_questions
    st.success(f"✅ 第 {st.session_state.gen_count} 批：生成咗 {len(qs)} 條題目 — 請老師 review")

    # 逐條顯示
    for i, q in enumerate(qs, 1):
        with st.expander(f"Q{i}: {q.get('q', '')}", expanded=(i <= 2)):
            st.markdown(f"**💡 提示：** {q.get('hint', '')}")
            st.markdown(f"**📋 評分準則：**")
            st.markdown(q.get("rubric", ""))
            st.markdown(f"**📝 參考答案：** {q.get('answer', '')}")

    # 採用 / 下載
    st.subheader("✅ 3. 採用題目")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ 採用呢批題目（送去練習平台）", type="primary", use_container_width=True):
            if "pending_questions" not in st.session_state:
                st.session_state.pending_questions = []
            existing = {q.get("q") for q in st.session_state.pending_questions}
            added = 0
            for q in qs:
                if q.get("q") not in existing:
                    st.session_state.pending_questions.append(q)
                    existing.add(q.get("q"))
                    added += 1
            if added > 0:
                st.success(f"✅ 已採用 {added} 條新題目！")
                st.session_state.pending_added = added
                time.sleep(1.5)
                if PRACTICE_PAGE:
                    st.switch_page(PRACTICE_PAGE)
            else:
                st.info("呢批題目之前已經採用過，冇重複加入")

    # 採用後引導（同一 tab 先見到）
    if st.session_state.get("pending_added", 0) > 0:
        st.markdown("""
<div style="background:#e8f5e9;border:2px solid #4caf50;border-radius:12px;padding:16px;margin:8px 0;text-align:center">
<b style="font-size:1.1em">🆕 已採用 {} 條題目！</b><br>
<span style="color:#555">⚠️ 要用<b>同一個 tab</b> 去練習平台先見到（開新 tab 會係新 session）</span>
</div>
""".format(st.session_state.pending_added), unsafe_allow_html=True)
        st.page_link(PRACTICE_PAGE, label="👉 撳呢度去練習平台（同一個 tab）", icon="🏋️")
    with c2:
        # 下載 JSON（俾 Openclaw commit 入題目庫）
        payload = json.dumps({"subject": "🆕 老師新生成", "source": f"AI 生成（{tb_name}）", "questions": qs}, ensure_ascii=False, indent=2)
        st.download_button("⬇️ 下載題目 JSON", payload, f"generated_{tb_name.replace('.md','')}.json", "application/json", use_container_width=True)

    st.info("💡 **提示：** 採用咗嘅題目會喺「🏋️ AI 練習」→「🆕 老師新生成」出現（今次 session 有效）。想永久保存？下載 JSON 俾 Openclaw commit 入 `resources/questions/` 就得。")
