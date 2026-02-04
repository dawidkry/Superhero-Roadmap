"""
🦸‍♂️ Superhero Roadmap PDF Generator – Pro Visual Version

Features:
- Add roadmap milestones dynamically
- Reorder steps
- Optional emoji/icon for each step
- Highlight color per step
- Visual PDF timeline layout
- Download PDF directly
"""

import streamlit as st
from fpdf import FPDF
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="Superhero Roadmap Pro", page_icon="🦸‍♂️", layout="centered")
st.title("🦸‍♂️ Superhero Roadmap Pro")

# --- INITIALIZE SESSION STATE ---
if "roadmap_items" not in st.session_state:
    st.session_state.roadmap_items = []

# --- ADD NEW STEP ---
st.subheader("Add Roadmap Step")
with st.form("add_step_form", clear_on_submit=True):
    step_name = st.text_input("Step Name")
    step_desc = st.text_area("Step Description (optional)")
    step_icon = st.text_input("Icon/Emoji (optional)", value="🟦")
    step_color = st.color_picker("Highlight Color", "#4CAF50")
    submit = st.form_submit_button("Add Step")

    if submit and step_name:
        st.session_state.roadmap_items.append({
            "name": step_name,
            "desc": step_desc,
            "icon": step_icon,
            "color": step_color
        })
        st.success(f"Added step: {step_name}")

# --- DISPLAY AND REORDER STEPS ---
if st.session_state.roadmap_items:
    st.subheader("Current Roadmap")
    for idx, item in enumerate(st.session_state.roadmap_items):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"{item['icon']} **{item['name']}** — {item['desc']}")
        with col2:
            if st.button("⬆️", key=f"up_{idx}") and idx > 0:
                st.session_state.roadmap_items[idx], st.session_state.roadmap_items[idx-1] = \
                    st.session_state.roadmap_items[idx-1], st.session_state.roadmap_items[idx]
                st.experimental_rerun()
        with col3:
            if st.button("⬇️", key=f"down_{idx}") and idx < len(st.session_state.roadmap_items)-1:
                st.session_state.roadmap_items[idx], st.session_state.roadmap_items[idx+1] = \
                    st.session_state.roadmap_items[idx+1], st.session_state.roadmap_items[idx]
                st.experimental_rerun()
        with col4:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.roadmap_items.pop(idx)
                st.experimental_rerun()

# --- PDF GENERATION ---
def generate_pdf():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "🦸‍♂️ Superhero Roadmap", ln=True, align="C")
    pdf.ln(8)

    y_start = pdf.get_y()
    for item in st.session_state.roadmap_items:
        # Colored box
        pdf.set_fill_color(*[int(item['color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)])
        pdf.set_font("Arial", "B", 14)
        pdf.multi_cell(0, 10, f"{item['icon']} {item['name']}", border=1, fill=True)
        if item["desc"]:
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, f"{item['desc']}")
        pdf.ln(2)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# --- GENERATE PDF BUTTON ---
if st.button("📄 Generate PDF"):
    if not st.session_state.roadmap_items:
        st.warning("Add at least one roadmap step before generating the PDF.")
    else:
        pdf_file = generate_pdf()
        st.download_button(
            label="💾 Download Superhero Roadmap PDF",
            data=pdf_file,
            file_name="superhero_roadmap.pdf",
            mime="application/pdf"
        )
