# AI-Based Resume Screening & Interview Prep Tool

A Flask web application that:
1. Accepts a resume (PDF / DOCX / TXT) and a job description.
2. Calculates a **match score** using TF-IDF + Cosine Similarity (NLP/ML).
3. Shows **matched skills**, **missing skills**, and **extra skills**.
4. Generates **mock technical + behavioral interview questions** based on the skills found in your resume.

---

## 📁 Project Structure

```
resume_screening_tool/
├── app.py                  # Main Flask application (routes)
├── requirements.txt        # Python dependencies
├── utils/
│   ├── resume_parser.py    # Extracts text from PDF/DOCX/TXT
│   ├── matcher.py          # TF-IDF similarity + skill matching logic
│   └── question_bank.py    # Interview question generator
├── templates/
│   ├── index.html          # Upload form page
│   └── result.html         # Results page (score, skills, questions)
├── static/
│   └── style.css           # Basic styling
└── uploads/                # Temporary storage for uploaded resumes (auto-cleared)
```

---

## 🖥️ How to Extract the ZIP File

**On Windows:**
1. Right-click the downloaded `resume_screening_tool.zip` file.
2. Click **"Extract All..."**
3. Choose a destination folder and click **Extract**.

**On Mac:**
1. Double-click the `resume_screening_tool.zip` file — it extracts automatically into the same folder.

**On Linux / Terminal (Windows/Mac too, if you prefer command line):**
```bash
unzip resume_screening_tool.zip -d resume_screening_tool
cd resume_screening_tool
```

---

## ⚙️ How to Run the Project

### Step 1 — Install Python
Make sure Python 3.9+ is installed. Check with:
```bash
python --version
```
(If not installed, download from https://www.python.org/downloads/)

### Step 2 — (Recommended) Create a virtual environment
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in browser
Go to: **http://127.0.0.1:5000**

Upload a resume (PDF/DOCX/TXT), paste a job description, and click **Analyze Resume**.

---

## 🧠 How It Works (for your project report / viva)

1. **Resume Parsing** (`utils/resume_parser.py`)
   Uses `PyPDF2` for PDFs and `python-docx` for Word files to extract raw text.

2. **Match Scoring** (`utils/matcher.py`)
   - Cleans and normalizes both resume text and job description text.
   - Converts both into TF-IDF vectors using `scikit-learn`'s `TfidfVectorizer`.
   - Computes **Cosine Similarity** between the two vectors → gives a 0–100% match score.

3. **Skill Extraction & Gap Analysis** (`utils/matcher.py`)
   - Matches text against a curated list (`SKILLS_DB`) of ~80 common technical/soft skills.
   - Reports:
     - **Matched skills** — present in both resume and JD.
     - **Missing skills** — required by JD but not found in resume.
     - **Extra skills** — present in resume but not required by JD.

4. **Interview Question Generation** (`utils/question_bank.py`)
   - Uses a curated question bank mapped to common skills.
   - Falls back to templated questions for skills not in the bank.
   - Adds a set of standard behavioral/HR questions.

---

## 🚀 Possible Enhancements (Future Scope)

- Replace TF-IDF with sentence embeddings (e.g., `sentence-transformers`) for smarter semantic matching.
- Add authentication and a database (SQLite/MongoDB) to save analysis history.
- Support OCR (`pytesseract`) for scanned/image-based resumes.
- Deploy on cloud (Render/Railway/Heroku/AWS) for public access.
- Integrate a large language model API for dynamic, context-aware interview questions.
- Add a resume formatting/ATS-friendliness checker.

---

## 🐛 Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside the activated virtual environment. |
| Port 5000 already in use | Change the port in the last line of `app.py`, e.g. `app.run(debug=True, port=5001)`. |
| PDF text not extracting | The PDF might be a scanned image. Try converting it to text-based PDF, or use a DOCX/TXT file instead. |
| Blank/0% score | Make sure both the resume and job description have enough real text (not just a title). |

---

## 📄 License
Free to use and modify for academic/educational purposes (final year project).
