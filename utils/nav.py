import streamlit as st

def require_login():
    """Redirect to login if not authenticated."""
    for key, default in [("logged_in", False), ("username", None)]:
        if key not in st.session_state:
            st.session_state[key] = default
    if not st.session_state["logged_in"]:
        st.switch_page("app.py")

def navbar(active_page: str):
    """Render the top Homely-style navigation bar."""
    pages = {
        "Dashboard":   ("pages/1_Dashboard.py",   "Dashboard",  "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z"),
        "Transactions":("pages/2_Transactions.py", "Transactions","M4 6h16M4 12h16M4 18h7"),
        "AI Forecast": ("pages/3_Forecast.py",     "AI Forecast", "M22 12h-4l-3 9L9 3l-3 9H2"),
        "Split Bills": ("pages/4_Split.py",        "Split Bills", "M6 3h12M6 8h8a4 4 0 0 1 0 8H6l5 5M6 16h2"),
        "Smart Upload":("pages/5_Upload.py",       "Smart Upload","M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"),
        "Settings":    ("pages/6_Settings.py",     "Settings",   "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"),
    }

    nav_items_html = ""
    for name, (path, label, icon_path) in pages.items():
        is_active = (name == active_page)
        color     = "#3fb950" if is_active else "#8b949e"
        underline = f"border-bottom:2px solid #3fb950;padding-bottom:2px;" if is_active else ""
        nav_items_html += f"""
        <a href="/{path.replace('pages/','').replace('.py','').strip()}"
           style="display:flex;align-items:center;gap:6px;text-decoration:none;color:{color};
                  font-size:13px;font-weight:{'600' if is_active else '400'};
                  white-space:nowrap;{underline}padding:4px 0;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="{icon_path}"/>
          </svg>
          {label}
        </a>"""

    st.markdown(f"""
    <div style="background:#161b22;border-bottom:1px solid #21262d;
                padding:12px 24px;margin:-1.5rem -2rem 1.5rem -2rem;
                display:flex;align-items:center;gap:0;">
      <div style="display:flex;align-items:center;gap:8px;margin-right:32px;flex-shrink:0;">
        <div style="width:28px;height:28px;background:#238636;border-radius:6px;
                    display:flex;align-items:center;justify-content:center;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff"
               stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <span style="font-size:15px;font-weight:700;color:#f0f6fc;">SmartExpense</span>
      </div>
      <div style="display:flex;align-items:center;gap:24px;flex:1;overflow-x:auto;">
        {nav_items_html}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit page_link buttons (invisible — drive actual navigation)
    st.markdown("""
    <style>
    [data-testid="stPageLink"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(len(pages))
    for i, (name, (path, label, _)) in enumerate(pages.items()):
        with cols[i]:
            if st.page_link(path, label=label):
                pass