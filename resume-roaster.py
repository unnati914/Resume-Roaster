
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def get_gemini_response(resume_text, mode="Roast"):
    model = genai.GenerativeModel("gemini-1.5-flash") 

    if mode == "Roast":
        prompt = f"""
You are a savage but insightful hiring manager. The user has submitted a resume.
Roast them line by line — be witty, sarcastic, and brutally honest.
But end each roast with a helpful tip.

Resume:
{resume_text}
"""
    else:
        prompt = f"""
You are a professional career coach. Give detailed, section-wise feedback on this resume.
Evaluate clarity, formatting, ATS-friendliness, grammar, and impact. Provide actionable improvements.

Resume:
{resume_text}
"""

    response = model.generate_content(prompt)
    return response.text

st.set_page_config(page_title="Resume Roaster Bot", layout="centered")
st.title("🔥 Resume Roaster Bot")

mode = st.radio("Choose your flavor:", ["Brutal Roast", "Serious Review"])

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("Roast Me 🔥" if mode == "Brutal Roast" else "Review Me 👔"):
        with st.spinner("Letting the AI cook with Gemini..."):
            response = get_gemini_response(resume_text, mode="Roast" if mode == "Brutal Roast" else "Review")

        st.markdown("---")
        st.subheader("📋 Feedback")
        st.write(response)

        st.markdown("---")
        st.caption("Made with ❤️ by Unnati's AI")
