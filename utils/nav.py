import streamlit as st


def require_login():
    """Redirect to login if not authenticated."""
    for key, default in [("logged_in", False), ("username", None)]:
        if key not in st.session_state:
            st.session_state[key] = default
    if not st.session_state["logged_in"]:
        st.switch_page("app.py")


def navbar(active_page: str):
    """
    Top navigation bar built with pure Streamlit buttons + st.switch_page.
    No HTML anchor tags. No st.page_link. Works reliably on all Streamlit versions.
    """

    pages = [
        ("Dashboard",    "pages/1_Dashboard.py"),
        ("Transactions", "pages/2_Transactions.py"),
        ("AI Forecast",  "pages/3_Forecast.py"),
        ("Split Bills",  "pages/4_Split.py"),
        ("Smart Upload", "pages/5_Upload.py"),
        ("Settings",     "pages/6_Settings.py"),
    ]

    # ── Navbar CSS ───────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Navbar container */
    div[data-testid="stHorizontalBlock"].navbar-row {
        background: #161b22;
    }

    /* Style ALL buttons in the navbar row */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: #8b949e !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 10px 4px !important;
        width: 100% !important;
        white-space: nowrap !important;
        transition: color 0.15s !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
        color: #f0f6fc !important;
        background: #21262d !important;
    }

    /* Navbar wrapper — dark background strip */
    .navbar-wrap {
        background: #161b22;
        border-bottom: 1px solid #21262d;
        padding: 0 8px;
        margin: -1.5rem -2rem 1.5rem -2rem;
        display: flex;
        align-items: center;
    }
    .navbar-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px 10px 8px;
        flex-shrink: 0;
        min-width: 160px;
        border-right: 1px solid #21262d;
        margin-right: 8px;
    }
    .navbar-logo-icon {
        width: 26px; height: 26px;
        background: #238636;
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
    }
    .navbar-logo-text {
        font-size: 14px; font-weight: 700;
        color: #f0f6fc; white-space: nowrap;
    }
    /* Active nav item — override button color */
    .nav-active > div > button {
        color: #3fb950 !important;
        border-bottom: 2px solid #3fb950 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Logo HTML ────────────────────────────────────────────────
    st.markdown("""
    <div class="navbar-wrap">
      <div class="navbar-logo">
        <div class="navbar-logo-icon">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#fff"
               stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <span class="navbar-logo-text">SmartExpense</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nav buttons row ──────────────────────────────────────────
    cols = st.columns(len(pages))
    for col, (name, path) in zip(cols, pages):
        is_active = (name == active_page)
        # Wrap active button in a div we can target with CSS
        if is_active:
            col.markdown('<div class="nav-active">', unsafe_allow_html=True)
        with col:
            if st.button(name, key=f"nav_{name}", use_container_width=True):
                st.switch_page(path)
        if is_active:
            col.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)