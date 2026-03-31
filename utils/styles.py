"""Shared CSS styles injected on every page."""
import streamlit as st


SHARED_CSS = """
<style>
/* Fully offline — no CDN dependency. Inter ships on macOS 13+/iOS 16+/Windows 11;
   system-ui picks the best available sans-serif on all other platforms. */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont,
                 'Helvetica Neue', Arial, sans-serif;
}
.stApp { background: radial-gradient(circle at top left, #1e1b4b, #0f172a 40%, #020617); }
/* Hide Streamlit chrome — but NOT 'header': that's where the mobile hamburger lives */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; background: transparent !important; }

.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 900px !important; }

h1, h2, h3 {
    background: linear-gradient(to right, #e0e7ff, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
}

[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 14px;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white !important;
    border: none !important;
    border-radius: 12px;
    font-weight: 500;
    width: 100%;
    padding: 0.6rem 1rem;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
    color: white !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    color: white;
}

[data-testid="stForm"] {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
}

[data-testid="stDataFrame"] > div {
    background: rgba(30, 41, 59, 0.4);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

.stAlert {
    border-radius: 12px;
    border: none;
    background: rgba(30, 41, 59, 0.5);
    border-left: 4px solid #6366f1;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(10, 15, 30, 0.98) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* Card/component helpers */
.hero-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 20px; margin-bottom: 12px; }
.hero-label  { font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:0.07em; margin:0 0 4px; }
.hero-amount { font-size:36px; font-weight:600; color:#f8fafc; margin:0 0 14px; }
.progress-track { height:6px; background:rgba(255,255,255,0.08); border-radius:99px; overflow:hidden; margin-bottom:8px; }
.progress-fill-ok   { height:100%; border-radius:99px; background:#22c55e; }
.progress-fill-warn { height:100%; border-radius:99px; background:#ef4444; }
.progress-meta { display:flex; justify-content:space-between; font-size:11px; color:#64748b; }
.warn-strip { background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.25); border-radius:10px; padding:10px 14px; font-size:12px; color:#fca5a5; margin-bottom:12px; line-height:1.5; }
.ok-strip   { background:rgba(34,197,94,0.1);  border:1px solid rgba(34,197,94,0.2);  border-radius:10px; padding:10px 14px; font-size:12px; color:#86efac;  margin-bottom:12px; line-height:1.5; }
.txn-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07); border-radius:14px; overflow:hidden; margin-bottom:12px; }
.txn-row  { display:flex; align-items:center; gap:10px; padding:10px 14px; border-bottom:1px solid rgba(255,255,255,0.05); }
.txn-row:last-child { border-bottom:none; }
.txn-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.txn-name { font-size:13px; font-weight:500; color:#f1f5f9; flex:1; }
.txn-meta { font-size:11px; color:#64748b; }
.txn-amt  { font-size:13px; font-weight:500; color:#f87171; }
.section-head { font-size:11px; font-weight:500; color:#64748b; text-transform:uppercase; letter-spacing:0.07em; margin:16px 0 8px; }
.settings-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:16px; margin-bottom:10px; }
.settings-label { font-size:13px; font-weight:500; color:#f1f5f9; margin:0 0 4px; }
.settings-sub   { font-size:11px; color:#64748b; margin:0 0 10px; }
</style>
"""


def inject_styles():
    """Call at the top of every page to inject shared CSS."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def require_login():
    """
    Guard function — call at the top of every page script.
    If the user is not logged in, redirect them to app.py (the login page)
    by switching to it via st.switch_page.
    Returns True when the user IS logged in (page can continue rendering).
    """
    if not st.session_state.get("logged_in"):
        st.switch_page("app.py")
        st.stop()
    return True
