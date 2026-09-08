import streamlit as st
import json
import os
import requests
import io

st.set_page_config(page_title="📖 Interactive Story Book", page_icon="📖", layout="wide")

# Demo story data (Fable-style)
STORIES = {
    "小貓找星星": {
        "title": "小貓找星星",
        "moral": "只要堅持，夢想總會實現",
        "pages": [
            {
                "text": "有一隻小貓，名字叫咪咪。每個夜晚，佢都望住天上嘅星星發呆。",
                "animation": "fade-in",
                "scene": "night_sky"
            },
            {
                "text": "「我想摸到星星！」咪咪對媽媽說。媽媽笑笑咁話：「星星好遠好遠㗎。」",
                "animation": "slide-left",
                "scene": "cat_mother"
            },
            {
                "text": "但咪咪冇放棄。佢爬上山頂、游過河川、穿過森林...",
                "animation": "zoom-in",
                "scene": "journey"
            },
            {
                "text": "最後，咪咪發現 — 每條河水入面都有星星倒影。原來星星一直喺身邊。",
                "animation": "glow",
                "scene": "reflection"
            }
        ]
    },
    "企鵝飛天記": {
        "title": "企鵝飛天記",
        "moral": "勇敢嘗試，突破自我限制",
        "pages": [
            {
                "text": "有一隻企鵝，名字叫波波。佢唔似其他企鵝，想飛。",
                "animation": "bounce",
                "scene": "penguin"
            },
            {
                "text": "「企鵝點會飛呀？」其他動物都笑佢。但波波相信自己做得到。",
                "animation": "shake",
                "scene": "mocking"
            },
            {
                "text": "波波用魚鱗做翅膀、用冰塊做滑翔翼，日日練習...",
                "animation": "spin",
                "scene": "training"
            },
            {
                "text": "終於！波波飛上天啦！原來只要肯試，不可能都變可能。",
                "animation": "float-up",
                "scene": "flying"
            }
        ]
    }
}

# Scene emoji mapping
SCENE_EMOJIS = {
    "night_sky": "🌙✨",
    "cat_mother": "🐱",
    "journey": "🏔️🌊🌲",
    "reflection": "🪞⭐",
    "penguin": "🐧",
    "mocking": "😂",
    "training": "🛩️❄️",
    "flying": "🎉"
}

# TTS Configuration - using Edge TTS (free, no API key needed)
def get_tts_audio(text):
    """Generate TTS audio using Edge TTS (Microsoft edge-free-tts)"""
    try:
        import urllib.request
        import urllib.parse
        
        # Use edge-tts via a simple HTTP approach
        # Microsoft Edge TTS endpoint (free, no auth required)
        voice = "zh-CN-XiaoyiNeural"  # Chinese female voice
        lang = "zh-CN"
        
        # Build SSML
        ssml = f'''
        <speak version="1.0" xml:lang="{lang}">
            <voice name="{voice}">
                {text}
            </voice>
        </speak>
        '''
        
        # Call Azure Speech Service free tier or use alternative
        # Fallback: use gTTS (Google TTS)
        return None  # Will use gTTS below
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

def get_tts_audio_gttss(text):
    """Generate TTS audio using gTTS (Google Text-to-Speech)"""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='zh-tw', slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.read()
    except ImportError:
        st.warning("gTTS not installed. Please add gtts to requirements.txt")
        return None
    except Exception as e:
        st.error(f"gTTS Error: {str(e)}")
        return None

def play_tts(page_text):
    """Play TTS audio for current page"""
    with st.spinner("🔊 Generating speech..."):
        audio_data = get_tts_audio_gttss(page_text)
    if audio_data:
        st.audio(audio_data, format="audio/mpeg")
        st.success("🎧 Audio ready!")
    else:
        st.error("Failed to generate audio")

# Animation CSS
ANIMATION_CSS = """
<style>
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideLeft { from { transform: translateX(100px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes zoomIn { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes glow { 0%, 100% { text-shadow: 0 0 5px gold; } 50% { text-shadow: 0 0 20px gold, 0 0 40px orange; } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
@keyframes shake { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(-5deg); } 75% { transform: rotate(5deg); } }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes floatUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.anim-fade-in { animation: fadeIn 1s ease-in-out; }
.anim-slide-left { animation: slideLeft 0.8s ease-out; }
.anim-zoom-in { animation: zoomIn 0.6s ease-out; }
.anim-glow { animation: glow 2s infinite; }
.anim-bounce { animation: bounce 1s infinite; }
.anim-shake { animation: shake 0.5s ease-in-out; }
.anim-spin { animation: spin 1s ease-in-out; }
.anim-float-up { animation: floatUp 0.8s ease-out; }

.story-page {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 40px;
    margin: 20px 0;
    color: white;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.scene-emoji {
    font-size: 80px;
    text-align: center;
    margin: 20px 0;
    filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));
}

.moral-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 1.2em;
    margin-top: 20px;
}

.nav-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1em;
    cursor: pointer;
    margin: 5px;
    transition: transform 0.2s;
}

.nav-btn:hover { transform: scale(1.05); }

.home-card {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 20px;
    padding: 30px;
    margin: 15px;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
}

.home-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}
</style>
"""

st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# Session state management
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_story' not in st.session_state:
    st.session_state.selected_story = None
if 'current_story_page' not in st.session_state:
    st.session_state.current_story_page = 0

def go_home():
    st.session_state.current_page = 'home'
    st.rerun()

def start_story(story_key):
    st.session_state.selected_story = story_key
    st.session_state.current_story_page = 0
    st.session_state.current_page = 'read'
    st.rerun()

def go_next():
    story = STORIES[st.session_state.selected_story]
    if st.session_state.current_story_page < len(story['pages']) - 1:
        st.session_state.current_story_page += 1
        st.rerun()

def go_prev():
    if st.session_state.current_story_page > 0:
        st.session_state.current_story_page -= 1
        st.rerun()

# ==================== PAGE 1: HOME ====================
if st.session_state.current_page == 'home':
    st.markdown("# 📖 互動童書")
    st.markdown("### 揀一本你鍾意嘅故事開始閱讀！")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="home-card">
            <div style="font-size: 60px;">🐱✨</div>
            <h3>小貓找星星</h3>
            <p>一隻小貓嘅追夢旅程</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("開始閱讀 ➡️", key="btn_cat", use_container_width=True):
            start_story("小貓找星星")
    
    with col2:
        st.markdown("""
        <div class="home-card">
            <div style="font-size: 60px;">🐧️</div>
            <h3>企鵝飛天記</h3>
            <p>一隻企鵝嘅飛天冒險</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("開始閱讀 ➡️", key="btn_penguin", use_container_width=True):
            start_story("企鵝飛天記")
    
    st.markdown("---")
    st.markdown("<div class='moral-box'>💡 靈感來自 Anthropic Fable 5.1 — AI 生成互動童書</div>", unsafe_allow_html=True)

# ==================== PAGE 2: READ ====================
elif st.session_state.current_page == 'read':
    story = STORIES[st.session_state.selected_story]
    pages = story['pages']
    current_idx = st.session_state.current_story_page
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 首頁"):
            go_home()
    with col2:
        st.markdown(f"## 📖 {story['title']}")
    with col3:
        st.markdown(f"**{current_idx + 1} / {len(pages)}**")
    
    # Progress bar
    st.progress((current_idx + 1) / len(pages))
    
    # Current page content
    page = pages[current_idx]
    scene_emoji = SCENE_EMOJIS.get(page['scene'], '📖')
    
    st.markdown(f"""
    <div class="story-page anim-{page['animation']}">
        <div class="scene-emoji">{scene_emoji}</div>
        <p style="font-size: 1.4em; line-height: 2; text-align: center;">
            {page['text']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 上一頁", disabled=current_idx == 0, use_container_width=True):
            go_prev()
    with col2:
        if st.button("🔊 朗讀呢頁", use_container_width=True):
            play_tts(page['text'])
    with col3:
        if st.button("下一頁 ➡️", disabled=current_idx == len(pages) - 1, use_container_width=True):
            go_next()
    
    # Moral at last page
    if current_idx == len(pages) - 1:
        st.markdown(f"""
        <div class="moral-box">
            🌟 故事寓意：{story['moral']} 🌟
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 重新閱讀", use_container_width=True):
            st.session_state.current_story_page = 0
            st.rerun()

# ==================== PAGE 3: ILLUSTRATE ====================
elif st.session_state.current_page == 'illustrate':
    story = STORIES[st.session_state.selected_story]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 首頁"):
            go_home()
    with col2:
        st.markdown(f"## 🎨 {story['title']} — 插畫世界")
    with col3:
        pass
    
    st.markdown("### 🖼️ 分層 3D 場景展示")
    
    for i, page in enumerate(story['pages']):
        scene_emoji = SCENE_EMOJIS.get(page['scene'], '📖')
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                font-size: 70px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                transform: perspective(500px) rotateY(-5deg);
                transition: transform 0.3s;
            ">
                {scene_emoji}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            **第 {i+1} 幕**
            
            {page['text']}
            
            *動畫效果：{page['animation']}*
            """)
        
        st.markdown("---")
    
    st.markdown("""
    <div class="moral-box">
        🎯 模板重用：換一個故事，自動生成新配音、動畫與插畫！
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📖 返回閱讀", use_container_width=True):
        st.session_state.current_page = 'read'
        st.rerun()
