"""
🐍 Python Quest - A Fun Game to Learn Python!
For Primary 6 students (age 11-12)
Run with: streamlit run python_quest.py
"""

import streamlit as st
import random
import time

# Page config
st.set_page_config(
    page_title="🐍 Python Quest",
    page_icon="🐍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.5em;
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.score-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px;
    border-radius: 10px;
    color: white;
    text-align: center;
    font-size: 1.2em;
}
.code-block {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 15px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
}
.success { color: #4CAF50; font-weight: bold; }
.fail { color: #f44336; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.badges = []
    st.session_state.current_game = None
    st.session_state.streak = 0

# ──────────────────────────────────────────────────────────
# GAME 1: Guess the Number (Teaches: variables, input, loops)
# ──────────────────────────────────────────────────────────
def game_guess_number():
    st.header("🎯 Level 1: Guess the Number")
    
    st.markdown("""
    **Learn Python concepts:** Variables, Input, While Loop, If/Else
    
    ```python
    # This is how Python code looks!
    secret_number = random.randint(1, 100)
    guess = 0
    
    while guess != secret_number:
        guess = int(input("Guess a number (1-100): "))
        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print("🎉 You got it!")
    ```
    """)
    
    # Game logic
    if 'gtn_number' not in st.session_state:
        st.session_state.gtn_number = random.randint(1, 100)
        st.session_state.gtn_attempts = 0
        st.session_state.gtn_won = False
    
    if not st.session_state.gtn_won:
        col1, col2 = st.columns([2, 1])
        with col1:
            guess = st.number_input("Guess a number (1-100):", min_value=1, max_value=100, value=50, key="gtn_input")
        with col2:
            st.write(f"Attempts: {st.session_state.gtn_attempts}")
        
        if st.button("🎯 Submit Guess", key="gtn_submit"):
            st.session_state.gtn_attempts += 1
            secret = st.session_state.gtn_number
            
            if guess < secret:
                st.warning("⬆️ Too low! Try a higher number.")
            elif guess > secret:
                st.warning("⬇️ Too high! Try a lower number.")
            else:
                st.session_state.gtn_won = True
                st.balloons()
                points = max(100 - (st.session_state.gtn_attempts * 10), 10)
                st.session_state.score += points
                if "🎯 Guess Master" not in st.session_state.badges:
                    st.session_state.badges.append("🎯 Guess Master")
                st.success(f"🎉 You got it in {st.session_state.gtn_attempts} attempts! +{points} points")
        
        if st.session_state.gtn_attempts > 0 and not st.session_state.gtn_won:
            st.info(f"💡 Hint: The number is {'higher' if guess < st.session_state.gtn_number else 'lower'} than {guess}")
    else:
        st.success(f"✅ Completed! Number was {st.session_state.gtn_number}")
        if st.button("🔄 Play Again", key="gtn_again"):
            del st.session_state.gtn_number
            del st.session_state.gtn_attempts
            del st.session_state.gtn_won
            st.rerun()

# ──────────────────────────────────────────────────────────
# GAME 2: Python Quiz (Teaches: lists, dictionaries, functions)
# ──────────────────────────────────────────────────────────
def game_quiz():
    st.header("📝 Level 2: Python Quiz")
    
    st.markdown("""
    **Learn Python concepts:** Lists, Dictionaries, Functions, Print
    
    ```python
    # A dictionary stores key-value pairs
    question = {
        "question": "What does print() do?",
        "options": ["Shows text", "Deletes files", "Makes sounds"],
        "answer": "Shows text"
    }
    
    # A function is reusable code
    def check_answer(user_answer, correct):
        if user_answer == correct:
            return "Correct! 🎉"
        return "Try again! ❌"
    ```
    """)
    
    questions = [
        {
            "q": "What does `print('Hello')` do?",
            "options": ["Shows 'Hello' on screen", "Deletes Hello", "Sends an email", "Creates a file"],
            "answer": "Shows 'Hello' on screen",
            "explain": "print() shows text on the screen. It's like putting text in the chat!"
        },
        {
            "q": "Which one stores a list of items?",
            "options": ["print()", "[1, 2, 3]", "if/else", "while"],
            "answer": "[1, 2, 3]",
            "explain": "Square brackets [] create a list. Like a shopping list: ['eggs', 'milk', 'bread']"
        },
        {
            "q": "What does `if x > 10:` mean?",
            "options": ["Always do something", "Do something only if x is bigger than 10", "Make x bigger than 10", "Count to 10"],
            "answer": "Do something only if x is bigger than 10",
            "explain": "'if' checks a condition. If it's true, the code runs. If not, it skips!"
        },
        {
            "q": "How do you make a loop that counts 5 times?",
            "options": ["loop(5)", "for i in range(5):", "count = 5", "5 times do:"],
            "answer": "for i in range(5):",
            "explain": "'for i in range(5)' repeats code 5 times. i will be 0,1,2,3,4"
        },
        {
            "q": "What is a variable?",
            "options": ["A type of loop", "A box that stores data", "A math equation", "A Python error"],
            "answer": "A box that stores data",
            "explain": "Variables are like labeled boxes. x = 5 puts 5 in the box named 'x'"
        },
        {
            "q": "What does `len('hello')` return?",
            "options": ["'hello'", "5", "0", "Error"],
            "answer": "5",
            "explain": "len() counts how many characters. 'hello' has 5 letters!"
        },
        {
            "q": "Which is the correct way to define a function?",
            "options": ["function myFunc():", "def myFunc():", "make myFunc():", "func myFunc():"],
            "answer": "def myFunc():",
            "explain": "'def' is short for 'define'. It creates a new function in Python!"
        },
        {
            "q": "What will `2 ** 3` give you?",
            "options": ["6", "8", "5", "23"],
            "answer": "8",
            "explain": "** means 'power of'. 2**3 = 2×2×2 = 8. Like 2 to the power of 3!"
        }
    ]
    
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_correct = 0
        st.session_state.quiz_answered = False
    
    idx = st.session_state.quiz_index
    
    if idx < len(questions):
        q = questions[idx]
        st.progress((idx) / len(questions))
        st.subheader(f"Question {idx+1}/{len(questions)}")
        st.write(f"**{q['q']}**")
        
        answer = st.radio("Choose your answer:", q['options'], key=f"quiz_{idx}")
        
        if not st.session_state.quiz_answered:
            if st.button("✅ Submit", key=f"quiz_submit_{idx}"):
                st.session_state.quiz_answered = True
                if answer == q['answer']:
                    st.session_state.quiz_correct += 1
                    st.session_state.score += 20
                    st.session_state.streak += 1
                    st.success(f"🎉 Correct! {q['explain']}")
                    if st.session_state.streak >= 3:
                        st.info(f"🔥 {st.session_state.streak} in a row! On fire!")
                else:
                    st.session_state.streak = 0
                    st.error(f"❌ The answer is: **{q['answer']}**")
                    st.info(f"💡 {q['explain']}")
        else:
            if st.button("➡️ Next Question", key=f"quiz_next_{idx}"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.rerun()
    else:
        st.balloons()
        score = st.session_state.quiz_correct
        st.success(f"🏆 Quiz Complete! You got {score}/{len(questions)} correct!")
        if score >= 6 and "📝 Quiz Master" not in st.session_state.badges:
            st.session_state.badges.append("📝 Quiz Master")
        if st.button("🔄 Retry Quiz", key="quiz_retry"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_correct = 0
            st.session_state.quiz_answered = False
            st.session_state.streak = 0
            st.rerun()

# ──────────────────────────────────────────────────────────
# GAME 3: Code Builder (Teaches: syntax, sequencing)
# ──────────────────────────────────────────────────────────
def game_code_builder():
    st.header("🔧 Level 3: Code Builder")
    
    st.markdown("""
    **Learn Python concepts:** Code order, Indentation, Syntax
    
    Drag and drop? Nah, we're coding! Put the lines in the correct order.
    """)
    
    challenges = [
        {
            "title": "Make a greeting program",
            "lines": ['name = "Alice"', 'print("Hello, " + name + "!")', 'print("Welcome to Python!")'],
            "correct_order": [0, 2, 1],
            "hint": "First set the name, then welcome, then greet"
        },
        {
            "title": "Count from 1 to 5",
            "lines": ['for i in range(1, 6):', '    print(i)', 'print("Done counting!")'],
            "correct_order": [0, 1, 2],
            "hint": "Set up the loop, print inside the loop, then print after"
        },
        {
            "title": "Check if number is positive",
            "lines": ['x = 10', 'if x > 0:', '    print("Positive!")', 'else:', '    print("Negative!")'],
            "correct_order": [0, 1, 2, 3, 4],
            "hint": "Set x, check condition, handle both cases"
        },
        {
            "title": "Create and use a function",
            "lines": ['def add(a, b):', '    return a + b', 'result = add(3, 5)', 'print(result)'],
            "correct_order": [0, 1, 2, 3],
            "hint": "Define function, return value, call it, print result"
        }
    ]
    
    if 'cb_index' not in st.session_state:
        st.session_state.cb_index = 0
        st.session_state.cb_completed = []
    
    idx = st.session_state.cb_index
    
    if idx < len(challenges):
        ch = challenges[idx]
        st.subheader(f"Challenge {idx+1}/{len(challenges)}: {ch['title']}")
        st.progress(idx / len(challenges))
        
        st.write("**Put these lines in the correct order:**")
        
        # Show shuffled lines
        if f"cb_shuffled_{idx}" not in st.session_state:
            shuffled = list(range(len(ch['lines'])))
            random.shuffle(shuffled)
            st.session_state[f"cb_shuffled_{idx}"] = shuffled
        
        shuffled = st.session_state[f"cb_shuffled_{idx}"]
        
        user_order = []
        for i, pos in enumerate(shuffled):
            selected = st.selectbox(
                f"Position {i+1}:",
                options=list(range(len(ch['lines']))),
                format_func=lambda x: ch['lines'][x],
                key=f"cb_select_{idx}_{i}",
                index=0
            )
            user_order.append(selected)
        
        st.info(f"💡 Hint: {ch['hint']}")
        
        if st.button("✅ Check Order", key=f"cb_check_{idx}"):
            if user_order == ch['correct_order']:
                st.session_state.score += 30
                st.session_state.cb_completed.append(idx)
                if "🔧 Code Builder" not in st.session_state.badges:
                    st.session_state.badges.append("🔧 Code Builder")
                st.success("🎉 Perfect order!")
                st.code('\n'.join(ch['lines']), language='python')
            else:
                st.error("❌ Not quite right. Try again!")
        
        col1, col2 = st.columns(2)
        with col1:
            if idx > 0 and st.button("⬅️ Previous", key="cb_prev"):
                st.session_state.cb_index -= 1
                st.rerun()
        with col2:
            if st.button("➡️ Next Challenge", key="cb_next"):
                st.session_state.cb_index += 1
                st.rerun()
    else:
        st.balloons()
        st.success(f"🏆 All {len(challenges)} challenges completed!")
        if st.button("🔄 Retry", key="cb_retry"):
            st.session_state.cb_index = 0
            st.session_state.cb_completed = []
            st.rerun()

# ──────────────────────────────────────────────────────────
# GAME 4: Bug Hunter (Teaches: debugging, error finding)
# ──────────────────────────────────────────────────────────
def game_bug_hunter():
    st.header("🐛 Level 4: Bug Hunter")
    
    st.markdown("""
    **Learn Python concepts:** Debugging, Syntax Errors, Logic Errors
    
    Real programmers spend 50% of their time finding bugs! 🐛
    """)
    
    bugs = [
        {
            "buggy": 'print("Hello World")',
            "correct": 'print("Hello World")',
            "bug_type": "no_bug",
            "hint": "This one is actually correct! Always check carefully.",
            "explanation": "Sometimes code is correct! Good programmers verify before changing."
        },
        {
            "buggy": 'prnt("Hello")',
            "correct": 'print("Hello")',
            "bug_type": "typo",
            "hint": "Look at the function name closely...",
            "explanation": "print() has a 'i' in it! Typos are the #1 bug in Python."
        },
        {
            "buggy": 'if x = 5:\n    print("five")',
            "correct": 'if x == 5:\n    print("five")',
            "bug_type": "operator",
            "hint": "How do you CHECK if something equals something?",
            "explanation": "= means ASSIGN (put a value in). == means CHECK (is it equal?)"
        },
        {
            "buggy": 'for i in range(5)\n    print(i)',
            "correct": 'for i in range(5):\n    print(i)',
            "bug_type": "missing_colon",
            "hint": "What's missing at the end of the for line?",
            "explanation": "Python needs a colon (:) after for, if, while, def lines!"
        },
        {
            "buggy": 'name = "Bob"\nprint("Hello " + name)',
            "correct": 'name = "Bob"\nprint("Hello " + name)',
            "bug_type": "no_bug",
            "hint": "Is this actually wrong? Check carefully!",
            "explanation": "This is correct! String concatenation with + works fine."
        },
        {
            "buggy": 'x = 10\ny = 3\nprint(x / y)',
            "correct": 'x = 10\ny = 3\nprint(x // y)',
            "bug_type": "division",
            "hint": "Do you want a whole number or decimal result?",
            "explanation": "/ gives decimal (3.333). // gives whole number (3). Use // for integer division!"
        },
        {
            "buggy": 'numbers = [1, 2, 3]\nprint(numbers[3])',
            "correct": 'numbers = [1, 2, 3]\nprint(numbers[2])',
            "bug_type": "index",
            "hint": "Lists start counting from...",
            "explanation": "Lists start at 0! [1,2,3] → index 0=1, index 1=2, index 2=3. There's no index 3!"
        },
        {
            "buggy": 'def greet(name)\n    print("Hi " + name)',
            "correct": 'def greet(name):\n    print("Hi " + name)',
            "bug_type": "missing_colon",
            "hint": "What goes after the function definition?",
            "explanation": "def lines need a colon (:) at the end, just like for and if!"
        }
    ]
    
    if 'bh_index' not in st.session_state:
        st.session_state.bh_index = 0
        st.session_state.bh_correct = 0
        st.session_state.bh_answered = False
    
    idx = st.session_state.bh_index
    
    if idx < len(bugs):
        bug = bugs[idx]
        st.subheader(f"Bug {idx+1}/{len(bugs)}")
        st.progress(idx / len(bugs))
        
        st.write("**Find the bug in this code:**")
        st.code(bug['buggy'], language='python')
        
        if not st.session_state.bh_answered:
            choice = st.radio("Is there a bug?", ["🐛 Yes, there's a bug!", "✅ This code is correct!"], key=f"bh_{idx}")
            
            if st.button("🔍 Check", key=f"bh_check_{idx}"):
                st.session_state.bh_answered = True
                is_correct = (choice.startswith("🐛") and bug['bug_type'] != "no_bug") or \
                            (choice.startswith("✅") and bug['bug_type'] == "no_bug")
                
                if is_correct:
                    st.session_state.bh_correct += 1
                    st.session_state.score += 25
                    st.success(f"🎉 Correct! {bug['explanation']}")
                else:
                    st.error(f"❌ {bug['explanation']}")
                
                if bug['bug_type'] != "no_bug":
                    st.code(bug['correct'], language='python')
                    st.caption("✅ Fixed version")
        else:
            if st.button("➡️ Next Bug", key=f"bh_next_{idx}"):
                st.session_state.bh_index += 1
                st.session_state.bh_answered = False
                st.rerun()
    else:
        st.balloons()
        score = st.session_state.bh_correct
        st.success(f"🏆 Bug Hunt Complete! Found {score}/{len(bugs)} bugs correctly!")
        if score >= 6 and "🐛 Bug Hunter" not in st.session_state.badges:
            st.session_state.badges.append("🐛 Bug Hunter")
        if st.button("🔄 Retry", key="bh_retry"):
            st.session_state.bh_index = 0
            st.session_state.bh_correct = 0
            st.session_state.bh_answered = False
            st.rerun()

# ──────────────────────────────────────────────────────────
# GAME 5: Python Turtle Drawing (Teaches: loops, functions)
# ──────────────────────────────────────────────────────────
def game_drawing():
    st.header("🎨 Level 5: Pattern Designer")
    
    st.markdown("""
    **Learn Python concepts:** Loops, Math, Turtle Graphics
    
    ```python
    import turtle
    
    for i in range(4):
        t.forward(100)
        t.right(90)
    # This draws a square!
    ```
    """)
    
    pattern = st.selectbox("Choose a pattern:", [
        "Square", "Triangle", "Star", "Circle Spiral", "Diamond"
    ], key="draw_pattern")
    
    size = st.slider("Size:", 50, 200, 100, key="draw_size")
    color = st.color_picker("Color:", "#FF6B6B", key="draw_color")
    
    # Generate code
    code_templates = {
        "Square": f"""import turtle
t = turtle.Turtle()
t.color("{color}")
for i in range(4):
    t.forward({size})
    t.right(90)
turtle.done()""",
        "Triangle": f"""import turtle
t = turtle.Turtle()
t.color("{color}")
for i in range(3):
    t.forward({size})
    t.right(120)
turtle.done()""",
        "Star": f"""import turtle
t = turtle.Turtle()
t.color("{color}")
for i in range(5):
    t.forward({size})
    t.right(144)
turtle.done()""",
        "Circle Spiral": f"""import turtle
t = turtle.Turtle()
t.color("{color}")
for i in range(20):
    t.circle({size} - i * 5)
    t.right(18)
turtle.done()""",
        "Diamond": f"""import turtle
t = turtle.Turtle()
t.color("{color}")
for i in range(4):
    t.forward({size})
    if i % 2 == 0:
        t.right(60)
    else:
        t.right(120)
turtle.done()"""
    }
    
    st.code(code_templates[pattern], language='python')
    
    st.markdown("""
    **How to run this:**
    1. Copy the code above
    2. Open IDLE (comes with Python)
    3. Paste and press F5
    4. Watch the magic! ✨
    """)
    
    if st.button("✅ I ran it! (+20 points)", key="draw_done"):
        st.session_state.score += 20
        if "🎨 Pattern Designer" not in st.session_state.badges:
            st.session_state.badges.append("🎨 Pattern Designer")
        st.balloons()
        st.success("🎉 Great job! You're a Python artist!")

# ──────────────────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────────────────
def main():
    st.markdown('<h1 class="main-title">🐍 Python Quest 🐍</h1>', unsafe_allow_html=True)
    st.markdown("### Learn Python by playing games! 🎮")
    
    # Sidebar - Score & Navigation
    with st.sidebar:
        st.header("📊 Your Progress")
        st.markdown(f"""
        <div class="score-box">
            <h2>⭐ {st.session_state.score} Points</h2>
            <p>Level {st.session_state.level}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        
        if st.session_state.badges:
            st.header("🏆 Badges")
            for badge in st.session_state.badges:
                st.write(f"  {badge}")
        else:
            st.header("🏆 Badges")
            st.write("  Play games to earn badges!")
        
        st.write("---")
        st.header("🎮 Games")
        game = st.radio("Choose a game:", [
            "🏠 Home",
            "🎯 Guess the Number",
            "📝 Python Quiz",
            "🔧 Code Builder",
            "🐛 Bug Hunter",
            "🎨 Pattern Designer"
        ], key="game_select")
        
        st.write("---")
        st.markdown("""
        **💡 Tips:**
        - Each game teaches different Python skills
        - Earn points and badges
        - Read the code examples!
        - Have fun! 🎉
        """)
    
    # Main content
    if game == "🏠 Home":
        show_home()
    elif game == "🎯 Guess the Number":
        game_guess_number()
    elif game == "📝 Python Quiz":
        game_quiz()
    elif game == "🔧 Code Builder":
        game_code_builder()
    elif game == "🐛 Bug Hunter":
        game_bug_hunter()
    elif game == "🎨 Pattern Designer":
        game_drawing()

def show_home():
    st.markdown("""
    ## Welcome to Python Quest! 🐍🎮
    
    Learn Python programming by playing **5 fun games**:
    
    | Game | What You'll Learn | Difficulty |
    |------|-------------------|------------|
    | 🎯 Guess the Number | Variables, Input, Loops | ⭐ |
    | 📝 Python Quiz | Lists, Functions, Print | ⭐⭐ |
    | 🔧 Code Builder | Code Order, Syntax | ⭐⭐ |
    | 🐛 Bug Hunter | Debugging, Errors | ⭐⭐⭐ |
    | 🎨 Pattern Designer | Loops, Turtle Graphics | ⭐⭐ |
    
    ---
    
    ### 🚀 Ready to start?
    
    Pick a game from the sidebar and begin your Python adventure!
    
    **Remember:** Every great programmer started by playing with code. You're doing the same thing! 💪
    
    ---
    
    ### 📚 Quick Python Reference
    
    ```python
    # Variables - store data
    name = "Your Name"
    age = 11
    score = 100
    
    # Print - show text
    print("Hello, " + name + "!")
    
    # If - make decisions
    if age > 10:
        print("You're a tween!")
    
    # Loop - repeat things
    for i in range(5):
        print("Python is fun!")
    
    # Function - reusable code
    def say_hello(person):
        print("Hello, " + person)
    
    say_hello("World")
    ```
    """)

if __name__ == "__main__":
    main()