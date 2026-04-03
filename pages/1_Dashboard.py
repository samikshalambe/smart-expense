import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS, get_badge, get_avatar, AVATAR_COLORS
from utils.db_manager import execute_query
from utils.forecaster import get_budget_status
from utils.auth import get_user_details
from utils.report_gen import generate_pdf_report

st.set_page_config(page_title="Dashboard · SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()

user_name = get_user_details(st.session_state["username"])
hour      = datetime.now().hour
greeting  = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

# ── Header ──────────────────────────────────────────────────────
col_h, col_a = st.columns([8, 1])
with col_h:
    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <p style="font-size:24px;font-weight:700;color:#f0f6fc;margin:0;">{greeting}, {user_name} 👋</p>
      <p style="font-size:13px;color:#8b949e;margin:4px 0 0;">{datetime.now().strftime('%A, %d %B %Y')}</p>
    </div>""", unsafe_allow_html=True)
with col_a:
    initials = user_name[:2].upper()
    st.markdown(f"""
    <div style="width:42px;height:42px;border-radius:50%;background:#1f6feb33;
                display:flex;align-items:center;justify-content:center;
                font-size:14px;font-weight:600;color:#58a6ff;margin-top:4px;">
      {initials}
    </div>""", unsafe_allow_html=True)

# ── Budget hero ─────────────────────────────────────────────────
status   = get_budget_status()
budget   = status["total_budget"]
current  = status["current_total"]
forecast = status["predicted_total"]
pct      = min(int((current / budget * 100) if budget > 0 else 0), 100)
remaining = max(budget - current, 0)
bar_color = "#f85149" if status["is_over_budget"] else "#3fb950"

st.markdown(f"""
<div class="card" style="border-top:2px solid {'#f85149' if status['is_over_budget'] else '#3fb950'};">
  <p class="section-label">Total monthly budget</p>
  <p class="hero-amount">₹{budget:,.0f}</p>
  <div class="progress-track">
    <div class="progress-fill" style="width:{pct}%;background:{bar_color};"></div>
  </div>
  <div style="display:flex;justify-content:space-between;">
    <span style="font-size:12px;color:#8b949e;">₹{current:,.0f} spent</span>
    <span style="font-size:12px;color:#8b949e;">{pct}% used</span>
  </div>
</div>
""", unsafe_allow_html=True)

if status["is_over_budget"]:
    over = forecast - budget
    st.error(f"⚠ Forecast: you may exceed your budget by ₹{over:,.0f} this month.")
else:
    st.success("✓ Your spending is on track for this month.")

# ── Stat cards ──────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="stat-card top-border-red">
      <p class="stat-label">Current spending</p>
      <p class="stat-value red">₹{current:,.0f}</p>
      <p class="stat-sub">{datetime.now().strftime('%B %Y')}</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-card top-border-blue">
      <p class="stat-label">Month-end forecast</p>
      <p class="stat-value" style="color:#58a6ff;">₹{forecast:,.0f}</p>
      <p class="stat-sub">AI prediction</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-card top-border-green">
      <p class="stat-label">Remaining budget</p>
      <p class="stat-value green">₹{remaining:,.0f}</p>
      <p class="stat-sub">available to spend</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ──────────────────────────────────────────────────────
cat_data = execute_query("SELECT category, amount FROM expenses", fetch=True)
if cat_data:
    df_exp = pd.DataFrame(cat_data)
    df_exp["amount"] = df_exp["amount"].astype(float)
    totals = df_exp.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="card"><p class="card-title">Spending by category</p>', unsafe_allow_html=True)
        cat_colors = {"Food":"#3fb950","Rent":"#a78bfa","Utilities":"#58a6ff","Entertainment":"#22d3ee","Transport":"#fbbf24","Other":"#8b949e"}
        fig = px.bar(totals, x="amount", y="category", orientation="h",
                     color="category", color_discrete_map=cat_colors,
                     labels={"amount":"","category":""})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#8b949e", size=12), showlegend=False,
                          margin=dict(l=0, r=0, t=0, b=0), height=200,
                          xaxis=dict(gridcolor="#21262d"), yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card"><p class="card-title">Category breakdown</p>', unsafe_allow_html=True)
        fig2 = px.pie(totals, values="amount", names="category", hole=0.55,
                      color="category", color_discrete_map=cat_colors)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e", size=12),
                           margin=dict(l=0, r=0, t=0, b=0), height=200,
                           legend=dict(font=dict(color="#8b949e", size=11)))
        fig2.update_traces(textinfo="none")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Recent transactions ──────────────────────────────────────────
recent = execute_query(
    "SELECT date, category, amount, description FROM expenses ORDER BY date DESC LIMIT 6",
    fetch=True)

st.markdown('<div class="card"><p class="card-title">Recent transactions</p>', unsafe_allow_html=True)
if recent:
    rows_html = ""
    for r in recent:
        cat      = r["category"]
        bg, fg   = AVATAR_COLORS.get(cat, ("#2a2a2a","#8b949e"))
        letter   = (r["description"] or cat)[0].upper()
        date_str = r["date"].strftime("%d %b") if hasattr(r["date"], "strftime") else str(r["date"])
        desc     = str(r["description"] or cat)[:28]
        badge    = get_badge(cat)
        rows_html += f"""
        <div class="txn-row">
          <div class="avatar" style="background:{bg};color:{fg};">{letter}</div>
          <div class="txn-info">
            <p class="txn-name">{desc}</p>
            <p class="txn-meta">{date_str} &nbsp;·&nbsp; {badge}</p>
          </div>
          <div class="txn-right">
            <p class="txn-amt">-₹{float(r['amount']):,.0f}</p>
          </div>
        </div>"""
    st.markdown(rows_html, unsafe_allow_html=True)
else:
    st.info("No transactions yet. Add one or upload a PDF statement.")
st.markdown('</div>', unsafe_allow_html=True)

# ── Export report ────────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-title">Export report</p>', unsafe_allow_html=True)
cm, cy, cg = st.columns([2, 2, 3])
with cm:
    report_month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1,
                                format_func=lambda x: datetime(2024, x, 1).strftime("%B"))
with cy:
    report_year = st.selectbox("Year", range(2023, datetime.now().year + 1),
                               index=datetime.now().year - 2023)
with cg:
    st.write(" ")
    if st.button("Generate PDF Report"):
        with st.spinner("Generating..."):
            st.session_state["current_report"]  = generate_pdf_report(report_month, report_year)
            st.session_state["report_filename"] = f"Expense_Report_{report_month}_{report_year}.pdf"
if "current_report" in st.session_state:
    st.download_button("⬇ Download Report", data=st.session_state["current_report"],
                       file_name=st.session_state["report_filename"], mime="application/pdf")
st.markdown('</div>', unsafe_allow_html=True)