import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS, get_badge, AVATAR_COLORS
from utils.db_manager import execute_query, get_categories, add_expense
from utils.auth import get_user_details

st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()
navbar("Transactions")

# ── Stat cards ──────────────────────────────────────────────────
total_out = execute_query("SELECT SUM(amount) as t FROM expenses", fetch=True)
total_out = float(total_out[0]["t"] or 0) if total_out else 0
count_out = execute_query("SELECT COUNT(*) as c FROM expenses", fetch=True)
count_out = int(count_out[0]["c"] or 0) if count_out else 0

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="stat-card top-border-red">
      <p class="stat-label">Total outflow</p>
      <p class="stat-value red">-₹{total_out:,.0f}</p>
      <p class="stat-sub"><span style="background:#f8514933;color:#f85149;border-radius:99px;padding:2px 8px;font-size:11px;font-weight:600;">{count_out} txns</span> &nbsp; all time</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-card top-border-green">
      <p class="stat-label">Categories</p>
      <p class="stat-value green">{execute_query("SELECT COUNT(DISTINCT category) as c FROM expenses", fetch=True)[0]['c'] or 0}</p>
      <p class="stat-sub">active categories</p>
    </div>""", unsafe_allow_html=True)
with c3:
    avg = (total_out / count_out) if count_out > 0 else 0
    st.markdown(f"""
    <div class="stat-card top-border-blue">
      <p class="stat-label">Avg transaction</p>
      <p class="stat-value" style="color:#58a6ff;">₹{avg:,.0f}</p>
      <p class="stat-sub">per transaction</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filters ──────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

col_title, col_f, col_e = st.columns([4, 1, 1])
with col_title:
    st.markdown('<p class="card-title" style="margin-bottom:12px;">All transactions</p>', unsafe_allow_html=True)
with col_f:
    categories = get_categories()
    cat_options = ["All"] + [c["name"] for c in categories]
    filter_cat = st.selectbox("Category", cat_options, label_visibility="collapsed")
with col_e:
    if st.button("Export CSV"):
        data = execute_query("SELECT date, category, amount, description FROM expenses ORDER BY date DESC", fetch=True)
        if data:
            df = pd.DataFrame(data)
            st.download_button("⬇ Download", df.to_csv(index=False).encode(),
                               "expenses.csv", "text/csv")

# ── Transaction list ─────────────────────────────────────────────
query  = "SELECT date, category, amount, description FROM expenses"
params = ()
if filter_cat != "All":
    query  += " WHERE category = %s"
    params  = (filter_cat,)
query += " ORDER BY date DESC LIMIT 50"

data = execute_query(query, params, fetch=True) if params else execute_query(query, fetch=True)

if data:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)

    current_date = None
    rows_html = ""
    for _, row in df.iterrows():
        row_date = row["date"].strftime("%d %B %Y").upper()
        if row_date != current_date:
            if current_date is not None:
                rows_html += "<div style='height:8px;'></div>"
            rows_html += f'<p style="font-size:11px;color:#8b949e;font-weight:600;letter-spacing:0.08em;margin:16px 0 8px;">{row_date}</p>'
            current_date = row_date

        cat    = row["category"]
        bg, fg = AVATAR_COLORS.get(cat, ("#2a2a2a","#8b949e"))
        letter = (str(row["description"] or cat))[0].upper()
        desc   = str(row["description"] or cat)[:35]
        badge  = get_badge(cat)
        time   = row["date"].strftime("%I:%M %p") if hasattr(row["date"], "strftime") else ""

        rows_html += f"""
        <div class="txn-row">
          <div class="avatar" style="background:{bg};color:{fg};">{letter}</div>
          <div class="txn-info">
            <p class="txn-name">{desc}</p>
            <p class="txn-meta">{cat} &nbsp;·&nbsp; {badge}</p>
          </div>
          <div class="txn-right">
            <p class="txn-amt">-₹{row['amount']:,.0f}</p>
            <p style="font-size:11px;color:#8b949e;margin:2px 0 0;">{time}</p>
          </div>
        </div>"""

    st.markdown(rows_html, unsafe_allow_html=True)
else:
    st.info("No transactions found. Add one using the Add Expense page.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Add expense inline ────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-title">Add expense</p>', unsafe_allow_html=True)
cat_names = [c["name"] for c in categories]
with st.form("add_form", clear_on_submit=True):
    c1, c2, c3, c4 = st.columns([2, 2, 2, 3])
    with c1: date = st.date_input("Date", datetime.now())
    with c2: cat  = st.selectbox("Category", cat_names)
    with c3: amt  = st.number_input("Amount (₹)", min_value=0.01, max_value=500000.0, step=1.0)
    with c4: desc = st.text_input("Description")
    if st.form_submit_button("Add transaction →"):
        if add_expense(date, cat, amt, desc):
            st.success("Added!")
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)