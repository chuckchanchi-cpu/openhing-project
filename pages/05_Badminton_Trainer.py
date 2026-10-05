import streamlit as st
import random
import json

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

if 'ai_mode' not in st.session_state:
    st.session_state.ai_mode = False

# ===== AI Analysis Function =====
def analyze_badminton_move(move_type, position, opponent_positions=None, partner_position=None):
    """AI analysis of badminton doubles move"""
    
    analysis = {
        "move_type": move_type,
        "position": position,
        "rating": "",
        "reason": "",
        "suggestion": ""
    }
    
    if move_type == "placement":
        # Analyze birdy placement
        x, y = position
        if y < 47:  # Opponent's court
            # Check distance from best zone
            scenario = BIRDY_SCENARIOS[st.session_state.birdy_idx]
            best = scenario["best_zone"]
            dist = ((x - best["x"])**2 + (y - best["y"])**2)**0.5
            
            if dist <= best["radius"]:
                analysis["rating"] = "✅ Excellent!"
                analysis["reason"] = f"Perfect placement! You hit the open space between opponents."
                analysis["suggestion"] = "Keep this strategy against similar formations."
            elif dist <= best["radius"] * 1.5:
                analysis["rating"] = "⚠️ Good try"
                analysis["reason"] = "Decent placement but could be better."
                analysis["suggestion"] = f"Try aiming closer to ({best['x']}, {best['y']}) for optimal coverage."
            else:
                analysis["rating"] = "❌ Not ideal"
                analysis["reason"] = "This placement is too far from the optimal zone."
                analysis["suggestion"] = f"Focus on hitting towards the open areas, especially around ({best['x']}, {best['y']})."
        else:
            analysis["rating"] = "❌ Wrong court"
            analysis["reason"] = "You placed the birdy in your own court!"
            analysis["suggestion"] = "Always place the birdy in the OPPONENT'S court (upper half)."
            
    elif move_type == "positioning":
        # Analyze partner positioning
        x, y = position
        scenario = PARTNER_SCENARIOS[st.session_state.pos_idx]
        correct = scenario["correct_position"]
        dist = ((x - correct["x"])**2 + (y - correct["y"])**2)**0.2
        
        if dist <= correct["radius"]:
            analysis["rating"] = "✅ Perfect positioning!"
            analysis["reason"] = "Great court coverage with your partner!"
            analysis["suggestion"] = "Maintain this formation pattern."
        elif dist <= correct["radius"] * 1.5:
            analysis["rating"] = "⚠️ Acceptable"
            analysis["reason"] = "Reasonable positioning but could optimize coverage."
            analysis["suggestion"] = f"Move closer to ({correct['x']}, {correct['y']}) for better defense."
        else:
            analysis["rating"] = "❌ Poor positioning"
            analysis["reason"] = "This leaves a large gap in court coverage."
            analysis["suggestion"] = f"Stand more towards ({correct['x']}, {correct['y']}) to cover the open area."
    
    return analysis

# ===== UI Components =====
st.title("🏸 Badminton Doubles Trainer")
st.markdown("### Practice game — Two parts")

# Mode selection
mode_col1, mode_col2 = st.columns(2)
with mode_col1:
    tab1 = st.tabs(["1️⃣ Best Placement", "2️⃣ Partner Positioning"])[0]
with mode_col2:
    ai_mode = st.toggle("🤖 AI Analysis Mode", value=st.session_state.ai_mode, key="ai_toggle")
    st.session_state.ai_mode = ai_mode

# ===== SECTION 1: BIRDY PLACEMENT =====
with st.container():
    st.header("Part 1: Best Birdy Placement")
    
    scenario = BIRDY_SCENARIOS[st.session_state.birdy_idx]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Q{st.session_state.birdy_idx + 1}: {scenario['name']}")
        st.info(scenario['desc'])
        
        # Court visualization using coordinates
        court_width, court_height = 400, 800
        st.write(f"**Court Size:** {court_width} × {court_height}")
        st.write("**Instructions:** Click on the opponent's court (top half) where you want to place the birdy.")
        
        # Display opponent positions
        st.write("**Opponents:**")
        for i, opp in enumerate(scenario['opponents']):
            st.write(f"- Opponent {i+1}: ({opp['x']}%, {opp['y']}%)")
        
        # Input for player click
        click_x = st.number_input("X position (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0, key="click_x")
        click_y = st.number_input("Y position (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0, key="click_y")
        
        if st.button("Place Birdy 🎯"):
            x, y = click_x, click_y
            
            # Validate court
            if y >= 47:
                st.error("❌ This is YOUR court! Place it in the OPPONENT'S court (upper half).")
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
                    st.warning("⚠️ Could be better. Think about where the opponents' gaps are.")
                
                # Store answer
                st.session_state.birdy_answers.append({
                    "question": st.session_state.birdy_idx + 1,
                    "answer": (x, y),
                    "correct": good,
                    "distance": dist
                })
                
                # Show explanation
                st.info(f"💡 {scenario['explanation']}")
                
                # AI Analysis
                if st.session_state.ai_mode:
                    analysis = analyze_badminton_move("placement", (x, y))
                    st.json(analysis)
        
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
        """)
        
        st.subheader("Answer History")
        if st.session_state.birdy_answers:
            for ans in st.session_state.birdy_answers[-5:]:  # Show last 5
                status = "✅" if ans["correct"] else "❌"
                st.write(f"{status} Q{ans['question']}: ({ans['answer'][0]}, {ans['answer'][1]}) - Distance: {ans['distance']:.1f}")
        else:
            st.write("No answers yet.")

# ===== SECTION 2: PARTNER POSITIONING =====
with st.container():
    st.header("Part 2: Partner Positioning")
    
    scenario = PARTNER_SCENARIOS[st.session_state.pos_idx]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Q{st.session_state.pos_idx + 1}: {scenario['name']}")
        st.info(scenario['desc'])
        
        # Display partner position
        st.write("**Partner Position:**")
        st.write(f"- Partner: ({scenario['partner']['x']}%, {scenario['partner']['y']}%)")
        
        # Input for player position
        pos_x = st.number_input("Your X position (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0, key="pos_x")
        pos_y = st.number_input("Your Y position (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0, key="pos_y")
        
        if st.button("Position Yourself 📍"):
            x, y = pos_x, pos_y
            
            # Validate court
            if y <= 53:
                st.error("❌ You must stand in YOUR court (lower half)!")
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
                    st.warning("⚠️ Could optimize coverage. Think about covering open areas.")
                
                # Store answer
                st.session_state.pos_answers.append({
                    "question": st.session_state.pos_idx + 1,
                    "answer": (x, y),
                    "correct": good,
                    "distance": dist
                })
                
                # Show explanation
                st.info(f"💡 {scenario['explanation']}")
                
                # AI Analysis
                if st.session_state.ai_mode:
                    analysis = analyze_badminton_move("positioning", (x, y))
                    st.json(analysis)
        
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
        st.rerun()
with col2:
    if st.button("Clear Answers 🗑️"):
        st.session_state.birdy_answers = []
        st.session_state.pos_answers = []
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
        st.rerun()

st.markdown("---")
st.markdown("💡 **Tip:** Use AI mode to get personalized feedback on your moves!")
