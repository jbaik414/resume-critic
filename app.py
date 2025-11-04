import streamlit as st
from src.critique import critique_resume

# ---- Page Config ----
st.set_page_config(
    page_title="Resume Critic",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(to bottom right, #f5f8fc, #ffffff);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0B3C5D;
    color: white;
    padding-top: 2rem;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #F4D03F !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
    color: #EAECEE !important;
}

.main-header {
    text-align: center;
    margin-top: 1rem;
    padding: 1.5rem;
    background: linear-gradient(90deg, #2E86C1, #1B4F72);
    color: white;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}
.main-header h1 {
    font-size: 2.3rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.main-header p {
    font-size: 1.05rem;
    opacity: 0.95;
}

.upload-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    text-align: center;
}

.result-card {
    background-color: #fdfdfd;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 1rem 0;
    border: 1px solid #D6DBDF;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.result-card h4 {
    color: #1B4F72;
    margin-bottom: 0.4rem;
}

.progress-label {
    font-size: 14px;
    font-weight: 600;
    color: #2874A6;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("About")
st.sidebar.markdown("""
This app uses **Natural Language Processing (NLP)** and **AI models**  
to analyze your resume against job postings.  

Upload your resume (PDF) to receive:  
- Keyword and skill feedback  
- Job match scores  
- Actionable improvement tips  
""")

st.markdown("""
<div class="main-header">
    <h1>Resume Critic</h1>
    <p>Get instant, AI-powered feedback on your resume for top tech jobs.</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully!")
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
