import streamlit as st
from PyPDF2 import PdfReader
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# -------------------------------
# PREMIUM UI CSS
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}
.main {
    background: transparent;
    color: white;
}
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #6366f1);
    border-radius: 12px;
    height: 55px;
    width: 100%;
    font-size: 18px;
}
.glass {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-top: 20px;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FUNCTIONS
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += (page.extract_text() or "")
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def calculate_match(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return round(score[0][0] * 100, 2)

def find_missing_skills(resume_text, job_text):
    return list(set(job_text.split()) - set(resume_text.split()))[:10]

def matched_skills(resume_text, job_text):
    return list(set(job_text.split()) & set(resume_text.split()))[:10]

# -------------------------------
# AI SUGGESTIONS
# -------------------------------
def generate_suggestions(score, missing, matched):
    suggestions = []

    if score < 40:
        suggestions.append("Your resume is not aligned with the job. Improve skills and projects.")
    elif score < 70:
        suggestions.append("Your resume is moderately aligned. Add more relevant experience.")
    else:
        suggestions.append("Great match! Just improve presentation and clarity.")

    if missing:
        suggestions.append("Add these important skills: " + ", ".join(missing[:5]))

    if matched:
        suggestions.append("Highlight matched skills in projects and experience section.")

    suggestions.append("Add real-world projects related to job role.")
    suggestions.append("Use action words like 'developed', 'built', 'implemented'.")
    suggestions.append("Keep resume ATS-friendly (simple format).")

    return suggestions

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<div class='title'>🧠 AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Analyze • Improve • Get Hired 🚀</p>", unsafe_allow_html=True)

# -------------------------------
# INPUT SECTION
# -------------------------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf"])

with col2:
    st.subheader("📝 Job Description")
    job_description = st.text_area("", height=180)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# BUTTON ACTION
# -------------------------------
if st.button("🚀 Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = clean_text(extract_text_from_pdf(uploaded_file))
        job_text = clean_text(job_description)

        score = calculate_match(resume_text, job_text)
        missing = find_missing_skills(resume_text, job_text)
        matched = matched_skills(resume_text, job_text)
        suggestions = generate_suggestions(score, missing, matched)

        st.markdown("## 📊 Analysis Dashboard")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"<div class='metric-card'><h2>{score}%</h2><p>Match Score</p></div>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<div class='metric-card'><h2>{len(matched)}</h2><p>Matched Skills</p></div>", unsafe_allow_html=True)

        with c3:
            st.markdown(f"<div class='metric-card'><h2>{len(missing)}</h2><p>Missing Skills</p></div>", unsafe_allow_html=True)

        st.progress(score / 100)

        # Skills
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.subheader("✅ Matched Skills")
            st.write(", ".join(matched) if matched else "No matches")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "Perfect Resume!")
            st.markdown("</div>", unsafe_allow_html=True)

        # AI Suggestions
        st.markdown("## 🤖 AI Suggestions")

        for tip in suggestions:
            st.info(tip)

    else:
        st.warning("⚠️ Please upload resume and enter job description")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<br><p style='text-align:center; opacity:0.6;'>Built by Ali Ahmad 💻</p>", unsafe_allow_html=True)