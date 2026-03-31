import streamlit as st
import pandas as pd

from utils.db_manager import get_categories, add_expense
from utils.pdf_processor import parse_bank_statement

# set_page_config, inject_styles, sidebar, and login guard are all handled by app.py

st.title("Smart Upload")
st.write("Upload a bank statement PDF to auto-extract expenses.")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file:
    file_id = uploaded_file.name + str(uploaded_file.size)
    if st.session_state.get("upload_file_id") != file_id:
        with st.spinner("Analysing..."):
            df_extracted = parse_bank_statement(uploaded_file)
        st.session_state["upload_df"]      = df_extracted
        st.session_state["upload_file_id"] = file_id

if "upload_df" in st.session_state and not st.session_state["upload_df"].empty:
    df_extracted = st.session_state["upload_df"]
    categories   = get_categories()
    cat_names    = [c["name"] for c in categories]
    if "category" not in df_extracted.columns:
        df_extracted["category"] = "Other"

    st.subheader(f"Preview — {len(df_extracted)} transactions found")
    st.write("Review and edit categories, then save.")
    save_clicked = st.button("✅ Save All to Database", use_container_width=True)

    edited_df = st.data_editor(
        df_extracted,
        num_rows="dynamic",
        column_config={
            "category":    st.column_config.SelectboxColumn("Category", options=cat_names, required=True),
            "amount":      st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
            "date":        st.column_config.TextColumn("Date"),
            "description": st.column_config.TextColumn("Description"),
        },
        hide_index=True,
        use_container_width=True,
    )

    if save_clicked:
        count = skipped = 0
        for _, row in edited_df.iterrows():
            try:
                date_val = str(row["date"])[:10]
                desc     = str(row["description"])     if pd.notna(row["description"])     else ""
                source   = str(row["raw_text_source"]) if pd.notna(row["raw_text_source"]) else ""
                result   = add_expense(date_val, row["category"], float(row["amount"]), desc, source)
                if result: count += 1
                else:      skipped += 1
            except Exception:
                skipped += 1
        if count:
            st.success(f"✅ {count} expenses imported successfully!")
            del st.session_state["upload_df"]
            del st.session_state["upload_file_id"]
            st.balloons()
        if skipped:
            st.warning(f"⚠ {skipped} rows could not be saved.")

elif "upload_df" in st.session_state and st.session_state["upload_df"].empty:
    st.warning("No transactions found in this PDF. Try a different file or add manually.")
