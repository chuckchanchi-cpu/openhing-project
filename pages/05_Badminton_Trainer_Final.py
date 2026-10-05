import streamlit as st
import random

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
if 'birdy_answered' not in st.session_state:
    st.session_state.birdy_answered = False
if 'birdy_result' not in st.session_state:
    st.session_state.birdy_result = None

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
if 'pos_answered' not in st.session_state:
    st.session_state.pos_answered = False
if 'pos_result' not in st.session_state:
    st.session_state.pos_result = None

if 'ai_mode' not in st.session_state:
    st.session_state.ai_mode = False

def check_placement(x, y, scenario):
    """Check if placement is correct"""
    best = scenario['best_zone']
    dist = ((x - best['x'])**2 + (y - best['y'])**2)**0.5
    good = dist <= best['radius']
    return good, dist, best

def check_positioning(x, y, scenario):
    """Check if positioning is correct"""
    correct = scenario['correct_position']
    dist = ((x - correct['x'])**2 + (y - correct['y'])**2)**0.2
    good = dist <= correct['radius']
    return good, dist, correct

# ===== Generate Court HTML with Clickable Zones =====
def generate_court_html(court_id, width=400, height=700, show_opponents=False, show_partner=False, 
                        opponents=None, partner=None, best_zone=None, correct_pos=None,
                        selected_pos=None, is_correct=None):
    """Generate SVG court visualization"""
    
    svg_elements = f'''
    <svg id="{court_id}" width="{width}" height="{height}" style="border: 3px solid white; border-radius: 10px; background: linear-gradient(to bottom, #1a8a3c, #0f5e2b);">
        <!-- Net -->
        <line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#ffd43b" stroke-width="4"/>
        
        <!-- Service lines -->
        <line x1="{width/2}" y1="0" x2="{width/2}" y2="{height}" stroke="white" stroke-width="2" opacity="0.5"/>
        <line x1="0" y1="{height*0.15}" x2="{width}" y2="{height*0.15}" stroke="white" stroke-width="2" opacity="0.5"/>
        <line x1="0" y1="{height*0.85}" x2="{width}" y2="{height*0.85}" stroke="white" stroke-width="2" opacity="0.5"/>
        
        <!-- Labels -->
        <text x="{width/2}" y="30" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Opponents</text>
        <text x="{width/2}" y="{height-20}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">You</text>
    '''
    
    # Best zone indicator
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
        
        # Show court visualization
        court_html = generate_court_html(
            "placement_court",
            show_opponents=True,
            opponents=scenario['opponents'],
            best_zone=scenario['best_zone'],
            selected_pos=st.session_state.birdy_result['answer'] if st.session_state.birdy_answered and st.session_state.birdy_result else None,
            is_correct=st.session_state.birdy_result['correct'] if st.session_state.birdy_answered and st.session_state.birdy_result else None
        )
        st.components.v1.html(court_html, height=750, scrolling=False)
        
        # Create clickable grid buttons
        st.write("**Click on the court to place the birdy:**")
        cols = st.columns(10)
        
        for row in range(10):
            for col in range(10):
                x_pct = (col + 0.5) * 10
                y_pct = (row + 0.5) * 10
                
                # Only make opponent court (top half) clickable for placement
                if y_pct >= 47:
                    continue
                
                btn_key = f"birdy_{row}_{col}"
                if st.button(f"{int(x_pct)}%", key=btn_key, help=f"Place at ({x_pct:.0f}%, {y_pct:.0f}%)"):
                    x, y = x_pct, y_pct
                    
                    best = scenario['best_zone']
                    good, dist, _ = check_placement(x, y, scenario)
                    
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
                    
                    # Update result for visualization
                    st.session_state.birdy_answered = True
                    st.session_state.birdy_result = {"answer": (x, y), "correct": good, "distance": dist}
                    
                    # Show explanation
                    st.info(f"💡 {scenario['explanation']}")
                    
                    # Rerun to update visualization
                    st.rerun()
        
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
        - Click anywhere on the court to place the birdy!
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
        
        # Show court visualization
        court_html = generate_court_html(
            "positioning_court",
            show_partner=True,
            partner=scenario['partner'],
            correct_pos=scenario['correct_position'],
            selected_pos=st.session_state.pos_result['answer'] if st.session_state.pos_answered and st.session_state.pos_result else None,
            is_correct=st.session_state.pos_result['correct'] if st.session_state.pos_answered and st.session_state.pos_result else None
        )
        st.components.v1.html(court_html, height=750, scrolling=False)
        
        # Create clickable grid buttons
        st.write("**Click on the court to choose your position:**")
        cols = st.columns(10)
        
        for row in range(10):
            for col in range(10):
                x_pct = (col + 0.5) * 10
                y_pct = (row + 0.5) * 10
                
                # Only make your court (bottom half) clickable for positioning
                if y_pct <= 53:
                    continue
                
                btn_key = f"pos_{row}_{col}"
                if st.button(f"{int(x_pct)}%", key=btn_key, help=f"Stand at ({x_pct:.0f}%, {y_pct:.0f}%)"):
                    x, y = x_pct, y_pct
                    
                    correct = scenario['correct_position']
                    good, dist, _ = check_positioning(x, y, scenario)
                    
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
                    
                    # Update result for visualization
                    st.session_state.pos_answered = True
                    st.session_state.pos_result = {"answer": (x, y), "correct": good, "distance": dist}
                    
                    # Show explanation
                    st.info(f"💡 {scenario['explanation']}")
                    
                    # Rerun to update visualization
                    st.rerun()
        
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
        - Click anywhere on your court to choose where to stand!
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
        st.session_state.birdy_answered = False
        st.session_state.birdy_result = None
        st.rerun()
with col2:
    if st.button("Clear Answers 🗑️"):
        st.session_state.birdy_answers = []
        st.session_state.pos_answers = []
        st.session_state.birdy_answered = False
        st.session_state.birdy_result = None
        st.session_state.pos_answered = False
        st.session_state.pos_result = None
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
        st.session_state.birdy_answered = False
        st.session_state.birdy_result = None
        st.session_state.pos_answered = False
        st.session_state.pos_result = None
        st.rerun()

st.markdown("---")
st.markdown("💡 **Tip:** Click directly on the court image to place the birdy or choose your position!")
