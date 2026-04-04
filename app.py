import streamlit as st
from utils.auth import check_login, register_user

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0d1117; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Login page only */
.login-wrap .block-container { max-width: 460px !important; margin: 0 auto; }
.stButton > button {
    background: #238636; color: #fff !important; border: none !important;
    border-radius: 8px; font-weight: 500; font-size: 15px;
    width: 100%; padding: 0.6rem 1rem;
}
.stButton > button:hover { background: #2ea043 !important; }
.stTextInput > div > div > input {
    background: #161b22 !important; border: 1px solid #30363d !important;
    border-radius: 8px !important; color: #f0f6fc !important; font-size: 15px !important;
}
[data-testid="stForm"] {
    background: #161b22; border: 1px solid #21262d; border-radius: 14px; padding: 24px;
}
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"]      { background: transparent; color: #8b949e; font-size: 15px; }
.stTabs [aria-selected="true"]    { background: #21262d !important; color: #f0f6fc !important; }
</style>
""", unsafe_allow_html=True)

# ── Session defaults ─────────────────────────────────────────────
for key, default in [("logged_in", False), ("username", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Define all pages ─────────────────────────────────────────────
all_pages = [
    st.Page("pages/1_Dashboard.py",    title="Dashboard",    icon="⊞"),
    st.Page("pages/2_Transactions.py", title="Transactions", icon="⊜"),
    st.Page("pages/3_Forecast.py",     title="AI Forecast",  icon="∿"),
    st.Page("pages/4_Split.py",        title="Split Bills",  icon="₹"),
    st.Page("pages/5_Upload.py",       title="Smart Upload", icon="⬆"),
    st.Page("pages/6_Settings.py",     title="Settings",     icon="⚙"),
]

# ── Routing ──────────────────────────────────────────────────────
if st.session_state["logged_in"]:
    # Run navigation — position="hidden" suppresses default sidebar nav
    # Our custom navbar() in each page handles navigation via st.page_link
    pg = st.navigation(all_pages, position="hidden")
    pg.run()

else:
    # Register pages so st.switch_page works, but don't run any
    st.navigation(all_pages, position="hidden")

    # ── Login UI ─────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px;">
          <div style="display:inline-flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:40px;height:40px;background:#238636;border-radius:10px;
                        display:flex;align-items:center;justify-content:center;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff"
                   stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
            <span style="font-size:24px;font-weight:700;color:#f0f6fc;">SmartExpense</span>
          </div>
          <p style="color:#8b949e;font-size:15px;margin:0;">Household finance, simplified</p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign in", "Create account"])

        with tab_login:
            with st.form("login_form"):
                user = st.text_input("Username")
                pw   = st.text_input("Password", type="password")
                if st.form_submit_button("Sign in", use_container_width=True):
                    if check_login(user, pw):
                        st.session_state["logged_in"] = True
                        st.session_state["username"]  = user
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with tab_register:
            with st.form("register_form"):
                new_name = st.text_input("Full name")
                new_user = st.text_input("Username")
                new_pw   = st.text_input("Password", type="password")
                new_pw2  = st.text_input("Confirm password", type="password")
                if st.form_submit_button("Create account", use_container_width=True):
                    if not new_name or not new_user or not new_pw:
                        st.error("Please fill in all fields.")
                    elif new_pw != new_pw2:
                        st.error("Passwords do not match.")
                    elif len(new_pw) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif register_user(new_user, new_pw, new_name):
                        st.success("Account created! Sign in now.")
                    else:
                        st.error("Username already taken.")