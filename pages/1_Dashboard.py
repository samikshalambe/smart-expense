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
    .welcome-header {
        margin-bottom: 32px;
    }
    .welcome-header h1 {
        color: #4a3f72 !important;
        font-size: 28px !important;
        margin-bottom: 4px !important;
        font-weight: 700 !important;
    }
    .welcome-header p {
        color: #a685d0 !important;
        font-size: 14px !important;
        margin: 0 !important;
    }
    .balance-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 245, 252, 0.95) 100%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(171, 131, 201, 0.3) !important;
        padding: 28px 32px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 20px rgba(166, 108, 205, 0.1) !important;
    }
    .balance-label {
        color: #a685d0 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px !important;
    }
    .balance-value {
        color: #7c5ca8 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin-bottom: 12px !important;
    }
    .card-hint {
        color: #a685d0 !important;
        font-size: 12px !important;
    }
    .category-grid-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(248, 245, 252, 0.8) 100%) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(171, 131, 201, 0.2) !important;
        padding: 16px !important;
        text-align: center;
        transition: all 0.3s ease;
    }
    .category-grid-item:hover {
        border-color: rgba(171, 131, 201, 0.4) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(166, 108, 205, 0.1) !important;
    }
    .category-name {
        color: #4a3f72 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    .category-amount {
        color: #7c5ca8 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    .recent-payment-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(248, 245, 252, 0.6) 100%) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(171, 131, 201, 0.15) !important;
        padding: 12px 16px !important;
        margin-bottom: 8px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .payment-category {
        color: #4a3f72 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    .payment-amount {
        color: #7c5ca8 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }
    .section-title {
        color: #4a3f72 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        margin-top: 28px !important;
        margin-bottom: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Category palette ─────────────────────────────────────────────────
CAT_COLOR = {
    "Food": "#34d399", "Groceries": "#34d399",
    "Utilities": "#60a5fa",
    "Dining": "#a78bfa",
    "Transport": "#fbbf24",
    "Rent": "#818cf8",
    "Entertainment": "#ec4899",
    "Laundry": "#14b8a6",
    "Internet": "#3b82f6",
    "Services": "#f472b6",
    "Miscellaneous": "#f59e0b",
    "Outings": "#8b5cf6",
    "Car": "#ef4444",
    "Other": "#9ca3af",
}

# ── Get user and budget data ─────────────────────────────────────────
user_name = get_user_details(st.session_state["username"]) or "User"
status = get_budget_status()
budget = status["total_budget"]
current = status["current_total"]
forecast = status["predicted_total"]
remaining = budget - current
pct = int(current / budget * 100) if budget > 0 else 0

# Get category-wise expenses
cat_rows = execute_query(
    """SELECT category, SUM(amount) AS total
       FROM expenses
       WHERE MONTH(date)=MONTH(CURDATE()) AND YEAR(date)=YEAR(CURDATE())
       GROUP BY category ORDER BY total DESC""",
    fetch=True,
) or []

# Get recent expenses
recent = execute_query(
    "SELECT date, category, description, amount FROM expenses "
    "ORDER BY date DESC LIMIT 8",
    fetch=True,
) or []

# ── Welcome Header ───────────────────────────────────────────────────
st.markdown(f'''
<div class="welcome-header">
    <h1>Welcome back, {user_name}!</h1>
    <p>Here's your spending overview</p>
</div>
''', unsafe_allow_html=True)

# ── Main Layout ──────────────────────────────────────────────────────
main_col, side_col = st.columns([2, 1])

with main_col:
    # ── Available Balance Card ─────────────────────────────────────
    st.markdown(f'''
    <div class="balance-card">
        <div class="balance-label">Available Balance</div>
        <div class="balance-value">₹ {remaining:,.2f}</div>
        <div class="card-hint">•••• 3922</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # ── Stats Cards ────────────────────────────────────────────────
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Monthly Income", f"₹ {budget:,.0f}")
    with stats_col2:
        st.metric("Monthly Budget (Limit)", f"₹ {budget:,.0f}")
    with stats_col3:
        st.metric("Spent", f"₹ {current:,.0f}")
    
    # ── Recent Payments ────────────────────────────────────────────
    st.markdown('<div class="section-title">Recent Payments</div>', unsafe_allow_html=True)
    
    if recent:
        payment_html = ""
        for r in recent[:6]:
            cat = r.get("category", "Other")
            amt = r.get("amount", 0)
            payment_html += f'''
            <div class="recent-payment-item">
                <div style="display: flex; align-items: center;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {CAT_COLOR.get(cat, '#9ca3af')}; margin-right: 12px;"></div>
                    <span class="payment-category">{cat}</span>
                </div>
                <span class="payment-amount">-  ₹ {amt:,.0f}</span>
            </div>
            '''
        st.markdown(payment_html, unsafe_allow_html=True)
    else:
        st.info("No recent payments.")

with side_col:
    # ── Expenses Statistics Chart ──────────────────────────────────
    if cat_rows:
        labels = [r["category"] for r in cat_rows]
        values = [float(r["total"]) for r in cat_rows]
        colors = [CAT_COLOR.get(l, "#9ca3af") for l in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors, line=dict(color="white", width=2)),
            textinfo="none",
            hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>",
        )])
        fig.add_annotation(
            text=f"<b>{pct}%</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=24, color="#7c5ca8"),
        )
        fig.update_layout(
            title="Expenses Statistics",
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.divider()

# ── Monthly Expenses Grid ───────────────────────────────────────────
st.markdown('<div class="section-title">Monthly Expenses</div>', unsafe_allow_html=True)

if cat_rows:
    # Display categories in a grid
    cols = st.columns(3)
    for idx, (cat, val) in enumerate([(r["category"], r["total"]) for r in cat_rows]):
        with cols[idx % 3]:
            st.markdown(f'''
            <div class="category-grid-item">
                <div style="width: 20px; height: 20px; border-radius: 4px; background: {CAT_COLOR.get(cat, '#9ca3af')}; margin: 0 auto 8px;"></div>
                <div class="category-name">{cat}</div>
                <div class="category-amount">₹ {val:,.0f}</div>
            </div>
            ''', unsafe_allow_html=True)
else:
    st.info("No expenses recorded this month.")

st.divider()

# ── Daily vs Monthly Trends ────────────────────────────────────────
st.markdown('<div class="section-title">Spending Trends</div>', unsafe_allow_html=True)
trend_tab1, trend_tab2 = st.tabs(["Daily", "Monthly"])

# DAILY TREND
with trend_tab1:
    daily_data = execute_query(
        """SELECT DATE(date) AS day, SUM(amount) AS total
           FROM expenses
           WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
           GROUP BY DATE(date)
           ORDER BY day ASC""",
        fetch=True,
    ) or []
    
    if daily_data:
        df_daily = pd.DataFrame(daily_data)
        df_daily["day"] = pd.to_datetime(df_daily["day"])
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=df_daily["day"],
            y=df_daily["total"],
            mode="lines",
            name="Daily Spending",
            line=dict(color="#a685d0", width=3),
            marker=dict(size=0),
            fill="tozeroy",
            fillcolor="rgba(182, 159, 232, 0.3)",
            hovertemplate="<b>%{x|%d %b}</b><br>₹%{y:,.0f}<extra></extra>",
            smooth=True,
        ))
        fig_daily.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248, 245, 252, 0.3)",
            height=360,
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(color="#6b5b8a"),
            xaxis=dict(gridcolor="rgba(182, 159, 232, 0.1)"),
            yaxis=dict(gridcolor="rgba(182, 159, 232, 0.1)"),
        )
        st.plotly_chart(fig_daily, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No daily spending data available.")

# MONTHLY TREND
with trend_tab2:
    monthly_data = execute_query(
        """SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) AS total
           FROM expenses
           WHERE date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
           GROUP BY DATE_FORMAT(date, '%Y-%m')
           ORDER BY month ASC""",
        fetch=True,
    ) or []
    
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        df_monthly["month_label"] = pd.to_datetime(df_monthly["month"]).dt.strftime("%b %Y")
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=df_monthly["month_label"],
            y=df_monthly["total"],
            mode="lines",
            name="Monthly Spending",
            line=dict(color="#a685d0", width=3),
            marker=dict(size=0),
            fill="tozeroy",
            fillcolor="rgba(182, 159, 232, 0.3)",
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
            smooth=True,
        ))
        fig_monthly.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount (₹)",
            hovermode="x",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248, 245, 252, 0.3)",
            height=360,
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(color="#6b5b8a"),
            xaxis=dict(gridcolor="rgba(182, 159, 232, 0.1)"),
            yaxis=dict(gridcolor="rgba(182, 159, 232, 0.1)"),
        )
        st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No monthly spending data available.")
