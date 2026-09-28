import time

import streamlit as st

from randselect.selector import random_selection

st.session_state.setdefault("names", [])
st.session_state.setdefault("questions", [])
st.session_state.setdefault("used_names", set())
st.session_state.setdefault("used_questions", set())
st.session_state.setdefault("last_result", None)

st.title("Random Question Picker")

with st.form("add_name_form", clear_on_submit=True):
    new_name = st.text_input("Name")
    add_name = st.form_submit_button("Add")
    if add_name and new_name.strip():
        st.session_state.names.append(new_name.strip())

st.subheader("Names")
if st.session_state.names:
    st.write(st.session_state.names)
else:
    st.caption("No names added yet.")

with st.form("add_question_form", clear_on_submit=True):
    new_question = st.text_input("Question")
    add_question = st.form_submit_button("Add")
    if add_question and new_question.strip():
        st.session_state.questions.append(new_question.strip())

st.subheader("Questions")
if st.session_state.questions:
    st.write(st.session_state.questions)
else:
    st.caption("No questions added yet.")

no_repeats = st.checkbox("No repeats this session")

if no_repeats:
    eligible_names = [n for n in st.session_state.names if n not in st.session_state.used_names]
    eligible_questions = [q for q in st.session_state.questions if q not in st.session_state.used_questions]
else:
    eligible_names = st.session_state.names
    eligible_questions = st.session_state.questions

pool_ready = bool(eligible_names) and bool(eligible_questions)

st.divider()

result_placeholder = st.empty()
status_placeholder = st.empty()

if st.button("Draw", disabled=not pool_ready):
    for _ in range(20):  # ~20 * 0.15s ≈ 3s
        flash_name, flash_question = random_selection(eligible_names, eligible_questions)
        result_placeholder.markdown(f"*{flash_name}* — *{flash_question}*")
        time.sleep(0.15)

    chosen_name, chosen_question = random_selection(eligible_names, eligible_questions)
    st.session_state.last_result = (chosen_name, chosen_question)
    if no_repeats:
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)

if st.session_state.last_result:
    name, question = st.session_state.last_result
    result_placeholder.markdown(f"### {name}, please answer: {question}")

if not pool_ready:
    if not st.session_state.names or not st.session_state.questions:
        status_placeholder.info("Add at least one name and one question to draw.")
    else:
        status_placeholder.warning(
            "All names or questions have been drawn this session. "
            "Add more, or uncheck 'No repeats' to draw again."
        )
