"""
📱 QR Code Generator Pro + PDF Export

Features:
- Dynamic QR generator at the top
- Predefined app QR codes from JSON
- Grid layout adjusts columns automatically
- Download buttons for all QR codes
- QR color customization
- Add new URLs directly via a Streamlit form
- Export the list of apps as a PDF (built-in font)
"""

import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import os
import json
import math
from fpdf import FPDF

# --- PAGE CONFIG ---
st.set_page_config(page_title="QR Code Generator Pro", page_icon="📱", layout="wide")
st.title("📱 QR Code Generator Pro Dashboard")

# --- HELPER FUNCTION TO CREATE QR IMAGE ---
def generate_qr_image(url: str, fill_color="black", back_color="white") -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
    return img

# --- DYNAMIC QR GENERATOR ---
st.header("🔹 Generate a QR Code for Any URL")
user_url = st.text_input("Enter a URL here:")

# Optional color customization
st.subheader("QR Code Colors")
col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("Fill Color", "#000000")
with col2:
    back_color = st.color_picker("Background Color", "#ffffff")

if user_url:
    pil_user = generate_qr_image(user_url, fill_color, back_color)
    buf = BytesIO()
    pil_user.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(byte_im, caption=f"QR Code for {user_url}", use_column_width=False)
    st.markdown(f"[🔗 Click to open URL]({user_url})")
    st.download_button(
        label="💾 Download QR Code",
        data=byte_im,
        file_name="dynamic_QR.png",
        mime="image/png"
    )

st.divider()
st.markdown("### Predefined App QR Codes")

# --- CREATE FOLDER FOR SAVED QR CODES ---
save_folder = "qr_codes"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# --- LOAD PREDEFINED APPS FROM JSON ---
json_file = "apps_config.json"
if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump({}, f)

with open(json_file) as f:
    apps = json.load(f)

# --- FORM TO ADD NEW URL ---
st.subheader("➕ Add New App/URL")
with st.form("add_url_form", clear_on_submit=True):
    new_name = st.text_input("App Name")
    new_url = st.text_input("App URL")
    submit = st.form_submit_button("Add App")
    if submit and new_name and new_url:
        apps[new_name] = new_url
        with open(json_file, "w") as f:
            json.dump(apps, f, indent=4)
        st.success(f"Added {new_name}!")
        st.experimental_rerun()  # Refresh app to show new QR code

# --- PDF GENERATION FUNCTION ---
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)  # Built-in font, no TTF needed

    pdf.cell(0, 10, "📱 QR Code App List", ln=True, align="C")
    pdf.ln(5)

    for i, (name, url) in enumerate(apps.items(), 1):
        pdf.multi_cell(0, 8, f"{i}. {name}: {url}")
        pdf.ln(2)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# --- BUTTON TO DOWNLOAD PDF ---
if st.button("📄 Download App List as PDF"):
    pdf_file = generate_pdf()
    st.download_button(
        label="💾 Download PDF",
        data=pdf_file,
        file_name="App_List.pdf",
        mime="application/pdf"
    )

# --- RESPONSIVE GRID DISPLAY ---
total_apps = len(apps)
if total_apps == 0:
    st.info("No apps available.")
else:
    # Determine columns based on number of apps
    # Minimum 1 column, max 4 for desktop-friendly layout
    cols_per_row = min(max(math.ceil(total_apps / 2), 1), 4)
    cols = st.columns(cols_per_row)

    for i, (name, url) in enumerate(apps.items()):
        pil_img = generate_qr_image(url)

        # Save PNG locally
        filename = os.path.join(save_folder, f"{name.replace(' ', '_')}_QR.png")
        pil_img.save(filename)

        # Convert to BytesIO for display
        buf = BytesIO()
        pil_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Determine column
        col = cols[i % cols_per_row]

        with col:
            st.markdown(f"**{name}**")
            st.image(byte_im, caption=f"Scan to open {name}", use_column_width=True)
            st.markdown(f"[🔗 Open {name}]({url})")
            st.download_button(
                label="💾 Download QR Code",
                data=byte_im,
                file_name=f"{name.replace(' ', '_')}_QR.png",
                mime="image/png"
            )

        # Start a new row after every cols_per_row
        if (i + 1) % cols_per_row == 0:
            cols = st.columns(cols_per_row)

