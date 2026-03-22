# Resume Scanner & Course Recommendation System

A web-based application that analyzes resumes, identifies skill gaps, and recommends relevant courses to improve career opportunities.

---

## Project Background

Developed during the **Industry Innovation Hackathon – Chennai 2026**, a 24-hour hackathon.

**Award:** Best Use of AI & Generative AI  
**Team Name:** Innovatrix

### Team Members

- Harshith B
- Boomika
- Ganesh Jaishi
- Ashvini
- Bharat Bani
- Dayanand HS

---

## Features

- Upload resumes in PDF, JPEG, and other supported formats
- Extract text using Python NLP libraries
- Identify and parse key skills from resume content
- Compare extracted skills against job descriptions
- Detect skill gaps between candidate profile and job requirements
- Recommend relevant courses to bridge identified gaps
- Language toggle (English / Tamil)
- Dark and light theme toggle
- Local LLM-based chatbot assistant
- Offline and online mode *(Beta — experimental, not fully reliable)*

---

## How It Works

1. User uploads a resume (PDF or image format)
2. Python libraries extract raw text from the file
3. Extracted text is analyzed to identify present skills
4. Skills are compared against target job descriptions
5. Missing skills (gaps) are identified
6. The system recommends courses tailored to bridge those gaps

---

## Course Recommendation System

- Contains 100 curated courses
- All course links are relevant to the problem domain
- Resources are focused on Tamil Nadu-based platforms and institutions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python |
| Data Storage | CSV (no database) |
| AI/NLP | Local LLM, NLP text processing |

---

## Project Structure

```
IIH-v6.1/
├── service/
│   ├── __init__.py
│   └── courses.csv
├── static/
│   ├── admin.html
│   ├── test.html
│   ├── theme-lang.css
│   └── theme-lang.js
├── app.py
└── README.md
```

---

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/Harshith55072/IIH---resume-scanner-and-course-recommend-system.git
cd IIH---resume-scanner-and-course-recommend-system
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment**

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the application**

```bash
python app.py
```

---

## Usage

1. Launch the application and open it in your browser
2. Upload your resume
3. View the extracted skills
4. Review identified skill gaps
5. Browse the recommended courses

---

## Limitations

- Offline mode is experimental (beta) and may be unreliable
- Skill extraction accuracy varies depending on resume formatting
- No persistent database — CSV is used for simplicity

---

## Planned Improvements

- Integration of advanced AI/ML models (e.g., BERT, enhanced LLMs)
- Database support (MongoDB or MySQL)
- Skill scoring and analytics dashboard
- User authentication and profile management
- Improved UI/UX with mobile responsiveness
- Cloud deployment support

---

## Project Status

**Status:** Completed  
**Last Updated:** March 2026

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Commit your changes with clear messages
4. Open a Pull Request for review

---

## License

This project is open-source and available under the [MIT License](LICENSE).
