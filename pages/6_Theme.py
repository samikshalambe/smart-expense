"""Daily Spending — spending trends and forecasts."""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

from utils.db_manager import execute_query, get_categories
from utils.forecaster import get_budget_status

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

# ── Palette ───────────────────────────────────────────────────────────
CAT_COLOR = {
    "Food": "#22c55e", "Groceries": "#22c55e",
    "Utilities": "#3b82f6",
    "Dining": "#a855f7",
    "Transport": "#f59e0b",
    "Rent": "#6366f1",
    "Entertainment": "#ec4899",
    "Other": "#6b7280",
}

# ── Date context ──────────────────────────────────────────────────────
now     = datetime.now()
month   = now.month
year    = now.year
today   = now.day
first   = now.replace(day=1)
last    = (first.replace(month=month % 12 + 1, year=year + month // 12) - timedelta(days=1))
days_in_month = last.day

# ── Budget & totals ───────────────────────────────────────────────────
status  = get_budget_status()
budget  = status["total_budget"]
current = status["current_total"]
forecast = status["predicted_total"]

# ── Header row ────────────────────────────────────────────────────────
st.markdown(f'<div class="form-header"><h2>Daily Spending</h2><p>{now.strftime("%B %Y")}  ·  Day {today} of {days_in_month}</p></div>', unsafe_allow_html=True)
st.write("")

proj_color = "🔴" if forecast > budget else "🟢"
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Spent so far", f"₹{current:,.0f}")
with c2:
    delta = "over budget!" if forecast > budget else f"within ₹{budget:,.0f} limit"
    st.metric("Projected",   f"₹{forecast:,.0f}", delta=delta,
              delta_color="inverse" if forecast > budget else "normal")
with c3:
    st.metric("Budget limit", f"₹{budget:,.0f}")

st.divider()

# ── Daily spending chart ──────────────────────────────────────────────
daily_rows = execute_query(
    """SELECT DAY(date) AS day, SUM(amount) AS total
       FROM expenses
       WHERE MONTH(date)=%s AND YEAR(date)=%s
       GROUP BY DAY(date) ORDER BY day""",
    (month, year), fetch=True,
) or []

day_map = {int(r["day"]): float(r["total"]) for r in daily_rows}

# Build actual cumulative
actual_days  = list(range(1, today + 1))
cumulative   = []
running      = 0.0
for d in actual_days:
    running += day_map.get(d, 0.0)
    cumulative.append(running)

# Build projection (linear from current spend rate)
daily_rate  = (cumulative[-1] / today) if today > 0 and cumulative else 0.0
proj_days   = list(range(today, days_in_month + 1))
proj_vals   = [
    cumulative[-1] + daily_rate * (d - today) if cumulative else 0.0
    for d in proj_days
]

# ── Category selector tabs ────────────────────────────────────────────
cats_available = sorted({r.get("category", "Other") for r in
                          (execute_query("SELECT DISTINCT category FROM expenses", fetch=True) or [])})
all_cats = ["All"] + cats_available
chosen_cat = st.radio("Filter by category", all_cats, horizontal=True,
                       label_visibility="collapsed")

# Filter data per-category if needed
if chosen_cat != "All":
    daily_cat = execute_query(
        """SELECT DAY(date) AS day, SUM(amount) AS total
           FROM expenses
           WHERE MONTH(date)=%s AND YEAR(date)=%s AND category=%s
           GROUP BY DAY(date) ORDER BY day""",
        (month, year, chosen_cat), fetch=True,
    ) or []
    day_map   = {int(r["day"]): float(r["total"]) for r in daily_cat}
    cumulative = []
    running    = 0.0
    for d in range(1, today + 1):
        running += day_map.get(d, 0.0)
        cumulative.append(running)
    cur = cumulative[-1] if cumulative else 0.0
    daily_rate = cur / today if today > 0 else 0.0
    proj_vals  = [cur + daily_rate * (d - today) for d in proj_days]

proj_over = bool(proj_vals) and proj_vals[-1] > budget
proj_line_color = "#ef4444" if proj_over else "#10b981"

fig = go.Figure()

# Actual area with fill (smooth wavy effect)
if cumulative:
    fig.add_trace(go.Scatter(
        x=actual_days, y=cumulative,
        mode="lines", name="Actual",
        line=dict(color="#a685d0", width=3, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(182, 159, 232, 0.3)",
        hovertemplate="<b>Day %{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))

# Projected area with dashed fill
if len(proj_vals) > 1:
    fig.add_trace(go.Scatter(
        x=proj_days, y=proj_vals,
        mode="lines", name="Projected",
        line=dict(color=proj_line_color, width=2.5, dash="dash", shape="spline"),
        fill="tonexty" if cumulative else "tozeroy",
        fillcolor=f"rgba({255 if proj_over else 16}, {180 if proj_over else 185}, {129 if not proj_over else 52}, 0.15)",
        hovertemplate="<b>Day %{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))

# Budget limit horizontal
if budget > 0:
    fig.add_hline(
        y=budget,
        line_dash="dash", line_color="#a685d0", line_width=2,
        annotation_text="Budget Limit", annotation_position="right",
        annotation_font_color="#a685d0", annotation_font_size=12,
    )

# Today marker
fig.add_vline(
    x=today,
    line_dash="dash", line_color="#a685d0", line_width=1.5, opacity=0.7,
    annotation_text="Today", annotation_position="top",
    annotation_font_color="#a685d0", annotation_font_size=11,
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(248, 245, 252, 0.3)",
    font=dict(color="#6b5b8a", size=12),
    height=400,
    margin=dict(l=16, r=100, t=16, b=48),
    xaxis=dict(
        gridcolor="rgba(182, 159, 232, 0.1)", zeroline=False,
        range=[1, days_in_month], title="Day of Month",
        tickvals=list(range(1, days_in_month + 1, 5)),
        tickcolor="#a685d0",
        linecolor="#a685d0",
    ),
    yaxis=dict(
        gridcolor="rgba(182, 159, 232, 0.1)", zeroline=False,
        title="Cumulative Spending (₹)", tickprefix="₹",
        tickcolor="#a685d0",
        linecolor="#a685d0",
    ),
    legend=dict(
        orientation="h", y=1.12, x=0,
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6b5b8a"),
    ),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Per-category forecast bars ────────────────────────────────────────
st.divider()
st.markdown("**Category breakdown**")
st.caption("Solid = actual · faded extension = projected · dotted = budget limit")
st.write("")

categories = get_categories() or []
# Get this-month spend per category
cat_spend_rows = execute_query(
    """SELECT category, SUM(amount) AS spent
       FROM expenses
       WHERE MONTH(date)=%s AND YEAR(date)=%s
       GROUP BY category""",
    (month, year), fetch=True,
) or []
cat_spent = {r["category"]: float(r["spent"]) for r in cat_spend_rows}

for cat in categories:
    name        = cat["name"]
    cat_budget  = float(cat["budget_limit"])
    spent       = cat_spent.get(name, 0.0)
    projected   = (spent / today * days_in_month) if today > 0 else spent
    is_over     = projected > cat_budget and cat_budget > 0
    color       = CAT_COLOR.get(name, "#6b7280")
    over_color  = "#ef4444"
    bar_color   = over_color if is_over else color

    # Faded version of bar color for the projected extension
    def hex_to_rgba(hex_color: str, alpha: float) -> str:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    proj_color_faded = hex_to_rgba(bar_color, 0.30)
    extension        = max(projected - spent, 0.0)
    x_max            = max(cat_budget * 1.15, projected * 1.05, 1.0)

    fig_bar = go.Figure()
    # Actual spent (solid)
    fig_bar.add_trace(go.Bar(
        x=[spent], y=[""],
        orientation="h",
        marker_color=bar_color,
        name="Spent", width=0.5,
        hovertemplate=f"Spent: ₹{spent:,.0f}<extra></extra>",
    ))
    # Projected extension (faded)
    if extension > 0:
        fig_bar.add_trace(go.Bar(
            x=[extension], y=[""],
            orientation="h",
            marker_color=proj_color_faded,
            name="Projected", width=0.5,
            hovertemplate=f"Projected extra: ₹{extension:,.0f}<extra></extra>",
        ))
    # Budget limit tick
    if cat_budget > 0:
        fig_bar.add_vline(
            x=cat_budget,
            line_dash="dot", line_color="rgba(255,255,255,0.3)", line_width=1,
        )

    fig_bar.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=52,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        xaxis=dict(range=[0, x_max], showticklabels=False,
                   showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )

    col_label, col_bar = st.columns([1, 3])
    with col_label:
        st.write(f"**{name}**")
        ksp, kpr, kbu = spent / 1000, projected / 1000, cat_budget / 1000
        st.caption(f"₹{ksp:.1f}k · proj ₹{kpr:.1f}k / ₹{kbu:.1f}k")
    with col_bar:
        st.plotly_chart(fig_bar, use_container_width=True,
                        config={"displayModeBar": False}, key=f"bar_{name}")

    if is_over:
        excess = projected - cat_budget
        st.warning(f"⚠  **{name}** may exceed budget by ₹{excess:,.0f}", icon="🔴")
