import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from utils.styles import inject_styles, require_login
from utils.db_manager import execute_query
from utils.forecaster import get_budget_status
from utils.auth import get_user_details
from utils.report_gen import generate_pdf_report

st.set_page_config(page_title="Dashboard · SmartExpense", page_icon="⊞", layout="wide")
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

# ── Greeting header ────────────────────────────────────────────────
user_name = get_user_details(st.session_state["username"])
hour      = datetime.now().hour
greeting  = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
      <div>
        <p style="font-size:22px;font-weight:600;color:#f1f5f9;margin:0;">{greeting}, {user_name} 👋</p>
        <p style="font-size:13px;color:#64748b;margin:4px 0 0;">{datetime.now().strftime('%A, %d %B %Y')}</p>
      </div>
      <div style="width:42px;height:42px;border-radius:50%;background:rgba(99,102,241,0.2);
                  display:flex;align-items:center;justify-content:center;
                  font-size:15px;font-weight:600;color:#818cf8;">
        {user_name[:2].upper()}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Budget hero card ───────────────────────────────────────────────
status   = get_budget_status()
budget   = status["total_budget"]
current  = status["current_total"]
forecast = status["predicted_total"]
pct      = min(int((current / budget * 100) if budget > 0 else 0), 100)
fill_cls = "progress-fill-warn" if status["is_over_budget"] else "progress-fill-ok"

st.markdown(
    f"""
    <div class="hero-card">
      <p class="hero-label">Total monthly budget</p>
      <p class="hero-amount">₹{budget:,.0f}</p>
      <div class="progress-track"><div class="{fill_cls}" style="width:{pct}%;"></div></div>
      <div class="progress-meta"><span>₹{current:,.0f} spent</span><span>{pct}% used</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if status["is_over_budget"]:
    over = forecast - budget
    st.markdown(
        f'<div class="warn-strip">⚠ Forecast: you may exceed budget by ₹{over:,.0f} this month.</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="ok-strip">✓ Your spending is on track for this month.</div>', unsafe_allow_html=True)

# ── Metrics ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1: st.metric("Current Spending",   f"₹{current:,.0f}")
with c2: st.metric("Month-end Forecast", f"₹{forecast:,.0f}")
with c3: st.metric("Remaining Budget",   f"₹{max(budget - current, 0):,.0f}")

# ── Charts ─────────────────────────────────────────────────────────
cat_data = execute_query("SELECT category, amount FROM expenses", fetch=True)
if cat_data:
    df_exp = pd.DataFrame(cat_data)
    df_exp["amount"] = df_exp["amount"].astype(float)
    totals = df_exp.groupby("category")["amount"].sum().reset_index()
    totals = totals.sort_values("amount", ascending=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-head">Spending by category</p>', unsafe_allow_html=True)
        fig = px.bar(
            totals, x="amount", y="category", orientation="h",
            labels={"amount": "", "category": ""},
            color="amount", color_continuous_scale="Purples",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#94a3b8", coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=0, b=0), height=240,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-head">Category share</p>', unsafe_allow_html=True)
        fig2 = px.pie(
            totals, values="amount", names="category", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8",
            margin=dict(l=0, r=0, t=0, b=0), height=240,
            showlegend=True, legend=dict(font=dict(color="#94a3b8")),
        )
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No expenses yet. Add one via the sidebar navigation or upload a PDF statement.")

# ── Recent transactions ────────────────────────────────────────────
recent = execute_query(
    "SELECT date, category, amount, description FROM expenses ORDER BY date DESC LIMIT 8",
    fetch=True,
)
if recent:
    dot_colors = {
        "Food": "#22c55e", "Rent": "#818cf8", "Utilities": "#f59e0b",
        "Transport": "#f97316", "Entertainment": "#ec4899", "Other": "#64748b",
    }
    st.markdown('<p class="section-head">Recent transactions</p>', unsafe_allow_html=True)
    rows_html = ""
    for r in recent:
        color    = dot_colors.get(r["category"], "#64748b")
        date_str = r["date"].strftime("%d %b") if hasattr(r["date"], "strftime") else str(r["date"])
        desc     = str(r["description"] or r["category"])[:30]
        rows_html += f"""
        <div class="txn-row">
          <div class="txn-dot" style="background:{color};"></div>
          <div style="flex:1;">
            <div class="txn-name">{desc}</div>
            <div class="txn-meta">{date_str} · {r['category']}</div>
          </div>
          <span class="txn-amt">-₹{float(r['amount']):,.0f}</span>
        </div>"""
    st.markdown(f'<div class="txn-card">{rows_html}</div>', unsafe_allow_html=True)

# ── PDF report export ──────────────────────────────────────────────
st.markdown('<p class="section-head">Export report</p>', unsafe_allow_html=True)
cm, cy, cg = st.columns([2, 2, 3])
with cm:
    report_month = st.selectbox(
        "Month", range(1, 13), index=datetime.now().month - 1,
        format_func=lambda x: datetime(2024, x, 1).strftime("%B"),
    )
with cy:
    report_year = st.selectbox(
        "Year", range(2023, datetime.now().year + 1),
        index=datetime.now().year - 2023,
    )
with cg:
    st.write(" ")
    if st.button("Generate PDF Report"):
        with st.spinner("Generating..."):
            st.session_state["current_report"]  = generate_pdf_report(report_month, report_year)
            st.session_state["report_filename"] = f"Expense_Report_{report_month}_{report_year}.pdf"

if "current_report" in st.session_state:
    st.download_button(
        "⬇ Download Report",
        data=st.session_state["current_report"],
        file_name=st.session_state["report_filename"],
        mime="application/pdf",
    )
