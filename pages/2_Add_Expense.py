"""Add Expense — manual entry and PDF upload combined."""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db_manager import get_categories, add_expense
from utils.pdf_processor import parse_bank_statement

st.markdown("""
<style>
    .form-header {
        background: linear-gradient(135deg, #b29fe8 0%, #a685d0 100%);
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(166, 108, 205, 0.2);
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

st.markdown('<div class="form-header"><h2>Add Expenses</h2><p>Record transactions manually or upload bank statements</p></div>', unsafe_allow_html=True)

categories = get_categories() or []
cat_names  = [c["name"] for c in categories]

if not cat_names:
    st.warning("No categories yet. Create one in Settings first.")
    st.stop()

# ── Tabs for manual entry and upload ──────────────────────────────────
tab1, tab2 = st.tabs(["Manual Entry", "Upload Statement"])

# ── Tab 1: Manual Entry ───────────────────────────────────────────────
with tab1:
    with st.form("expense_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            exp_date = st.date_input("Date", datetime.now())
            category = st.selectbox("Category", cat_names)
        with c2:
            amount      = st.number_input("Amount (₹)", min_value=0.01, max_value=500_000.0, step=1.0, format="%.2f")
            description = st.text_input("Description", placeholder="e.g. Grocery shopping")
        st.write("")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.form_submit_button("Save", use_container_width=True, type="primary"):
                if add_expense(exp_date, category, amount, description):
                    st.success(f"₹{amount:,.2f} in {category} saved!")
                    st.balloons()
                else:
                    st.error("Failed to save — check DB connection.")

# ── Tab 2: Upload Statement ───────────────────────────────────────────
with tab2:
    st.write("")
    
    uploaded = st.file_uploader(
        "Drop your bank statement PDF here or click to browse",
        type=["pdf"],
        label_visibility="visible",
    )

    if uploaded:
        file_id = uploaded.name + str(uploaded.size)
        if st.session_state.get("upload_file_id") != file_id:
            with st.spinner("Parsing transactions..."):
                df = parse_bank_statement(uploaded)
            st.session_state["upload_df"]      = df
            st.session_state["upload_file_id"] = file_id

    df_ex: pd.DataFrame | None = st.session_state.get("upload_df")

    if df_ex is not None and not df_ex.empty:
        if "category" not in df_ex.columns:
            df_ex["category"] = "Other"

        n = len(df_ex)
        st.success(f"Found {n} transaction(s) — review and save below.")
        st.write("")

        st.markdown("**Parsed Transactions** — edit categories before saving")

        edited = st.data_editor(
            df_ex,
            num_rows="dynamic",
            hide_index=True,
            use_container_width=True,
            column_config={
                "category":    st.column_config.SelectboxColumn("Category",    options=cat_names, required=True, width="medium"),
                "amount":      st.column_config.NumberColumn("Amount (₹)",     format="₹%.2f",    width="small"),
                "date":        st.column_config.TextColumn("Date",             width="small"),
                "description": st.column_config.TextColumn("Description",      width="large"),
            },
        )
        
        st.write("")
        
        if st.button("Save All Transactions", type="primary", use_container_width=True):
            saved = 0
            for _, row in edited.iterrows():
                if add_expense(row["date"], row["category"], row["amount"], row.get("description", "")):
                    saved += 1
            st.success(f"Saved {saved} transactions!")
