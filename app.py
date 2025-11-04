import streamlit as st
from src.critique import critique_resume

st.set_page_config(
    page_title="Resume Critic",
    layout="centered",
)

st.markdown("""
<style>
/* Main page background */
.stApp {
    background-color: #f8f9fa;
}

/* Title styling */
h1 {
    color: #1A5276;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0;
}

h4 {
    color: #154360;
}

/* Subtitle text */
.subtitle {
    text-align: center;
    color: #34495E;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Result card styling */
.result-card {
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 25px;
    border-radius: 15px;
    background-color: white;
    border: 1px solid #D5DBDB;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05);
}

/* Progress bar label */
.progress-label {
    font-size: 14px;
    font-weight: 500;
    color: #1F618D;
    margin-top: -5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>Resume Critic</h1>
<p class="subtitle">
    Get instant, AI-powered feedback on your resume for top tech jobs.
</p>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.header("About")
st.sidebar.info(
    "This app uses **Natural Language Processing (NLP)** and **AI models** "
    "to analyze your resume against job postings.\n\n"
    "Upload your resume (PDF) to receive feedback on skills, keywords, "
    "and relevance to tech roles."
)

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully!")
    st.info("Please wait while AI analyzes your resume...")

    with st.spinner("Analyzing resume with AI..."):
        feedback = critique_resume("temp_resume.pdf", top_k=3)

    # ---- Results Section ----
    st.markdown("##Results")

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
        <div style="margin-top:-10px; margin-bottom:10px;">
            <b>Suggested Keywords:</b> {missing_keywords}
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("Please upload a PDF resume to begin analysis.")
