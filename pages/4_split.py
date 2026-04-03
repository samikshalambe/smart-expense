import streamlit as st
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS
from utils.upi_helper import generate_upi_qr

st.set_page_config(page_title="Split Bills · SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()

col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<div class="card"><p class="card-title">Create a split</p>', unsafe_allow_html=True)

    total_amount = st.number_input("Total amount (₹)", min_value=0.0, step=100.0, value=0.0)
    description  = st.text_input("Description", placeholder="e.g. Monthly rent · Flat 4B · April 2026")
    upi_id       = st.text_input("Your UPI ID", placeholder="name@bank")
    biller_name  = st.text_input("Your name", value="")

    st.markdown('<p style="font-size:13px;color:#8b949e;margin:12px 0 8px;">People splitting this expense</p>', unsafe_allow_html=True)
    num_people = st.slider("", min_value=2, max_value=10, value=2, label_visibility="collapsed")

    if total_amount > 0:
        split = total_amount / num_people
        st.markdown(f"""
        <div style="background:#0d2818;border:1px solid #238636;border-radius:10px;padding:16px;margin:12px 0;">
          <p style="font-size:13px;color:#8b949e;margin:0 0 4px;">per person · scan via any UPI app</p>
          <p style="font-size:32px;font-weight:700;color:#3fb950;margin:0 0 12px;">₹{split:,.0f}</p>
          <div style="width:64px;height:64px;background:#21262d;border-radius:8px;display:flex;align-items:center;justify-content:center;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3fb950" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h1v1h-1zM16 14h1v1h-1zM18 14h3v3h-3zM14 16h1v1h-1zM14 18h1v3h-1zM16 16h1v1h-1zM18 18h1v1h-1zM20 18h1v1h-1zM16 19h3v2h-3z"/></svg>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if upi_id and biller_name:
            try:
                qr_img = generate_upi_qr(upi_id, biller_name, split, description)
                st.image(qr_img, caption="Scan to pay via any UPI app", width=200)
                col_dl, _ = st.columns([1, 2])
                with col_dl:
                    st.download_button("Download QR", data=qr_img,
                                       file_name="upi_qr.png", mime="image/png")
            except Exception as e:
                st.error(f"Could not generate QR: {e}")
        else:
            st.caption("Enter your UPI ID and name above to generate the QR code.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown("""
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <p class="card-title" style="margin:0;">How it works</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:16px;">
        <div style="display:flex;gap:12px;align-items:flex-start;">
          <div style="width:32px;height:32px;background:#1f6feb33;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <span style="color:#58a6ff;font-weight:700;font-size:14px;">1</span>
          </div>
          <div>
            <p style="font-size:14px;font-weight:500;color:#f0f6fc;margin:0 0 2px;">Enter the total bill</p>
            <p style="font-size:12px;color:#8b949e;margin:0;">Add description, your UPI ID, and how many people to split with.</p>
          </div>
        </div>
        <div style="display:flex;gap:12px;align-items:flex-start;">
          <div style="width:32px;height:32px;background:#1f6feb33;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <span style="color:#58a6ff;font-weight:700;font-size:14px;">2</span>
          </div>
          <div>
            <p style="font-size:14px;font-weight:500;color:#f0f6fc;margin:0 0 2px;">Share the QR code</p>
            <p style="font-size:12px;color:#8b949e;margin:0;">Each person scans the QR code with any UPI app — GPay, PhonePe, Paytm.</p>
          </div>
        </div>
        <div style="display:flex;gap:12px;align-items:flex-start;">
          <div style="width:32px;height:32px;background:#1f6feb33;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <span style="color:#58a6ff;font-weight:700;font-size:14px;">3</span>
          </div>
          <div>
            <p style="font-size:14px;font-weight:500;color:#f0f6fc;margin:0 0 2px;">Get paid instantly</p>
            <p style="font-size:12px;color:#8b949e;margin:0;">Payment goes directly to your UPI account. No middleman, no delays.</p>
          </div>
        </div>
      </div>
      <div style="margin-top:24px;padding:16px;background:#0d2818;border:1px solid #238636;border-radius:10px;">
        <p style="font-size:12px;color:#3fb950;margin:0;">
          ✓ Works with GPay, PhonePe, Paytm, BHIM, and all UPI apps<br>
          ✓ No registration needed for the people paying<br>
          ✓ Instant settlement to your bank account
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)