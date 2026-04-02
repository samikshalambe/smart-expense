import streamlit as st
from utils.styles import inject_styles
from utils.auth import get_user_details

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
)

# ── Session defaults ───────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

# Inject theme-aware CSS
inject_styles()

# ── Route: logged in → custom nav sidebar, not logged in → login ───
if st.session_state["logged_in"]:

    # ── Sidebar ───────────────────────────────────────────────────
    with st.sidebar:
        theme = st.session_state["theme"]

        # Brand header
        brand_color = "#e0e7ff" if theme == "dark" else "#3730a3"
        sub_color   = "#64748b"
        hr_color    = "rgba(255,255,255,0.06)" if theme == "dark" else "rgba(99,102,241,0.15)"

        st.markdown(
            f"""
            <div style="padding:20px 4px 10px;">
              <p style="font-size:20px;font-weight:700;color:{brand_color};margin:0;letter-spacing:-0.3px;">
                ✨ SmartExpense
              </p>
              <p style="font-size:12px;color:{sub_color};margin:4px 0 0;">
                {get_user_details(st.session_state["username"])}
              </p>
            </div>
            <hr style="border:none;border-top:1px solid {hr_color};margin:0 0 10px;">
            """,
            unsafe_allow_html=True,
        )

        # ── Theme toggle ──────────────────────────────────────────
        moon = "🌙" if theme == "light" else "☀️"
        toggle_label = f"{moon}  {'Switch to Dark' if theme == 'light' else 'Switch to Light'}"
        if st.button(toggle_label, key="theme_toggle", use_container_width=True):
            st.session_state["theme"] = "light" if theme == "dark" else "dark"
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Detect current page for active highlighting ───────────
        # st.navigation sets this internal key after first run  
        current_script = st.session_state.get("_current_page", "")

        NAV_ITEMS = [
            ("pages/1_Dashboard.py",   "📊  Dashboard"),
            ("pages/2_Add_Expense.py", "➕  Add Expense"),
            ("pages/3_Smart_Upload.py","📄  Smart Upload"),
            ("pages/4_Split_Settle.py","💰  Split & Settle"),
            ("pages/5_Settings.py",    "🔧  Settings"),
            ("pages/6_Theme.py",       "🎨  Theme"),
        ]

        st.markdown(
            '<p style="font-size:10px;font-weight:600;color:#64748b;'
            'text-transform:uppercase;letter-spacing:.08em;margin:0 0 6px;">Navigation</p>',
            unsafe_allow_html=True,
        )

        for page_path, label in NAV_ITEMS:
            is_active = page_path in current_script
            css_class = "nav-btn-active" if is_active else "nav-btn"
            with st.container():
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{page_path}", use_container_width=True):
                    st.session_state["_current_page"] = page_path
                    st.switch_page(page_path)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── Logout ────────────────────────────────────────────────
        st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 10px;">', unsafe_allow_html=True)
        if st.button("↩  Log Out", key="logout_btn", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"]  = None
            st.session_state.pop("_current_page", None)
            st.rerun()

    # Use st.navigation but hide it (nav is done via custom buttons above)
    pg = st.navigation(
        [
            st.Page("pages/1_Dashboard.py",   title="Dashboard",     icon="📊"),
            st.Page("pages/2_Add_Expense.py", title="Add Expense",   icon="➕"),
            st.Page("pages/3_Smart_Upload.py",title="Smart Upload",  icon="📄"),
            st.Page("pages/4_Split_Settle.py",title="Split & Settle",icon="💰"),
            st.Page("pages/5_Settings.py",    title="Settings",      icon="🔧"),
            st.Page("pages/6_Theme.py",       title="Theme",         icon="🎨"),
        ],
        position="hidden",   # hide the default nav — we use our own buttons
    )

else:
    # Not logged in — show only the login page, no sidebar
    pg = st.navigation(
        [st.Page("pages/0_Login.py", title="Login", icon="🔑")],
        position="hidden",
    )

pg.run()