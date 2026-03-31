import streamlit as st
from utils.auth import check_login, register_user
from utils.styles import inject_styles

st.set_page_config(
    page_title="SmartExpense",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",   # no sidebar on login screen
)

inject_styles()

# ── If already logged in, jump straight to Dashboard ──────────────
if st.session_state.get("logged_in"):
    st.switch_page("pages/1_Dashboard.py")

# ── Login / Register UI ───────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
_, col, _ = st.columns([1, 2, 1])
with col:
    st.markdown(
        "<h1 style='text-align:center;font-size:2.5rem;'>✨ SmartExpense</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#94a3b8;margin-bottom:20px;'>"
        "Your smart household finance manager</p>",
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Username")
            pw   = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if check_login(user, pw):
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = user
                    st.switch_page("pages/1_Dashboard.py")
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