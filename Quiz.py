import streamlit as st
import json
import random

# Load questions from the JSON file
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

# Initialize session state for tracking displayed questions, reveal state, and scores
if "displayed_indices" not in st.session_state:
    st.session_state["displayed_indices"] = []
if "current_index" not in st.session_state:
    st.session_state["current_index"] = None
if "reveal_answer" not in st.session_state:
    st.session_state["reveal_answer"] = False
if "correct_count" not in st.session_state:
    st.session_state["correct_count"] = 0
if "incorrect_count" not in st.session_state:
    st.session_state["incorrect_count"] = 0
if "selected_answers" not in st.session_state:
    st.session_state["selected_answers"] = []

# Function to get the next random question index
def get_next_question_index():
    remaining_indices = list(set(range(len(questions))) - set(st.session_state["displayed_indices"]))
    if remaining_indices:
        return random.choice(remaining_indices)
    else:
        return None  # No more questions left

# Get the current question index
if st.session_state["current_index"] is None:
    next_index = get_next_question_index()
    if next_index is not None:
        st.session_state["current_index"] = next_index
        st.session_state["displayed_indices"].append(next_index)
    else:
        st.write("No more questions available!")
        st.stop()

current_question = questions[st.session_state["current_index"]]

# Styling
st.set_page_config(layout="wide")

# Display the question
st.title("Azure Practice Quiz")
st.subheader(f"Question {len(st.session_state['displayed_indices'])}")
st.write(current_question["question"])

# Display all associated images (if available)
if current_question.get("images"):
    for image_url in current_question["images"]:
        st.image(image_url)

# Display the answer options
st.write("### Answer Options:")
if len(current_question["correct_answers"]) == 1:
    # Use radio buttons for single-correct-answer questions
    selected_answer = st.radio(
        "Select your answer:",
        options=current_question["answers"],
        key=f"radio_{st.session_state['current_index']}"
    )
    st.session_state["selected_answers"] = [selected_answer]
else:
    # Use checkboxes for multiple-correct-answer questions
    selected_answers = []
    for i, answer in enumerate(current_question["answers"]):
        if st.checkbox(answer, key=f"checkbox_{st.session_state['current_index']}_{i}"):
            selected_answers.append(answer)
    st.session_state["selected_answers"] = selected_answers

# Button to reveal the correct answer
if st.button("Reveal Correct Answer"):
    st.session_state["reveal_answer"] = True
    if set(st.session_state["selected_answers"]) == set(current_question["correct_answers"]):
        st.session_state["correct_count"] += 1
        st.success("Your answer is correct!")
    else:
        st.session_state["incorrect_count"] += 1
        st.error("Your answer is incorrect!")
    st.rerun()

# Highlight correct answers if revealed
if st.session_state["reveal_answer"]:
    st.write("### Correct Answer(s):")
    for i, answer in enumerate(current_question["answers"], start=1):
        if answer in current_question["correct_answers"]:
            st.markdown(f"**{i}. {answer}** :white_check_mark:")
        else:
            st.write(f"{i}. {answer}")

# Display score
st.write("### Score:")
st.write(f"Correct: {st.session_state['correct_count']}")
st.write(f"Incorrect: {st.session_state['incorrect_count']}")

# Navigation buttons
col1, col2 = st.columns(2)

# Previous question button
if col1.button("Previous Question"):
    if len(st.session_state["displayed_indices"]) > 1:
        st.session_state["displayed_indices"].pop()  # Remove the current question
        st.session_state["current_index"] = st.session_state["displayed_indices"][-1]
        st.session_state["reveal_answer"] = False
        st.session_state["selected_answers"] = []
        st.rerun()

# Next question button
if col2.button("Next Question"):
    next_index = get_next_question_index()
    if next_index is not None:
        st.session_state["current_index"] = next_index
        st.session_state["displayed_indices"].append(next_index)
        st.session_state["reveal_answer"] = False
        st.session_state["selected_answers"] = []
        st.rerun()
    else:
        st.write("No more questions available!")