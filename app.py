import csv
import random
import streamlit as st

# ---------- LOAD QUESTIONS ----------
def load_questions(csv_file):
    questions = []
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            with open(csv_file, "r", encoding=enc, errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 5:
                        question = row[0]
                        correct_answer = row[1]
                        options = row[1:5]
                        questions.append((question, correct_answer, options))
            break
        except UnicodeDecodeError:
            continue
    return questions

# ---------- INITIALISE SESSION STATE ----------
if "questions" not in st.session_state:
    st.session_state.questions = load_questions("Limitations_v2.csv")
    random.shuffle(st.session_state.questions)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.total = len(st.session_state.questions)
    st.session_state.feedback = ""
    st.session_state.answered = False
    st.session_state.shuffled_options = {}

questions = st.session_state.questions
idx = st.session_state.index

# ---------- UI ----------
st.title("Limitations Quiz")

if idx < st.session_state.total:
    question, correct_answer, options = questions[idx]

    st.subheader(f"Question {idx+1}/{st.session_state.total}")
    st.write(question)

    # Shuffle options ONCE per question
    if idx not in st.session_state.shuffled_options:
        shuffled = options[:]
        random.shuffle(shuffled)
        st.session_state.shuffled_options[idx] = shuffled
    else:
        shuffled = st.session_state.shuffled_options[idx]

    answer = st.radio(
        "Select your answer:",
        shuffled,
        index=None,            # NO default selection
        key=f"q{idx}"
    )

    if st.button("Submit"):
        if answer is None:
            st.warning("Please select an answer before submitting.")
        else:
            st.session_state.answered = True
            if answer == correct_answer:
                st.session_state.score += 1
                st.session_state.feedback = "✔ Correct!"
            else:
                st.session_state.feedback = f"✘ Incorrect. Correct answer: {correct_answer}"

    if st.session_state.answered:
        st.write(st.session_state.feedback)

        if st.button("Next question"):
            st.session_state.index += 1
            st.session_state.answered = False
            st.rerun()

else:
    st.subheader("Quiz Complete")
    st.write(f"Score: {st.session_state.score} / {st.session_state.total}")

    if st.button("Restart quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
