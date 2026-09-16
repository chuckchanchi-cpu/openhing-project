#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 AI 作文批改助手（Openhing 子頁面）
功能：上傳 Google Forms 段落題回應（CSV）→ AI 自動批改（內容/結構/文法/創意）→ 輸出分數 + 評語
用法：Google Forms → 回應 → 連結試算表 → 檔案 → 下載 CSV
"""

import streamlit as st
import os
import json
import time
import traceback
import requests
import pandas as pd
import io

st.set_page_config(page_title="📝 AI 作文批改", page_icon="📝", layout="wide")

# 將 Streamlit Secrets 注入環境變數（multipage 每個 page 獨立執行，要各自注入！）
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k, v in st.secrets.items():
        os.environ[k] = str(v)

st.title("📝 AI 作文批改助手")
st.caption("AI 做初批（快），你做最終把關（準）— 跟 Openhing「AI 增強人類」理念")

# ===== API 配置（env-first，Streamlit Secrets 自動注入）=====
def get_api_config():
    """從環境變數/Secrets 攞 API 設定，支援多種 provider + 兼容舊設定名"""
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "deepseek-chat")
    # 兼容 SILRA_API_URL 格式（https://api.silra.cn/v1/chat/completions）
    if not base:
        silra_url = os.environ.get("SILRA_API_URL", "")
        if silra_url:
            base = silra_url.replace("/chat/completions", "").rstrip("/")
    # 如果冇 set base，預設 DeepSeek 官方
    if not base:
        base = "https://api.deepseek.com"
    return base, key, model

# ===== 批改核心 =====
def grade_essay(text, rubric, api_base, api_key, model):
    """用 LLM 批改一篇作文，返回 JSON 結果"""
    if not api_key:
        return None, "未偵測到 API key — 請喺 Streamlit Cloud → Settings → Secrets 設定 OPENAI_API_KEY"
    prompt = f"""你係一個專業英文老師。根據以下評分準則，批改學生嘅英文作文。

評分準則（每項 0-10 分）：
{rubric}

學生作文：
\"\"\"
{text}
\"\"\"

請用以下 JSON 格式回覆（唔好加其他文字）：
{{"scores": {{"內容": 8, "結構": 7, "文法": 6, "創意": 8}}, "total": 29, "comment": "整體評語（中文，2-3 句）", "strengths": ["優點1", "優點2"], "improvements": ["改善1", "改善2"]}}
"""
    try:
        r = requests.post(
            f"{api_base}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "你係專業英文作文批改老師。直接輸出 JSON，唔好有任何其他文字。"},
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
        content = r.json()["choices"][0]["message"]["content"]
        # 嘗試解析 JSON（可能要清理 markdown fence）
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(content), None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== Rubric 預設（按科目）=====
RUBRIC_PRESETS = {
    "📕 英文作文": """- 內容（Content）：主題相關、有細節、有個人想法
- 結構（Structure）：有開頭/中間/結尾、句子流暢
- 文法（Grammar）：時態正確、句子完整、標點正確
- 創意（Creativity）：用詞豐富、有想像力""",
    "🌍 常識科長問題": """- 內容準確性（Accuracy）：答案正確、冇事實錯誤
- 解釋清晰度（Clarity）：解釋有邏輯、有因果關係、人哋睇得明
- 關鍵詞運用（Keywords）：有用到課堂教嘅關鍵詞/概念
- 完整性（Completeness）：有答齊問題所有部分、有例子""",
    "📗 中文作文": """- 內容（內容）：主題相關、有細節、有個人感受
- 結構（結構）：有開頭/經過/結尾、段落分明
- 用詞（用詞）：詞彙豐富、有適當成語/修辭
- 標點與字詞（標點與字詞）：標點正確、冇錯別字""",
    "🔢 數學解題": """- 步驟（Steps）：解題步驟清晰、完整
- 準確性（Accuracy）：計算正確、答案正確
- 解釋（Explanation）：有解釋點解用呢個方法
- 單位與格式（Format）：有寫單位、格式正確""",
}

# ===== Sidebar：設定 =====
with st.sidebar:
    st.header("⚙️ 設定")
    api_base, api_key, model = get_api_config()
    st.info(f"API: `{api_base}`\n\nModel: `{model}`")
    if not api_key:
        st.warning("⚠️ 未偵測到 API key — 請喺 Streamlit Cloud Secrets 設定 `OPENAI_API_KEY`，或者本地用 .env")
    
    st.subheader("📋 評分準則（Rubric）")
    subject_key = st.selectbox("科目", list(RUBRIC_PRESETS.keys()))
    rubric = st.text_area("Rubric（每項 0-10 分）", RUBRIC_PRESETS[subject_key], height=150, key=f"rubric_{subject_key}")
    
    st.subheader("📊 輸出選項")
    show_detail = st.checkbox("顯示詳細評語", value=True)

# ===== 主頁面 =====
tab1, tab2 = st.tabs(["📄 上傳 CSV 批改", "✍️ 直接貼文批改"])

with tab1:
    st.header("📄 上傳 Google Forms 回應（CSV）")
    st.markdown("""
**點攞 CSV：**
1. 喺你嘅 Google Form → 「回應」分頁 → 「連結試算表」
2. 喺 Google Sheets → 「檔案」→「下載」→「CSV (.csv)」
3. 上傳下面
""")
    uploaded = st.file_uploader("上傳 CSV", type=["csv"])
    
    if uploaded:
        try:
            # 每次重新讀 bytes（避免 rerun 後 pointer 到尾）+ 自動偵測 encoding
            raw = uploaded.getvalue()
            df = None
            last_err = None
            for enc in ["utf-8-sig", "utf-8", "gb18030", "big5", "latin-1"]:
                try:
                    df = pd.read_csv(io.BytesIO(raw), encoding=enc)
                    break
                except Exception as e:
                    last_err = e
                    continue
            if df is None:
                raise last_err
            st.success(f"✅ 讀到 {len(df)} 份回應")
            
            if len(df) == 0:
                st.warning("⚠️ CSV 冇任何回應資料 — 要學生提交咗先有得批改。如果你想測試，可以用下面「✍️ 直接貼文批改」分頁。")
            
            # 全部欄位都俾揀（唔限 dtype — 空欄會被 pandas 當做數字欄）
            all_cols = list(df.columns)
            essay_col = st.selectbox("邊一欄係作文答案？", all_cols)
            name_col = st.selectbox("邊一欄係學生名？（可選）", ["（無）"] + all_cols)
            
            if st.button("🚀 開始 AI 批改", type="primary"):
                results = []
                progress = st.progress(0)
                for i, row in df.iterrows():
                    essay_text = str(row[essay_col]).strip() if pd.notna(row[essay_col]) else ""
                    if not essay_text or essay_text == "nan":
                        continue
                    student = str(row[name_col]).strip() if name_col != "（無）" and pd.notna(row[name_col]) else f"學生 {i+1}"
                    with st.spinner(f"批改緊 {student}..."):
                        result, err = grade_essay(essay_text, rubric, api_base, api_key, model)
                    if result:
                        results.append({
                            "student": student,
                            "essay": essay_text[:100] + ("..." if len(essay_text) > 100 else ""),
                            **result
                        })
                    else:
                        st.error(f"{student}: {err}")
                    progress.progress((i + 1) / len(df))
                    time.sleep(0.5)  # rate limit 緩衝
                
                st.session_state.results = results
                st.success(f"✅ 批改完成：{len(results)} 份")
        except Exception as e:
            st.error(f"讀 CSV 出錯: {e}")
            st.code(traceback.format_exc())

with tab2:
    st.header("✍️ 直接貼文批改")
    essay_input = st.text_area("貼上學生作文：", height=200)
    student_name = st.text_input("學生名（可選）：")
    if st.button("🚀 批改", type="primary"):
        if not essay_input.strip():
            st.warning("請先貼上作文")
        else:
            with st.spinner("AI 批改中..."):
                result, err = grade_essay(essay_input.strip(), rubric, api_base, api_key, model)
            if result:
                st.session_state.results = [{"student": student_name or "學生", "essay": essay_input[:100], **result}]
            else:
                st.error(err)

# ===== 顯示結果 =====
if "results" in st.session_state and st.session_state.results:
    st.divider()
    st.header("📊 批改結果")
    
    # 總覽表
    overview = pd.DataFrame([
        {"學生": r["student"], "總分": r.get("total", sum(r.get("scores", {}).values())), "評語": r.get("comment", "")}
        for r in st.session_state.results
    ])
    st.dataframe(overview, use_container_width=True)
    
    # 詳細
    if show_detail:
        for r in st.session_state.results:
            with st.expander(f"📝 {r['student']} — {r.get('total', 'N/A')} 分"):
                scores = r.get("scores", {})
                cols = st.columns(len(scores) if scores else 1)
                for col, (k, v) in zip(cols, scores.items()):
                    col.metric(k, f"{v}/10")
                st.markdown(f"**💬 評語：** {r.get('comment', '')}")
                st.markdown(f"**✅ 優點：** " + "、".join(r.get("strengths", [])))
                st.markdown(f"**🔧 改善：** " + "、".join(r.get("improvements", [])))
    
    # 下載
    csv_out = io.StringIO()
    pd.DataFrame([
        {"學生": r["student"], "總分": r.get("total", ""), "評語": r.get("comment", ""),
         "優點": "、".join(r.get("strengths", [])), "改善": "、".join(r.get("improvements", []))}
        for r in st.session_state.results
    ]).to_csv(csv_out, index=False)
    st.download_button("⬇️ 下載批改結果 (CSV)", csv_out.getvalue(), "ai_grading_results.csv", "text/csv")
else:
    st.info("👆 上傳 CSV 或者貼文，開始批改")
