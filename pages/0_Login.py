import streamlit as st
from utils.auth import check_login, register_user
from utils.styles import SHARED_CSS

st.set_page_config(page_title="Login · SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Center the login form
st.markdown("""
<style>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding-top: 80px;
}
.login-title {
    font-size: 32px;
    font-weight: 700;
    color: #f0f6fc;
    text-align: center;
    margin-bottom: 8px;
}
.login-subtitle {
    font-size: 14px;
    color: #8b949e;
    text-align: center;
    margin-bottom: 32px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="login-container">', unsafe_allow_html=True)

st.markdown('<div class="login-title">SmartExpense</div>', unsafe_allow_html=True)
st.markdown('<div class="login-subtitle">Smart household finance manager</div>', unsafe_allow_html=True)

tab_login, tab_reg = st.tabs(["Login", "Register"])

with tab_login:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Username", placeholder="your username")
        pw   = st.text_input("Password", type="password", placeholder="••••••••")
        st.write("")
        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            if check_login(user, pw):
                st.session_state["logged_in"] = True
                st.session_state["username"]  = user
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_reg:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("reg_form"):
        nm   = st.text_input("Full Name",        placeholder="Jane Doe")
        ru   = st.text_input("Username",         placeholder="janedoe")
        rp   = st.text_input("Password",         type="password", placeholder="min 6 chars")
        rp2  = st.text_input("Confirm Password", type="password", placeholder="repeat")
        st.write("")
        if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
            if not nm or not ru or not rp:
                st.error("Fill in all fields.")
            elif rp != rp2:
                st.error("Passwords don't match.")
            elif len(rp) < 6:
                st.error("Password must be ≥ 6 chars.")
            elif register_user(ru, rp, nm):
                st.success("Account created! Log in above.")
            else:
                st.error("Username already taken.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
