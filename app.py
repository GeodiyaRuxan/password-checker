from flask import Flask, render_template, request

import re

app = Flask(__name__)

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add at least one special character (!@#$%^&* etc).")

    return score, feedback

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    feedback = []
    if request.method == "POST":
        password = request.form.get("password")
        score, feedback = check_password_strength(password)
        result = {"score": score, "max_score": 5, "feedback": feedback}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
