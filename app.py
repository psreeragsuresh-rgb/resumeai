import streamlit as st
from scorer import extract_text, score_resume
import json
import tempfile
import os

st.set_page_config(page_title="ResumeAI", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .title { font-size: 2.5rem; font-weight: 800; color: #ffffff; text-align: center; margin-bottom: 0; }
    .subtitle { font-size: 1rem; color: #888; text-align: center; margin-bottom: 2rem; }
    .score-box { background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 16px; padding: 2rem; text-align: center; margin: 1rem 0; }
    .score-num { font-size: 4rem; font-weight: 900; color: #00d4aa; }
    .score-label { color: #888; font-size: 0.9rem; }
    .section-card { background: #1e1e2e; border-radius: 12px; padding: 1.2rem; margin: 0.5rem 0; }
    .tag { display: inline-block; background: #ff4b4b22; color: #ff4b4b; border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: 0.85rem; }
    .tag-green { background: #00d4aa22; color: #00d4aa; border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: 0.85rem; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📄 ResumeAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Score your resume against any job description using AI</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Upload Resume (PDF)", type="pdf")
with col2:
    job_desc = st.text_area("Paste Job Description", height=150)

if st.button("🔍 Analyse My Resume", use_container_width=True):
    if not uploaded or not job_desc:
        st.warning("Please upload a resume and paste a job description.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(uploaded.read())
            path = f.name
        resume_text = extract_text(path)
        os.unlink(path)

        with st.spinner("Analysing with AI..."):
            raw = score_resume(resume_text, job_desc)
            result = json.loads(raw)

        score = result['score']
        color = "#00d4aa" if score >= 70 else "#ffaa00" if score >= 50 else "#ff4b4b"

        st.markdown(f"""
            <div class="score-box">
                <div class="score-num" style="color:{color}">{score}</div>
                <div class="score-label">out of 100 — ATS Match Score</div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Strengths")
            for s in result["strengths"]:
                st.markdown(f'<span class="tag-green">✓ {s}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown("### ❌ Missing Keywords")
            for k in result["missing_keywords"]:
                st.markdown(f'<span class="tag">✗ {k}</span>', unsafe_allow_html=True)

        st.markdown("### ✍️ Improved Bullet Points")
        for b in result["improved_bullets"]:
            st.markdown(f"- {b}")

        st.markdown("### 💡 ATS Tips")
        for t in result["ats_tips"]:
            st.info(t)