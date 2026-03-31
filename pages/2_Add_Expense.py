import streamlit as st
from datetime import datetime

from utils.db_manager import get_categories, add_expense

# set_page_config, inject_styles, sidebar, and login guard are all handled by app.py

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
