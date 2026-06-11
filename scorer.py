from groq import Groq
import pdfplumber
import json
import os
from dotenv import load_dotenv

load_dotenv()

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

def score_resume(resume_text, job_desc):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an expert ATS resume screener and hiring consultant.

Analyse this resume against the job description and return ONLY a valid JSON object with no extra text, no markdown, no backticks:

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_desc[:1500]}

Return this exact JSON format:
{{
  "score": <number 0-100>,
  "missing_keywords": ["keyword1", "keyword2"],
  "strengths": ["strength1", "strength2"],
  "improved_bullets": ["rewritten bullet 1", "rewritten bullet 2"],
  "ats_tips": ["tip1", "tip2"]
}}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content