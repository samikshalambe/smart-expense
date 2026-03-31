import streamlit as st
from utils.styles import inject_styles
from utils.auth import get_user_details

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
)
inject_styles()

# ── Session defaults ───────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# ── Route: logged in → show pages, not logged in → show login ─────
if st.session_state["logged_in"]:
    # Sidebar header + logout (appears on every page)
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:20px 16px 12px;">
              <p style="font-size:20px;font-weight:600;color:#e0e7ff;margin:0;">✨ SmartExpense</p>
              <p style="font-size:12px;color:#64748b;margin:4px 0 0;">{get_user_details(st.session_state["username"])}</p>
            </div>
            <hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 16px 12px;">
            """,
            unsafe_allow_html=True,
        )
        if st.button("↩  Log Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"]  = None
            st.rerun()

    pg = st.navigation([
        st.Page("pages/1_Dashboard.py",   title="Dashboard",     icon="📊"),
        st.Page("pages/2_Add_Expense.py", title="Add Expense",   icon="➕"),
        st.Page("pages/3_Smart_Upload.py",title="Smart Upload",  icon="📄"),
        st.Page("pages/4_Split_Settle.py",title="Split & Settle",icon="💰"),
        st.Page("pages/5_Settings.py",    title="Settings",      icon="🔧"),
    ])
else:
    # Hide nav entirely — only the login page is accessible
    pg = st.navigation(
        [st.Page("pages/0_Login.py", title="Login", icon="🔑")],
        position="hidden",
    )

pg.run()