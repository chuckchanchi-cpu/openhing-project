#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing AI 教學平台（合併版 — 題目生成器 + 練習平台）

Streamlit Cloud 嘅 Main module 指向呢個檔案（pages/05_AI_題目生成器.py），
所以兩個功能合併喺同一個 app，用 tabs 切換：
  🛠️ AI 題目生成器：老師生成題目 → review → 發布
  🏋️ AI 練習平台：學生揀題目 → 作答 → AI 即時批改

Session state 共享 → 生成器「發布」嘅題目即刻喺練習平台「🆕 老師新生成」出現！
"""

import streamlit as st
import os
import json
import glob
import io
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🦀 Openhing AI 教學平台", page_icon="🦀", layout="wide")

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

# ===== 各科目預設 rubric（發布/下載共用）=====
RUBRIC_DEFAULT = {
    "中文": "- 內容（Content）：主題相關、有細節\n- 結構（Structure）：有開頭/中間/結尾\n- 用詞（Vocabulary）：用詞豐富\n- 標點（Punctuation）：標點正確",
    "常識": "- 內容準確性（Accuracy）：答案正確、冇事實錯誤\n- 解釋清晰度（Clarity）：解釋有邏輯、有因果關係\n- 關鍵詞運用（Keywords）：有用到教材關鍵詞\n- 完整性（Completeness）：有答齊所有部分",
    "英文": "- 內容（Content）：主題相關、有細節\n- 結構（Structure）：有開頭/中間/結尾\n- 文法（Grammar）：時態正確、句子完整\n- 創意（Creativity）：用詞豐富",
    "數學": "- 步驟（Steps）：解題步驟清晰\n- 準確性（Accuracy）：計算正確\n- 解釋（Explanation）：有解釋點解用呢個方法\n- 格式（Format）：答案有寫單位",
}
RUBRIC_FALLBACK = "- 內容準確性（Accuracy）：答案正確\n- 解釋清晰度（Clarity）：解釋清楚\n- 完整性（Completeness）：有答齊\n- 創意（Creativity）：有自己嘅諗法"

# ===== 練習平台內置題目庫（fallback）=====
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

def load_question_bank():
    """讀 repo 入面 resources/questions/ 嘅題目 JSON，合併內置題目"""
    bank = {}
    for k, v in QUESTION_BANK.items():
        bank[k] = [dict(q, **{"rubric": q.get("rubric", "")}) for q in v]
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
    return bank

# ===== 生成器：題目格式轉換 + AI 生成 =====
def to_practice_format(q, subject):
    """將生成器題目 dict 轉做練習平台格式"""
    return {
        "q": q.get('question') or q.get('title', ''),
        "hint": q.get('tip', ''),
        "rubric": RUBRIC_DEFAULT.get(subject, RUBRIC_FALLBACK),
        "answer": q.get('reference_answer', ''),
    }

def generate_questions(subject, grade, topic, count=5, material_path=None):
    """Generate practice questions using AI"""
    api_base, api_key, model = get_api_config()
    if not api_key:
        st.error("⚠️ 未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY")
        return []
    try:
        # 教材 context（可選）— 出題跟教材內容
        material_ctx = ""
        if material_path and os.path.exists(material_path):
            with open(material_path, encoding="utf-8") as f:
                material_ctx = f.read()[:4000]

        material_section = ""
        if material_ctx.strip():
            material_section = f"""
**教材內容（題目必須根據呢份教材嚟出，用返教材嘅詞彙同概念）：**
{material_ctx}
"""

        system_prompt = f"""你係一位經驗豐富嘅小學{subject}科老師，專門為{grade}學生設計練習題目。
{material_section}
請根據以上要求生成 {count} 條練習題目：

**要求：**
1. 題目要清晰、具體，適合{grade}學生水平
2. 涵蓋不同難易度 (簡單、中等、挑戰)
3. 每條題目包含：題目內容、評分標準、參考答案
4. 用{subject}語撰寫 (英文科用英文，其他用廣東話)
5. 格式要統一，方便學生作答

**輸出格式 (JSON)：**
```json
[
  {{
    "id": 1,
    "title": "題目標題",
    "question": "完整題目內容",
    "difficulty": "簡單/中等/挑戰",
    "marks": 10,
    "reference_answer": "參考答案要点",
    "tip": "提示或解題技巧"
  }}
]
```

只返回 JSON，唔好有其他文字。"""

        user_message = f"科目: {subject}\n年級: {grade}\n主題: {topic if topic else '請根據課程標準自行選擇合適主題'}\n數量: {count} 條"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 3000,
            "temperature": 0.8
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"{api_base}/chat/completions", json=payload, headers=headers, timeout=180)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            try:
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    json_str = content.split("```")[1].split("```")[0].strip()
                else:
                    json_str = content

                questions = json.loads(json_str)
                return questions
            except json.JSONDecodeError:
                return [{
                    "id": 1,
                    "title": f"{subject}練習 - {topic or '綜合'}",
                    "question": content[:500],
                    "difficulty": "中等",
                    "marks": 10,
                    "reference_answer": "參見 AI 生成內容",
                    "tip": "💡 仔細閱讀題目，結合所學知識作答。"
                }]
        else:
            st.error(f"❌ AI 生成失敗 (錯誤碼: {response.status_code}: {response.text[:200]})")
            return []
    except Exception as e:
        st.error(f"❌ 生成出錯: {str(e)}")
        return []

# ===== 練習平台：AI 批改核心 =====
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

# ===== Tab 1：AI 題目生成器（老師）=====
def render_generator():
    # Session state management
    if 'current_subject' not in st.session_state:
        st.session_state.current_subject = "中文"
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = []
    if 'reviewed_questions' not in st.session_state:
        st.session_state.reviewed_questions = []

    st.header("🛠️ AI 自動出題平台")
    st.markdown("👨‍🏫 教師模式：AI 自動生成題目 → 教師審核 → 發布 → 學生喺「🏋️ 練習平台」做")

    # Sidebar: Settings
    with st.sidebar:
        st.header("⚙️ 出題設定")

        subject = st.selectbox("科目", ["中文", "常識", "英文", "數學"],
                               index=["中文", "常識", "英文", "數學"].index(st.session_state.current_subject))
        grade = st.selectbox("年級", ["小一", "小二", "小三", "小四", "小五", "小六"])
        topic = st.text_input("主題 (可選)", placeholder="例如：水的循環、近義詞、小數除法")
        question_count = st.slider("題目數量", 1, 10, 5)

        st.session_state.current_subject = subject

        st.divider()

        # 📖 教材選擇（openedujustan）
        st.header("📖 教材 (可選)")
        material_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "openedujustan")
        material_files = sorted(glob.glob(os.path.join(material_dir, "*.md")))
        material_names = ["（唔用教材 — AI 自由出題）"] + [os.path.basename(f) for f in material_files]
        material_choice = st.selectbox("出題根據教材", material_names)
        material_path = None
        if material_choice != "（唔用教材 — AI 自由出題）":
            material_path = os.path.join(material_dir, material_choice)
            st.caption(f"✅ 已揀：`{material_choice}`")

    # Main content area
    st.subheader(f"🤖 出題 — {subject}")

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("🎲 生成題目", type="primary", use_container_width=True):
            with st.spinner(f"🤖 正在生成 {question_count} 條 {subject} 題目..."):
                new_questions = generate_questions(subject, grade, topic, question_count, material_path)

            if new_questions:
                st.session_state.generated_questions = new_questions
                st.success(f"✅ 成功生成 {len(new_questions)} 條題目！")
            else:
                st.error("❌ 生成失敗，請再試一次")

    with col2:
        if st.session_state.generated_questions:
            st.info(f"💡 當前有 {len(st.session_state.generated_questions)} 條題目，可點擊「全部重新生成」獲得新題目")

    # Display generated questions
    if st.session_state.generated_questions:
        st.markdown("---")
        st.subheader("📋 生成嘅題目")

        for idx, q in enumerate(st.session_state.generated_questions):
            with st.expander(f"#{q.get('id', idx+1)} {q.get('title', '未命名')}", expanded=(idx == 0)):
                col_a, col_b = st.columns([3, 1])

                with col_a:
                    st.markdown(f"**{q.get('question', '無內容')}**")
                    st.markdown("**評分標準：**")
                    st.write(f"- 難度: {q.get('difficulty', '中等')}")
                    st.write(f"- 分數: {q.get('marks', 10)} 分")
                    if q.get('tip'):
                        st.info(q['tip'])

                with col_b:
                    st.markdown("**教師操作：**")

                    if st.button("✅ 通過", key=f"approve_{idx}", use_container_width=True):
                        q['reviewed'] = True
                        q['reviewed_at'] = datetime.now().isoformat()
                        st.session_state.reviewed_questions.append(q)
                        st.success("✅ 已通過！")
                        st.rerun()

                    if st.button("🔄 重出這題", key=f"regenerate_{idx}", use_container_width=True):
                        with st.spinner("🤖 正在重新生成..."):
                            single_q = generate_questions(subject, grade, topic, 1, material_path)
                            if single_q:
                                st.session_state.generated_questions[idx] = single_q[0]
                                st.success("✅ 已替換！")
                                st.rerun()

                    if st.button("❌ 刪除", key=f"delete_{idx}", use_container_width=True):
                        st.session_state.generated_questions.pop(idx)
                        st.success("❌ 已刪除！")
                        st.rerun()

        # Batch actions
        st.markdown("---")
        col_x, col_y, col_z = st.columns(3)

        with col_x:
            if st.button("🔄 全部重新生成", use_container_width=True):
                with st.spinner("🤖 正在重新生成所有題目..."):
                    new_qs = generate_questions(subject, grade, topic, question_count, material_path)
                if new_qs:
                    st.session_state.generated_questions = new_qs
                    st.success(f"✅ 已生成 {len(new_qs)} 條新題目！")
                else:
                    st.error("❌ 生成失敗")

        with col_y:
            if st.button("💾 保存到文件", use_container_width=True):
                filename = f"{subject}_{grade}_{topic or 'custom'}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# {subject}練習題目\n\n")
                    f.write(f"**年級**: {grade}  \n")
                    f.write(f"**日期**: {datetime.now().strftime('%Y-%m-%d')}  \n")
                    f.write(f"**主題**: {topic or '自訂'}  \n\n")

                    for q in st.session_state.generated_questions:
                        f.write(f"## #{q.get('id', 'N/A')} {q.get('title', '未命名')}\n\n")
                        f.write(f"{q.get('question', '')}\n\n")
                        f.write(f"- 難度: {q.get('difficulty', '中等')}\n")
                        f.write(f"- 分數: {q.get('marks', 10)} 分\n")
                        if q.get('tip'):
                            f.write(f"- 提示: {q['tip']}\n")
                        if q.get('reference_answer'):
                            f.write(f"\n**參考答案**:\n{q['reference_answer']}\n")
                        f.write("\n---\n\n")

                st.success(f"✅ 已保存至 {filename}")

        with col_z:
            if st.button("📤 發布給學生", use_container_width=True, type="primary"):
                # 發布全部生成嘅題目（通過與否都發布 — 老師可以之後用「重出/刪除」調整）
                to_publish = st.session_state.generated_questions
                reviewed_count = len([q for q in to_publish if q.get('reviewed')])
                # 轉換做練習平台格式（q/hint/rubric/answer）
                pending = []
                skipped = 0
                for q in to_publish:
                    p = to_practice_format(q, subject)
                    if p["q"]:
                        p["source"] = f"AI 生成（{subject} {grade} {topic or ''}）"
                        pending.append(p)
                    else:
                        skipped += 1
                if "pending_questions" not in st.session_state:
                    st.session_state.pending_questions = []
                existing_q = {x.get("q") for x in st.session_state.pending_questions}
                added = 0
                for p in pending:
                    if p.get("q") and p["q"] not in existing_q:
                        st.session_state.pending_questions.append(p)
                        existing_q.add(p["q"])
                        added += 1
                if added > 0:
                    st.session_state.pending_added = added
                    msg = f"🎉 已發布 {added} 條題目去練習平台！"
                    if skipped:
                        msg += f"（{skipped} 條格式不完整被跳過 — 可以撳「🔄 重出這題」）"
                    st.success(msg)
                    st.info("👉 而家切去上面「🏋️ AI 練習平台」tab → 揀科目「🆕 老師新生成」→ 學生即刻做到！")
                    st.balloons()
                else:
                    st.info("呢批題目已經發布過，冇重複加入")

        # 永久保存：下載 JSON 俾 Openclaw commit 入題目庫
        with st.expander("💾 永久保存（下載 JSON 俾 Openclaw commit 入 resources/questions/）"):
            payload_qs = [to_practice_format(q, subject) for q in st.session_state.generated_questions if (q.get('question') or q.get('title'))]
            payload = json.dumps({
                "subject": f"🆕 {subject}（AI 生成）",
                "source": f"AI 生成（{subject} {grade} {topic or ''}）— {datetime.now().strftime('%Y-%m-%d')}",
                "questions": payload_qs
            }, ensure_ascii=False, indent=2)
            st.download_button(
                "⬇️ 下載題目 JSON",
                payload,
                f"questions_{subject}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                "application/json",
                use_container_width=True
            )
            st.caption("下載後將個 JSON 檔案 send 俾 Openclaw，佢會 commit 入題目庫 → 所有學生永久見到")

# ===== Tab 2：AI 練習平台（學生）=====
def render_practice():
    bank = load_question_bank()

    # 合併老師用生成器「發布」嘅題目（session 內共享）
    if "pending_questions" in st.session_state and st.session_state.pending_questions:
        pending = [q for q in st.session_state.pending_questions if q.get("q")]
        if pending:
            bank.setdefault("🆕 老師新生成", [])
            existing_q = {q.get("q") for q in bank["🆕 老師新生成"]}
            for q in pending:
                if q.get("q") not in existing_q:
                    bank["🆕 老師新生成"].append(q)

    st.header("🏋️ AI 練習平台")
    st.caption("揀練習 → 作答 → AI 即時批改！答完即刻知道點改善 💪")

    api_base, api_key, model = get_api_config()

    # Sidebar
    with st.sidebar:
        st.header("📊 老師選項")
        pending_count = len(st.session_state.get("pending_questions", []))
        if pending_count > 0:
            st.success(f"🆕 老師新生成：{pending_count} 條題目已加入（喺「揀科目」度揀「🆕 老師新生成」）")
        if st.checkbox("顯示老師工具"):
            st.caption("下載當前 session 嘅練習紀錄 CSV")
            if st.session_state.get("practice_log"):
                df_log = pd.DataFrame(st.session_state.practice_log)
                csv_out = io.StringIO()
                df_log.to_csv(csv_out, index=False)
                st.download_button("⬇️ 下載練習紀錄 CSV", csv_out.getvalue(), "practice_results.csv", "text/csv")
            else:
                st.info("未有練習紀錄（學生做過練習先有）")

    # 揀科目 + 題目
    subject = st.selectbox("📚 揀科目", list(bank.keys()))
    questions = bank[subject]
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
            st.markdown("### 💬 老師評語")
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
                "科目": subject, "題目": question["q"],
                "答案": answer.strip(), "總分": total, "評語": result.get("comment", "")
            })

            st.info("💡 想再試多次？改完答案再撳「提交批改」就得！")
        else:
            st.error(err)

    st.divider()
    st.caption("💪 練習多啲，進步快啲！AI 老師 24 小時喺度")

# ===== Main：Tabs 切換兩個功能 =====
st.title("🦀 Openhing AI 教學平台")
st.caption("🛠️ 老師出題 → 🏋️ 學生練習 → 🤖 AI 批改")

tab_gen, tab_prac = st.tabs(["🛠️ AI 題目生成器", "🏋️ AI 練習平台"])

with tab_gen:
    render_generator()

with tab_prac:
    render_practice()

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>OpenEduJustan © 2026 | AI 教學平台</div>", unsafe_allow_html=True)
