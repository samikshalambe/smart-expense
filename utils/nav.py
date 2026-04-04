import streamlit as st


def require_login():
    """Stop the page and show login prompt if not authenticated."""
    for key, default in [("logged_in", False), ("username", None)]:
        if key not in st.session_state:
            st.session_state[key] = default
    if not st.session_state["logged_in"]:
        st.error("Please log in to access this page.")
        st.stop()


def navbar(active_page: str):
    """
    Top navigation bar using st.page_link.
    Works correctly when pages are run via st.navigation() in app.py.
    st.page_link is the right API here — st.switch_page cannot be called
    from within a page that was launched by st.navigation.
    """

    PAGES = {
        "Dashboard":    "pages/1_Dashboard.py",
        "Transactions": "pages/2_Transactions.py",
        "AI Forecast":  "pages/3_Forecast.py",
        "Split Bills":  "pages/4_Split.py",
        "Smart Upload": "pages/5_Upload.py",
        "Settings":     "pages/6_Settings.py",
    }

    # ── CSS ──────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Navbar row background */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background: #161b22 !important;
        border-bottom: 1px solid #21262d !important;
        padding: 2px 12px !important;
        margin: -1.5rem -2rem 1.5rem -2rem !important;
        gap: 0 !important;
        align-items: center !important;
    }
    /* Page link default style */
    div[data-testid="stPageLink"] a {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        color: #8b949e !important;
        text-decoration: none !important;
        padding: 12px 6px !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
        white-space: nowrap !important;
        transition: color 0.15s !important;
    }
    div[data-testid="stPageLink"] a:hover {
        color: #f0f6fc !important;
        background: rgba(255,255,255,0.04) !important;
    }
    /* Active page link */
    div[data-testid="stPageLink"] a[aria-current="page"] {
        color: #3fb950 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #3fb950 !important;
    }
    /* Logo column */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])
        > div:first-child {
        min-width: 160px !important;
        flex-shrink: 0 !important;
        border-right: 1px solid #21262d !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Logo + nav links ─────────────────────────────────────────
    logo_col, *nav_cols = st.columns([2] + [1] * len(PAGES))

    with logo_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:10px 4px;">
          <div style="width:26px;height:26px;background:#238636;border-radius:6px;
                      display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#fff"
                 stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <span style="font-size:14px;font-weight:700;color:#f0f6fc;white-space:nowrap;">
            SmartExpense
          </span>
        </div>
        """, unsafe_allow_html=True)

    for col, (name, path) in zip(nav_cols, PAGES.items()):
        with col:
            st.page_link(path, label=name, use_container_width=True)

    # ── Logout (only on Settings page) ───────────────────────────
    if active_page == "Settings":
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↩ Log out", key="_logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"]  = None
            st.rerun()