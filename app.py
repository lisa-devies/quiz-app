import streamlit as st
import random
import json
from typing import Any

# Set page configuration
st.set_page_config(page_title="Exam Quiz quiz-app", page_icon="📝", layout="centered")

# load custom CSS from text file
with open("style.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_questions_from_file(file_path: str = "questions/questions.json") -> Any:
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


def reset_quiz(shuffle: bool = None) -> None:
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


def display_quiz_stats() -> None:
    """Display quiz statistics in the sidebar."""
    st.header("Quiz Stats")

    if st.session_state.total_answered > 0:
        score_percentage = (
            st.session_state.correct_answers / st.session_state.total_answered
        ) * 100
        st.metric("Score", f"{score_percentage:.1f}%")
        st.write(
            f"Correct Answers: {st.session_state.correct_answers}/{st.session_state.total_answered}"
        )


def display_quiz_settings() -> None:
    """Display and handle quiz settings in the sidebar."""
    st.header("Quiz Settings")

    # Option to shuffle questions with callback
    previous_shuffle = st.session_state.shuffle_questions
    shuffle = st.checkbox("Shuffle Questions", value=previous_shuffle)

    # Only reset if shuffle setting has changed
    if shuffle != previous_shuffle:
        reset_quiz(shuffle=shuffle)
        st.rerun()


def create_sidebar() -> None:
    """Create the quiz sidebar with settings and stats."""
    with st.sidebar:
        display_quiz_settings()
        display_quiz_stats()

        # Reset button
        if st.button("Restart Quiz", key="restart_quiz"):
            reset_quiz()
            st.rerun()

        # Choose question set
        st.header("Choose Question Set")
        if st.button("Hard questions", key="load_hard_questions"):
            st.session_state.questions = load_questions_from_file("questions/hard_questions.json")
            reset_quiz()
            st.rerun()

        if st.button("Azure tools questions", key="load_azure_questions"):
            st.session_state.questions = load_questions_from_file("questions/azure_tools_questions.json")
            reset_quiz()
            st.rerun()

        if st.button("Default questions", key="load_default_questions"):
            st.session_state.questions = load_questions_from_file("questions/questions.json")
            reset_quiz()
            st.rerun()



def display_progress_bar() -> None:
    # Progress bar
    progress = (st.session_state.current_question) / len(st.session_state.questions)
    st.progress(progress)
    st.markdown(
        f'<p class="progress-text">Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}</p>',
        unsafe_allow_html=True,
    )


def display_question(question_data: dict[str, str]) -> None:
    """Display the current question."""
    st.markdown(
        f'<div class="question-card"><h3>{question_data["question"]}</h3></div>',
        unsafe_allow_html=True,
    )


def handle_answer_selection(question_data: dict[str, str]) -> None:
    """Display answer options as buttons and handle selection."""
    if not st.session_state.answered:
        for option in question_data["options"]:
            if st.button(option, key=option):
                st.session_state.selected_option = option
                st.session_state.answered = True
                st.session_state.total_answered += 1

                if option == question_data["correct_answer"]:
                    st.session_state.correct_answers += 1

                st.rerun()


def show_answer_feedback(question_data: dict[str, str]) -> None:
    """Show feedback after the user has answered."""
    is_correct = st.session_state.selected_option == question_data["correct_answer"]

    # Highlight selected option and correct answer
    for option in question_data["options"]:
        if option == st.session_state.selected_option:
            if is_correct:
                st.success(f"✓ {option}")
            else:
                st.error(f"✗ {option}")
        elif option == question_data["correct_answer"] and not is_correct:
            st.success(f"✓ {option} (Correct answer)")
        else:
            st.write(option)

    # Show explanation
    if is_correct:
        st.markdown(
            f'<div class="feedback-correct"><b>Correct!</b><br>{question_data["explanation"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="feedback-incorrect"><b>Incorrect.</b> The correct answer is: {question_data["correct_answer"]}<br>{question_data["explanation"]}</div>',
            unsafe_allow_html=True,
        )

    # Next question button
    if st.button("Next Question", key="next_question"):
        st.session_state.current_question += 1
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.rerun()


def restart_quiz() -> None:
    """Reset quiz to initial state."""
    if st.session_state.shuffle_questions:
        random.shuffle(st.session_state.questions)
    st.session_state.current_question = 0
    st.session_state.correct_answers = 0
    st.session_state.total_answered = 0
    st.session_state.answered = False
    st.session_state.selected_option = None


def show_quiz_completion() -> None:
    """Display quiz completion screen with score and feedback."""
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
        restart_quiz()
        st.rerun()


def show_quiz_interface() -> None:
    """Display the main quiz interface based on current state."""
    if st.session_state.current_question < len(st.session_state.questions):
        display_progress_bar()

        # Get current question
        current_q = st.session_state.questions[st.session_state.current_question]

        # Display question
        display_question(current_q)

        # Handle answering or showing feedback
        if not st.session_state.answered:
            handle_answer_selection(current_q)
        else:
            show_answer_feedback(current_q)
    else:
        show_quiz_completion()


def main() -> None:
    # Initialize state
    initialize_state()

    # App header
    st.title("🍀quiz-app🍀")

    # Sidebar
    create_sidebar()

    show_quiz_interface()


if __name__ == "__main__":
    main()
