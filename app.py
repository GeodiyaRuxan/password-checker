from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Basic list of common passwords (expandable)
COMMON_PASSWORDS = ['password', '123456', '12345678', 'qwerty', 'abc123', 'letmein', '111111']

def check_password_strength(password):
    feedback = []
    score = 0

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8–12 characters.")

    # Upper and lowercase check
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Use a combination of uppercase and lowercase letters.")

    # Numbers and symbols
    if re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Include numbers and special symbols.")

    # Common password detection
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Avoid common passwords like 'password', '123456', etc.")
        score = 0

    # Pattern detection
    if re.search(r'(.)\1{2,}', password) or re.search(r'123|abc|qwerty', password.lower()):
        feedback.append("Avoid repeated characters or simple sequences like 'abc123'.")
        score -= 1

    # Final strength level
    if score >= 4:
        strength = "Strong"
        color = "green"
    elif score == 3:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Weak"
        color = "red"

    return strength, feedback, color

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = None
    feedback = []
    color = "black"

    if request.method == 'POST':
        password = request.form['password']
        strength, feedback, color = check_password_strength(password)

    return render_template('index.html', strength=strength, feedback=feedback, color=color)

if __name__ == '__main__':
    app.run(debug=True)
