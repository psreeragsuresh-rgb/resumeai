import streamlit as st
from scorer import extract_text, score_resume
import json
import tempfile
import os

st.set_page_config(page_title="ResumeAI", page_icon="📄")
st.title("📄 ResumeAI — Score your resume instantly")
st.write("Upload your resume and paste a job description to get an AI-powered match score.")

uploaded = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_desc = st.text_area("Paste the job description here", height=200)

if st.button("🔍 Analyse my resume"):
    if not uploaded or not job_desc:
        st.warning("Please upload a resume and paste a job description.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(uploaded.read())
            path = f.name
        resume_text = extract_text(path)
        os.unlink(path)

        with st.spinner("Analysing your resume with AI..."):
            raw = score_resume(resume_text, job_desc)
            result = json.loads(raw)

        st.success("Analysis complete!")
        st.metric("Match Score", f"{result['score']} / 100")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Strengths")
            for s in result["strengths"]:
                st.write("•", s)
        with col2:
            st.subheader("❌ Missing Keywords")
            for k in result["missing_keywords"]:
                st.write("•", k)

        st.subheader("✍️ Improved Bullet Points")
        for b in result["improved_bullets"]:
            st.write("•", b)

        st.subheader("💡 ATS Tips")
        for t in result["ats_tips"]:
            st.write("•", t)