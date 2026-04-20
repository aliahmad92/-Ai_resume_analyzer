# 🚀 AI Resume Analyzer

An AI-powered Resume Analyzer built using **Python, NLP, and Streamlit**.

It compares your resume with a job description and gives:
- ✅ Match score
- 📊 Skill comparison
- 💡 Smart suggestions to improve your resume

---

## 🧠 Features

- 📄 Upload Resume (PDF)
- 📝 Paste Job Description
- 📊 Match Score using TF-IDF & Cosine Similarity
- 🔍 Extract skills from resume
- 💡 AI-based improvement suggestions
- 🎨 Clean & modern UI (Streamlit)

---

## 🛠 Tech Stack

- Python 🐍
- Streamlit 🎨
- Scikit-learn 🤖
- PyPDF2 📄
- NLP (TF-IDF + Cosine Similarity)

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/aliahmad92/Ai_resume_analyzer.git
cd Ai_resume_analyzer

# create virtual env (optional)
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run app
streamlit run app.py
