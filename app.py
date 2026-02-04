"""
📄 Medical AI Roadmap PDF Generator – Streamlit App
Fully Unicode-safe (supports emojis) and ready for Streamlit Cloud
"""

import streamlit as st
from fpdf import FPDF
from io import BytesIO
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Medical AI Roadmap PDF", page_icon="📄", layout="centered")
st.title("📄 Medical AI + Automation Roadmap Generator")

st.markdown("""
This app generates a **professional PDF** of your 3–6 month roadmap for building scalable medical tools with Python, Streamlit, and AI.
Click the button below to generate the PDF instantly.
""")

# --- HELPER FUNCTION TO CREATE PDF ---
def generate_pdf() -> BytesIO:
    pdf = FPDF(format='A4', unit='mm')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- ADD UTF-8 FONT ---
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        st.error("DejaVuSans.ttf font file not found. Please upload it in the same folder as app.py.")
        return None
    pdf.add_font('DejaVu', '', font_path, uni=True)
    
    # Title
    pdf.set_font("DejaVu", "B", 18)
    pdf.multi_cell(0, 10, "🚀 Medical AI + Automation Roadmap", align='C')
    pdf.ln(5)

    # Subtitle
    pdf.set_font("DejaVu", "I", 12)
    pdf.multi_cell(0, 8, "A 3–6 month step-by-step roadmap to build scalable medical tools with Python, Streamlit, and AI", align='C')
    pdf.ln(10)

    # Helper to add sections
    def add_section(title, content):
        pdf.set_font("DejaVu", "B", 14)
        pdf.multi_cell(0, 8, title)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)

    # --- PHASES ---
    add_section("Phase 1: Foundation (Weeks 1–4)",
    """
Goal: Build a base of reusable Streamlit apps + modular code.

1. Medical Calculators Hub (MVP)
   - Apps: NIHSS, CHADS-BLED, MELD, Ranson.
   - Real-time score calculation
   - QR codes for each calculator
   - Add new calculator via JSON config

2. Patient Dashboard Prototype
   - Inputs for anonymized patient data
   - Show multiple scores per patient
   - MVP: Display trends with charts
    """)

    add_section("Phase 2: Automation & Sharing (Weeks 5–8)",
    """
Goal: Make tools interactive, shareable, and partially automated.

1. Enhanced QR Hub
   - Remove old calculators
   - Auto-generate QR codes
   - Optional color themes

2. AI-Powered Suggestions (MVP)
   - Input labs/vitals → AI suggests score ranges and alerts

3. Training Modules
   - Interactive quiz for residents
   - QR code access for mobile
    """)

    add_section("Phase 3: Integration & Scaling (Weeks 9–12)",
    """
Goal: Combine all apps into a unified ecosystem.

1. Central Dashboard
   - Launch page with all calculators + AI tools
   - Dynamic QR codes for each tool

2. Patient Outcome Tracking
   - Store patient data (SQLite or Google Sheets)
   - Trend reports and export options

3. AI-Driven Insights
   - Summarize patient data
   - Suggest next steps
   - Optional: Auto-generate slides for rounds
    """)

    add_section("Phase 4: Advanced Automation (Weeks 13–24)",
    """
Goal: Fully “broken skill mode”.

1. Hospital Workflow Apps
   - Admit/discharge checklists with QR codes
   - Medication dosing calculators
   - Flag abnormal labs automatically

2. Collaboration Tools
   - Shared dashboards with auto-updating QR codes

3. Research + Reporting Automation
   - Generate draft manuscript tables
   - AI-assisted visualizations
   - QR codes link to interactive dashboards
    """)

    add_section("Key Principles",
    """
- Everything modular: JSON configs → no new code needed.
- Always QR-enabled: share tools instantly.
- MVP first → add AI, automation, reporting later.
- Start with patient data display & scoring → then AI suggestions → full workflow automation.
    """)

    add_section("Meta Advantage",
    """
By Month 3–4, you can have your own mini-hospital tool ecosystem:
- Web-based
- Instantly shareable
- Partially AI-driven
- Saves hours weekly
- Trains residents better
- Real-time decisions faster than old workflows
    """)

    # Save PDF to BytesIO
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# --- STREAMLIT BUTTON ---
if st.button("📄 Generate PDF"):
    pdf_file = generate_pdf()
    if pdf_file:
        st.success("PDF generated successfully!")
        st.download_button(
            label="💾 Download Roadmap PDF",
            data=pdf_file,
            file_name="Medical_AI_Roadmap.pdf",
            mime="application/pdf"
        )
