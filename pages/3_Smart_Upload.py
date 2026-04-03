"""Smart Upload — modern form with drop zone and transaction parsing."""
import streamlit as st
import pandas as pd
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

CAT_COLOR = {
    "Food": "🟢", "Groceries": "🟢",
    "Utilities": "🔵", "Dining": "🟣",
    "Transport": "🟡", "Rent": "🔷",
    "Entertainment": "🩷", "Other": "⚫",
}

st.markdown('<div class="form-header"><h2>📤 Smart Upload</h2><p>Drop a bank statement PDF to auto-parse transactions</p></div>', unsafe_allow_html=True)

# ── Drop zone ────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Drop your PDF here or click to browse",
    type=["pdf"],
    label_visibility="visible",
)

if uploaded:
    file_id = uploaded.name + str(uploaded.size)
    if st.session_state.get("upload_file_id") != file_id:
        with st.spinner("🔄 Parsing transactions… this takes a moment"):
            df = parse_bank_statement(uploaded)
        st.session_state["upload_df"]      = df
        st.session_state["upload_file_id"] = file_id

df_ex: pd.DataFrame | None = st.session_state.get("upload_df")

if df_ex is not None and not df_ex.empty:
    categories = get_categories() or []
    cat_names  = [c["name"] for c in categories]
    if "category" not in df_ex.columns:
        df_ex["category"] = "Other"

    n = len(df_ex)
    st.success(f"✅ Found **{n} transaction{'s' if n != 1 else ''}** — review and save below.", icon="✨")
    st.write("")

    # ── Live transaction table with editable categories ───────────
    st.markdown("**✏️ Parsed Transactions** — edit categories before saving")

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

    # ── Category summary pills ─────────────────────────────────────
    if not edited.empty:
        summary = edited.groupby("category")["amount"].agg(["count", "sum"])
        pill_cols = st.columns(min(len(summary), 5))
        for i, (cat, row) in enumerate(summary.iterrows()):
            emoji = CAT_COLOR.get(cat, "⚫")
            with pill_cols[i % len(pill_cols)]:
                st.metric(f"{emoji} {cat}", f"₹{row['sum']:,.0f}", f"{int(row['count'])} txns")

    st.write("")
    if st.button("✅  Save All to Database", type="primary", use_container_width=True):
        count = skipped = 0
        for _, row in edited.iterrows():
            try:
                date_val = str(row["date"])[:10]
                desc     = str(row.get("description", "")) if pd.notna(row.get("description")) else ""
                src      = str(row.get("raw_text_source", "")) if pd.notna(row.get("raw_text_source")) else ""
                if add_expense(date_val, row["category"], float(row["amount"]), desc, src):
                    count += 1
                else:
                    skipped += 1
            except Exception:
                skipped += 1

        if count:
            st.success(f"✅  {count} expense{'s' if count != 1 else ''} imported!", icon="🎉")
            del st.session_state["upload_df"]
            del st.session_state["upload_file_id"]
            st.balloons()
        if skipped:
            st.warning(f"{skipped} row(s) could not be saved.")

elif df_ex is not None and df_ex.empty:
    st.warning("No transactions found in this PDF. Try a different file or add manually.", icon="⚠️")
