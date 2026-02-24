import pdfplumber
import re

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def compute_resume_score(text):
    skills = [
        "python", "java", "sql", "machine learning",
        "data science", "flask", "django", "react",
        "node", "html", "css", "javascript"
    ]

    score = 0
    found_skills = []

    for skill in skills:
        if skill in text:
            score += 5
            found_skills.append(skill)

    return score, found_skills

def generate_report(text):
    score, skills = compute_resume_score(text)

    if score >= 60:
        level = "Excellent"
    elif score >= 40:
        level = "Good"
    elif score >= 20:
        level = "Average"
    else:
        level = "Needs Improvement"

    return {
        "score": score,
        "level": level,
        "skills_found": skills
    }