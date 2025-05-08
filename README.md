# Quiz App

An Streamlit application designed for exam preparation through customizable quizzes.

## Features

- Multiple-choice questions with immediate feedback
- Detailed explanations for each answer
- Progress tracking and score calculation
- Option to shuffle questions for varied practice
- Quiz statistics sidebar to track performance
- Personalized feedback based on quiz performance
- Default set of Azure Data Fundamentals questions
- Questions loaded from an external JSON file for easy customization

## Setup Instructions

### Prerequisites

- Python 3.7+
- uv package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/quiz-app.git
cd quiz-app
```

2. Create a virtual environment and install dependencies using uv:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install streamlit
```

3. Run the application:

```bash
streamlit run app.py
```

### Customizing Questions
Question sets are stored as separate .json files in the questions/ directory. Each file is automatically loaded and displayed as a selectable button in the app's sidebar, so there's no need to manually update the code when adding new sets.

To create your own set of questions, create a new .json file in the questions/ folder (e.g., azure_questions.json). Use the following format for each question:

```json
{
    "question": "What is Azure Synapse Analytics?",
    "options": [
        "A NoSQL database service",
        "An integrated analytics service",
        "A blockchain service",
        "A machine learning framework"
    ],
    "correct_answer": "An integrated analytics service",
    "explanation": "Azure Synapse Analytics is an integrated analytics service that brings together data integration, enterprise data warehousing, and big data analytics."
}
```
Save the file. The new question set will appear in the sidebar automatically, with the filename (excluding .json) converted into a readable button label (e.g., azure_questions.json becomes "Azure Questions").



## Project Structure

```
quiz-app/
├── app.py                        # Main Streamlit application
├── questions.json                # Quiz questions data file
├── .gitignore                    # Git ignore file
├── justfile                      # Task runner commands for development
├── pyproject.toml                # Project metadata and dependencies (managed with uv)
└── README.md                     # This file
```

## Usage

1. Start the application using the instructions above
2. Answer questions by clicking on one of the four options
3. Receive immediate feedback on your answer with an explanation
4. Click "Next Question" to proceed to the next question
5. View your final score and performance feedback at the end of the quiz
6. Use the sidebar options to:
   - Shuffle questions
   - Reset the quiz
   - View your current score

## Adding More Question Topics

To create a quiz for a different topic:

1. Create a new JSON file (e.g., `security_questions.json`)
2. Modify the file path in `app.py` where `load_questions_from_file()` is called
3. Run the app with the new question set
