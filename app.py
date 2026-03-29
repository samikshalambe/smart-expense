import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.db_manager import get_categories, add_expense, execute_query, clear_all_expenses
from utils.pdf_processor import parse_bank_statement
from utils.forecaster import get_budget_status
from utils.upi_helper import generate_upi_qr
from utils.auth import check_login, get_user_details, register_user
from utils.report_gen import generate_pdf_report

st.set_page_config(page_title="SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(circle at top left, #1e1b4b, #0f172a 40%, #020617); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 900px !important; }

    h1, h2, h3 {
        background: linear-gradient(to right, #e0e7ff, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    [data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 14px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white !important;
        border: none !important;
        border-radius: 12px;
        font-weight: 500;
        width: 100%;
        padding: 0.6rem 1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
        color: white !important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
    }

    [data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 20px;
    }

    [data-testid="stDataFrame"] > div {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .stAlert {
        border-radius: 12px;
        border: none;
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #6366f1;
    }

    /* ── LEFT SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.98) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div { display: flex !important; flex-direction: column !important; gap: 2px !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { display: flex !important; align-items: center !important; gap: 10px !important; padding: 10px 16px !important; border-radius: 10px !important; cursor: pointer !important; transition: background 0.15s !important; border-left: 3px solid transparent !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: rgba(99,102,241,0.1) !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background: rgba(99,102,241,0.18) !important; border-left: 3px solid #818cf8 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div > p { font-size: 14px !important; color: #94a3b8 !important; margin: 0 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) > div > p { color: #e0e7ff !important; font-weight: 500 !important; }

    /* ── Page card styles ── */
    .hero-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 20px; margin-bottom: 12px; }
    .hero-label  { font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:0.07em; margin:0 0 4px; }
    .hero-amount { font-size:36px; font-weight:600; color:#f8fafc; margin:0 0 14px; }
    .progress-track { height:6px; background:rgba(255,255,255,0.08); border-radius:99px; overflow:hidden; margin-bottom:8px; }
    .progress-fill-ok   { height:100%; border-radius:99px; background:#22c55e; }
    .progress-fill-warn { height:100%; border-radius:99px; background:#ef4444; }
    .progress-meta { display:flex; justify-content:space-between; font-size:11px; color:#64748b; }
    .warn-strip { background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.25); border-radius:10px; padding:10px 14px; font-size:12px; color:#fca5a5; margin-bottom:12px; line-height:1.5; }
    .ok-strip   { background:rgba(34,197,94,0.1);  border:1px solid rgba(34,197,94,0.2);  border-radius:10px; padding:10px 14px; font-size:12px; color:#86efac;  margin-bottom:12px; line-height:1.5; }
    .txn-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07); border-radius:14px; overflow:hidden; margin-bottom:12px; }
    .txn-row  { display:flex; align-items:center; gap:10px; padding:10px 14px; border-bottom:1px solid rgba(255,255,255,0.05); }
    .txn-row:last-child { border-bottom:none; }
    .txn-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
    .txn-name { font-size:13px; font-weight:500; color:#f1f5f9; flex:1; }
    .txn-meta { font-size:11px; color:#64748b; }
    .txn-amt  { font-size:13px; font-weight:500; color:#f87171; }
    .section-head { font-size:11px; font-weight:500; color:#64748b; text-transform:uppercase; letter-spacing:0.07em; margin:16px 0 8px; }
    .settings-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:16px; margin-bottom:10px; }
    .settings-label { font-size:13px; font-weight:500; color:#f1f5f9; margin:0 0 4px; }
    .settings-sub   { font-size:11px; color:#64748b; margin:0 0 10px; }
    </style>
""", unsafe_allow_html=True)

# ── SESSION STATE ───────────────────────────────────────────────
for key, default in [("logged_in", False), ("username", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── LOGIN / REGISTER ────────────────────────────────────────────
if not st.session_state["logged_in"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h1 style='text-align:center;font-size:2.5rem;'>✨ SmartExpense</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8;margin-bottom:20px;'>Your smart household finance manager</p>", unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            with st.form("login_form"):
                user = st.text_input("Username")
                pw   = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True):
                    if check_login(user, pw):
                        st.session_state["logged_in"] = True
                        st.session_state["username"]  = user
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with tab_register:
            with st.form("register_form"):
                new_name = st.text_input("Full Name")
                new_user = st.text_input("Username")
                new_pw   = st.text_input("Password", type="password")
                new_pw2  = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True):
                    if not new_name or not new_user or not new_pw:
                        st.error("Please fill in all fields.")
                    elif new_pw != new_pw2:
                        st.error("Passwords do not match.")
                    elif len(new_pw) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif register_user(new_user, new_pw, new_name):
                        st.success("Account created! You can now log in.")
                    else:
                        st.error("Username already taken — please choose another.")
    st.stop()

# ── LEFT SIDEBAR NAV ────────────────────────────────────────────
NAV_OPTIONS = ["⊞  Dashboard", "⊕  Add Expense", "⊜  Smart Upload", "₹  Split & Settle", "⚙  Settings"]
NAV_KEYS    = ["Dashboard", "Add Expense", "Smart Upload", "Split & Settle", "Settings"]

with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 16px 12px;">
      <p style="font-size:20px;font-weight:600;color:#e0e7ff;margin:0;">✨ SmartExpense</p>
      <p style="font-size:12px;color:#64748b;margin:4px 0 0;">{get_user_details(st.session_state['username'])}</p>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 16px 12px;">
    """, unsafe_allow_html=True)

    selected_label = st.radio("nav", NAV_OPTIONS, label_visibility="hidden")
    page = NAV_KEYS[NAV_OPTIONS.index(selected_label)]

    st.markdown("<div style='position:absolute;bottom:20px;width:calc(100% - 32px);'>", unsafe_allow_html=True)
    if st.button("↩  Log Out", key="logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"]  = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── DASHBOARD ───────────────────────────────────────────────────
if page == "Dashboard":
    user_name = get_user_details(st.session_state["username"])
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
      <div>
        <p style="font-size:22px;font-weight:600;color:#f1f5f9;margin:0;">{greeting}, {user_name} 👋</p>
        <p style="font-size:13px;color:#64748b;margin:4px 0 0;">{datetime.now().strftime('%A, %d %B %Y')}</p>
      </div>
      <div style="width:42px;height:42px;border-radius:50%;background:rgba(99,102,241,0.2);display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:600;color:#818cf8;">
        {user_name[:2].upper()}
      </div>
    </div>
    """, unsafe_allow_html=True)

    status   = get_budget_status()
    budget   = status["total_budget"]
    current  = status["current_total"]
    forecast = status["predicted_total"]
    pct      = min(int((current / budget * 100) if budget > 0 else 0), 100)
    fill_cls = "progress-fill-warn" if status["is_over_budget"] else "progress-fill-ok"

    st.markdown(f"""
    <div class="hero-card">
      <p class="hero-label">Total monthly budget</p>
      <p class="hero-amount">₹{budget:,.0f}</p>
      <div class="progress-track"><div class="{fill_cls}" style="width:{pct}%;"></div></div>
      <div class="progress-meta"><span>₹{current:,.0f} spent</span><span>{pct}% used</span></div>
    </div>
    """, unsafe_allow_html=True)

    if status["is_over_budget"]:
        over = forecast - budget
        st.markdown(f'<div class="warn-strip">⚠ Forecast: you may exceed budget by ₹{over:,.0f} this month.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ok-strip">✓ Your spending is on track for this month.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Current Spending",  f"₹{current:,.0f}")
    with c2: st.metric("Month-end Forecast", f"₹{forecast:,.0f}")
    with c3: st.metric("Remaining Budget",   f"₹{max(budget - current, 0):,.0f}")

    cat_data = execute_query("SELECT category, amount FROM expenses", fetch=True)
    if cat_data:
        df_exp = pd.DataFrame(cat_data)
        df_exp["amount"] = df_exp["amount"].astype(float)
        totals = df_exp.groupby("category")["amount"].sum().reset_index()
        totals = totals.sort_values("amount", ascending=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<p class="section-head">Spending by category</p>', unsafe_allow_html=True)
            fig = px.bar(totals, x="amount", y="category", orientation="h",
                         labels={"amount": "", "category": ""},
                         color="amount", color_continuous_scale="Purples")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#94a3b8", coloraxis_showscale=False,
                              margin=dict(l=0, r=0, t=0, b=0), height=240)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown('<p class="section-head">Category share</p>', unsafe_allow_html=True)
            fig2 = px.pie(totals, values="amount", names="category", hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8",
                               margin=dict(l=0, r=0, t=0, b=0), height=240,
                               showlegend=True, legend=dict(font=dict(color="#94a3b8")))
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No expenses yet. Add one via the sidebar or upload a PDF statement.")

    recent = execute_query(
        "SELECT date, category, amount, description FROM expenses ORDER BY date DESC LIMIT 8",
        fetch=True)
    if recent:
        dot_colors = {"Food":"#22c55e","Rent":"#818cf8","Utilities":"#f59e0b",
                      "Transport":"#f97316","Entertainment":"#ec4899","Other":"#64748b"}
        st.markdown('<p class="section-head">Recent transactions</p>', unsafe_allow_html=True)
        rows_html = ""
        for r in recent:
            color    = dot_colors.get(r["category"], "#64748b")
            date_str = r["date"].strftime("%d %b") if hasattr(r["date"], "strftime") else str(r["date"])
            desc     = str(r["description"] or r["category"])[:30]
            rows_html += f"""
            <div class="txn-row">
              <div class="txn-dot" style="background:{color};"></div>
              <div style="flex:1;"><div class="txn-name">{desc}</div><div class="txn-meta">{date_str} · {r['category']}</div></div>
              <span class="txn-amt">-₹{float(r['amount']):,.0f}</span>
            </div>"""
        st.markdown(f'<div class="txn-card">{rows_html}</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-head">Export report</p>', unsafe_allow_html=True)
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

# ── ADD EXPENSE ─────────────────────────────────────────────────
elif page == "Add Expense":
    st.title("Add Expense")
    categories = get_categories()
    cat_names  = [c["name"] for c in categories]
    with st.form("expense_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date     = st.date_input("Date", datetime.now())
            category = st.selectbox("Category", cat_names)
        with c2:
            amount      = st.number_input("Amount (₹)", min_value=0.01, max_value=500000.0, step=0.01)
            description = st.text_input("Description")
        if st.form_submit_button("Save Expense"):
            if add_expense(date, category, amount, description):
                st.success("Expense added!")
                st.balloons()

# ── SMART UPLOAD ────────────────────────────────────────────────
elif page == "Smart Upload":
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
            use_container_width=True
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

# ── SPLIT & SETTLE ──────────────────────────────────────────────
elif page == "Split & Settle":
    st.title("Split & Settle")
    st.write("Split a bill and generate a UPI payment QR instantly.")
    c1, c2 = st.columns(2)
    with c1:
        total_amount = st.number_input("Total Bill (₹)", min_value=0.0, step=10.0)
        description  = st.text_input("Description", placeholder="e.g. Dinner at Taj")
        upi_id       = st.text_input("Your UPI ID", placeholder="name@bank")
        biller_name  = st.text_input("Your Name", value="Biller")
        num_people   = st.slider("Split between", 2, 10, 2)
        if total_amount > 0:
            split = total_amount / num_people
            st.info(f"Each person pays: ₹{split:,.2f}")
    with c2:
        if total_amount > 0 and upi_id:
            try:
                split  = total_amount / num_people
                qr_img = generate_upi_qr(upi_id, biller_name, split, description)
                st.image(qr_img, caption="Scan via any UPI app", use_container_width=True)
                st.download_button("Download QR", data=qr_img,
                                   file_name="upi_qr.png", mime="image/png")
            except Exception as e:
                st.error(f"Could not generate QR: {e}")
        else:
            st.markdown("<div style='height:200px;display:flex;align-items:center;justify-content:center;color:#64748b;font-size:13px;'>QR code will appear here</div>", unsafe_allow_html=True)

# ── SETTINGS ────────────────────────────────────────────────────
elif page == "Settings":
    st.title("Settings")

    st.markdown('<p class="section-head">Category budgets</p>', unsafe_allow_html=True)
    categories = get_categories()
    with st.form("budget_form"):
        cols = st.columns(2)
        new_limits = {}
        for i, cat in enumerate(categories):
            with cols[i % 2]:
                new_limits[cat["name"]] = st.number_input(
                    cat["name"], min_value=0.0, max_value=500000.0,
                    value=float(cat["budget_limit"]), step=100.0,
                    key=f"budget_{cat['id']}")
        if st.form_submit_button("Save Budget Changes"):
            for name, limit in new_limits.items():
                execute_query("UPDATE categories SET budget_limit = %s WHERE name = %s", (limit, name))
            st.success("Budget limits updated!")
            st.rerun()

    st.markdown('<p class="section-head">Add new category</p>', unsafe_allow_html=True)
    with st.form("add_category_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1: new_cat_name  = st.text_input("Category name")
        with c2: new_cat_limit = st.number_input("Monthly budget (₹)", min_value=0.0, step=100.0)
        if st.form_submit_button("Add Category"):
            if new_cat_name.strip():
                execute_query("INSERT INTO categories (name, budget_limit) VALUES (%s, %s)",
                              (new_cat_name.strip(), new_cat_limit))
                st.success(f"Category '{new_cat_name}' added!")
                st.rerun()
            else:
                st.warning("Please enter a category name.")

    st.markdown('<p class="section-head" style="color:#f87171;">Danger zone</p>', unsafe_allow_html=True)
    st.markdown('<div class="settings-card"><p class="settings-label">Clear all expenses</p><p class="settings-sub">Permanently deletes every expense record. This cannot be undone.</p></div>', unsafe_allow_html=True)
    confirm_text = st.text_input("Type DELETE to confirm", key="danger_confirm")
    if st.button("Clear All Data", key="clear_data"):
        if confirm_text == "DELETE":
            clear_all_expenses()
            st.success("All expense data cleared.")
            st.rerun()
        else:
            st.error("Please type DELETE exactly to confirm.")