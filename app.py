import streamlit as st
from src.critique import critique_resume

# ---- Page Config ----
st.set_page_config(
    page_title="Resume Critic",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---- Custom CSS ----
st.markdown("""
<style>
/* ---------- GLOBAL ---------- */
:root {
    --blue-primary: #006BC3;
    --blue-deep: #0009C3;
    --teal-accent: #00C3BA;
}

.stApp {
    background: linear-gradient(to bottom right, #f8fbff, #ffffff);
    color: #1b263b;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e6e9ed;
    padding-top: 2rem;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--blue-primary) !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
    color: #2c3e50 !important;
    font-size: 0.95rem;
}
[data-testid="stSidebar"] ul {
    margin-left: -1rem;
}

/* ---------- HEADER ---------- */
.main-header {
    text-align: center;
    margin-top: 1rem;
    padding: 1.6rem;
    background: linear-gradient(90deg, var(--blue-primary), var(--teal-accent));
    color: white;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.main-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.main-header p {
    font-size: 1.05rem;
    opacity: 0.95;
}

/* ---------- UPLOAD BOX ---------- */
.upload-box {
    background-color: #ffffff;
    border-radius: 14px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    text-align: center;
}

/* ---------- FEEDBACK CARDS ---------- */
.result-card {
    background-color: #fdfdfd;
    border-radius: 14px;
    padding: 1.2rem;
    margin: 1rem 0;
    border: 1px solid #D6DBDF;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.result-card h4 {
    color: var(--blue-deep);
    margin-bottom: 0.4rem;
}
.progress-label {
    font-size: 14px;
    font-weight: 600;
    color: var(--blue-primary);
    margin-top: 4px;
}

/* ---------- PROGRESS BAR COLOR ---------- */
div[data-testid="stProgressBar"] > div > div > div {
    background-color: var(--teal-accent) !important;
}

/* ---------- ALERT BOXES (Custom Colors) ---------- */
div.stAlert > div {
    border-radius: 10px !important;
    font-weight: 500;
    border-left: 5px solid var(--blue-primary) !important;
}

/* success */
div[data-testid="stNotification"][class*="success"],
div[data-baseweb="notification"][kind="success"] {
    background-color: rgba(0, 195, 186, 0.12) !important;
    color: var(--blue-deep) !important;
}

/* info */
div[data-testid="stNotification"][class*="info"],
div[data-baseweb="notification"][kind="info"] {
    background-color: rgba(0, 107, 195, 0.1) !important;
    color: var(--blue-primary) !important;
}

/* warning */
div[data-testid="stNotification"][class*="warning"],
div[data-baseweb="notification"][kind="warning"] {
    background-color: rgba(0, 9, 195, 0.08) !important;
    color: var(--blue-deep) !important;
}

/* ---------- BUTTONS ---------- */
button[kind="primary"] {
    background-color: var(--blue-primary) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
}
button[kind="primary"]:hover {
    background-color: var(--blue-deep) !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.title("About")
st.sidebar.markdown("""
This app uses **Natural Language Processing (NLP)** and **AI models**  
to analyze your resume against job postings.

Upload your resume (PDF) to receive:  
- Keyword and skill feedback  
- Job match scores  
- Actionable improvement tips  
""")

# ---- Main Header ----
st.markdown("""
<div class="main-header">
    <h1>Resume Critic</h1>
    <p>Get instant, AI-powered feedback on your resume for top tech jobs.</p>
</div>
""", unsafe_allow_html=True)

# ---- File Upload ----
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ---- Resume Analysis ----
if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully.")
    st.info("Analyzing your resume. Please wait...")

    with st.spinner("Running AI analysis..."):
        feedback = critique_resume("temp_resume.pdf", top_k=3)

    st.markdown("### Analysis Results")

    for f in feedback:
        missing_keywords = ", ".join(f['missing_keywords']) if f['missing_keywords'] else "None"
        score_display = f"{f['match_score'] * 100:.1f}%"

        st.markdown(f"""
        <div class="result-card">
            <h4>{f['job_title']}</h4>
            <p><b>Match Score:</b> {score_display}</p>
            <div class="progress-label">Relevance</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(f['match_score'] * 100))

        st.markdown(f"""
        <div style="margin-top:-10px; margin-bottom:15px;">
            <b>Suggested Keywords:</b> {missing_keywords}
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Please upload a PDF resume to begin analysis.")
