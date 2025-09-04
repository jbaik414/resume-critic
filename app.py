import streamlit as st
from src.critique import critique_resume

st.set_page_config(page_title="Resume Critic", page_icon="")



st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #2E86C1;">📄 Resume Critic</h1>
        <p style="font-size:18px;">Get instant, AI-powered feedback on your resume against top tech jobs.</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("About")
st.sidebar.info(
    "This app analyzes your resume against job postings using NLP & AI.\n\n"
    
    "Upload your resume (PDF) to get personalized feedback."
)


# Upload PDF
uploaded_file = st.file_uploader("Upload Resume", type="pdf")

if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Resume uploaded successfully!")
    with st.spinner("Analyzing resume with AI..."):
        feedback = critique_resume("temp_resume.pdf", top_k=3)

        
    st.subheader("Results")


    for f in feedback:
        st.markdown(f"""
        **Job Title Match:** {f['job_title']}  
        **Match Score:** {f['match_score']}  
        **Suggested Keywords:** {", ".join(f['missing_keywords']) if f['missing_keywords'] else "None"}
        """)
        
        st.markdown(f"""
        <div style="padding:15px; margin-bottom:15px; border-radius:12px; 
                    background-color:#F4F6F7; border:1px solid #D5DBDB;">
            <h4 style="color:#1F618D;">{job_title}</h4>
            <p><b>Match Score:</b> {score} 
            <br><b>Suggested Keywords:</b> {keywords}</p>
        </div>
        """, unsafe_allow_html=True)
