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
    "git", "linux", "docker", "rest api", "mongodb", "mysql",
    "cybersecurity", "network security", "penetration testing",
    "cryptography", "nmap", "wireshark", "metasploit", "burp suite",
    "owasp", "c++", "sqlite", "tailwind css", "john the ripper",
    "tcp/ip", "socket", "threading", "tkinter", "aes", "pbkdf2",
    "github", "vs code", "kotlin", "swift", "postgresql", "redis",
    "kubernetes", "aws", "azure", "gcp", "data science",
    "computer vision", "pytorch", "opencv", "selenium", "api testing",
    "postman", "jenkins", "bash", "powershell", "ruby", "php",
    "wordpress", "figma", "ui design", "ux design"
]

SKILL_RESOURCES = {
    "python": [
        {"platform": "Coursera", "course": "Python for Everybody", "link": "https://www.coursera.org/specializations/python", "duration": "8 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "Python Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=rfscVS0vtbw", "duration": "4 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Complete Python Bootcamp", "link": "https://www.udemy.com/course/complete-python-bootcamp/", "duration": "22 hours", "level": "Beginner"}
    ],
    "java": [
        {"platform": "Coursera", "course": "Java Programming and Software Engineering", "link": "https://www.coursera.org/specializations/java-programming", "duration": "6 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "Java Full Course - Telusko", "link": "https://www.youtube.com/watch?v=BGTx91t8q50", "duration": "13 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Java Masterclass", "link": "https://www.udemy.com/course/java-the-complete-java-developer-course/", "duration": "80 hours", "level": "Beginner"}
    ],
    "sql": [
        {"platform": "Coursera", "course": "SQL for Data Science", "link": "https://www.coursera.org/learn/sql-for-data-science", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "SQL Tutorial - Programming with Mosh", "link": "https://www.youtube.com/watch?v=7S_tz1z_5bA", "duration": "3 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "SQL Tutorial", "link": "https://www.w3schools.com/sql/", "duration": "Self paced", "level": "Beginner"}
    ],
    "machine learning": [
        {"platform": "Coursera", "course": "Machine Learning Specialization - Andrew Ng", "link": "https://www.coursera.org/specializations/machine-learning-introduction", "duration": "3 months", "level": "Intermediate"},
        {"platform": "YouTube", "course": "ML Full Course - Simplilearn", "link": "https://www.youtube.com/watch?v=9f-GarcDY58", "duration": "10 hours", "level": "Beginner"},
        {"platform": "Kaggle", "course": "Intro to Machine Learning", "link": "https://www.kaggle.com/learn/intro-to-machine-learning", "duration": "3 hours", "level": "Beginner"}
    ],
    "deep learning": [
        {"platform": "Coursera", "course": "Deep Learning Specialization - Andrew Ng", "link": "https://www.coursera.org/specializations/deep-learning", "duration": "5 months", "level": "Intermediate"},
        {"platform": "fast.ai", "course": "Practical Deep Learning", "link": "https://course.fast.ai", "duration": "Self paced", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Deep Learning - freeCodeCamp", "link": "https://www.youtube.com/watch?v=V_xro1bcAuA", "duration": "10 hours", "level": "Intermediate"}
    ],
    "nlp": [
        {"platform": "Coursera", "course": "NLP Specialization - DeepLearning.AI", "link": "https://www.coursera.org/specializations/natural-language-processing", "duration": "4 months", "level": "Advanced"},
        {"platform": "YouTube", "course": "NLP with Python - freeCodeCamp", "link": "https://www.youtube.com/watch?v=X2vAabgKiuM", "duration": "5 hours", "level": "Intermediate"},
        {"platform": "Kaggle", "course": "Natural Language Processing", "link": "https://www.kaggle.com/learn/natural-language-processing", "duration": "3 hours", "level": "Intermediate"}
    ],
    "flask": [
        {"platform": "YouTube", "course": "Flask Tutorial - Corey Schafer", "link": "https://www.youtube.com/watch?v=MwZwr5Tvyxo", "duration": "6 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "REST APIs with Flask and Python", "link": "https://www.udemy.com/course/rest-api-flask-and-python/", "duration": "17 hours", "level": "Intermediate"},
        {"platform": "freeCodeCamp", "course": "Flask Full Course", "link": "https://www.youtube.com/watch?v=Z1RJmh_OqeA", "duration": "6 hours", "level": "Beginner"}
    ],
    "django": [
        {"platform": "Coursera", "course": "Django for Everybody", "link": "https://www.coursera.org/specializations/django", "duration": "4 months", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Django Full Course - Dennis Ivy", "link": "https://www.youtube.com/watch?v=PtQiiknWUcI", "duration": "10 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Django 4 and Python Full Stack", "link": "https://www.udemy.com/course/django-and-python-full-stack-developer-masterclass/", "duration": "30 hours", "level": "Intermediate"}
    ],
    "react": [
        {"platform": "Coursera", "course": "Meta React Basics", "link": "https://www.coursera.org/learn/react-basics", "duration": "4 weeks", "level": "Intermediate"},
        {"platform": "YouTube", "course": "React JS Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "React - The Complete Guide", "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "duration": "48 hours", "level": "Intermediate"}
    ],
    "javascript": [
        {"platform": "Coursera", "course": "JavaScript Basics - UC Davis", "link": "https://www.coursera.org/learn/javascript-basics", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "JavaScript Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=jS4aFq5-91M", "duration": "8 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "JavaScript Tutorial", "link": "https://www.w3schools.com/js/", "duration": "Self paced", "level": "Beginner"}
    ],
    "html": [
        {"platform": "freeCodeCamp", "course": "Responsive Web Design", "link": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "duration": "300 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "HTML Tutorial", "link": "https://www.w3schools.com/html/", "duration": "Self paced", "level": "Beginner"},
        {"platform": "YouTube", "course": "HTML Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=pQN-pnXPaVg", "duration": "2 hours", "level": "Beginner"}
    ],
    "css": [
        {"platform": "freeCodeCamp", "course": "Responsive Web Design", "link": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "duration": "300 hours", "level": "Beginner"},
        {"platform": "YouTube", "course": "CSS Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=OXGznpKZ_sA", "duration": "6 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "CSS Tutorial", "link": "https://www.w3schools.com/css/", "duration": "Self paced", "level": "Beginner"}
    ],
    "tailwind css": [
        {"platform": "YouTube", "course": "Tailwind CSS Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=pfaSUYaSgRo", "duration": "4 hours", "level": "Beginner"},
        {"platform": "Official Docs", "course": "Tailwind CSS Documentation", "link": "https://tailwindcss.com/docs", "duration": "Self paced", "level": "Beginner"}
    ],
    "data analysis": [
        {"platform": "Coursera", "course": "Data Analysis with Python - IBM", "link": "https://www.coursera.org/learn/data-analysis-with-python", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "Kaggle", "course": "Pandas Course", "link": "https://www.kaggle.com/learn/pandas", "duration": "4 hours", "level": "Beginner"},
        {"platform": "YouTube", "course": "Data Analysis with Python - freeCodeCamp", "link": "https://www.youtube.com/watch?v=r-uOLxNrNk8", "duration": "4 hours", "level": "Beginner"}
    ],
    "pandas": [
        {"platform": "Kaggle", "course": "Pandas Course", "link": "https://www.kaggle.com/learn/pandas", "duration": "4 hours", "level": "Beginner"},
        {"platform": "YouTube", "course": "Pandas Full Course - Keith Galli", "link": "https://www.youtube.com/watch?v=vmEHCJofslg", "duration": "3 hours", "level": "Beginner"},
        {"platform": "Official Docs", "course": "Pandas Documentation", "link": "https://pandas.pydata.org/docs/getting_started/index.html", "duration": "Self paced", "level": "Beginner"}
    ],
    "numpy": [
        {"platform": "YouTube", "course": "NumPy Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=QUT1VHiLmmI", "duration": "1 hour", "level": "Beginner"},
        {"platform": "Kaggle", "course": "NumPy Tutorial", "link": "https://www.kaggle.com/learn/intro-to-machine-learning", "duration": "Self paced", "level": "Beginner"}
    ],
    "tensorflow": [
        {"platform": "Coursera", "course": "DeepLearning.AI TensorFlow Developer", "link": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "duration": "4 months", "level": "Intermediate"},
        {"platform": "YouTube", "course": "TensorFlow 2.0 - freeCodeCamp", "link": "https://www.youtube.com/watch?v=tPYj3fFJGjk", "duration": "6 hours", "level": "Intermediate"},
        {"platform": "Official Docs", "course": "TensorFlow Tutorials", "link": "https://www.tensorflow.org/tutorials", "duration": "Self paced", "level": "Intermediate"}
    ],
    "keras": [
        {"platform": "YouTube", "course": "Keras with TensorFlow - freeCodeCamp", "link": "https://www.youtube.com/watch?v=qFJeN9V1ZsI", "duration": "3 hours", "level": "Intermediate"},
        {"platform": "Official Docs", "course": "Keras Documentation", "link": "https://keras.io/getting_started/", "duration": "Self paced", "level": "Intermediate"}
    ],
    "pytorch": [
        {"platform": "YouTube", "course": "PyTorch Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=Z_ikDlimN6A", "duration": "10 hours", "level": "Intermediate"},
        {"platform": "Official Docs", "course": "PyTorch Tutorials", "link": "https://pytorch.org/tutorials/", "duration": "Self paced", "level": "Intermediate"},
        {"platform": "fast.ai", "course": "Practical Deep Learning", "link": "https://course.fast.ai", "duration": "Self paced", "level": "Intermediate"}
    ],
    "opencv": [
        {"platform": "YouTube", "course": "OpenCV Python Tutorial - freeCodeCamp", "link": "https://www.youtube.com/watch?v=oXlwWbU8l2o", "duration": "4 hours", "level": "Intermediate"},
        {"platform": "Official Docs", "course": "OpenCV Documentation", "link": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html", "duration": "Self paced", "level": "Intermediate"}
    ],
    "computer vision": [
        {"platform": "Coursera", "course": "Deep Learning Specialization", "link": "https://www.coursera.org/specializations/deep-learning", "duration": "5 months", "level": "Advanced"},
        {"platform": "YouTube", "course": "Computer Vision - freeCodeCamp", "link": "https://www.youtube.com/watch?v=01sAkU_NvOY", "duration": "6 hours", "level": "Intermediate"}
    ],
    "git": [
        {"platform": "Coursera", "course": "Introduction to Git and GitHub - Google", "link": "https://www.coursera.org/learn/introduction-git-github", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "Git and GitHub - freeCodeCamp", "link": "https://www.youtube.com/watch?v=RGOj5yH7evk", "duration": "1 hour", "level": "Beginner"},
        {"platform": "Official Docs", "course": "Git Documentation", "link": "https://git-scm.com/doc", "duration": "Self paced", "level": "Beginner"}
    ],
    "linux": [
        {"platform": "Coursera", "course": "Linux Fundamentals", "link": "https://www.coursera.org/learn/linux-fundamentals", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "Linux Command Line - freeCodeCamp", "link": "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "duration": "5 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Linux Mastery", "link": "https://www.udemy.com/course/linux-mastery/", "duration": "11 hours", "level": "Beginner"}
    ],
    "docker": [
        {"platform": "Coursera", "course": "Docker for the Absolute Beginner", "link": "https://www.coursera.org/learn/docker-for-the-absolute-beginner", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "Docker Tutorial - TechWorld with Nana", "link": "https://www.youtube.com/watch?v=3c-iBn73dDE", "duration": "3 hours", "level": "Beginner"},
        {"platform": "Official Docs", "course": "Docker Getting Started", "link": "https://docs.docker.com/get-started/", "duration": "Self paced", "level": "Beginner"}
    ],
    "kubernetes": [
        {"platform": "Coursera", "course": "Google Kubernetes Engine", "link": "https://www.coursera.org/learn/google-kubernetes-engine", "duration": "4 weeks", "level": "Advanced"},
        {"platform": "YouTube", "course": "Kubernetes - TechWorld with Nana", "link": "https://www.youtube.com/watch?v=X48VuDVv0do", "duration": "4 hours", "level": "Intermediate"}
    ],
    "aws": [
        {"platform": "Coursera", "course": "AWS Fundamentals Specialization", "link": "https://www.coursera.org/specializations/aws-fundamentals", "duration": "4 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "AWS Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=SOTamWNgDKc", "duration": "5 hours", "level": "Beginner"},
        {"platform": "Official", "course": "AWS Training and Certification", "link": "https://aws.amazon.com/training/", "duration": "Self paced", "level": "Beginner"}
    ],
    "azure": [
        {"platform": "Coursera", "course": "Microsoft Azure Fundamentals AZ-900", "link": "https://www.coursera.org/specializations/microsoft-azure-fundamentals-az-900", "duration": "3 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "Azure Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=NKEFWyqJ5XA", "duration": "11 hours", "level": "Beginner"}
    ],
    "mongodb": [
        {"platform": "Official", "course": "MongoDB University", "link": "https://learn.mongodb.com", "duration": "Self paced", "level": "Beginner"},
        {"platform": "YouTube", "course": "MongoDB Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=-bt_y4Loofg", "duration": "4 hours", "level": "Beginner"}
    ],
    "mysql": [
        {"platform": "Coursera", "course": "MySQL for Data Analytics", "link": "https://www.coursera.org/learn/mysql", "duration": "4 weeks", "level": "Beginner"},
        {"platform": "YouTube", "course": "MySQL Full Course - Programming with Mosh", "link": "https://www.youtube.com/watch?v=7S_tz1z_5bA", "duration": "3 hours", "level": "Beginner"}
    ],
    "postgresql": [
        {"platform": "YouTube", "course": "PostgreSQL Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=qw--VYLpxG4", "duration": "4 hours", "level": "Beginner"},
        {"platform": "Official Docs", "course": "PostgreSQL Tutorial", "link": "https://www.postgresql.org/docs/online-resources/", "duration": "Self paced", "level": "Beginner"}
    ],
    "rest api": [
        {"platform": "YouTube", "course": "REST API Tutorial - freeCodeCamp", "link": "https://www.youtube.com/watch?v=qbLc5a9jdXo", "duration": "2 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "REST APIs with Flask", "link": "https://www.udemy.com/course/rest-api-flask-and-python/", "duration": "17 hours", "level": "Intermediate"}
    ],
    "cybersecurity": [
        {"platform": "Coursera", "course": "Google Cybersecurity Certificate", "link": "https://www.coursera.org/professional-certificates/google-cybersecurity", "duration": "6 months", "level": "Beginner"},
        {"platform": "Coursera", "course": "IBM Cybersecurity Analyst", "link": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst", "duration": "8 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "Cybersecurity Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=hXSFdwIOfnE", "duration": "9 hours", "level": "Beginner"}
    ],
    "network security": [
        {"platform": "Coursera", "course": "Network Security & Database Vulnerabilities - IBM", "link": "https://www.coursera.org/learn/network-security-database-vulnerabilities", "duration": "4 weeks", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Network Security - freeCodeCamp", "link": "https://www.youtube.com/watch?v=qiQR5rTSshw", "duration": "9 hours", "level": "Beginner"}
    ],
    "penetration testing": [
        {"platform": "Coursera", "course": "IBM Cybersecurity Analyst", "link": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst", "duration": "8 months", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Ethical Hacking Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "duration": "15 hours", "level": "Intermediate"},
        {"platform": "TryHackMe", "course": "Jr Penetration Tester Path", "link": "https://tryhackme.com/path/outline/jrpenetrationtester", "duration": "Self paced", "level": "Beginner"}
    ],
    "cryptography": [
        {"platform": "Coursera", "course": "Cryptography I - Stanford", "link": "https://www.coursera.org/learn/crypto", "duration": "7 weeks", "level": "Advanced"},
        {"platform": "YouTube", "course": "Cryptography Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=AQDCe585Lnc", "duration": "11 hours", "level": "Intermediate"}
    ],
    "nmap": [
        {"platform": "YouTube", "course": "Nmap Tutorial - NetworkChuck", "link": "https://www.youtube.com/watch?v=4t4kBkMsDbQ", "duration": "1 hour", "level": "Beginner"},
        {"platform": "TryHackMe", "course": "Nmap Room", "link": "https://tryhackme.com/room/furthernmap", "duration": "2 hours", "level": "Beginner"}
    ],
    "wireshark": [
        {"platform": "YouTube", "course": "Wireshark Full Course - David Bombal", "link": "https://www.youtube.com/watch?v=lb1Dw0elw0Q", "duration": "4 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Wireshark: Packet Analysis", "link": "https://www.udemy.com/course/wireshark-packet-analysis-and-ethical-hacking/", "duration": "10 hours", "level": "Intermediate"}
    ],
    "metasploit": [
        {"platform": "YouTube", "course": "Metasploit Tutorial - HackerSploit", "link": "https://www.youtube.com/watch?v=8lR27r8Y_ik", "duration": "2 hours", "level": "Intermediate"},
        {"platform": "TryHackMe", "course": "Metasploit Room", "link": "https://tryhackme.com/room/metasploitintro", "duration": "2 hours", "level": "Intermediate"}
    ],
    "burp suite": [
        {"platform": "PortSwigger", "course": "Web Security Academy - Burp Suite", "link": "https://portswigger.net/burp/documentation/desktop/getting-started", "duration": "Self paced", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Burp Suite Tutorial - HackerSploit", "link": "https://www.youtube.com/watch?v=G3hpAeoZ4ek", "duration": "2 hours", "level": "Intermediate"},
        {"platform": "TryHackMe", "course": "Burp Suite Basics", "link": "https://tryhackme.com/room/burpsuitebasics", "duration": "2 hours", "level": "Beginner"}
    ],
    "owasp": [
        {"platform": "YouTube", "course": "OWASP Top 10 - freeCodeCamp", "link": "https://www.youtube.com/watch?v=rW9gZTzXBTo", "duration": "2 hours", "level": "Beginner"},
        {"platform": "Official", "course": "OWASP WebGoat", "link": "https://owasp.org/www-project-webgoat/", "duration": "Self paced", "level": "Intermediate"}
    ],
    "c++": [
        {"platform": "Coursera", "course": "C++ For C Programmers", "link": "https://www.coursera.org/learn/c-plus-plus-a", "duration": "5 weeks", "level": "Intermediate"},
        {"platform": "YouTube", "course": "C++ Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=vLnPwxZdW4Y", "duration": "4 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "C++ Tutorial", "link": "https://www.w3schools.com/cpp/", "duration": "Self paced", "level": "Beginner"}
    ],
    "bash": [
        {"platform": "YouTube", "course": "Bash Scripting Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=SPwyp2NG-bE", "duration": "3 hours", "level": "Beginner"},
        {"platform": "Udemy", "course": "Linux Shell Scripting", "link": "https://www.udemy.com/course/linux-shell-scripting-projects/", "duration": "8 hours", "level": "Intermediate"}
    ],
    "selenium": [
        {"platform": "YouTube", "course": "Selenium Python Tutorial - freeCodeCamp", "link": "https://www.youtube.com/watch?v=Xjv1sY630Uc", "duration": "2 hours", "level": "Intermediate"},
        {"platform": "Udemy", "course": "Selenium WebDriver with Python", "link": "https://www.udemy.com/course/selenium-real-time-examplesi-interview-questions/", "duration": "10 hours", "level": "Intermediate"}
    ],
    "postman": [
        {"platform": "YouTube", "course": "Postman API Testing - freeCodeCamp", "link": "https://www.youtube.com/watch?v=VywxIQ2ZXw4", "duration": "2 hours", "level": "Beginner"},
        {"platform": "Official", "course": "Postman Learning Center", "link": "https://learning.postman.com", "duration": "Self paced", "level": "Beginner"}
    ],
    "figma": [
        {"platform": "Coursera", "course": "UI/UX Design Specialization", "link": "https://www.coursera.org/specializations/ui-ux-design", "duration": "6 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "Figma Tutorial - freeCodeCamp", "link": "https://www.youtube.com/watch?v=jwCmIBJ8Jtc", "duration": "2 hours", "level": "Beginner"},
        {"platform": "Official", "course": "Figma Learn", "link": "https://www.figma.com/resources/learn-design/", "duration": "Self paced", "level": "Beginner"}
    ],
    "kotlin": [
        {"platform": "Coursera", "course": "Kotlin for Java Developers", "link": "https://www.coursera.org/learn/kotlin-for-java-developers", "duration": "5 weeks", "level": "Intermediate"},
        {"platform": "YouTube", "course": "Kotlin Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=F9UC9DY-vIU", "duration": "2 hours", "level": "Beginner"}
    ],
    "php": [
        {"platform": "YouTube", "course": "PHP Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=OK_JCtrrv-c", "duration": "4 hours", "level": "Beginner"},
        {"platform": "W3Schools", "course": "PHP Tutorial", "link": "https://www.w3schools.com/php/", "duration": "Self paced", "level": "Beginner"}
    ],
    "data science": [
        {"platform": "Coursera", "course": "IBM Data Science Professional Certificate", "link": "https://www.coursera.org/professional-certificates/ibm-data-science", "duration": "11 months", "level": "Beginner"},
        {"platform": "Kaggle", "course": "Data Science Courses", "link": "https://www.kaggle.com/learn", "duration": "Self paced", "level": "Beginner"},
        {"platform": "YouTube", "course": "Data Science Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=ua-CiDNNj30", "duration": "6 hours", "level": "Beginner"}
    ],
    "aws": [
        {"platform": "Coursera", "course": "AWS Fundamentals Specialization", "link": "https://www.coursera.org/specializations/aws-fundamentals", "duration": "4 months", "level": "Beginner"},
        {"platform": "YouTube", "course": "AWS Full Course - freeCodeCamp", "link": "https://www.youtube.com/watch?v=SOTamWNgDKc", "duration": "5 hours", "level": "Beginner"},
        {"platform": "Official", "course": "AWS Training and Certification", "link": "https://aws.amazon.com/training/", "duration": "Self paced", "level": "Beginner"}
    ]
}


def get_job_links(matched_skills):
    job_map = {
        "python": [
            {"title": "Python Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/python-internship"},
            {"title": "Python Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/python-developer-jobs"},
            {"title": "Python Developer", "company": "Naukri", "link": "https://www.naukri.com/python-developer-jobs"}
        ],
        "machine learning": [
            {"title": "ML Engineer Intern", "company": "Internshala", "link": "https://internshala.com/internships/machine-learning-internship"},
            {"title": "ML Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/machine-learning-intern-jobs"},
            {"title": "ML Engineer", "company": "Naukri", "link": "https://www.naukri.com/machine-learning-jobs"}
        ],
        "deep learning": [
            {"title": "Deep Learning Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/deep-learning-jobs"},
            {"title": "Deep Learning Engineer", "company": "Naukri", "link": "https://www.naukri.com/deep-learning-jobs"}
        ],
        "nlp": [
            {"title": "NLP Engineer Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/nlp-engineer-jobs"},
            {"title": "NLP Researcher", "company": "Naukri", "link": "https://www.naukri.com/nlp-jobs"}
        ],
        "data analysis": [
            {"title": "Data Analyst Intern", "company": "Internshala", "link": "https://internshala.com/internships/data-science-internship"},
            {"title": "Data Analyst", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/data-analyst-jobs"},
            {"title": "Data Analyst", "company": "Naukri", "link": "https://www.naukri.com/data-analyst-jobs"}
        ],
        "data science": [
            {"title": "Data Science Intern", "company": "Internshala", "link": "https://internshala.com/internships/data-science-internship"},
            {"title": "Data Scientist", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/data-scientist-jobs"},
            {"title": "Data Scientist", "company": "Naukri", "link": "https://www.naukri.com/data-scientist-jobs"}
        ],
        "flask": [
            {"title": "Flask Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "Backend Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/flask-developer-jobs"},
            {"title": "Flask Developer", "company": "Naukri", "link": "https://www.naukri.com/flask-developer-jobs"}
        ],
        "django": [
            {"title": "Django Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/django-internship"},
            {"title": "Django Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/django-developer-jobs"},
            {"title": "Django Developer", "company": "Naukri", "link": "https://www.naukri.com/django-jobs"}
        ],
        "sql": [
            {"title": "SQL Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/sql-internship"},
            {"title": "Database Analyst", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/sql-developer-jobs"},
            {"title": "SQL Developer", "company": "Naukri", "link": "https://www.naukri.com/sql-developer-jobs"}
        ],
        "javascript": [
            {"title": "Frontend Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/javascript-internship"},
            {"title": "JS Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/javascript-developer-jobs"},
            {"title": "JavaScript Developer", "company": "Naukri", "link": "https://www.naukri.com/javascript-developer-jobs"}
        ],
        "react": [
            {"title": "React Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/reactjs-internship"},
            {"title": "React Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/react-developer-jobs"},
            {"title": "React Developer", "company": "Naukri", "link": "https://www.naukri.com/reactjs-developer-jobs"}
        ],
        "cybersecurity": [
            {"title": "Cybersecurity Intern", "company": "Internshala", "link": "https://internshala.com/internships/cyber-security-internship"},
            {"title": "Security Analyst Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/cyber-security-internship-jobs"},
            {"title": "Cybersecurity Analyst", "company": "Naukri", "link": "https://www.naukri.com/cyber-security-jobs"}
        ],
        "network security": [
            {"title": "Network Security Intern", "company": "Internshala", "link": "https://internshala.com/internships/network-security-internship"},
            {"title": "Network Engineer Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/network-security-jobs"},
            {"title": "Network Security Engineer", "company": "Naukri", "link": "https://www.naukri.com/network-security-jobs"}
        ],
        "penetration testing": [
            {"title": "Penetration Tester Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/penetration-tester-jobs"},
            {"title": "Ethical Hacker", "company": "Naukri", "link": "https://www.naukri.com/ethical-hacker-jobs"},
            {"title": "Security Tester", "company": "Internshala", "link": "https://internshala.com/internships/cyber-security-internship"}
        ],
        "cryptography": [
            {"title": "Security Engineer Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/cryptography-jobs"},
            {"title": "Cryptography Engineer", "company": "Naukri", "link": "https://www.naukri.com/cryptography-jobs"}
        ],
        "nmap": [
            {"title": "SOC Analyst Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/soc-analyst-jobs"},
            {"title": "Security Operations Analyst", "company": "Naukri", "link": "https://www.naukri.com/soc-analyst-jobs"}
        ],
        "wireshark": [
            {"title": "Network Analyst Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/network-analyst-jobs"},
            {"title": "Network Engineer", "company": "Naukri", "link": "https://www.naukri.com/network-engineer-jobs"}
        ],
        "metasploit": [
            {"title": "Ethical Hacker Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/ethical-hacker-jobs"},
            {"title": "Penetration Tester", "company": "Naukri", "link": "https://www.naukri.com/penetration-tester-jobs"}
        ],
        "burp suite": [
            {"title": "Web Security Tester", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/web-security-jobs"},
            {"title": "Application Security Analyst", "company": "Naukri", "link": "https://www.naukri.com/application-security-jobs"}
        ],
        "owasp": [
            {"title": "Application Security Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/owasp-jobs"},
            {"title": "Security Engineer", "company": "Naukri", "link": "https://www.naukri.com/security-engineer-jobs"}
        ],
        "c++": [
            {"title": "C++ Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/c++-internship"},
            {"title": "C++ Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/c++-developer-jobs"},
            {"title": "C++ Engineer", "company": "Naukri", "link": "https://www.naukri.com/c-plus-plus-developer-jobs"}
        ],
        "java": [
            {"title": "Java Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/java-internship"},
            {"title": "Java Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/java-developer-jobs"},
            {"title": "Java Engineer", "company": "Naukri", "link": "https://www.naukri.com/java-developer-jobs"}
        ],
        "docker": [
            {"title": "DevOps Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/docker-jobs"},
            {"title": "DevOps Engineer", "company": "Naukri", "link": "https://www.naukri.com/docker-jobs"}
        ],
        "kubernetes": [
            {"title": "Kubernetes Engineer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/kubernetes-jobs"},
            {"title": "DevOps Engineer", "company": "Naukri", "link": "https://www.naukri.com/kubernetes-jobs"}
        ],
        "aws": [
            {"title": "Cloud Intern", "company": "Internshala", "link": "https://internshala.com/internships/cloud-computing-internship"},
            {"title": "AWS Engineer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/aws-jobs"},
            {"title": "Cloud Developer", "company": "Naukri", "link": "https://www.naukri.com/aws-jobs"}
        ],
        "azure": [
            {"title": "Azure Cloud Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/azure-jobs"},
            {"title": "Cloud Engineer", "company": "Naukri", "link": "https://www.naukri.com/azure-jobs"}
        ],
        "git": [
            {"title": "Software Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/software-development-internship"},
            {"title": "Software Engineer", "company": "Naukri", "link": "https://www.naukri.com/software-developer-jobs"}
        ],
        "linux": [
            {"title": "Linux Admin Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/linux-administrator-jobs"},
            {"title": "System Admin", "company": "Naukri", "link": "https://www.naukri.com/linux-jobs"}
        ],
        "pandas": [
            {"title": "Data Science Intern", "company": "Internshala", "link": "https://internshala.com/internships/data-science-internship"},
            {"title": "Data Analyst", "company": "Naukri", "link": "https://www.naukri.com/data-analyst-jobs"}
        ],
        "tensorflow": [
            {"title": "AI/ML Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/tensorflow-jobs"},
            {"title": "ML Engineer", "company": "Naukri", "link": "https://www.naukri.com/tensorflow-jobs"}
        ],
        "pytorch": [
            {"title": "Deep Learning Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/pytorch-jobs"},
            {"title": "AI Engineer", "company": "Naukri", "link": "https://www.naukri.com/pytorch-jobs"}
        ],
        "opencv": [
            {"title": "Computer Vision Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/computer-vision-jobs"},
            {"title": "Computer Vision Engineer", "company": "Naukri", "link": "https://www.naukri.com/computer-vision-jobs"}
        ],
        "computer vision": [
            {"title": "Computer Vision Intern", "company": "Internshala", "link": "https://internshala.com/internships/machine-learning-internship"},
            {"title": "CV Engineer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/computer-vision-engineer-jobs"}
        ],
        "selenium": [
            {"title": "QA Automation Intern", "company": "Internshala", "link": "https://internshala.com/internships/software-testing-internship"},
            {"title": "QA Engineer", "company": "Naukri", "link": "https://www.naukri.com/selenium-jobs"}
        ],
        "postman": [
            {"title": "API Tester Intern", "company": "Internshala", "link": "https://internshala.com/internships/software-testing-internship"},
            {"title": "QA Engineer", "company": "Naukri", "link": "https://www.naukri.com/api-testing-jobs"}
        ],
        "bash": [
            {"title": "DevOps Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/bash-scripting-jobs"},
            {"title": "Linux Admin", "company": "Naukri", "link": "https://www.naukri.com/bash-scripting-jobs"}
        ],
        "figma": [
            {"title": "UI/UX Design Intern", "company": "Internshala", "link": "https://internshala.com/internships/ui-ux-design-internship"},
            {"title": "UI Designer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/figma-designer-jobs"},
            {"title": "Product Designer", "company": "Naukri", "link": "https://www.naukri.com/figma-designer-jobs"}
        ],
        "php": [
            {"title": "PHP Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/php-internship"},
            {"title": "PHP Developer", "company": "Naukri", "link": "https://www.naukri.com/php-developer-jobs"}
        ],
        "kotlin": [
            {"title": "Android Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/android-app-development-internship"},
            {"title": "Android Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/kotlin-developer-jobs"}
        ],
        "mongodb": [
            {"title": "Backend Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "MongoDB Developer", "company": "Naukri", "link": "https://www.naukri.com/mongodb-jobs"}
        ],
        "mysql": [
            {"title": "Database Intern", "company": "Internshala", "link": "https://internshala.com/internships/sql-internship"},
            {"title": "MySQL Developer", "company": "Naukri", "link": "https://www.naukri.com/mysql-developer-jobs"}
        ],
        "rest api": [
            {"title": "Backend Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "API Developer", "company": "Naukri", "link": "https://www.naukri.com/api-developer-jobs"}
        ],
        "html": [
            {"title": "Web Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "Frontend Developer", "company": "Naukri", "link": "https://www.naukri.com/html-developer-jobs"}
        ],
        "css": [
            {"title": "UI Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "Frontend Developer", "company": "Naukri", "link": "https://www.naukri.com/css-developer-jobs"}
        ],
        "tailwind css": [
            {"title": "Frontend Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "UI Developer", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/tailwind-css-jobs"}
        ],
        "sqlite": [
            {"title": "Backend Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/web-development-internship"},
            {"title": "Database Developer", "company": "Naukri", "link": "https://www.naukri.com/sqlite-jobs"}
        ],
        "socket": [
            {"title": "Network Developer Intern", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/network-developer-jobs"},
            {"title": "Backend Engineer", "company": "Naukri", "link": "https://www.naukri.com/socket-programming-jobs"}
        ],
        "github": [
            {"title": "Software Developer Intern", "company": "Internshala", "link": "https://internshala.com/internships/software-development-internship"},
            {"title": "Open Source Contributor", "company": "LinkedIn", "link": "https://www.linkedin.com/jobs/software-engineer-jobs"}
        ]
    }

    seen = set()
    jobs = []
    for skill in matched_skills:
        if skill in job_map:
            for job in job_map[skill]:
                if job["title"] not in seen:
                    seen.add(job["title"])
                    jobs.append(job)
    return jobs


def get_ats_tips(score, matched, missing):
    tips = []
    if score < 40:
        tips.append("Your resume matches less than 40% of the job requirements. Consider tailoring it specifically for this role.")
    if score >= 70:
        tips.append("Great match! Your resume is well aligned with this job. Apply confidently.")
    if len(missing) > 5:
        tips.append(f"You are missing {len(missing)} key skills. Focus on adding projects that showcase these skills.")
    if "python" in missing:
        tips.append("Python is a highly demanded skill. Add Python projects to your resume immediately.")
    if "git" in missing:
        tips.append("Git is expected by almost every employer. Create a GitHub profile and push your projects.")
    if "cybersecurity" in matched:
        tips.append("Your cybersecurity background is valuable. Highlight your security tools and certifications prominently.")
    if len(matched) > 0:
        tips.append(f"Good news — you already have {len(matched)} matching skills. Highlight these prominently in your resume.")
    tips.append("Use bullet points and action verbs like 'Built', 'Developed', 'Designed' in your resume.")
    tips.append("Keep your resume to 1 page if you have less than 2 years of experience.")
    tips.append("Include your GitHub profile link and LinkedIn URL at the top of your resume.")
    tips.append("Use keywords from the job description naturally throughout your resume for better ATS scoring.")
    tips.append("Quantify your achievements — e.g. 'Scanned 1000+ ports' is better than 'Scanned ports'.")
    return tips[:6]


def get_word_frequencies(resume_text):
    stopwords = set([
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "is", "was", "are", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "i", "my", "me", "we", "our",
        "you", "your", "he", "she", "they", "it", "this", "that", "as",
        "from", "by", "not", "also", "which", "who", "can", "more"
    ])
    words = re.findall(r'\b[a-z]{4,}\b', resume_text)
    freq = {}
    for word in words:
        if word not in stopwords:
            freq[word] = freq.get(word, 0) + 1
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:30]
    return [{"word": w, "count": c} for w, c in sorted_freq]


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
    phones = re.findall(r'\+?\d[\d\s\-]{8,14}\d', resume_text)

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
        "word_count": len(resume_text.split()),
        "tips": get_ats_tips(score, matched, missing),
        "jobs": get_job_links(matched),
        "word_freq": get_word_frequencies(resume_text)
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