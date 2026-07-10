from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
import ast
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE_NAME = "bugfixer.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debug_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_code TEXT NOT NULL,
            error_message TEXT NOT NULL,
            bug_type TEXT NOT NULL,
            explanation TEXT NOT NULL,
            fixed_code TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def extract_line_number(error_message):
    match = re.search(r"line (\d+)", error_message)

    if match:
        return int(match.group(1))

    return None

def analyze_code_structure(code):
    try:
        tree = ast.parse(code)

        function_names = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)

        return {
            "is_valid_python": True,
            "function_names": function_names,
            "function_count": len(function_names)
        }

    except SyntaxError:
        return {
            "is_valid_python": False,
            "function_names": [],
            "function_count": 0
        }

def classify_bug(error_message):
    error_message = error_message.lower()

    if "syntaxerror" in error_message:
        return "SyntaxError"
    elif "nameerror" in error_message:
        return "NameError"
    elif "typeerror" in error_message:
        return "TypeError"
    elif "indexerror" in error_message:
        return "IndexError"
    elif "keyerror" in error_message:
        return "KeyError"
    elif "indentationerror" in error_message:
        return "IndentationError"
    else:
        return "Unknown Error"


def explain_bug(bug_type):
    if bug_type == "SyntaxError":
        return "Your code has invalid Python syntax, like a missing colon, quote, or parenthesis."
    elif bug_type == "NameError":
        return "Your code is using a variable name that Python does not recognize."
    elif bug_type == "TypeError":
        return "Your code is using the wrong type of value, like mixing a string and a number."
    elif bug_type == "IndexError":
        return "Your code is trying to access a list item that may not exist."
    elif bug_type == "KeyError":
        return "Your code is trying to access a dictionary key that does not exist."
    elif bug_type == "IndentationError":
        return "Your code has spacing or indentation problems."
    else:
        return "BugFixerAI could not detect the exact bug type yet."


def suggest_fix(code, bug_type):
    if bug_type == "IndexError":
        return (
            "# Suggested fix: check if the list is empty first\n\n"
            "def get_first(lst):\n"
            "    if len(lst) == 0:\n"
            "        return None\n"
            "    return lst[0]"
        )

    elif bug_type == "NameError":
        return "# Suggested fix: check that all variable names are spelled correctly\n\n" + code

    elif bug_type == "TypeError":
        return "# Suggested fix: make sure values are the correct type before using them together\n\n" + code

    elif bug_type == "SyntaxError":
        return "# Suggested fix: check for missing colons, quotes, or parentheses\n\n" + code

    elif bug_type == "KeyError":
        return "# Suggested fix: check if the key exists before accessing it\n\n" + code

    elif bug_type == "IndentationError":
        return "# Suggested fix: make sure your indentation is consistent\n\n" + code

    else:
        return "# BugFixerAI could not suggest an exact fix yet.\n\n" + code

def save_debug_session(code, error_message, bug_type, explanation, fixed_code):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO debug_sessions
        (original_code, error_message, bug_type, explanation, fixed_code, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        code,
        error_message,
        bug_type,
        explanation,
        fixed_code,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return jsonify({
        "message": "BugFixerAI backend is running"
    })


@app.route("/api/debug", methods=["POST"])
def debug_code():
    data = request.get_json()

    code = data.get("code", "")
    error_message = data.get("error_message", "")

    if not code or not error_message:
        return jsonify({
            "error": "Code and error message are required."
        }), 400

    bug_type = classify_bug(error_message)
    explanation = explain_bug(bug_type)
    fixed_code = suggest_fix(code, bug_type)
    line_number = extract_line_number(error_message)
    code_analysis = analyze_code_structure(code)

    save_debug_session(code, error_message, bug_type, explanation, fixed_code)

    return jsonify({
        "bug_type": bug_type,
        "line_number": line_number,
        "explanation": explanation,
        "fixed_code": fixed_code,
        "code_analysis": code_analysis
    })

@app.route("/api/history", methods=["GET"])
def get_history():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, bug_type, original_code, error_message, explanation, fixed_code, created_at
        FROM debug_sessions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "bug_type": row[1],
            "original_code": row[2],
            "error_message": row[3],
            "explanation": row[4],
            "fixed_code": row[5],
            "created_at": row[6]
        })

    return jsonify(history)

if __name__ == "__main__":
    create_database()
    app.run(debug=True)