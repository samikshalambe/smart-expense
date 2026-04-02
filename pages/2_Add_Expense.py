"""Add Expense — modern form with gradient styling."""
import streamlit as st
from datetime import datetime
from utils.db_manager import get_categories, add_expense

st.markdown("""
<style>
    .form-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .form-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 28px !important;
    }
    .form-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 8px 0 0 0 !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="form-header"><h2>➕ Add Expense</h2><p>Record a new transaction quickly</p></div>', unsafe_allow_html=True)

categories = get_categories() or []
cat_names  = [c["name"] for c in categories]

if not cat_names:
    st.warning("No categories yet. Create one in ⚙️ Settings first.")
    st.stop()

with st.form("expense_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        exp_date = st.date_input("📅 Date", datetime.now())
        category = st.selectbox("📂 Category", cat_names)
    with c2:
        amount      = st.number_input("💵 Amount (₹)", min_value=0.01, max_value=500_000.0, step=1.0, format="%.2f")
        description = st.text_input("📝 Description", placeholder="e.g. Grocery shopping")
    st.write("")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.form_submit_button("💾 Save", use_container_width=True, type="primary"):
            if add_expense(exp_date, category, amount, description):
                st.success(f"✅ ₹{amount:,.2f} in **{category}** saved!")
                st.balloons()
            else:
                st.error("Failed to save — check DB connection.")
    with col2:
        st.write("")
