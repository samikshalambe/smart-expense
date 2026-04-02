"""PDF Report — monthly report generation and export."""
import streamlit as st
from datetime import datetime
from utils.db_manager import execute_query
from utils.report_gen import generate_pdf_report

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

st.markdown('<div class="form-header"><h2>PDF Report</h2><p>Generate and download monthly expense reports</p></div>', unsafe_allow_html=True)

# ── Month chip selector (horizontal radio = pill chips) ───────────────
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

col_l, col_r = st.columns([3, 1])
with col_l:
    selected_month_name = st.radio(
        "Month",
        MONTHS,
        index=datetime.now().month - 1,
        horizontal=True,
        label_visibility="collapsed",
    )
with col_r:
    selected_year = st.selectbox(
        "Year",
        list(range(2023, datetime.now().year + 1)),
        index=datetime.now().year - 2023,
        label_visibility="collapsed",
    )

month_num = MONTHS.index(selected_month_name) + 1
month_label = f"{selected_month_name} {selected_year}"

st.write("")
st.divider()

# ── Compact transaction summary ────────────────────────────────────────
summary_rows = execute_query(
    """SELECT category,
              COUNT(*) AS txns,
              SUM(amount) AS total
       FROM expenses
       WHERE MONTH(date)=%s AND YEAR(date)=%s
       GROUP BY category ORDER BY total DESC""",
    (month_num, selected_year),
    fetch=True,
) or []

if summary_rows:
    st.markdown(f"**{month_label} — transaction summary**")
    st.write("")

    grand_total = sum(float(r["total"]) for r in summary_rows)
    grand_txns  = sum(int(r["txns"]) for r in summary_rows)

    # Header row
    hc1, hc2, hc3 = st.columns([3, 2, 2])
    hc1.caption("Category")
    hc2.caption("Transactions")
    hc3.caption("Amount")

    for r in summary_rows:
        rc1, rc2, rc3 = st.columns([3, 2, 2])
        rc1.write(r["category"])
        rc2.write(f"{int(r['txns'])} txns")
        rc3.write(f"**₹{float(r['total']):,.0f}**")

    st.divider()
    t1, t2, t3 = st.columns([3, 2, 2])
    t1.write("**Total**")
    t2.write(f"**{grand_txns} txns**")
    t3.write(f"**₹{grand_total:,.0f}**")

    st.write("")

    # ── Generate + Download ───────────────────────────────────────
    if "pdf_data" not in st.session_state or st.session_state.get("pdf_month") != (month_num, selected_year):
        if st.button(f"⬇  Generate {month_label} report", type="primary", use_container_width=True):
            with st.spinner("Generating PDF…"):
                pdf_bytes = generate_pdf_report(month_num, selected_year)
            st.session_state["pdf_data"]  = pdf_bytes
            st.session_state["pdf_month"] = (month_num, selected_year)
            st.rerun()
    else:
        st.download_button(
            label=f"⬇  Download {month_label} report →",
            data=st.session_state["pdf_data"],
            file_name=f"SmartExpense_{month_label.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
        col_regen, _ = st.columns([1, 2])
        with col_regen:
            if st.button("↩  Select different month"):
                del st.session_state["pdf_data"]
                del st.session_state["pdf_month"]
                st.rerun()
else:
    st.info(f"No expenses found for **{month_label}**.", icon="📭")
    st.caption("Add some expenses first, then come back here to generate a report.")
