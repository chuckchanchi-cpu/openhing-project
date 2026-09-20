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
import re
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

**訓練目的（最重要，出題前必讀）：** 訓練嘅意義係 ①**recall 課堂知識** — 令學生諗返上堂老師教過嘅內容（唔係出新嘢）②**證明真係明白** — 唔係靠背答案，係要理解點解 ③**令知識更牢固** — 透過重溫同變化題目，將課堂知識記得更穩。題目設計要令學生「諗返上堂學過嘅嘢」先答到；MC 陷阱選項要測到學生係「真明白」定「靠估」；批改評語要連結返課堂知識，幫學生鞏固。

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

**技巧 + 陷阱要求（必須跟足，令訓練深入細緻、唔忽略細節）：**
- 每條題目都要有「解題技巧（technique）」同「陷阱提示（trap）」兩個欄位
- **陷阱設計**：MC 嘅錯誤選項要包含至少 1 個「陷阱選項」— 針對學生最常見嘅錯誤（例如：數學小數點位/單位換算錯、中文近義詞混淆、英文串法近似/固定搭配錯、忽略題目關鍵字「不」「最多」「大約」等）；短答/長答要喺「trap」欄提醒易錯位
- **技巧設計**：每題喺「technique」欄寫清楚解題步驟/口訣/方法（例如：先圈關鍵字→列式→檢查單位；先睇空格前後詞性→再返教材搵）
- 題目本身要考細節（數字、單位、關鍵字、詞語搭配），唔可以淨係表面答案就答到

**難度階梯（必須跟足，第 1 題最簡單）：**
- 第 1 題（⭐）：最簡單 — MC 選擇題，直接從教材搵到答案（記憶/辨認）
- 第 2 題（⭐⭐）：簡單 — T/F 判斷題，基礎理解
- 第 3 題（⭐⭐⭐）：中等 — 短答題，簡單應用（一步計算/填充/改寫）
- 第 4 題（⭐⭐⭐⭐）：較難 — MC 或短答，多步驟/比較/分析
- 第 5 題（⭐⭐⭐⭐⭐）：最難 — 長答題，要解釋原因/綜合教材概念

**同學名字（題目要自然融入，令學生覺得親切熟悉）：**
- 中文科/數學科/常識科用：皓一、仲庭、仲希、少軍、心謐、信一、依純、炭次郎、伊窩座、無慘、尼豆子
- 英文科用：Hugo、Jay、Ethan
- 鬼滅之刃角色（炭次郎、伊窩座、無慘、尼豆子）可以自然融入情境，例如：「炭次郎有 28.4 元，他想購買每枝售價 7.8 元的雪條，他最多可以購買多少枝？」

**語言要求（必須跟足）：**
- 所有「題目內容（question）」「提示（tip）」「評分準則（rubric）」必須用**正式書面語**（學校測驗卷風格），嚴禁口語、廣東話、網絡用語
- 英文科：題目、提示、評分準則用英文；其他科目用書面語中文
- 同學名可以照用，但句子要正式（例如：「皓一有 28.4 元，他想購買每枝售價 7.8 元的雪條，他最多可以購買多少枝？」）

**每條題目包含：**
- "question": 題目內容（書面語）
- "type": "MC" / "T/F" / "short" / "long"
- "options": 只有 MC 先有（4 個選項 array）
- "answer": 正確答案（MC 寫正確選項嘅內容；T/F 寫「對」或「錯」；short/long 寫參考答案要點）
- "difficulty": 難度級數（"⭐"/"⭐⭐"/"⭐⭐⭐"/"⭐⭐⭐⭐"/"⭐⭐⭐⭐⭐"）
- "tip": 提示（引導學生思考，唔好直接俾答案）
- "technique": 解題技巧（步驟/口訣/方法，書面語）
- "trap": 陷阱提示（呢題最易錯嘅位/常見錯誤，書面語）
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
                {"role": "user", "content": f"請根據教材生成 {count} 條每日溫習題目：混合題型（MC/判斷/短答/長答）、由淺入深、自然融入同學名、每題附解題技巧同陷阱提醒、全部用教材內容！"}
            ],
            "max_tokens": 6000,
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
            try:
                questions = json.loads(content)
            except json.JSONDecodeError:
                # AI 有時會加雜質文字 → 嘗試抽取 JSON 部分
                m = re.search(r'[\[{].*[\]}]', content, re.S)
                if not m:
                    raise
                questions = json.loads(m.group(0))
            if isinstance(questions, dict):
                questions = questions.get("questions", [])
            # 淨係留有效題目 + 補 rubric
            valid = []
            for q in questions:
                text = q_text(q)
                if text:
                    q["question"] = text
                    q["q"] = text  # 雙保險：q 同 question 都有
                    q.setdefault("rubric", RUBRIC_DEFAULT.get(subject, RUBRIC_FALLBACK))
                    q.setdefault("tip", "💡 諗下教材入面講過嘅重點")
                    q.setdefault("technique", "")
                    q.setdefault("trap", "")
                    q.setdefault("difficulty", "")
                    q.setdefault("type", "short")
                    q.setdefault("options", [])
                    q.setdefault("answer", "")
                    valid.append(q)
            if not valid:
                st.error("❌ AI 回覆格式唔啱（冇有效題目）— 請再試一次")
                return []
            return valid
        except json.JSONDecodeError:
            st.error("❌ AI 回覆格式唔啱（唔係 JSON）— 請再試一次")
            return []
    except Exception as e:
        st.error(f"❌ 生成出錯：{str(e)}")
        return []

# ===== 文章填空（Cloze）生成 =====
def generate_cloze(material_path, subject):
    api_base, api_key, model = get_api_config()
    if not api_key:
        st.error("⚠️ 未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY")
        return None
    try:
        with open(material_path, encoding="utf-8") as f:
            material_ctx = f.read()[:5000]

        system_prompt = f"""你係一位經驗豐富嘅小學六年級{subject}科老師。

**教材內容（文章同詞語必須根據呢份教材嚟寫，用返教材嘅詞彙、概念同例子）：**
{material_ctx}

請根據教材生成一篇**文章填空（Cloze）練習**。**呢個係「每日溫習」**：目的係幫學生練習「從文章中搵詞語填空」，回顧學校今日所學，唔好出太深太偏嘅嘢嚇怕學生。

**訓練目的（最重要）：** 幫學生 recall 課堂學過嘅詞語同文章內容、證明佢明白詞語點用、透過「從文章搵答案」嘅過程令知識更牢固 — 題目要令學生返去文章度諗返學過嘅嘢。

**🔒 鐵律（最重要，必須跟足）：**
1. **只准用教材內容** — 文章主題、詞彙、概念全部要喺上面教材內容出現過
2. **嚴禁教材以外嘅知識** — 唔可以用互聯網/課外常識嘅事實
3. **難度升級只可以「基於教材延伸」** — 換情境/換角度/綜合教材概念，唔准引入新知識
4. **出完自檢** — 每個空格嘅答案都一定要喺教材內容出現過

**文章要求：**
- 文章長度：英文 150-300 字；中文 120-250 字
- 文章主題：圍繞教材主題（例如動物領養、植物適應環境、課文道理），生活化
- 文章內要包含 6-8 個「目標詞彙」（即係學生要喺文章搵到嘅詞）
- 文章主角可以用同學名或鬼滅之刃角色（炭次郎、伊窩座、無慘、尼豆子），令學生覺得親切有趣

**填充題要求（重點）：**
- 另外出 4-6 條**新填充題**，用（1）（2）（3）...標記
- 每題係一條**新句子**（唔可以照抄文章句子，要換情境、換講法），句子入面有一個空格
- **每個空格嘅答案 = 文章入面出現過嘅詞語**（目標詞彙之一）
- **難度遞增**：前面嘅題目答案容易搵（喺文章開頭直接出現），後面嘅難（要理解文章先搵到）
- 每題嘅 tip 一定要講「答案喺文章邊度搵」（例如：留意第 2 段關於動物庇護所嘅句子）
- 每題要包含「揾詞技巧（technique）」同「陷阱（trap）」：technique 教學生點搵（例如：睇空格前後詞性、搵關鍵搭配詞、留意同義詞替換）；trap 提醒易錯位（例如：同義詞混淆、串法近似、抄錯字）

**語言要求（必須跟足）：**
- 英文科：文章、提示、答案全英文
- 其他科：文章、提示、答案用正式書面語（學校測驗卷風格），嚴禁口語/廣東話

**輸出格式（只輸出 JSON object，唔好有其他文字）：**
{{
  "article": "成篇文章（正常文章，冇空格）",
  "questions": [
    {{"id": 1, "sentence": "新句子，空格用（1）標記", "answer": "答案詞語（必須喺文章出現過）", "tip": "書面語提示：答案喺文章邊度搵（例如：留意第 2 段關於……嘅句子）", "technique": "揾詞技巧（例如：睇空格前詞性→搵搭配詞）", "trap": "易錯位提醒（例如：小心同義詞混淆）"}},
    ...
  ],
  "word_bank": ["詞1", "詞2", ...]（可選：答案詞語嘅詞彙庫，幫學生篩選）
}}"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "請根據教材生成：一篇短文 + 4-6 條新填充題（答案要喺文章入面搵到），全部用教材內容！"}
            ],
            "max_tokens": 6000,
            "temperature": 0.8
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(f"{api_base}/chat/completions", json=payload, headers=headers, timeout=180)
        if response.status_code != 200:
            st.error(f"❌ AI 生成失敗（錯誤碼 {response.status_code}）：{response.text[:200]}")
            return None
        content = response.json()["choices"][0]["message"]["content"]
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            cloze = json.loads(content)
        except json.JSONDecodeError:
            # AI 有時會加雜質文字 → 嘗試抽取 JSON 部分
            m = re.search(r'\{.*\}', content, re.S)
            if not m:
                st.error("❌ AI 回覆格式唔啱（唔係 JSON）— 請再試一次")
                return None
            cloze = json.loads(m.group(0))
        if not isinstance(cloze, dict) or not cloze.get("article") or not (cloze.get("questions") or cloze.get("blanks")):
            st.error("❌ AI 回覆格式唔啱（缺 article/questions）— 請再試一次")
            return None
        cloze.setdefault("word_bank", [])
        qs = cloze.get("questions") or cloze.get("blanks")
        for b in qs:
            b.setdefault("sentence", "")
            b.setdefault("tip", "💡 答案喺文章入面，留意空格前後嘅意思，返文章搵")
            b.setdefault("technique", "")
            b.setdefault("trap", "")
            b.setdefault("answer", "")
        cloze["questions"] = qs
        return cloze
    except Exception as e:
        st.error(f"❌ 生成出錯：{str(e)}")
        return None


# ===== AI 批改文章填空 =====
def grade_cloze(cloze, answers, api_base, api_key, model):
    if not api_key:
        return None, "未偵測到 API key — 請老師喺 Streamlit Cloud Secrets 設定 OPENAI_API_KEY"
    blanks = cloze.get("questions") or cloze.get("blanks", [])
    lines = []
    for b in blanks:
        bid = b.get("id")
        student_ans = answers.get(bid, "").strip() or "（冇作答）"
        lines.append(f"（{bid}）句子：{b.get('sentence','')}｜學生答案：{student_ans}｜正確答案：{b.get('answer','')}｜答案喺文章邊度：{b.get('tip','')}｜揾詞技巧：{b.get('technique','')}｜易錯陷阱：{b.get('trap','')}")
    ans_text = "\n".join(lines)
    prompt = f"""你係一位專業同友善嘅小學老師。以下係「從文章中搵詞語填空」練習嘅學生答案同正確答案（學生要喺文章入面搵啱嘅詞語，填入新句子嘅空格），請逐題批改：

{ans_text}

請輸出 JSON array，每項對應一個空格：
- "id": 空格編號
- "correct": true/false（同正確答案一致先算啱；英文串法小錯可當啱但要喺評語提醒）
- "feedback": 書面語評語（英文科用英文）— 啱：讚一句 + 簡單講點解係呢個詞；錯：話俾學生聽正確答案 + 點樣從文章搵（留意邊啲線索）；如果學生中咗陷阱（見每題陷阱），要指出嚟教佢避免
- "total": 0 或 1

最後加一項總結：{{"id": 0, "correct": true, "feedback": "總結：X/Y 題答啱，……（鼓勵說話，書面語）", "total": 0}}
只輸出 JSON array，唔好有其他文字。"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你係一位專業、友善、有耐心嘅小學老師，評語用正式書面語（英文科用英文）。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.3
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(f"{api_base}/chat/completions", json=payload, headers=headers, timeout=180)
        if response.status_code != 200:
            return None, f"❌ AI 批改失敗（錯誤碼 {response.status_code}）：{response.text[:200]}"
        content = response.json()["choices"][0]["message"]["content"]
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content), None
    except Exception as e:
        return None, f"❌ 批改出錯：{str(e)}"


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
技巧：{q.get('technique', '冇提供')}
陷阱：{q.get('trap', '冇提供')}
學生答案：
\"\"\"
{a}
\"\"\"

"""

    prompt = f"""你係一個專業同友善嘅小學老師。根據每題嘅評分準則，逐題批改學生嘅答案，評語全部用正式書面語（英文科題目可用英文），語氣鼓勵為主。
選擇題/判斷題：直接對「正確答案」判斷對錯（揀啱就滿分，揀錯就 0 分）；短答/長答：按評分準則評分。如果學生答錯係因為中咗題目「陷阱」（見每題陷阱欄），評語要明確指出嚟，教佢下次點避免；答啱嘅可以讚佢避開咗陷阱。

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
if 'current_cloze' not in st.session_state:
    st.session_state.current_cloze = None
if 'cloze_mode' not in st.session_state:
    st.session_state.cloze_mode = False

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

    train_mode = st.radio("訓練模式", ["🎯 每日溫習（混合題型）", "📖 文章填充（從文章搵詞）"], key="train_mode")
    is_cloze = train_mode.startswith("📖")

    if st.button("🎲 生成文章+填充題" if is_cloze else "🎲 生成 5 條題目", type="primary", use_container_width=True):
        if is_cloze:
            with st.spinner(f"🤖 根據《{material_choice}》生成緊文章填空..."):
                cloze = generate_cloze(material_path, subject)
            if cloze:
                st.session_state.current_cloze = cloze
                st.session_state.current_material = material_choice
                st.session_state.grade_results = None
                st.session_state.current_questions = []
                st.session_state.cloze_mode = True
                st.success("✅ 文章填空準備好！")
            else:
                st.error("❌ 生成失敗，請再試")
        else:
            with st.spinner(f"🤖 根據《{material_choice}》生成緊 5 條題目..."):
                qs = generate_questions(material_path, subject, 5)
            if qs:
                st.session_state.current_questions = qs
                st.session_state.current_material = material_choice
                st.session_state.grade_results = None
                st.session_state.current_cloze = None
                st.session_state.cloze_mode = False
                st.success(f"✅ 生成咗 {len(qs)} 條題目！")
            else:
                st.error("❌ 生成失敗，請再試")

    if st.session_state.current_questions or st.session_state.current_cloze:
        if st.button("🔄 新一輪（重新生成）", use_container_width=True):
            if is_cloze:
                with st.spinner("🤖 重新生成緊..."):
                    cloze = generate_cloze(material_path, subject)
                if cloze:
                    st.session_state.current_cloze = cloze
                    st.session_state.current_material = material_choice
                    st.session_state.grade_results = None
                    st.session_state.current_questions = []
                    st.session_state.cloze_mode = True
                    st.success("✅ 新文章準備好！")
                else:
                    st.error("❌ 生成失敗，請再試")
            else:
                with st.spinner("🤖 重新生成緊..."):
                    qs = generate_questions(material_path, subject, 5)
                if qs:
                    st.session_state.current_questions = qs
                    st.session_state.current_material = material_choice
                    st.session_state.grade_results = None
                    st.session_state.current_cloze = None
                    st.session_state.cloze_mode = False
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

if not st.session_state.current_questions and not st.session_state.current_cloze:
    st.info("👆 左邊揀教材，然後撳「🎲 生成」開始！")
    st.stop()

# ===== 文章填空（Cloze）模式 =====
if st.session_state.cloze_mode and st.session_state.current_cloze:
    cloze = st.session_state.current_cloze
    st.markdown(f"**📖 教材：** `{st.session_state.current_material}`　**📚 科目：** {subject}")
    st.divider()
    st.subheader("📖 文章填充訓練（從文章搵詞語）")
    st.caption("🎯 先讀文章，再喺文章入面搵出啱嘅詞語填入新句子 — 由淺入深，加油！")

    article = cloze.get("article", "")
    article_disp = re.sub(r"（(\d+)）", r"＿＿＿（\1）＿＿＿", article)
    st.markdown(article_disp)

    word_bank = cloze.get("word_bank", [])
    if word_bank:
        st.markdown("**🧰 詞彙庫（Word Bank）：**　" + "　・　".join(word_bank))

    blanks = cloze.get("questions") or cloze.get("blanks", [])
    cloze_answers = {}
    for b in blanks:
        bid = b.get("id")
        sentence_disp = re.sub(r"（(\d+)）", r"＿＿＿（\1）＿＿＿", b.get("sentence", ""))
        st.markdown(f"### （{bid}）{sentence_disp}")
        cloze_answers[bid] = st.text_input(f"（{bid}）請從文章中揾出適當詞語填入", key=f"cloze_{bid}", placeholder="打低你嘅答案⋯")
        with st.expander(f"💡 提示（第 {bid} 題）"):
            st.markdown(b.get("tip", ""))
            if b.get("technique"):
                st.markdown(f"🛠️ **技巧：** {b['technique']}")
            if b.get("trap"):
                st.markdown(f"⚠️ **陷阱：** {b['trap']}")

    submitted = st.button("🚀 提交批改", type="primary", use_container_width=True, disabled=not any(cloze_answers.values()))
    if submitted:
        api_base, api_key, model = get_api_config()
        with st.spinner("🤖 AI 老師批改緊（約 10-20 秒）..."):
            results, err = grade_cloze(cloze, cloze_answers, api_base, api_key, model)
        if err:
            st.error(err)
        else:
            st.session_state.grade_results = results
            st.rerun()

    if st.session_state.grade_results:
        results = st.session_state.grade_results
        st.markdown("---")
        st.subheader("📊 批改結果")
        correct_count = 0
        for r in results:
            bid = r.get("id", 0)
            if bid == 0:
                st.success(r.get("feedback", ""))
                continue
            if r.get("correct"):
                correct_count += 1
                st.markdown(f"✅ **（{bid}）** {r.get('feedback', '')}")
            else:
                st.markdown(f"❌ **（{bid}）** {r.get('feedback', '')}")
        if correct_count:
            st.success(f"🏆 答啱 **{correct_count} / {len(blanks)}** 題！")
        st.info("💡 想再試？撳「🔄 新一輪」做新文章！")
        if "practice_log" not in st.session_state:
            st.session_state.practice_log = []
        st.session_state.practice_log.append({
            "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "教材": st.session_state.current_material,
            "模式": "文章填空",
            "總分": correct_count,
            "滿分": len(blanks),
        })
    st.stop()

# 顯示而家教材
st.markdown(f"**📖 教材：** `{st.session_state.current_material}`　**📚 科目：** {subject}")
st.divider()

questions = st.session_state.current_questions
answers = {}

# 顯示題目 + 作答區
st.subheader(f"📝 每日溫習（{len(questions)} 條題目）")
st.caption("🎯 混合題型 + 由淺入深 + 每題拆解技巧陷阱：第 1 題最簡單，越後越有挑戰性 — 加油！")
TYPE_BADGE = {"MC": "🔘 選擇題", "T/F": "⚖️ 判斷題", "short": "✏️ 短答", "long": "📝 長答"}
for i, q in enumerate(questions):
    diff = q.get("difficulty", "")
    qtype = q.get("type", "short")
    badge = TYPE_BADGE.get(qtype, "")
    st.markdown(f"### {i+1}. {q_text(q)}　{diff}　{badge}")
    with st.expander("💡 提示（撳開睇）"):
        st.markdown(q.get("tip", ""))
        if q.get("technique"):
            st.markdown(f"🛠️ **技巧：** {q['technique']}")
        if q.get("trap"):
            st.markdown(f"⚠️ **陷阱：** {q['trap']}")
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
if st.session_state.grade_results and not st.session_state.cloze_mode:
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
