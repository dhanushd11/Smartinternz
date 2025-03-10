import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Set up Google Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual API Key

# Streamlit UI
st.set_page_config(page_title="Smart Resume Generator", layout="wide")
st.title("📄 Smart Resume Generator")

# Sidebar Inputs
st.sidebar.header("📝 Enter Your Details")
name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone Number")
linkedin = st.sidebar.text_input("LinkedIn Profile URL")
experience = st.sidebar.text_area("Work Experience")
skills = st.sidebar.text_area("Skills (comma-separated)")
education = st.sidebar.text_area("Education")

# AI Enhancement Function using Google Gemini
def enhance_text(text, prompt="Optimize this resume section for ATS and impact with strong action verbs."):
    try:
        model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
        response = model.generate_content([prompt, text])
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Optimize Experience Section
if experience:
    enhanced_experience = enhance_text(experience)
    st.subheader("📌 Optimized Work Experience")
    st.write(enhanced_experience)
else:
    enhanced_experience = ""

# PDF Generation Function
from fpdf import FPDF

def generate_pdf(name, email, phone, linkedin, experience, skills, education):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, name, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    
    if email:
        pdf.cell(200, 10, email, ln=True, align='C')
    if phone:
        pdf.cell(200, 10, phone, ln=True, align='C')
    if linkedin:
        pdf.cell(200, 10, linkedin, ln=True, align='C')

    pdf.ln(10)

    # Work Experience Section
    if experience.strip():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, "Work Experience", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, experience)
        pdf.ln(5)

    # Skills Section
    if skills.strip():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, "Skills", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, skills)
        pdf.ln(5)

    # Education Section
    if education.strip():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, "Education", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, education)
        pdf.ln(5)

    # Save as PDF
    pdf.output("generated_resume.pdf")
    return "generated_resume.pdf"

# PDF Download Button
if st.sidebar.button("Download PDF"):
    file_path = generate_pdf(name, email, phone, linkedin, enhanced_experience, skills, education)
    with open(file_path, "rb") as file:
        st.download_button("📥 Download Resume", file, file_name="SmartResume.pdf")