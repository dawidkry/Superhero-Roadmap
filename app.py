"""
🦸‍♂️ Superhero Roadmap PDF Generator

Features:
- Add roadmap milestones/steps dynamically
- Generate a professional PDF
- Download the PDF directly from Streamlit
- Uses built-in FPDF fonts (no TTF required)
"""

import streamlit as st
from fpdf import FPDF
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="Superhero Roadmap", page_icon="🦸‍♂️", layout="centered")
st.title("🦸‍♂️ Superhero Roadmap Generator")

st.markdown("""
This app lets you create a visual roadmap of your goals/milestones and download it as a PDF.
""")

# --- INPUT FORM FOR ROADMAP ITEMS ---
st.subheader("Add Roadmap Steps")
with st.form("roadmap_form", clear_on_submit=True):
    step_name = st.text_input("Step/Milestone Name")
    step_desc = st.text_area("Step Description (optional)")
    submit = st.form_submit_button("Add Step")
    
    if "roadmap_items" not in st.session_state:
        st.session_state.roadmap_items = []
    
    if submit and step_name:
        st.session_state.roadmap_items.append({"name": step_name, "desc": step_desc})
        st.success(f"Added step: {step_name}")

# --- DISPLAY CURRENT ROADMAP ---
if "roadmap_items" in st.session_state and st.session_state.roadmap_items:
    st.subheader("Current Roadmap")
    for i, item in enumerate(st.session_state.roadmap_items, start=1):
        st.markdown(f"**{i}. {item['name']}**")
        if item["desc"]:
            st.markdown(f"- {item['desc']}")

# --- PDF GENERATION FUNCTION ---
def generate_pdf():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🦸‍♂️ Superhero Roadmap", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for idx, item in enumerate(st.session_state.roadmap_items, start=1):
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, f"{idx}. {item['name']}")
        if item["desc"]:
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 6, f"   {item['desc']}")
        pdf.ln(2)
    
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# --- GENERATE & DOWNLOAD PDF ---
if st.button("📄 Generate PDF"):
    if "roadmap_items" not in st.session_state or not st.session_state.roadmap_items:
        st.warning("Add at least one roadmap step before generating the PDF.")
    else:
        pdf_file = generate_pdf()
        st.download_button(
            label="💾 Download Roadmap PDF",
            data=pdf_file,
            file_name="superhero_roadmap.pdf",
            mime="application/pdf"
        )

