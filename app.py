import streamlit as st
import random
import json
from typing import Any

# Set page configuration
st.set_page_config(page_title="Exam Quiz quiz-app", page_icon="📝", layout="centered")

# load custom CSS from text file
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def load_questions_from_file(file_path: str = "questions.json") -> Any:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []


default_questions = load_questions_from_file()


# Function to initialize session state variables
def initialize_state() -> None:
    if "questions" not in st.session_state:
        st.session_state.questions = default_questions
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = 0
    if "total_answered" not in st.session_state:
        st.session_state.total_answered = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "shuffle_questions" not in st.session_state:
        st.session_state.shuffle_questions = False

def reset_quiz(shuffle=None):
    """Reset the quiz to its initial state."""
    # Only update shuffle setting if explicitly provided
    if shuffle is not None:
        st.session_state.shuffle_questions = shuffle

    if st.session_state.shuffle_questions:
        random.shuffle(st.session_state.questions)

    st.session_state.current_question = 0
    st.session_state.correct_answers = 0
    st.session_state.total_answered = 0
    st.session_state.answered = False

def display_quiz_stats():
    """Display quiz statistics in the sidebar."""
    st.header("Quiz Stats")

    if st.session_state.total_answered > 0:
        score_percentage = (st.session_state.correct_answers / st.session_state.total_answered) * 100
        st.metric("Score", f"{score_percentage:.1f}%")
        st.write(f"Correct Answers: {st.session_state.correct_answers}/{st.session_state.total_answered}")


def display_quiz_settings():
    """Display and handle quiz settings in the sidebar."""
    st.header("Quiz Settings")
    
    # Option to shuffle questions with callback
    previous_shuffle = st.session_state.shuffle_questions
    shuffle = st.checkbox("Shuffle Questions", value=previous_shuffle)
    
    # Only reset if shuffle setting has changed
    if shuffle != previous_shuffle:
        reset_quiz(shuffle=shuffle)
        st.rerun()



def create_sidebar():
    """Create the quiz sidebar with settings and stats."""
    with st.sidebar:
        display_quiz_settings()
        display_quiz_stats()

        # Reset button
        if st.button("Restart Quiz", key="restart_quiz"):
            reset_quiz()
            st.rerun()


def main():
    # Initialize state
    initialize_state()

    # App header
    st.title("📝 Exam Quiz quiz-app")

    # Sidebar
    create_sidebar()

    # Main quiz interface
    if st.session_state.current_question < len(st.session_state.questions):
        # Progress bar
        progress = (st.session_state.current_question) / len(st.session_state.questions)
        st.progress(progress)
        st.markdown(
            f'<p class="progress-text">Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}</p>',
            unsafe_allow_html=True,
        )

        current_q = st.session_state.questions[st.session_state.current_question]

        # Display question
        st.markdown(
            f'<div class="question-card"><h3>{current_q["question"]}</h3></div>',
            unsafe_allow_html=True,
        )

        # Display options as buttons
        if not st.session_state.answered:
            for option in current_q["options"]:
                if st.button(option, key=option):
                    st.session_state.selected_option = option
                    st.session_state.answered = True
                    st.session_state.total_answered += 1
                    if option == current_q["correct_answer"]:
                        st.session_state.correct_answers += 1
                    st.rerun()
        else:
            # Show feedback after answering
            is_correct = st.session_state.selected_option == current_q["correct_answer"]

            # Highlight the selected option
            for option in current_q["options"]:
                if option == st.session_state.selected_option:
                    if is_correct:
                        st.success(f"✓ {option}")
                    else:
                        st.error(f"✗ {option}")
                elif option == current_q["correct_answer"] and not is_correct:
                    st.success(f"✓ {option} (Correct answer)")
                else:
                    st.write(option)

            # Show explanation
            if is_correct:
                st.markdown(
                    f'<div class="feedback-correct"><b>Correct!</b><br>{current_q["explanation"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="feedback-incorrect"><b>Incorrect.</b> The correct answer is: {current_q["correct_answer"]}<br>{current_q["explanation"]}</div>',
                    unsafe_allow_html=True,
                )

            # Next question button
            if st.button("Next Question", key="next_question"):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()
    else:
        # Quiz completed
        st.success("🎉 Quiz Completed!")

        score_percentage = (
            st.session_state.correct_answers / len(st.session_state.questions)
        ) * 100
        st.markdown(
            f"### Your Score: {st.session_state.correct_answers}/{len(st.session_state.questions)} ({score_percentage:.1f}%)"
        )

        # Performance feedback
        if score_percentage >= 90:
            st.markdown("#### 🏆 Excellent job! You've mastered this material!")
        elif score_percentage >= 70:
            st.markdown(
                "#### 👍 Good work! You have a solid understanding of the material."
            )
        elif score_percentage >= 50:
            st.markdown("#### 📚 Not bad, but there's room for improvement.")
        else:
            st.markdown("#### 💪 Keep practicing! Review the material and try again.")

        if st.button("Restart Quiz", key="restart_quiz_final"):
            if st.session_state.shuffle_questions:
                random.shuffle(st.session_state.questions)
            st.session_state.current_question = 0
            st.session_state.correct_answers = 0
            st.session_state.total_answered = 0
            st.session_state.answered = False
            st.rerun()



if __name__ == "__main__":
    main()
