import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS
from utils.db_manager import execute_query
from utils.forecaster import get_budget_status, forecast_monthly_expense

st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()
navbar("AI Forecast")

status   = get_budget_status()
budget   = status["total_budget"]
current  = status["current_total"]
forecast = status["predicted_total"]
is_over  = status["is_over_budget"]

# ── Stat cards ──────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="stat-card top-border-blue">
      <p class="stat-label">Current spending</p>
      <p class="stat-value" style="color:#58a6ff;">₹{current:,.0f}</p>
      <p class="stat-sub">as of today</p>
    </div>""", unsafe_allow_html=True)
with c2:
    fc_color = "#f85149" if is_over else "#3fb950"
    st.markdown(f"""
    <div class="stat-card" style="border-top:2px solid {fc_color};">
      <p class="stat-label">Month-end forecast</p>
      <p class="stat-value" style="color:{fc_color};">₹{forecast:,.0f}</p>
      <p class="stat-sub">AI prediction · Linear Regression</p>
    </div>""", unsafe_allow_html=True)
with c3:
    diff = forecast - budget
    st.markdown(f"""
    <div class="stat-card {'top-border-red' if is_over else 'top-border-green'}">
      <p class="stat-label">vs budget</p>
      <p class="stat-value {'red' if is_over else 'green'}">{'+'if diff>0 else ''}₹{diff:,.0f}</p>
      <p class="stat-sub">{'over budget ⚠' if is_over else 'within budget ✓'}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Forecast chart ───────────────────────────────────────────────
today     = datetime.now()
first_day = today.replace(day=1)
last_day  = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

data = execute_query(
    "SELECT date, amount FROM expenses WHERE date >= %s ORDER BY date ASC",
    (first_day.strftime("%Y-%m-%d"),), fetch=True)

st.markdown('<div class="card"><p class="card-title">Spending trend & forecast</p>', unsafe_allow_html=True)
if data and len(data) >= 2:
    df = pd.DataFrame(data)
    df["date"]   = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)
    daily = df.groupby("date")["amount"].sum().reset_index()
    daily["cumulative"] = daily["amount"].cumsum()

    last_actual_date = daily["date"].max()
    last_actual_val  = daily["cumulative"].iloc[-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["cumulative"],
        mode="lines+markers", name="Actual",
        line=dict(color="#58a6ff", width=2),
        marker=dict(size=5, color="#58a6ff"),
    ))
    fig.add_trace(go.Scatter(
        x=[last_actual_date, last_day],
        y=[last_actual_val, forecast],
        mode="lines", name="Forecast",
        line=dict(color="#f85149" if is_over else "#3fb950", width=2, dash="dot"),
    ))
    fig.add_hline(y=budget, line_color="#fbbf24", line_dash="dash", line_width=1,
                  annotation_text=f"Budget ₹{budget:,.0f}",
                  annotation_font_color="#fbbf24")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8b949e", size=12),
        margin=dict(l=0, r=0, t=10, b=0), height=280,
        xaxis=dict(gridcolor="#21262d"), yaxis=dict(gridcolor="#21262d"),
        legend=dict(font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add at least 2 expenses this month to see your spending forecast.")
st.markdown('</div>', unsafe_allow_html=True)

# ── Category breakdown ────────────────────────────────────────────
cat_data = execute_query(
    "SELECT category, SUM(amount) as total, COUNT(*) as count FROM expenses GROUP BY category ORDER BY total DESC",
    fetch=True)

if cat_data:
    st.markdown('<div class="card"><p class="card-title">Spending by category</p>', unsafe_allow_html=True)
    cat_colors = {"Food":"#3fb950","Rent":"#a78bfa","Utilities":"#58a6ff",
                  "Entertainment":"#22d3ee","Transport":"#fbbf24","Other":"#8b949e"}
    max_val = max(float(r["total"]) for r in cat_data)
    rows = ""
    for r in cat_data:
        cat   = r["category"]
        total = float(r["total"])
        count = r["count"]
        pct   = int(total / max_val * 100)
        color = cat_colors.get(cat, "#8b949e")
        rows += f"""
        <div style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-size:13px;color:#f0f6fc;">{cat}</span>
            <span style="font-size:13px;color:#f0f6fc;font-weight:600;">
              ₹{total:,.0f} &nbsp;
              <span style="color:#8b949e;font-weight:400;font-size:11px;">{count} txns</span>
            </span>
          </div>
          <div class="progress-track" style="margin:0;">
            <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
          </div>
        </div>"""
    st.markdown(rows, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)