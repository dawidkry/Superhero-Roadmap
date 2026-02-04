import streamlit as st
from fpdf import FPDF
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="Medical AI Roadmap PDF", page_icon="📄", layout="centered")
st.title("📄 Medical AI + Automation Roadmap Generator")

st.markdown("""
Generate a **professional PDF** of your 3–6 month roadmap for building scalable medical tools with Python, Streamlit, and AI.
Click the button below to generate the PDF instantly.
""")

# --- PDF GENERATOR FUNCTION ---
def generate_pdf() -> BytesIO:
    pdf = FPDF(format='A4', unit='mm')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- LOAD FONT DIRECTLY ---
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)

    # Title
    pdf.set_font("DejaVu", "B", 18)
    pdf.multi_cell(0, 10, "🚀 Medical AI + Automation Roadmap", align='C')
    pdf.ln(5)

    # Subtitle
    pdf.set_font("DejaVu", "I", 12)
    pdf.multi_cell(0, 8, "A 3–6 month roadmap to build scalable medical tools with Python, Streamlit, and AI", align='C')
    pdf.ln(10)

    # Helper function to add sections
    def add_section(title, content):
        pdf.set_font("DejaVu", "B", 14)
        pdf.multi_cell(0, 8, title)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)

    # Example phases
    add_section("Phase 1: Foundation (Weeks 1–4)",
    """
Goal: Build a base of reusable Streamlit apps + modular code.

1. Medical Calculators Hub (MVP)
   - Apps: NIHSS, CHADS-BLED, MELD, Ranson.
   - Real-time score calculation
   - QR codes for each calculator
   - Add new calculator via JSON config
    """)

    add_section("Phase 2: Automation & Sharing (Weeks 5–8)",
    """
Goal: Make tools interactive, shareable, and partially automated.

1. Enhanced QR Hub
   - Remove old calculators
   - Auto-generate QR codes
   - Optional color themes
    """)

    add_section("Phase 3: Integration & Scaling (Weeks 9–12)",
    """
Goal: Combine all apps into a unified ecosystem.

1. Central Dashboard
   - Launch page with all calculators + AI tools
   - Dynamic QR codes for each tool
    """)

    # Save PDF to BytesIO
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# --- STREAMLIT INTERFACE ---
if st.button("📄 Generate PDF"):
    pdf_file = generate_pdf()
    st.success("PDF generated successfully!")
    st.download_button(
        label="💾 Download Roadmap PDF",
        data=pdf_file,
        file_name="Medical_AI_Roadmap.pdf",
        mime="application/pdf"
    )

