# AI Resume Screener using NLP

An AI-powered web application that analyzes resumes against job descriptions, generates a match score with an animated gauge chart, and recommends courses for missing skills.

## Screenshots

### Upload Page
![Upload Page](screenshots/upload.png)

### Results Page
![Results Page](screenshots/results.png)

## Features

- Upload resume as PDF or TXT file
- Paste any job description
- Animated gauge chart showing match score visually
- Matched skills highlighted in green
- Missing skills highlighted in red
- Course recommendations (Coursera/YouTube) for every missing skill
- Auto-extracts contact info (email, phone)
- Clean responsive UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Flask |
| NLP | spaCy (en_core_web_sm) |
| PDF Parsing | PyMuPDF (fitz) |
| ML | scikit-learn |
| Charts | Chart.js |
| Frontend | HTML5, CSS3, JavaScript |

## Project Structure
```
resume_screener/
├── app.py              # Flask backend + NLP logic
├── requirements.txt    # Dependencies
├── README.md
├── templates/
│   ├── index.html      # Upload form UI
│   └── result.html     # Results page with gauge chart
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
└── uploads/            # Stores uploaded resumes
```

## How It Works

1. User uploads a resume (PDF or TXT)
2. PyMuPDF extracts raw text from the PDF
3. spaCy processes the text to detect emails and entities
4. App compares resume keywords against job description keywords
5. Match score is calculated based on skill overlap percentage
6. Gauge chart rendered using Chart.js
7. Course recommendations fetched from SKILL_RESOURCES dictionary
8. Results displayed with matched skills, missing skills, and learn links

## Setup and Run Locally
```bash
# Clone the repo
git clone https://github.com/pagalavan2210/ai-resume-screener.git
cd ai-resume-screener

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Requirements
```
flask
spacy
PyMuPDF
scikit-learn
```

## Sample Output

- Match Score: 38%
- Matched Skills: python, sql, flask, git, linux
- Missing Skills: machine learning, deep learning, nlp, pandas, numpy, docker, rest api
- Recommendations: Direct Coursera/YouTube links for each missing skill

## What I Learned

- Extracting text from PDF files using PyMuPDF
- NLP keyword extraction using spaCy
- Building REST APIs with Flask
- Rendering dynamic charts using Chart.js
- Connecting frontend forms to Python backend
- Deploying ML logic inside a web application

## Author

**Tamil Pagalavan**
- GitHub: [@pagalavan2210](https://github.com/pagalavan2210)
- Email: pagalavan167@gmail.com

## License

MIT License