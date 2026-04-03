import streamlit as st
from utils.auth import check_login, register_user

st.markdown("""
<style>
    .login-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0%, rgba(248, 245, 252, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(171, 131, 201, 0.3);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(166, 108, 205, 0.15);
    }
    .login-header {
        background: linear-gradient(135deg, #b29fe8 0%, #a685d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 48px !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 8px;
    }
    .login-subtitle {
        text-align: center;
        color: #a685d0 !important;
        font-size: 16px !important;
        margin-bottom: 32px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

_, col, _ = st.columns([1, 1.4, 1])
with col:
    st.markdown('<div class="login-header">SmartExpense</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Smart household finance manager</div>', unsafe_allow_html=True)
    st.write("")

    tab_login, tab_reg = st.tabs(["Login", "Register"])

    with tab_login:
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

    with tab_reg:
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
