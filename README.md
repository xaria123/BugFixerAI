# BugFixerAI

BugFixerAI is a full-stack debugging assistant that helps students understand and fix common Python errors. Users can paste Python code and an error message, and the app returns the detected bug type, problem line, code analysis, beginner-friendly explanation, and suggested fix.

## Features

* Classifies common Python errors such as `SyntaxError`, `NameError`, `TypeError`, `IndexError`, `KeyError`, and `IndentationError`
* Uses regex-based parsing to extract the problem line number from Python error messages
* Uses Python AST parsing to analyze code structure without executing user code
* Generates beginner-friendly explanations for debugging issues
* Suggests rule-based code fixes for common Python bugs
* Saves debugging sessions using SQLite
* Displays previous debugging history in the React frontend

## Tech Stack

**Frontend**

* React
* JavaScript
* Vite
* CSS

**Backend**

* Python
* Flask
* Flask-CORS
* SQLite
* Python AST
* Regex

**Tools**

* Git
* VS Code
* REST APIs

## How It Works

1. The user enters Python code and an error message.
2. The React frontend sends the data to the Flask backend.
3. The backend classifies the bug type.
4. Regex extracts the line number from the error message when available.
5. Python AST analyzes the submitted code structure.
6. The backend returns an explanation and suggested fix.
7. The debugging session is saved in SQLite.
8. The frontend displays the result and debugging history.

## API Endpoints

### `POST /api/debug`

Analyzes submitted Python code and error message.

Example request:

```json
{
  "code": "def get_first(lst):\n    return lst[0]",
  "error_message": "File \"main.py\", line 2, in get_first\nIndexError: list index out of range"
}
```

Example response:

```json
{
  "bug_type": "IndexError",
  "line_number": 2,
  "code_analysis": {
    "is_valid_python": true,
    "function_names": ["get_first"],
    "function_count": 1
  },
  "explanation": "Your code is trying to access a list item that may not exist.",
  "fixed_code": "def get_first(lst):\n    if len(lst) == 0:\n        return None\n    return lst[0]"
}
```

### `GET /api/history`

Returns saved debugging sessions.

## Project Structure

```text
BugFixerAI/
├── backend/
│   └── app.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
├── README.md
├── requirements.txt
└── .gitignore
```

## Running the Project Locally

### Backend

```bash
source venv/bin/activate
python backend/app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

### Frontend

```bash
cd frontend
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

## Future Improvements

* Add support for more advanced Python logic errors
* Add GitHub repository scanning
* Add user authentication
* Add support for JavaScript debugging
* Deploy frontend and backend online
* Add a VS Code extension version

## Resume Summary

Built a full-stack Python debugging assistant using React, Flask, SQLite, REST APIs, Python AST parsing, and regex-based error extraction to classify bugs, explain errors, suggest fixes, and track debugging history.
