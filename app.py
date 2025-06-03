import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="AI Resume Reviewer", layout="centered")
st.title("📄 AI Resume Reviewer Bot")
st.markdown("Upload your resume and paste a job description below. Get AI-powered feedback instantly!")

# Upload resume
resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Optional: Paste resume text
use_text_input = st.checkbox("Or paste your resume text instead")
resume_text = ""
if use_text_input:
    resume_text = st.text_area("Paste your resume text here")

# Paste job description
job_desc = st.text_area("Paste the job description")

# Extract text from PDF if uploaded
if resume_file and not use_text_input:
    pdf_reader = PyPDF2.PdfReader(resume_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

# Button to process
if st.button("🔍 Get Resume Feedback"):
    if not resume_text.strip() or not job_desc.strip():
        st.warning("Please provide both resume and job description.")
    else:
        # Initialize OpenAI client with API key from Streamlit secrets
        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

        with st.spinner("Analyzing your resume..."):
            prompt = f"""
            You are an expert AI resume reviewer. Given the resume and job description below, provide:
            - A match score from 0 to 100
            - 3 strengths of the candidate
            - 3 weaknesses or concerns
            - Specific improvement suggestions
            Be concise, specific, and professional.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_desc}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career coach and resume reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            feedback = response.choices[0].message.content
            st.markdown("### ✅ AI Feedback")
            st.markdown(feedback)
