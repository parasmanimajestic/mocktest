import streamlit as st
import json

# Sample questions as a string for download
SAMPLE_QUESTIONS = '''[
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "Madrid", "Rome"],
        "answer": 2
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": 2
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": 2
    }
]'''

# Function to load questions from uploaded file
def load_questions(uploaded_file):
    if uploaded_file is not None:
        try:
            questions = json.load(uploaded_file)
            return questions
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON.")
            return None
    return None

# Main app
st.title("MCQ Mock Test App")

# Step 1: Provide sample questions download and upload
st.download_button(
    label="Download Sample Questions",
    data=SAMPLE_QUESTIONS,
    file_name="sample_questions.json",
    mime="application/json"
)
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
    st.info("Please upload a JSON file to start. Use the 'Download Sample Questions' button to get a template.")