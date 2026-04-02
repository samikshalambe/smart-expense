"""Dashboard — display spending summary and analytics."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.db_manager import execute_query
from utils.forecaster import get_budget_status
from utils.auth import get_user_details

st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(59,130,246,0.2);
    }
    .dashboard-header h1 {
        color: white !important;
        margin: 0 !important;
        font-size: 32px !important;
    }
    .dashboard-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 8px 0 0 0 !important;
        font-size: 14px !important;
    }
    .month-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ── Category palette ─────────────────────────────────────────────────
CAT_COLOR = {
    "Food": "#22c55e", "Groceries": "#22c55e",
    "Utilities": "#3b82f6",
    "Dining": "#a855f7",
    "Transport": "#f59e0b",
    "Rent": "#6366f1",
    "Entertainment": "#ec4899",
    "Other": "#6b7280",
}

# ── Data ─────────────────────────────────────────────────────────────
status   = get_budget_status()
budget   = status["total_budget"]
current  = status["current_total"]
forecast = status["predicted_total"]
remaining = budget - current

cat_rows = execute_query(
    """SELECT category, SUM(amount) AS total
       FROM expenses
       WHERE MONTH(date)=MONTH(CURDATE()) AND YEAR(date)=YEAR(CURDATE())
       GROUP BY category ORDER BY total DESC""",
    fetch=True,
) or []

# ── Header with gradient ─────────────────────────────────────────────
user_name = get_user_details(st.session_state["username"]) or "User"
month_str = datetime.now().strftime("%B %Y")

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(f'<div class="dashboard-header"><h1>Dashboard</h1><p>Your spending overview</p></div>', unsafe_allow_html=True)
with header_col2:
    st.markdown(f'<div style="text-align: right; padding: 24px 0;"><span class="month-badge">{month_str}</span></div>', unsafe_allow_html=True)

# ── Global alert banner ───────────────────────────────────────────────
if status["is_over_budget"]:
    over = forecast - budget
    st.error(f"Month-end projection: ₹{forecast:,.0f} — over budget by ₹{over:,.0f}")
elif budget > 0 and forecast > budget * 0.85:
    st.warning(
        f"Projected to spend ₹{forecast:,.0f} — approaching your ₹{budget:,.0f} budget."
    )

# ── Three stat pills ─────────────────────────────────────────────────
st.write("")
c1, c2, c3 = st.columns(3)
pct = int(current / budget * 100) if budget > 0 else 0

with c1:
    st.metric("Spent", f"₹{current:,.0f}", f"{pct}% of budget")
with c2:
    st.metric("Budget", f"₹{budget:,.0f}")
with c3:
    delta_str = f"₹{abs(remaining):,.0f} {'over' if remaining < 0 else 'left'}"
    st.metric("Left", f"₹{remaining:,.0f}", delta=delta_str,
              delta_color="inverse" if remaining < 0 else "normal")

st.divider()

# ── Donut + Legend ────────────────────────────────────────────────────
if cat_rows:
    labels = [r["category"] for r in cat_rows]
    values = [float(r["total"]) for r in cat_rows]
    colors = [CAT_COLOR.get(l, "#6b7280") for l in labels]

    # Build donut
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        hole=0.64,
        marker=dict(colors=colors, line=dict(color="rgba(0,0,0,0.15)", width=2)),
        textinfo="none",
        hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>",
        sort=False,
    )])
    fig.add_annotation(
        text=f"<b>{pct}%</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=24, color="#e2e8f0"),
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=210,
    )

    st.markdown("**Spending by Category**")
    col_donut, col_legend = st.columns([1, 1.6])
    with col_donut:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_legend:
        st.write("")
        st.write("")
        for label, value in zip(labels, values):
            kk = value / 1000
            la, lb = st.columns([3, 2])
            with la:
                st.write(f"{label}")
            with lb:
                st.write(f"₹{kk:.1f}k")

else:
    st.info("No expenses recorded this month. Use Add Expenses to get started.")

st.divider()

# ── Recent Transactions ───────────────────────────────────────────────
st.markdown("**Recent Transactions**")

recent = execute_query(
    "SELECT date, category, description, amount FROM expenses "
    "ORDER BY date DESC LIMIT 10",
    fetch=True,
) or []

if recent:
    df = pd.DataFrame(recent)
    df["amount"]   = df["amount"].astype(float).map(lambda x: f"₹{x:,.0f}")
    df["date"]     = pd.to_datetime(df["date"]).dt.strftime("%d %b %Y")
    df["description"] = df["description"].fillna("—")
    df = df.rename(columns={
        "date": "Date", "category": "Category",
        "description": "Description", "amount": "Amount",
    })
    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.caption("No transactions yet.")
