import streamlit as st


def require_login():
    """Redirect to login if not authenticated."""
    for key, default in [("logged_in", False), ("username", None)]:
        if key not in st.session_state:
            st.session_state[key] = default
    if not st.session_state["logged_in"]:
        st.switch_page("app.py")


def navbar(active_page: str):
    """Render the top navigation bar using native st.page_link with CSS styling."""

    pages = {
        "Dashboard":    "pages/1_Dashboard.py",
        "Transactions": "pages/2_Transactions.py",
        "AI Forecast":  "pages/3_Forecast.py",
        "Split Bills":  "pages/4_Split.py",
        "Smart Upload": "pages/5_Upload.py",
        "Settings":     "pages/6_Settings.py",
    }

    # ── CSS: style the page_link row to look like a navbar ───────
    st.markdown("""
    <style>
    /* The horizontal block containing page links becomes the navbar */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background: #161b22 !important;
        border-bottom: 1px solid #21262d !important;
        padding: 4px 16px !important;
        margin: -1.5rem -2rem 1.5rem -2rem !important;
        gap: 0 !important;
        align-items: center !important;
    }

    /* Default link style */
    div[data-testid="stPageLink"] a {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        color: #8b949e !important;
        text-decoration: none !important;
        padding: 10px 8px !important;
        border-radius: 6px !important;
        border-bottom: 2px solid transparent !important;
        white-space: nowrap !important;
        transition: color 0.15s, background 0.15s !important;
    }

    /* Hover */
    div[data-testid="stPageLink"] a:hover {
        color: #f0f6fc !important;
        background: #21262d !important;
    }

    /* Active page — green underline */
    div[data-testid="stPageLink"] a[aria-current="page"] {
        color: #3fb950 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #3fb950 !important;
        background: transparent !important;
    }

    /* Logo column (first column) */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])
        > div:first-child {
        min-width: 170px !important;
        flex-shrink: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Logo + nav links rendered as Streamlit columns ────────────
    logo_col, *nav_cols = st.columns([2] + [1] * len(pages))

    with logo_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 0;">
          <div style="width:28px;height:28px;background:#238636;border-radius:6px;
                      display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff"
                 stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <span style="font-size:15px;font-weight:700;color:#f0f6fc;white-space:nowrap;">
            SmartExpense
          </span>
        </div>
        """, unsafe_allow_html=True)

    for col, (name, path) in zip(nav_cols, pages.items()):
        with col:
            st.page_link(path, label=name, use_container_width=True)