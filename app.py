import streamlit as st
from utils.styles import inject_styles
from utils.auth import get_user_details

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# Custom sidebar header styling
st.markdown("""
<style>
    .sidebar-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 20px 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 22px !important;
    }
</style>
""", unsafe_allow_html=True)

for k, v in [("logged_in", False), ("username", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Page registry ─────────────────────────────────────────────────────
DASHBOARD    = st.Page("pages/1_Dashboard.py",    title="Dashboard",    icon="📊")
ADD_EXPENSE  = st.Page("pages/2_Add_Expense.py",  title="Add Expense",  icon="➕")
SMART_UPLOAD = st.Page("pages/3_Smart_Upload.py", title="Smart Upload", icon="📤")
BILL_SPLIT   = st.Page("pages/4_Split_Settle.py", title="Bill Splitter",icon="👥")
AI_FORECAST  = st.Page("pages/6_Theme.py",        title="AI Forecast",  icon="📈")
PDF_REPORT   = st.Page("pages/7_PDF_Report.py",   title="PDF Report",   icon="📄")
SETTINGS     = st.Page("pages/5_Settings.py",     title="Settings",     icon="⚙️")

ALL_PAGES = [DASHBOARD, ADD_EXPENSE, SMART_UPLOAD, BILL_SPLIT,
             AI_FORECAST, PDF_REPORT, SETTINGS]

if st.session_state["logged_in"]:
    user = get_user_details(st.session_state["username"]) or "User"

    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h2>💰 SmartExpense</h2></div>', unsafe_allow_html=True)
        st.caption(f"👋 **{user}**")
        st.divider()

        for page in ALL_PAGES:
            st.page_link(page)

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"]  = None
            st.rerun()

    pg = st.navigation(ALL_PAGES, position="hidden")

else:
    pg = st.navigation([st.Page("pages/0_Login.py", title="Login", icon="🔑")], position="hidden")

pg.run()