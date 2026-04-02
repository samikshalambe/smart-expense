import streamlit as st
from utils.styles import inject_styles
from utils.auth import get_user_details

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for key, default in [("logged_in", False), ("username", None), ("theme", "dark")]:
    if key not in st.session_state:
        st.session_state[key] = default

inject_styles()

ALL_PAGES = [
    st.Page("pages/1_Dashboard.py",   title="Dashboard",     icon="📊"),
    st.Page("pages/2_Add_Expense.py", title="Add Expense",   icon="➕"),
    st.Page("pages/3_Smart_Upload.py",title="Smart Upload",  icon="📄"),
    st.Page("pages/4_Split_Settle.py",title="Split & Settle",icon="💰"),
    st.Page("pages/5_Settings.py",    title="Settings",      icon="🔧"),
    st.Page("pages/6_Theme.py",       title="Theme",         icon="🎨"),
]

NAV_ITEMS = [
    ("pages/1_Dashboard.py",   "📊", "Dashboard"),
    ("pages/2_Add_Expense.py", "➕", "Add"),
    ("pages/3_Smart_Upload.py","📄", "Upload"),
    ("pages/4_Split_Settle.py","💰", "Split"),
    ("pages/5_Settings.py",    "🔧", "Settings"),
    ("pages/6_Theme.py",       "🎨", "Theme"),
]

if st.session_state["logged_in"]:
    theme     = st.session_state["theme"]
    user      = get_user_details(st.session_state["username"])
    is_dark   = theme == "dark"
    nav_bg    = "rgba(10,15,30,0.97)"      if is_dark else "rgba(255,255,255,0.97)"
    nav_bdr   = "rgba(255,255,255,0.07)"   if is_dark else "rgba(99,102,241,0.15)"
    brand_col = "#e0e7ff"                  if is_dark else "#3730a3"
    accent    = "#818cf8"                  if is_dark else "#6366f1"
    txt_col   = "#94a3b8"                  if is_dark else "#64748b"

    # ── CSS: hide sidebar, create fixed top navbar ─────────────────
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {{ display: none !important; }}
    header {{ visibility: hidden !important; }}

    /* Push content below the fixed navbar */
    .block-container {{ padding: 72px 2rem 2rem !important; max-width: 1000px !important; }}

    /* Fixed navbar shell */
    .top-nav {{
        position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
        height: 56px;
        background: {nav_bg};
        border-bottom: 1px solid {nav_bdr};
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        display: flex; align-items: center;
        padding: 0 20px; gap: 6px;
    }}
    .nav-brand {{ font-size:16px; font-weight:700; color:{brand_col};
                  white-space:nowrap; margin-right:6px; letter-spacing:-0.3px; }}
    .nav-user  {{ font-size:11px; color:{txt_col}; white-space:nowrap; margin-right:auto; }}

    /* Transparent tab-style buttons fixed over the navbar */
    .nav-btn-row {{
        position: fixed; top: 0; left: 220px; right: 0; z-index: 10000;
        height: 56px; display: flex; align-items: stretch; padding: 0 8px;
    }}
    .nav-btn-row > div {{ flex: 1; display: flex; align-items: stretch; }}
    .nav-btn-row .stButton {{ width: 100%; }}
    .nav-btn-row .stButton > button {{
        background: transparent !important;
        border: none !important; border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
        color: {txt_col} !important;
        font-size: 12px !important; font-weight: 500 !important;
        height: 56px !important; width: 100% !important;
        padding: 0 6px !important; white-space: nowrap !important;
        transition: color 0.15s, border-color 0.15s !important;
    }}
    .nav-btn-row .stButton > button:hover {{
        color: {accent} !important;
        border-bottom-color: {accent} !important;
        background: rgba(99,102,241,0.06) !important;
    }}
    </style>

    <div class="top-nav">
        <span class="nav-brand">✨ SmartExpense</span>
        <span class="nav-user">{user}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Functional button row (fixed, overlaid on the top navbar) ──
    st.markdown('<div class="nav-btn-row">', unsafe_allow_html=True)
    btn_cols = st.columns(len(NAV_ITEMS) + 2)
    for i, (path, icon, label) in enumerate(NAV_ITEMS):
        with btn_cols[i]:
            if st.button(f"{icon} {label}", key=f"tnav_{i}", use_container_width=True):
                st.switch_page(path)
    with btn_cols[-2]:
        tog = "☀️" if is_dark else "🌙"
        if st.button(tog, key="theme_tog", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.rerun()
    with btn_cols[-1]:
        if st.button("↩ Out", key="logout_btn", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"]  = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    pg = st.navigation(ALL_PAGES, position="hidden")

else:
    pg = st.navigation(
        [st.Page("pages/0_Login.py", title="Login", icon="🔑")],
        position="hidden",
    )

pg.run()