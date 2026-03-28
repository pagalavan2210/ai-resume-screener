from flask import Flask, request, render_template
import fitz
import spacy
import re
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "flask", "django", "react", "javascript", "html", "css",
    "data analysis", "pandas", "numpy", "tensorflow", "keras",
    "git", "linux", "docker", "rest api", "mongodb", "mysql"
]

SKILL_RESOURCES = {
    "python": "https://www.coursera.org/learn/python",
    "java": "https://www.coursera.org/learn/java-programming",
    "sql": "https://www.coursera.org/learn/sql-for-data-science",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.coursera.org/specializations/deep-learning",
    "nlp": "https://www.coursera.org/specializations/natural-language-processing",
    "flask": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
    "django": "https://www.coursera.org/learn/django-web-framework",
    "react": "https://www.coursera.org/learn/react-basics",
    "javascript": "https://www.coursera.org/learn/javascript-basics",
    "html": "https://www.coursera.org/learn/html-css-javascript-for-web-developers",
    "css": "https://www.coursera.org/learn/html-css-javascript-for-web-developers",
    "data analysis": "https://www.coursera.org/learn/data-analysis-with-python",
    "pandas": "https://www.youtube.com/watch?v=vmEHCJofslg",
    "numpy": "https://www.youtube.com/watch?v=QUT1VHiLmmI",
    "tensorflow": "https://www.coursera.org/learn/introduction-tensorflow",
    "keras": "https://www.youtube.com/watch?v=qFJeN9V1ZsI",
    "git": "https://www.coursera.org/learn/introduction-git-github",
    "linux": "https://www.coursera.org/learn/linux-fundamentals",
    "docker": "https://www.coursera.org/learn/docker-for-the-absolute-beginner",
    "rest api": "https://www.youtube.com/watch?v=qbLc5a9jdXo",
    "mongodb": "https://learn.mongodb.com",
    "mysql": "https://www.coursera.org/learn/mysql"
}

def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()

def extract_text_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().lower()

def score_resume(resume_text, job_desc):
    job_desc = job_desc.lower()

    matched = []
    missing = []

    for skill in SKILL_KEYWORDS:
        if skill in resume_text and skill in job_desc:
            matched.append(skill)
        elif skill in job_desc and skill not in resume_text:
            missing.append(skill)

    total = len(matched) + len(missing)
    score = round((len(matched) / total) * 100) if total > 0 else 0

    doc = nlp(resume_text[:5000])
    emails = [token.text for token in doc if "@" in token.text]
    phones = re.findall(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', resume_text)

    recommendations = {
        skill: SKILL_RESOURCES[skill]
        for skill in missing
        if skill in SKILL_RESOURCES
    }

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "recommendations": recommendations,
        "email": emails[0] if emails else "Not found",
        "phone": phones[0] if phones else "Not found",
        "word_count": len(resume_text.split())
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    job_desc = request.form.get('job_desc', '')

    if not file or not job_desc:
        return render_template('index.html', error="Please upload a resume and enter a job description.")

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(filepath)
    elif filename.endswith('.txt'):
        resume_text = extract_text_from_txt(filepath)
    else:
        return render_template('index.html', error="Only PDF and TXT files supported.")

    result = score_resume(resume_text, job_desc)
    return render_template('result.html', result=result, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)