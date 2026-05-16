from flask import Flask, render_template, request
import os
import pdfplumber
import webbrowser

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['resume']

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # -----------------------------
    # Extract text from PDF
    # -----------------------------
    text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            if page.extract_text():
                text += page.extract_text()

    text = text.lower()

    # -----------------------------
    # Skills List
    # -----------------------------
    skills_list = [

        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "django",
        "machine learning",
        "data science",
        "deep learning",
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "c++",
        "ai",
        "ml"

    ]

    # -----------------------------
    # Detect Skills
    # -----------------------------
    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    # Extra matching
    if "ml" in text:
        found_skills.append("machine learning")

    if "ai" in text:
        found_skills.append("artificial intelligence")

    # Remove duplicates
    found_skills = list(set(found_skills))

    # -----------------------------
    # Resume Score
    # -----------------------------
    score = round(
        (len(found_skills) / len(skills_list)) * 100,
        2
    )

    # -----------------------------
    # Job Recommendations
    # -----------------------------
    jobs = []

    if "python" in found_skills:
        jobs.append("Data Scientist")

    if "sql" in found_skills:
        jobs.append("Data Analyst")

    if "html" in found_skills:
        jobs.append("Frontend Developer")

    if "flask" in found_skills:
        jobs.append("Backend Developer")

    if not jobs:
        jobs.append("Skill Improvement Needed")

    return render_template(
        'result.html',
        skills=", ".join(found_skills),
        score=score,
        jobs=", ".join(jobs)
    )


if __name__ == '__main__':

    webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True)