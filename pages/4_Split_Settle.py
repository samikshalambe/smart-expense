import streamlit as st

from utils.styles import inject_styles, require_login
from utils.upi_helper import generate_upi_qr
from utils.auth import get_user_details

st.set_page_config(page_title="Split & Settle · SmartExpense", page_icon="₹", layout="wide")
inject_styles()
require_login()

# ── Sidebar logout ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:20px 16px 12px;">
          <p style="font-size:20px;font-weight:600;color:#e0e7ff;margin:0;">✨ SmartExpense</p>
          <p style="font-size:12px;color:#64748b;margin:4px 0 0;">{get_user_details(st.session_state['username'])}</p>
        </div>
        <hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 16px 12px;">
        """,
        unsafe_allow_html=True,
    )
    if st.button("↩  Log Out", key="logout_sidebar"):
        st.session_state["logged_in"] = False
        st.session_state["username"]  = None
        st.switch_page("app.py")

# ── Page content ───────────────────────────────────────────────────
st.title("Split & Settle")
st.write("Split a bill and generate a UPI payment QR instantly.")

c1, c2 = st.columns(2)
with c1:
    total_amount = st.number_input("Total Bill (₹)", min_value=0.0, step=10.0)
    description  = st.text_input("Description", placeholder="e.g. Dinner at Taj")
    upi_id       = st.text_input("Your UPI ID", placeholder="name@bank")
    biller_name  = st.text_input("Your Name", value="Biller")
    num_people   = st.slider("Split between", 2, 10, 2)
    if total_amount > 0:
        split = total_amount / num_people
        st.info(f"Each person pays: ₹{split:,.2f}")

with c2:
    if total_amount > 0 and upi_id:
        try:
            split  = total_amount / num_people
            qr_img = generate_upi_qr(upi_id, biller_name, split, description)
            st.image(qr_img, caption="Scan via any UPI app", use_container_width=True)
            st.download_button("Download QR", data=qr_img, file_name="upi_qr.png", mime="image/png")
        except Exception as e:
            st.error(f"Could not generate QR: {e}")
    else:
        st.markdown(
            "<div style='height:200px;display:flex;align-items:center;"
            "justify-content:center;color:#64748b;font-size:13px;'>"
            "QR code will appear here</div>",
            unsafe_allow_html=True,
        )
