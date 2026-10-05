import streamlit as st
import random
import json
import requests

st.set_page_config(page_title="🏸 Badminton Doubles Trainer", page_icon="🏸", layout="wide")

# ===== Game Data =====

BIRDY_SCENARIOS = [
    {
        "name": "前後站位（Front-Back）",
        "desc": "一名對手在前場、一名在後場",
        "opponents": [{"x": 50, "y": 20}, {"x": 50, "y": 40}],
        "best_zone": {"x": 20, "y": 30, "radius": 15},
        "explanation": "對手前後站位，中間有空隙但兩側都係空位。打向兩側角落最安全，令佢哋要移動接球。"
    },
    {
        "name": "左右站位（Side-by-Side）",
        "desc": "兩名對手分別佔左邊同右邊",
        "opponents": [{"x": 20, "y": 28}, {"x": 80, "y": 28}],
        "best_zone": {"x": 50, "y": 35, "radius": 12},
        "explanation": "對手左右站位，中間會有空隙。打正中間令佢哋爭球或者無人接，係最佳選擇。"
    },
    {
        "name": "兩人靠近（Clustered）",
        "desc": "兩名對手靠攏同一邊",
        "opponents": [{"x": 25, "y": 25}, {"x": 30, "y": 35}],
        "best_zone": {"x": 80, "y": 30, "radius": 15},
        "explanation": "對手集中喺一邊，另一邊完全空出嚟。打遠端開闊位，佢哋要跑好遠先接到。"
    },
    {
        "name": "偏左站位（Left-Biased）",
        "desc": "對手一前一後但偏左邊",
        "opponents": [{"x": 30, "y": 18}, {"x": 25, "y": 42}],
        "best_zone": {"x": 75, "y": 28, "radius": 14},
        "explanation": "對手偏左，右邊空出嚟。打右邊中後場令佢哋要橫向移動，增加難度。"
    },
    {
        "name": "淺場站位（Net Players）",
        "desc": "兩名對手都喺近網位置",
        "opponents": [{"x": 30, "y": 12}, {"x": 70, "y": 12}],
        "best_zone": {"x": 50, "y": 42, "radius": 12},
        "explanation": "對手都靠前，深遠球可以逼佢哋退後，破壞佢哋嘅進攻陣型。"
    },
]

PARTNER_SCENARIOS = [
    {
        "name": "隊友上前場（Attack Formation）",
        "desc": "隊友上前場 → 你應該覆蓋後場",
        "partner": {"x": 50, "y": 80},
        "correct_position": {"x": 50, "y": 62, "radius": 12},
        "explanation": "隊友上前場封網，你應該退到後場保護深遠球，形成前後防守陣型。"
    },
    {
        "name": "左右站位（Defense Formation）",
        "desc": "隊友喺右邊 → 你應該喺左邊",
        "partner": {"x": 70, "y": 72},
        "correct_position": {"x": 30, "y": 72, "radius": 15},
        "explanation": "左右站位係基本防守陣型。隊友守右邊，你守左邊，確保全場冇空隙。"
    },
    {
        "name": "隊友偏左（Left Position）",
        "desc": "隊友喺左邊 → 你應該喺右邊",
        "partner": {"x": 25, "y": 72},
        "correct_position": {"x": 75, "y": 72, "radius": 15},
        "explanation": "無論隊友喺邊，你都應該站佢相反方向，保持場地被均勻覆蓋。"
    },
    {
        "name": "隊友上前偏左（Front-Left）",
        "desc": "隊友上前場偏左 → 你應該覆蓋右後方",
        "partner": {"x": 35, "y": 78},
        "correct_position": {"x": 65, "y": 70, "radius": 16},
        "explanation": "隊友上前偏左，你應該覆蓋右後方，避免對手打穿中間同右邊。"
    },
    {
        "name": "隊友中場（Mid-Court）",
        "desc": "隊友喺中場 → 一人守前一人守後",
        "partner": {"x": 50, "y": 68},
        "correct_position": {"x": 50, "y": 55, "radius": 12},
        "explanation": "當隊友喺中場，其中一人應該保持靠後保護深遠球，防止被直接殺穿。"
    },
]

# ===== Session State =====
if 'birdy_idx' not in st.session_state:
    st.session_state.birdy_idx = 0
if 'birdy_score' not in st.session_state:
    st.session_state.birdy_score = 0
if 'birdy_total' not in st.session_state:
    st.session_state.birdy_total = 0
if 'birdy_streak' not in st.session_state:
    st.session_state.birdy_streak = 0
if 'birdy_best' not in st.session_state:
    st.session_state.birdy_best = 0
if 'birdy_answers' not in st.session_state:
    st.session_state.birdy_answers = []
if 'birdy_last_choice' not in st.session_state:
    st.session_state.birdy_last_choice = None

if 'pos_idx' not in st.session_state:
    st.session_state.pos_idx = 0
if 'pos_score' not in st.session_state:
    st.session_state.pos_score = 0
if 'pos_total' not in st.session_state:
    st.session_state.pos_total = 0
if 'pos_streak' not in st.session_state:
    st.session_state.pos_streak = 0
if 'pos_best' not in st.session_state:
    st.session_state.pos_best = 0
if 'pos_answers' not in st.session_state:
    st.session_state.pos_answers = []
if 'pos_last_choice' not in st.session_state:
    st.session_state.pos_last_choice = None

if 'ai_mode' not in st.session_state:
    st.session_state.ai_mode = False

# ===== AI Analysis Function =====
def analyze_with_ai(move_type, position, scenario_name, explanation):
    """Call LLM API to analyze the move"""
    
    # Get API config from environment
    api_key = st.secrets.get("SILRA_API_KEY", "") or st.secrets.get("OPENAI_API_KEY", "")
    api_base = st.secrets.get("SILRA_API_URL", "https://api.silra.cn/v1/chat/completions")
    model = st.secrets.get("MODEL_NAME", "deepseek-v4-flash")
    
    if not api_key:
        return {"error": "API key not configured"}
    
    prompt = f"""You are a badminton doubles coach. Analyze this move and give feedback in Cantonese.

Move Type: {move_type}
Position: {position}
Scenario: {scenario_name}
Correct Strategy: {explanation}

Please provide:
1. Rating (Excellent/Good/Try Again/Poor)
2. Brief explanation why
3. One specific suggestion for improvement

Keep it under 100 words. Use Cantonese."""

    try:
        response = requests.post(
            api_base,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a friendly badminton doubles coach who speaks Cantonese."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            },
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"AI Error: {str(e)}"

# ===== Generate Court Visualization HTML =====
def generate_court_html(court_id, width=400, height=700, show_opponents=False, show_partner=False, 
                       opponents=None, partner=None, best_zone=None, correct_pos=None,
                       selected_pos=None, is_correct=None):
    """Generate interactive SVG court with clickable zones"""
    
    svg_elements = f'''
    <svg id="{court_id}" width="{width}" height="{height}" style="border: 3px solid white; border-radius: 10px; background: linear-gradient(to bottom, #1a8a3c, #0f5e2b); cursor: pointer;" onclick="handleCourtClick(event, '{court_id}')">
        <!-- Net -->
        <line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#ffd43b" stroke-width="4"/>
        
        <!-- Service lines -->
        <line x1="{width/2}" y1="0" x2="{width/2}" y2="{height}" stroke="white" stroke-width="2" opacity="0.5"/>
        <line x1="0" y1="{height*0.15}" x2="{width}" y2="{height*0.15}" stroke="white" stroke-width="2" opacity="0.5"/>
        <line x1="0" y1="{height*0.85}" x2="{width}" y2="{height*0.85}" stroke="white" stroke-width="2" opacity="0.5"/>
        
        <!-- Labels -->
        <text x="{width/2}" y="30" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Opponents</text>
        <text x="{width/2}" y="{height-20}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">You</text>
        
        <!-- Best zone indicator -->
    '''
    
    if best_zone:
        cx = best_zone['x'] / 100 * width
        cy = best_zone['y'] / 100 * height
        r = best_zone['radius'] / 100 * min(width, height)
        svg_elements += f'''
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(105, 219, 124, 0.3)" stroke="#69db7c" stroke-width="2" stroke-dasharray="5,5"/>
        '''
    
    if correct_pos:
        cx = correct_pos['x'] / 100 * width
        cy = correct_pos['y'] / 100 * height
        r = correct_pos['radius'] / 100 * min(width, height)
        svg_elements += f'''
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(116, 192, 252, 0.3)" stroke="#74c0fc" stroke-width="2" stroke-dasharray="5,5"/>
        '''
    
    # Add opponents
    if show_opponents and opponents:
        for opp in opponents:
            x = opp['x'] / 100 * width
            y = opp['y'] / 100 * height
            svg_elements += f'''
            <circle cx="{x}" cy="{y}" r="15" fill="#ff6b6b" stroke="white" stroke-width="2"/>
            <text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="12">🔴</text>
            '''
    
    # Add partner
    if show_partner and partner:
        x = partner['x'] / 100 * width
        y = partner['y'] / 100 * height
        svg_elements += f'''
        <circle cx="{x}" cy="{y}" r="15" fill="#74c0fc" stroke="white" stroke-width="2"/>
        <text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="12">🔵</text>
        '''
    
    # Add selected position marker
    if selected_pos:
        sx = selected_pos[0] / 100 * width
        sy = selected_pos[1] / 100 * height
        color = "#69db7c" if is_correct else "#ff6b6b"
        svg_elements += f'''
        <circle cx="{sx}" cy="{sy}" r="12" fill="{color}" stroke="white" stroke-width="2"/>
        <text x="{sx}" y="{sy+4}" text-anchor="middle" fill="white" font-size="10">{chr(10004 if is_correct else 10006)}</text>
        '''
    
    svg_elements += '</svg>'
    
    return svg_elements

# ===== JavaScript for interactive clicking =====
js_code = """
<script>
let lastClickX = null;
let lastClickY = null;

function handleCourtClick(event, courtId) {
    const svg = document.getElementById(courtId);
    const rect = svg.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    
    // Store coordinates for form submission
    const xInput = document.querySelector(`input[data-court="${courtId}-x"]`);
    const yInput = document.querySelector(`input[data-court="${courtId}-y"]`);
    if (xInput && yInput) {
        xInput.value = x.toFixed(1);
        yInput.value = y.toFixed(1);
        
        // Trigger change event to update Streamlit
        xInput.dispatchEvent(new Event('change'));
        yInput.dispatchEvent(new Event('change'));
    }
}
</script>
"""

# ===== UI Components =====
st.title("🏸 Badminton Doubles Trainer")
st.markdown("### Interactive Practice — Two parts")

# Mode selection
col1, col2 = st.columns(2)
with col1:
    tab1_name = "1️⃣ Best Placement"
    tab2_name = "2️⃣ Partner Positioning"
with col2:
    ai_mode = st.toggle("🤖 AI Analysis Mode", value=st.session_state.ai_mode, key="ai_toggle")
    st.session_state.ai_mode = ai_mode

tabs = st.tabs([tab1_name, tab2_name])

# ===== SECTION 1: BIRDY PLACEMENT =====
with tabs[0]:
    st.header("Part 1: Best Birdy Placement")
    
    scenario = BIRDY_SCENARIOS[st.session_state.birdy_idx]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Q{st.session_state.birdy_idx + 1}: {scenario['name']}")
        st.info(scenario['desc'])
        
        # Display opponent positions
        st.write("**Opponents:**")
        for i, opp in enumerate(scenario['opponents']):
            st.write(f"- Opponent {i+1}: ({opp['x']}%, {opp['y']}%)")
        
        # Show interactive court
        court_html = generate_court_html(
            "placement_court",
            show_opponents=True,
            opponents=scenario['opponents'],
            best_zone=scenario['best_zone'],
            selected_pos=st.session_state.birdy_last_choice,
            is_correct=any(ans['question'] == st.session_state.birdy_idx + 1 and ans['correct'] for ans in st.session_state.birdy_answers) if any(ans['question'] == st.session_state.birdy_idx + 1 for ans in st.session_state.birdy_answers) else None
        )
        st.components.v1.html(court_html + js_code, height=750, scrolling=False)
        
        # Hidden inputs for coordinates
        click_x = st.number_input("Selected X position (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0, key="click_x", help="Auto-updated when you click on the court")
        click_y = st.number_input("Selected Y position (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0, key="click_y", help="Auto-updated when you click on the court")
        
        if st.button("Place Birdy 🎯"):
            x, y = click_x, click_y
            
            # Validate court
            if y >= 47:
                st.error("❌ This is YOUR court! Place it in the OPPONENT'S court (upper half).")
                st.session_state.birdy_last_choice = None
            else:
                best = scenario['best_zone']
                dist = ((x - best['x'])**2 + (y - best['y'])**2)**0.5
                good = dist <= best['radius']
                
                st.session_state.birdy_total += 1
                if good:
                    st.session_state.birdy_score += 1
                    st.session_state.birdy_streak += 1
                    if st.session_state.birdy_streak > st.session_state.birdy_best:
                        st.session_state.birdy_best = st.session_state.birdy_streak
                    st.success("✅ Correct! Great placement!")
                else:
                    st.session_state.birdy_streak = 0
                    st.warning(f"⚠️ Could be better. Distance from optimal: {dist:.1f}%. Think about where the opponents' gaps are.")
                
                # Store answer
                st.session_state.birdy_answers.append({
                    "question": st.session_state.birdy_idx + 1,
                    "answer": (x, y),
                    "correct": good,
                    "distance": dist
                })
                
                # Update last choice for visualization
                st.session_state.birdy_last_choice = (x, y)
                
                # Show explanation
                st.info(f"💡 {scenario['explanation']}")
                
                # AI Analysis
                if st.session_state.ai_mode:
                    with st.spinner("🤖 AI analyzing your move..."):
                        analysis = analyze_with_ai(
                            "placement",
                            (x, y),
                            scenario['name'],
                            scenario['explanation']
                        )
                    st.success(f"🤖 {analysis}")
        
        # Score display
        st.write(f"**Score:** {st.session_state.birdy_score} / {st.session_state.birdy_total} | **Best Streak:** {st.session_state.birdy_best}")
    
    with col2:
        st.subheader("Strategy Tips")
        st.markdown("""
        **Key Principles:**
        - Hit to open spaces between opponents
        - Vary your shots to keep opponents moving
        - Aim for corners when possible
        - Consider opponent positioning carefully
        
        **Visual Guide:**
        - 🔴 Red circles = Opponents
        - 🟢 Green dashed circle = Best zone
        - Click anywhere on the court to see where you're placing the birdy
        """)
        
        st.subheader("Answer History")
        if st.session_state.birdy_answers:
            for ans in st.session_state.birdy_answers[-5:]:  # Show last 5
                status = "✅" if ans["correct"] else "❌"
                st.write(f"{status} Q{ans['question']}: ({ans['answer'][0]}, {ans['answer'][1]}) - Distance: {ans['distance']:.1f}")
        else:
            st.write("No answers yet.")

# ===== SECTION 2: PARTNER POSITIONING =====
with tabs[1]:
    st.header("Part 2: Partner Positioning")
    
    scenario = PARTNER_SCENARIOS[st.session_state.pos_idx]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Q{st.session_state.pos_idx + 1}: {scenario['name']}")
        st.info(scenario['desc'])
        
        # Display partner position
        st.write("**Partner Position:**")
        st.write(f"- Partner: ({scenario['partner']['x']}%, {scenario['partner']['y']}%)")
        
        # Show interactive court
        court_html = generate_court_html(
            "positioning_court",
            show_partner=True,
            partner=scenario['partner'],
            correct_pos=scenario['correct_position'],
            selected_pos=st.session_state.pos_last_choice,
            is_correct=any(ans['question'] == st.session_state.pos_idx + 1 and ans['correct'] for ans in st.session_state.pos_answers) if any(ans['question'] == st.session_state.pos_idx + 1 for ans in st.session_state.pos_answers) else None
        )
        st.components.v1.html(court_html + js_code, height=750, scrolling=False)
        
        # Input for player position
        pos_x = st.number_input("Your X position (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0, key="pos_x", help="Auto-updated when you click on the court")
        pos_y = st.number_input("Your Y position (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0, key="pos_y", help="Auto-updated when you click on the court")
        
        if st.button("Position Yourself 📍"):
            x, y = pos_x, pos_y
            
            # Validate court
            if y <= 53:
                st.error("❌ You must stand in YOUR court (lower half)!")
                st.session_state.pos_last_choice = None
            else:
                correct = scenario['correct_position']
                dist = ((x - correct['x'])**2 + (y - correct['y'])**2)**0.2
                good = dist <= correct['radius']
                
                st.session_state.pos_total += 1
                if good:
                    st.session_state.pos_score += 1
                    st.session_state.pos_streak += 1
                    if st.session_state.pos_streak > st.session_state.pos_best:
                        st.session_state.pos_best = st.session_state.pos_streak
                    st.success("✅ Perfect positioning! Great court coverage!")
                else:
                    st.session_state.pos_streak = 0
                    st.warning(f"⚠️ Could optimize coverage. Distance from optimal: {dist:.1f}%. Think about covering open areas.")
                
                # Store answer
                st.session_state.pos_answers.append({
                    "question": st.session_state.pos_idx + 1,
                    "answer": (x, y),
                    "correct": good,
                    "distance": dist
                })
                
                # Update last choice for visualization
                st.session_state.pos_last_choice = (x, y)
                
                # Show explanation
                st.info(f"💡 {scenario['explanation']}")
                
                # AI Analysis
                if st.session_state.ai_mode:
                    with st.spinner("🤖 AI analyzing your position..."):
                        analysis = analyze_with_ai(
                            "positioning",
                            (x, y),
                            scenario['name'],
                            scenario['explanation']
                        )
                    st.success(f"🤖 {analysis}")
        
        # Score display
        st.write(f"**Score:** {st.session_state.pos_score} / {st.session_state.pos_total} | **Best Streak:** {st.session_state.pos_best}")
    
    with col2:
        st.subheader("Positioning Tips")
        st.markdown("""
        **Key Principles:**
        - Cover opposite side from partner
        - Maintain balanced court coverage
        - Adjust based on partner's movement
        - Communication is key!
        
        **Visual Guide:**
        - 👤 Blue circle = Your partner
        - 🔵 Blue dashed circle = Correct position
        - Click anywhere on your court to see where you should stand
        """)
        
        st.subheader("Answer History")
        if st.session_state.pos_answers:
            for ans in st.session_state.pos_answers[-5:]:  # Show last 5
                status = "✅" if ans["correct"] else "❌"
                st.write(f"{status} Q{ans['question']}: ({ans['answer'][0]}, {ans['answer'][1]}) - Distance: {ans['distance']:.1f}")
        else:
            st.write("No answers yet.")

# ===== Navigation Buttons =====
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Next Scenario ➡️"):
        st.session_state.birdy_idx = (st.session_state.birdy_idx + 1) % len(BIRDY_SCENARIOS)
        st.session_state.birdy_last_choice = None
        st.rerun()
with col2:
    if st.button("Clear Answers 🗑️"):
        st.session_state.birdy_answers = []
        st.session_state.pos_answers = []
        st.session_state.birdy_last_choice = None
        st.session_state.pos_last_choice = None
        st.rerun()
with col3:
    if st.button("Reset Scores 🔄"):
        st.session_state.birdy_score = 0
        st.session_state.birdy_total = 0
        st.session_state.birdy_streak = 0
        st.session_state.birdy_best = 0
        st.session_state.pos_score = 0
        st.session_state.pos_total = 0
        st.session_state.pos_streak = 0
        st.session_state.pos_best = 0
        st.session_state.birdy_answers = []
        st.session_state.pos_answers = []
        st.session_state.birdy_last_choice = None
        st.session_state.pos_last_choice = None
        st.rerun()

st.markdown("---")
st.markdown("💡 **Tip:** Use AI mode to get personalized feedback on your moves! Click directly on the court to practice!")
