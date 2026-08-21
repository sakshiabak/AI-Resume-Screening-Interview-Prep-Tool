"""
matcher.py
Handles:
  1. Resume <-> Job Description similarity scoring (TF-IDF + Cosine Similarity)
  2. Skill extraction and matched/missing skill comparison
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A reasonably broad list of common technical & soft skills.
# Feel free to extend this list for your domain / branch.
SKILLS_DB = [
    # Programming languages
    "python", "java", "c++", "c", "javascript", "typescript", "sql", "r",
    "go", "golang", "rust", "kotlin", "swift", "php", "scala", "matlab",
    # Web dev
    "html", "css", "react", "angular", "vue", "node.js", "nodejs",
    "express", "django", "flask", "rest api", "graphql", "bootstrap",
    # Data / AI / ML
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data science", "data analysis", "pandas", "numpy",
    "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv",
    "power bi", "tableau", "excel",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "ci/cd",
    "git", "github", "linux", "terraform",
    # Databases
    "mysql", "postgresql", "mongodb", "oracle", "firebase", "redis",
    # Mobile
    "android", "ios", "flutter", "react native",
    # Other CS fundamentals
    "data structures", "algorithms", "oop", "system design",
    "operating systems", "computer networks", "dbms",
    # Soft skills
    "communication", "teamwork", "leadership", "problem solving",
    "project management", "agile", "scrum", "time management",
]


def clean_text(text):
    """Lowercase and normalize whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.#\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_match_score(resume_text, jd_text):
    """
    Calculate a similarity score (0-100) between resume and job description
    using TF-IDF vectorization + cosine similarity.
    """
    documents = [clean_text(resume_text), clean_text(jd_text)]

    if not documents[0] or not documents[1]:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
    except ValueError:
        # happens if vocabulary is empty after stop-word removal
        return 0.0

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


def extract_skills(text):
    """Return the set of known skills found in the given text."""
    text_clean = clean_text(text)
    found = set()
    for skill in SKILLS_DB:
        skill_clean = clean_text(skill)
        # word-boundary-ish match to avoid partial word issues (e.g. 'r' inside 'car')
        pattern = r"(?<!\w)" + re.escape(skill_clean) + r"(?!\w)"
        if re.search(pattern, text_clean):
            found.add(skill)
    return found


def compare_skills(resume_text, jd_text):
    """
    Compare skills mentioned in the resume vs the job description.
    Returns matched skills and missing skills (present in JD but not resume).
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(resume_skills.intersection(jd_skills))
    missing = sorted(jd_skills.difference(resume_skills))
    extra = sorted(resume_skills.difference(jd_skills))

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
    }


def verdict(score):
    """Give a human-friendly verdict based on the match score."""
    if score >= 75:
        return "Excellent Match", "success"
    elif score >= 50:
        return "Good Match", "info"
    elif score >= 30:
        return "Fair Match - resume needs improvement", "warning"
    else:
        return "Poor Match - resume needs significant tailoring", "danger"
