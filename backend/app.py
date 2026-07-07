from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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

    return jsonify({
        "bug_type": bug_type,
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)