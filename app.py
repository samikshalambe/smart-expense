import streamlit as st
from utils.auth import check_login, register_user
from utils.nav import require_login, navbar

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
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 2rem !important; max-width: 480px !important; margin: 0 auto; }
.stButton > button {
    background: #238636; color: #fff !important; border: none !important;
    border-radius: 8px; font-weight: 500; width: 100%; padding: 0.6rem 1rem;
}
.stButton > button:hover { background: #2ea043 !important; }
.stTextInput > div > div > input {
    background: #161b22 !important; border: 1px solid #30363d !important;
    border-radius: 8px !important; color: #f0f6fc !important;
}
[data-testid="stForm"] {
    background: #161b22; border: 1px solid #21262d; border-radius: 14px; padding: 24px;
}
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; font-size: 14px; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #21262d !important; color: #f0f6fc !important; }
</style>
""", unsafe_allow_html=True)

for key, default in [("logged_in", False), ("username", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state["logged_in"]:
    # Temporarily disabled automatic redirect to avoid st.switch_page error
    # st.switch_page("pages/1_Dashboard.py")
    pass  # Navigation is handled by individual pages
else:
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:28px;">
      <div style="display:inline-flex;align-items:center;gap:10px;margin-bottom:8px;">
        <div style="width:36px;height:36px;background:#238636;border-radius:8px;display:flex;align-items:center;justify-content:center;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        </div>
        <span style="font-size:22px;font-weight:700;color:#f0f6fc;">SmartExpense</span>
      </div>
      <p style="color:#8b949e;font-size:14px;margin:0;">Household finance, simplified</p>
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
                    # Temporarily disabled st.switch_page to avoid errors
                    # st.switch_page("pages/1_Dashboard.py")
                    st.success("Login successful!")
                    st.markdown("""
                    <div style="text-align:center;margin:20px 0;">
                      <a href="/1_Dashboard" style="background:#238636;color:#fff;text-decoration:none;padding:10px 20px;border-radius:8px;font-weight:500;display:inline-block;">
                        Go to Dashboard →
                      </a>
                    </div>
                    """, unsafe_allow_html=True)
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