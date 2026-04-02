"""Shared CSS — dark and light themes, injected on every page via inject_styles()."""
import streamlit as st

# ── Theme-agnostic base ───────────────────────────────────────────────────────
BASE_CSS = """
<style>
/* Offline font stack — no CDN */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system,
                 BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
}

/* Keep header visible — contains the mobile hamburger ☰ button */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; background: transparent !important; }

.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 900px !important; }

/* Buttons — same indigo gradient on both themes */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white !important;
    border: none !important;
    border-radius: 12px;
    font-weight: 500;
    width: 100%;
    padding: 0.6rem 1rem;
    transition: opacity 0.15s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
    color: white !important;
}
.stButton > button:disabled {
    opacity: 0.5 !important;
    cursor: default !important;
}

/* Shared structural helpers */
.progress-track  { height:6px; border-radius:99px; overflow:hidden; margin-bottom:8px; }
.progress-fill-ok   { height:100%; border-radius:99px; background:#22c55e; }
.progress-fill-warn { height:100%; border-radius:99px; background:#ef4444; }
.progress-meta   { display:flex; justify-content:space-between; font-size:11px; color:#64748b; }
.txn-row  { display:flex; align-items:center; gap:10px; padding:10px 14px;
            border-bottom:1px solid rgba(128,128,128,0.1); }
.txn-row:last-child { border-bottom:none; }
.txn-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.txn-name { font-size:13px; font-weight:500; flex:1; }
.txn-meta { font-size:11px; color:#64748b; }
.txn-amt  { font-size:13px; font-weight:500; color:#f87171; }
.section-head { font-size:11px; font-weight:500; color:#64748b; text-transform:uppercase;
                letter-spacing:0.07em; margin:16px 0 8px; }
.hero-label  { font-size:11px; color:#64748b; text-transform:uppercase;
               letter-spacing:0.07em; margin:0 0 4px; }
.hero-amount { font-size:36px; font-weight:600; margin:0 0 14px; }
.stAlert     { border-radius:12px; border:none; border-left:4px solid #6366f1; }

/* Theme card preview boxes */
.theme-card {
    border-radius: 16px;
    border: 2px solid transparent;
    padding: 20px;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    margin-bottom: 8px;
}
.theme-card.active { border-color: #6366f1; box-shadow: 0 0 0 4px rgba(99,102,241,0.15); }
</style>
"""

# ── Dark theme ────────────────────────────────────────────────────────────────
DARK_CSS = """
<style>
.stApp { background: radial-gradient(circle at top left, #1e1b4b, #0f172a 40%, #020617); }

h1, h2, h3 {
    background: linear-gradient(to right, #e0e7ff, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
}
.hero-amount { color: #f8fafc; }
.txn-name    { color: #f1f5f9; }

[data-testid="metric-container"] {
    background: rgba(30,41,59,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 14px;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: rgba(30,41,59,0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: white !important;
}
[data-testid="stForm"] {
    background: rgba(30,41,59,0.3);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 20px;
}
[data-testid="stDataFrame"] > div {
    background: rgba(30,41,59,0.4);
    border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);
}
.stAlert { background: rgba(30,41,59,0.5); }
[data-testid="stSidebar"] {
    background: rgba(10,15,30,0.98) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
.hero-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07);
             border-radius:18px; padding:20px; margin-bottom:12px; }
.progress-track { background: rgba(255,255,255,0.08); }
.warn-strip { background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.25);
              border-radius:10px; padding:10px 14px; font-size:12px;
              color:#fca5a5; margin-bottom:12px; line-height:1.5; }
.ok-strip   { background:rgba(34,197,94,0.1);  border:1px solid rgba(34,197,94,0.2);
              border-radius:10px; padding:10px 14px; font-size:12px;
              color:#86efac; margin-bottom:12px; line-height:1.5; }
.txn-card { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07);
            border-radius:14px; overflow:hidden; margin-bottom:12px; }
.settings-card  { background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.07);
                  border-radius:14px; padding:16px; margin-bottom:10px; }
.settings-label { font-size:13px; font-weight:500; color:#f1f5f9; margin:0 0 4px; }
.settings-sub   { font-size:11px; color:#64748b; margin:0 0 10px; }
.theme-card     { background: rgba(30,41,59,0.6); }
</style>
"""

# ── Light theme ───────────────────────────────────────────────────────────────
LIGHT_CSS = """
<style>
.stApp { background: linear-gradient(135deg, #eef2ff 0%, #fafafa 50%, #f0f9ff 100%); }

h1, h2, h3 {
    background: linear-gradient(to right, #4338ca, #6366f1);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
}
.hero-amount { color: #1e293b; }
.txn-name    { color: #1e293b; }

[data-testid="metric-container"] {
    background: white;
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px; padding: 14px;
    box-shadow: 0 2px 8px rgba(99,102,241,0.06);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: white !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important; color: #1e293b !important;
}
[data-testid="stForm"] {
    background: white;
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 16px; padding: 20px;
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
}
[data-testid="stDataFrame"] > div {
    background: white; border-radius: 12px;
    border: 1px solid rgba(99,102,241,0.1);
}
.stAlert { background: rgba(238,242,255,0.9); }
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid rgba(99,102,241,0.12) !important;
    box-shadow: 2px 0 16px rgba(99,102,241,0.06) !important;
}
.hero-card { background:white; border:1px solid rgba(99,102,241,0.15);
             border-radius:18px; padding:20px; margin-bottom:12px;
             box-shadow: 0 4px 16px rgba(99,102,241,0.08); }
.progress-track { background: rgba(99,102,241,0.1); }
.warn-strip { background:rgba(239,68,68,0.07); border:1px solid rgba(239,68,68,0.2);
              border-radius:10px; padding:10px 14px; font-size:12px;
              color:#b91c1c; margin-bottom:12px; line-height:1.5; }
.ok-strip   { background:rgba(34,197,94,0.07); border:1px solid rgba(34,197,94,0.2);
              border-radius:10px; padding:10px 14px; font-size:12px;
              color:#15803d; margin-bottom:12px; line-height:1.5; }
.txn-card { background:white; border:1px solid rgba(99,102,241,0.12);
            border-radius:14px; overflow:hidden; margin-bottom:12px;
            box-shadow: 0 2px 8px rgba(99,102,241,0.06); }
.settings-card  { background:white; border:1px solid rgba(99,102,241,0.12);
                  border-radius:14px; padding:16px; margin-bottom:10px; }
.settings-label { font-size:13px; font-weight:500; color:#1e293b; margin:0 0 4px; }
.settings-sub   { font-size:11px; color:#64748b; margin:0 0 10px; }
.theme-card     { background: white; }
.txn-amt        { color: #ef4444; }
</style>
"""


def inject_styles():
    """Inject base + the active theme CSS. Call at the top of every page."""
    theme = st.session_state.get("theme", "dark")
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    st.markdown(DARK_CSS if theme == "dark" else LIGHT_CSS, unsafe_allow_html=True)
