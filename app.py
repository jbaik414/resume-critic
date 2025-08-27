import streamlit as st
from src.critique import critique_resume

st.set_page_config(page_title="Resume Critic", page_icon="")

st.title("Resume Critic")
st.write("Upload your resume as a pdf file and get instant feedback against job postings!")

# Upload PDF
uploaded_file = st.file_uploader("Upload Resume", type="pdf")

if uploaded_file:
    # Save uploaded file temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    st.info("✅ Resume uploaded successfully. Analyzing...")

    # Run critique
    feedback = critique_resume("temp_resume.pdf", top_k=3)

    st.subheader("Results")
    for f in feedback:
        st.markdown(f"""
        **Job Title Match:** {f['job_title']}  
        **Match Score:** {f['match_score']}  
        **Missing Keywords:** {", ".join(f['missing_keywords']) if f['missing_keywords'] else "None 🎉"}
        """)
