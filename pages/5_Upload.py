import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS, get_badge, AVATAR_COLORS
from utils.db_manager import get_categories, add_expense
from utils.pdf_processor import parse_bank_statement

st.set_page_config(page_title="Smart Upload · SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()
navbar("Smart Upload")

col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<div class="card"><p class="card-title">Upload bank statement</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:12px;color:#8b949e;margin-bottom:12px;">
      GPay · PhonePe · HDFC · SBI · ICICI · Axis supported
    </p>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        file_id = uploaded_file.name + str(uploaded_file.size)
        if st.session_state.get("upload_file_id") != file_id:
            with st.spinner("Parsing statement..."):
                df_extracted = parse_bank_statement(uploaded_file)
            st.session_state["upload_df"]      = df_extracted
            st.session_state["upload_file_id"] = file_id

    if "upload_df" in st.session_state and not st.session_state["upload_df"].empty:
        df = st.session_state["upload_df"]
        categories = get_categories()
        cat_names  = [c["name"] for c in categories]
        if "category" not in df.columns:
            df["category"] = "Other"

        unmatched = len(df[df["category"] == "Other"])

        st.markdown(f"""
        <div style="background:#0d2818;border:1px solid #238636;border-radius:8px;padding:12px 14px;margin:12px 0;">
          <span style="color:#3fb950;font-size:13px;font-weight:500;">
            ✓ {len(df)} transactions extracted
            {f'· <span style="color:#fbbf24;">{unmatched} unmatched</span>' if unmatched else ''}
          </span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="section-label" style="margin:16px 0 8px;">AUTO-CATEGORISED</p>', unsafe_allow_html=True)

        rows_html = ""
        for _, row in df.head(8).iterrows():
            cat    = row.get("category","Other")
            desc   = str(row.get("description",""))[:28]
            amt    = float(row.get("amount", 0))
            letter = desc[0].upper() if desc else "?"
            bg, fg = AVATAR_COLORS.get(cat, ("#2a2a2a","#8b949e"))
            badge  = get_badge(cat)
            rows_html += f"""
            <div class="txn-row">
              <div class="avatar" style="background:{bg};color:{fg};">{letter}</div>
              <div class="txn-info">
                <p class="txn-name">{desc or 'Unknown'}</p>
                <p class="txn-meta">{badge}</p>
              </div>
              <p class="txn-amt">-₹{amt:,.0f}</p>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)
    elif "upload_df" in st.session_state and st.session_state["upload_df"].empty:
        st.warning("No transactions found. Try a different PDF.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="card"><p class="card-title">Parse summary</p>', unsafe_allow_html=True)

    if "upload_df" in st.session_state and not st.session_state["upload_df"].empty:
        df        = st.session_state["upload_df"]
        unmatched = len(df[df["category"] == "Other"])
        found     = len(df)

        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f'<div class="stat-card top-border-green"><p class="stat-label">Found</p><p class="stat-value">{found}</p></div>', unsafe_allow_html=True)
        with fc2:
            st.markdown(f'<div class="stat-card top-border-red"><p class="stat-label">Unmatched</p><p class="stat-value red">{unmatched}</p></div>', unsafe_allow_html=True)

        st.markdown('<p class="section-label" style="margin:16px 0 10px;">BY CATEGORY</p>', unsafe_allow_html=True)
        cat_counts = df["category"].value_counts()
        for cat, count in cat_counts.items():
            st.markdown(f"<p style='font-size:13px;margin:2px 0;'>{cat}: {count} txns</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- THE FIX IS HERE ---
        categories = get_categories()
        cat_names  = [c["name"] for c in categories]
        
        with st.expander("Review & edit before saving", expanded=True):
            edited_df = st.data_editor(
                df, num_rows="dynamic",
                column_config={
                    "category":    st.column_config.SelectboxColumn("Category", options=cat_names, required=True),
                    "amount":      st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                    "date":        st.column_config.TextColumn("Date"),
                    "description": st.column_config.TextColumn("Description"),
                },
                hide_index=True, use_container_width=True
            )

        # Button is now placed directly after the data_editor
        if st.button(f"🚀 Sync {len(edited_df)} transactions to database", use_container_width=True, type="primary"):
            count = skipped = 0
            for _, row in edited_df.iterrows():
                try:
                    res = add_expense(str(row["date"])[:10], row["category"], float(row["amount"]), str(row.get("description","")))
                    if res: count += 1
                    else: skipped += 1
                except: skipped += 1
            
            if count:
                st.success(f"✅ {count} transactions saved!")
                del st.session_state["upload_df"]
                st.balloons()
                st.rerun()

    else:
        st.info("Upload a PDF to see the summary.")

    st.markdown('</div>', unsafe_allow_html=True)