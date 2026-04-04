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
    Top navigation bar.
    Buttons store the destination in session state.
    st.switch_page() is called AFTER the full navbar renders — never inside a column.
    """

    PAGES = {
        "Dashboard":    "pages/1_Dashboard.py",
        "Transactions": "pages/2_Transactions.py",
        "AI Forecast":  "pages/3_Forecast.py",
        "Split Bills":  "pages/4_Split.py",
        "Smart Upload": "pages/5_Upload.py",
        "Settings":     "pages/6_Settings.py",
    }

    # ── Handle pending navigation from previous click ────────────
    # st.switch_page must be called at the top level — never inside
    # a column or button callback. We store the destination in session
    # state and switch here, before anything else renders.
    if st.session_state.get("_nav_goto"):
        dest = st.session_state.pop("_nav_goto")
        st.switch_page(dest)

    # ── CSS ──────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Dark navbar strip */
    [data-testid="stHorizontalBlock"]:has(button[kind="secondary"]):first-of-type {
        background: #161b22 !important;
        border-bottom: 1px solid #21262d !important;
        padding: 0 8px !important;
        margin: -1.5rem -2rem 1rem -2rem !important;
        gap: 0 !important;
        align-items: stretch !important;
    }

    /* All nav buttons — inactive */
    [data-testid="stHorizontalBlock"]:has(button[kind="secondary"]):first-of-type
        .stButton > button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: #8b949e !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 12px 4px !important;
        width: 100% !important;
        white-space: nowrap !important;
    }
    [data-testid="stHorizontalBlock"]:has(button[kind="secondary"]):first-of-type
        .stButton > button:hover {
        color: #f0f6fc !important;
        background: rgba(255,255,255,0.05) !important;
    }

    /* Active nav button */
    [data-testid="stHorizontalBlock"]:has(button[kind="secondary"]):first-of-type
        .stButton > button[data-active="true"] {
        color: #3fb950 !important;
        border-bottom: 2px solid #3fb950 !important;
        font-weight: 600 !important;
    }

    /* Logo column */
    [data-testid="stHorizontalBlock"]:has(button[kind="secondary"]):first-of-type
        > div:first-child {
        min-width: 155px !important;
        flex-shrink: 0 !important;
        border-right: 1px solid #21262d !important;
        display: flex !important;
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Logo + nav buttons in one row ────────────────────────────
    logo_col, *nav_cols = st.columns([2] + [1] * len(PAGES))

    with logo_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 4px;">
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

    clicked = None
    for col, (name, path) in zip(nav_cols, PAGES.items()):
        label = f"**{name}**" if name == active_page else name
        with col:
            if st.button(label, key=f"_nav_{name}", use_container_width=True):
                clicked = path

    # ── Navigate AFTER full navbar is rendered ───────────────────
    if clicked:
        st.session_state["_nav_goto"] = clicked
        st.rerun()