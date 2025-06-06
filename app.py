import streamlit as st
import random
import json
from typing import Any
import os

# Set page configuration
st.set_page_config(page_title="Exam Quiz quiz-app", page_icon="📝", layout="centered")

# load custom CSS from text file
with open("style.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_questions_from_file(
    file_path: str = "questions/default_questions.json",
) -> Any:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return []


def get_available_question_sets() -> list[tuple[str, str, str]]:
    """
    Get available question sets from the questions directory.

    Returns:
        list: List of tuples containing (filename, label, filepath)
    """
    question_dir = "questions"
    if not os.path.exists(question_dir):
        return []

    question_files = sorted([f for f in os.listdir(question_dir) if f.endswith(".json")])

    # Create list of (filename, label, filepath) tuples
    question_sets = []
    for filename in question_files:
        filepath = os.path.join(question_dir, filename)
        # Turn 'hard_questions.json' into 'Hard Questions'
        label = os.path.splitext(filename)[0].replace("_", " ").title()
        question_sets.append((filename, label, filepath))

    return question_sets


def initialize_question_set_state() -> None:
    """Initialize question set state if not already present."""
    if "selected_question_set" not in st.session_state:
        st.session_state.selected_question_set = None


def display_question_set_buttons() -> None:
    """
    Display buttons for question set selection UI.
    Does not return anything - purely handles UI rendering.
    """
    st.header("Choose Question Set")

    question_sets = get_available_question_sets()
    if not question_sets:
        st.warning("Questions directory not found.")
        return

    # Create a button for each question file
    for filename, label, filepath in question_sets:
        if st.button(label, key=f"load_{label.lower().replace(' ', '_')}"):
            st.session_state.questions = load_questions_from_file(filepath)
            st.session_state.selected_question_set = label
            reset_quiz()
            st.rerun()


def get_selected_question_set() -> Any:
    """
    Get the currently selected question set label.

    Returns:
        str: The label of the selected question set, or None if nothing selected
    """
    # Ensure state is initialized
    initialize_question_set_state()
    return st.session_state.selected_question_set


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
        initialize_question_set_state()

        display_question_set_buttons()


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


def handle_answer_selection(question_data: dict[str, list[str] | str]) -> None:
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
        st.markdown("#### 🥹 Excellent job! You really know this 🌟")
    elif score_percentage >= 70:
        st.markdown("#### 🥰 Good work! You know this pretty well.")
    elif score_percentage >= 50:
        st.markdown("#### 🤭 Not bad, but there's room for improvement")
    else:
        st.markdown("#### 🫣 Keep practicing! Review the material and try again.")

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

    selected_set = get_selected_question_set()
    if selected_set:
        st.markdown(f"### {selected_set}")
    else:
        st.markdown("### Default Questions")
    # Sidebar
    create_sidebar()

    show_quiz_interface()


if __name__ == "__main__":
    main()
