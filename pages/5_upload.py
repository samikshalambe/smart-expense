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

        # Count unmatched
        unmatched = len(df[df["category"] == "Other"])

        st.markdown(f"""
        <div style="background:#0d2818;border:1px solid #238636;border-radius:8px;
                    padding:12px 14px;margin:12px 0;">
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
        if len(df) > 8:
            st.caption(f"Showing 8 of {len(df)} transactions. All will be saved.")

    elif "upload_df" in st.session_state and st.session_state["upload_df"].empty:
        st.warning("No transactions found. Try a different PDF or add manually.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="card"><p class="card-title">Parse summary</p>', unsafe_allow_html=True)

    if "upload_df" in st.session_state and not st.session_state["upload_df"].empty:
        df       = st.session_state["upload_df"]
        unmatched = len(df[df["category"] == "Other"])
        found     = len(df)

        # Found / Unmatched
        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #21262d;border-top:2px solid #3fb950;border-radius:10px;padding:14px;">
              <p class="stat-label">Found</p>
              <p style="font-size:32px;font-weight:700;color:#f0f6fc;margin:4px 0 2px;">{found}</p>
              <p style="font-size:11px;color:#8b949e;margin:0;">transactions</p>
            </div>""", unsafe_allow_html=True)
        with fc2:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #21262d;border-top:2px solid #f85149;border-radius:10px;padding:14px;">
              <p class="stat-label">Unmatched</p>
              <p style="font-size:32px;font-weight:700;color:#f85149;margin:4px 0 2px;">{unmatched}</p>
              <p style="font-size:11px;color:#8b949e;margin:0;">need review</p>
            </div>""", unsafe_allow_html=True)

        # By category
        st.markdown('<p class="section-label" style="margin:16px 0 10px;">BY CATEGORY</p>', unsafe_allow_html=True)
        cat_colors = {"Food":"#3fb950","Rent":"#a78bfa","Utilities":"#58a6ff","Entertainment":"#22d3ee","Transport":"#fbbf24","Other":"#8b949e"}
        cat_counts = df["category"].value_counts()
        max_count  = cat_counts.max()
        for cat, count in cat_counts.items():
            pct   = int(count / max_count * 100)
            color = cat_colors.get(cat, "#8b949e")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
              <span style="font-size:13px;color:#f0f6fc;width:110px;flex-shrink:0;">{cat}</span>
              <div style="flex:1;height:6px;background:#21262d;border-radius:99px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:99px;"></div>
              </div>
              <span style="font-size:12px;color:#8b949e;width:48px;text-align:right;">{count} txns</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Edit & save
        categories = get_categories()
        cat_names  = [c["name"] for c in categories]
        with st.expander("Review & edit before saving"):
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
        else:
            edited_df = df

        if st.button(f"Sync {found} transactions to database →", use_container_width=True):
            count = skipped = 0
            for _, row in edited_df.iterrows():
                try:
                    result = add_expense(
                        str(row["date"])[:10], row["category"], float(row["amount"]),
                        str(row.get("description","")) if pd.notna(row.get("description","")) else "",
                        str(row.get("raw_text_source","")) if pd.notna(row.get("raw_text_source","")) else "",
                    )
                    if result: count += 1
                    else: skipped += 1
                except Exception: skipped += 1

            if count:
                st.success(f"✅ {count} expenses imported successfully!")
                del st.session_state["upload_df"]
                del st.session_state["upload_file_id"]
                st.balloons()
            if skipped:
                st.warning(f"⚠ {skipped} rows could not be saved.")

        st.markdown(f'<p style="font-size:11px;color:#8b949e;margin-top:8px;text-align:center;">{unmatched} unmatched transactions will be flagged for manual review</p>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:#8b949e;">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#30363d" stroke-width="1.5" style="margin-bottom:12px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
          <p style="font-size:14px;margin:0;">Upload a PDF to see the parse summary</p>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)