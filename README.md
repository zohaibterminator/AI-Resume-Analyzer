# 🧠 AI Resume Analyzer

An AI-powered resume parsing and evaluation tool built with **Streamlit**, **FastAPI**, and **Supabase**. Upload your resume and job description to get an AI-generated resume score, skill match, and recommendations!

---

## 📌 Features

- 📄 Upload PDF resumes
- 🧠 AI-powered resume parsing using `pyresparser`
- ⚙️ Custom skill and experience extraction
- 📝 Compare resumes with job descriptions
- 📊 Generate resume scores and recommendations
- 💾 Stores parsed resume, recomendations and user data in a Supabase database

---

## 🚀 Getting Started (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/zohaibterminator/AI-Resume-Analyzer.git
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m nltk.downloader all
python -m spacy download en_core_web_sm
```

### 3. Setup Supabase Connection
Update your `.env` file with your Supabase (PostgreSQL-compatible) credentials.

### 4. Start the FastAPI Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --reload
```

### 5. Start the Streamlit Frontend
```bash
streamlit run streamlit_app.py
```

---

## 🧪 Technologies Used
- Frontend: Streamlit
- Backend: FastAPI
- Database: Supabase (PostgreSQL)
- Resume Parsing: pyresparser + spaCy + custom logic
- Resume Scoring: Score generation using LLM

---

## Contact
Made by Zohaib Saqib
- Email: zohaibsaqib803@gmail.com
- LinkedIn: www.linkedin.com/in/muhammadzohaibsaqib
