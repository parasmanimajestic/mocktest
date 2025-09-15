import streamlit as st
import json

# Hide Streamlit header elements (three-dot menu, GitHub/Fork buttons)
st.markdown("""
    <style>
        /* Hide the three-dot hamburger menu */
        section[data-testid="stSidebar"] > div > div > div > div > div > div:first-child {
            display: none !important;
        }
        /* Alternative selector for the menu (if the above doesn't work) */
        .st-emotion-cache-1r4w99q {
            display: none !important;
        }
        /* Hide GitHub/Fork buttons in header */
        [data-testid="stHeader"] a[href*="github"] {
            display: none !important;
        }
        /* Hide the "Made with Streamlit" footer */
        footer {
            display: none !important;
        }
        /* Ensure header is clean */
        header > .css-1v3fvcr {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Function to load questions from uploaded file or default
def load_questions(uploaded_file):
    if uploaded_file is not None:
        try:
            questions = json.load(uploaded_file)
            return questions
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON.")
            return None
    # Load default questions.json if available
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("No default questions.json found. Please upload a JSON file.")
        return None

# Main app
st.title("MCQ Mock Test App")

# Step 1: Upload questions
uploaded_file = st.file_uploader("Upload your questions JSON file", type="json")
questions = load_questions(uploaded_file)

if questions:
    # Step 2: Display the test form
    st.header("Take the Test")
    with st.form(key="quiz_form"):
        user_answers = []
        for i, q in enumerate(questions):
            st.subheader(f"Question {i+1}: {q['question']}")
            selected = st.radio("Options:", q['options'], key=f"q{i}", index=None)
            user_answers.append(q['options'].index(selected) if selected else -1)
        
        submit_button = st.form_submit_button("Submit Test")
    
    if submit_button:
        # Step 3: Calculate and display results
        st.header("Results")
        score = 0
        total = len(questions)
        for i, q in enumerate(questions):
            user_ans = user_answers[i]
            correct_ans = q['answer'] - 1  # Convert 1-based option number to 0-based index
            if user_ans == correct_ans:
                score += 1
                st.success(f"Question {i+1}: Correct! (Your answer: Option {user_ans + 1} - {q['options'][user_ans]})")
            else:
                st.error(f"Question {i+1}: Incorrect. Correct answer: Option {correct_ans + 1} - {q['options'][correct_ans]} (Your answer: Option {user_ans + 1 if user_ans != -1 else 'None'} - {q['options'][user_ans] if user_ans != -1 else 'None'})")
        
        st.info(f"Your score: {score}/{total} ({(score/total)*100:.2f}%)")

else:
    st.info("Upload a JSON file or ensure a default questions.json is in the project folder.")