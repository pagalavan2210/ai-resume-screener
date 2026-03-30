# AI Resume Screener using NLP

An AI-powered web application that analyzes resumes against job descriptions, generates a match score, recommends courses with platform details, and shows relevant job opportunities.

## Features

- Upload resume as PDF or TXT file
- Paste any job description
- Animated gauge chart showing match score visually
- Skill breakdown with animated progress bars
- Matched skills highlighted in green
- Missing skills highlighted in red
- Course recommendations with platform, course title, duration and difficulty level for every missing skill
- ATS optimization tips based on your resume
- Job opportunities from Internshala, LinkedIn and Naukri based on matched skills
- Dark mode toggle
- Loading spinner while analyzing
- Hero section on homepage
- Drag and drop file upload
- Supports 40+ skills including cybersecurity, ML, web dev, DevOps
- Indian mobile number format detection

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

resume_screener/
├── app.py                  # Flask backend + NLP logic
├── requirements.txt        # Dependencies
├── README.md
├── templates/
│   ├── index.html          # Upload form with hero section
│   └── result.html         # Results page
├── static/
│   ├── style.css           # Full styling with dark mode
│   └── script.js           # Dark mode toggle + spinner
└── uploads/                # Stores uploaded resumes

## How It Works

1. User uploads a resume PDF or TXT
2. PyMuPDF extracts raw text from the PDF
3. spaCy processes the text to detect emails and phone numbers
4. App compares resume keywords against job description keywords
5. Match score calculated based on skill overlap percentage
6. Gauge chart rendered using Chart.js
7. Course recommendations shown with platform, duration and difficulty
8. Job opportunities fetched from Internshala, LinkedIn and Naukri
9. ATS tips generated based on score and missing skills

## Setup and Run Locally

Clone the repo

git clone https://github.com/pagalavan2210/ai-resume-screener.git
cd ai-resume-screener

Create virtual environment

python -m venv venv
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

Run the app

python app.py

Open http://127.0.0.1:5000 in your browser.

## Requirements

flask
spacy
PyMuPDF
scikit-learn

## Skills Covered

Python, Java, C++, SQL, JavaScript, React, HTML, CSS, Tailwind CSS, Flask, Django, Machine Learning, Deep Learning, NLP, Data Analysis, Data Science, Pandas, NumPy, TensorFlow, Keras, PyTorch, OpenCV, Computer Vision, Git, Linux, Docker, Kubernetes, AWS, Azure, MongoDB, MySQL, PostgreSQL, REST API, Cybersecurity, Network Security, Penetration Testing, Cryptography, Nmap, Wireshark, Metasploit, Burp Suite, OWASP, Bash, Selenium, Postman, Figma, Kotlin, PHP

## What I Learned

- Extracting text from PDF files using PyMuPDF
- NLP keyword extraction using spaCy
- Building REST APIs with Flask
- Rendering dynamic charts using Chart.js
- Dark mode implementation using CSS variables
- Connecting frontend forms to Python backend
- Deploying ML logic inside a web application

## Author

Tamil Pagalavan
- GitHub: @pagalavan2210 - https://github.com/pagalavan2210
- Email: pagalavan167@gmail.com

## License

MIT License