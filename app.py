"""
AI-Based Resume Screening & Interview Prep Tool
-------------------------------------------------
Run with:  python app.py
Then open: http://127.0.0.1:5000 in your browser.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from utils.resume_parser import extract_text
from utils.matcher import calculate_match_score, compare_skills, verdict
from utils.question_bank import generate_questions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB max upload
app.secret_key = "change-this-secret-key-in-production"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    jd_text = request.form.get("job_description", "").strip()

    # --- Validation ---
    if not resume_file or resume_file.filename == "":
        flash("Please upload a resume file (PDF, DOCX, or TXT).", "danger")
        return redirect(url_for("index"))

    if not allowed_file(resume_file.filename):
        flash("Unsupported file type. Please upload a PDF, DOCX, or TXT file.", "danger")
        return redirect(url_for("index"))

    if not jd_text:
        flash("Please paste the job description.", "danger")
        return redirect(url_for("index"))

    # --- Save & Parse Resume ---
    filename = secure_filename(resume_file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(filepath)

    try:
        resume_text = extract_text(filepath)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))
    finally:
        # clean up uploaded file after reading it
        if os.path.exists(filepath):
            os.remove(filepath)

    if not resume_text:
        flash("Could not extract any text from the uploaded resume. "
              "The file might be a scanned image without selectable text.", "danger")
        return redirect(url_for("index"))

    # --- Analysis ---
    score = calculate_match_score(resume_text, jd_text)
    skills_result = compare_skills(resume_text, jd_text)
    verdict_text, verdict_color = verdict(score)
    questions = generate_questions(skills_result["matched"])

    return render_template(
        "result.html",
        filename=filename,
        score=score,
        verdict_text=verdict_text,
        verdict_color=verdict_color,
        matched=skills_result["matched"],
        missing=skills_result["missing"],
        extra=skills_result["extra"],
        technical_questions=questions["technical"],
        behavioral_questions=questions["behavioral"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
