import streamlit as st
from datetime import datetime

from utils.styles import inject_styles, require_login
from utils.db_manager import get_categories, add_expense
from utils.auth import get_user_details

st.set_page_config(page_title="Add Expense · SmartExpense", page_icon="⊕", layout="wide")
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
st.title("Add Expense")

categories = get_categories()
cat_names  = [c["name"] for c in categories]

with st.form("expense_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        date     = st.date_input("Date", datetime.now())
        category = st.selectbox("Category", cat_names)
    with c2:
        amount      = st.number_input("Amount (₹)", min_value=0.01, max_value=500000.0, step=0.01)
        description = st.text_input("Description")
    if st.form_submit_button("Save Expense", use_container_width=True):
        if add_expense(date, category, amount, description):
            st.success("Expense added!")
            st.balloons()
