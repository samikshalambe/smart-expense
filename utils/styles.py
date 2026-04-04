SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 16px;          /* base size up from browser default 14px */
    line-height: 1.6;
}
.stApp { background: #0d1117; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1100px !important; }

/* All plain text in the app */
p, span, div, li { font-size: 15px; }

h1 { font-size: 28px !important; font-weight: 700 !important; color: #f0f6fc !important; }
h2 { font-size: 22px !important; font-weight: 600 !important; color: #f0f6fc !important; }
h3 { font-size: 18px !important; font-weight: 600 !important; color: #f0f6fc !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 20px;
}
[data-testid="stMetricValue"] { color: #f0f6fc !important; font-size: 32px !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.06em; }

/* Buttons */
.stButton > button {
    background: #238636;
    color: #fff !important;
    border: none !important;
    border-radius: 8px;
    font-weight: 500;
    font-size: 15px;
    padding: 0.6rem 1.2rem;
    width: 100%;
}
.stButton > button:hover { background: #2ea043 !important; }

/* Inputs — larger text so easier to type and read */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #f0f6fc !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 14px !important;
    color: #c9d1d9 !important;
}
.stSelectbox > div > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #f0f6fc !important;
    font-size: 15px !important;
}

[data-testid="stForm"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 24px;
}

[data-testid="stDataFrame"] > div {
    background: #161b22;
    border-radius: 12px;
    border: 1px solid #21262d;
    font-size: 14px;
}

.stAlert { border-radius: 10px; font-size: 15px; }
.stAlert p { font-size: 15px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #8b949e;
    font-size: 15px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #21262d !important;
    color: #f0f6fc !important;
}

/* Spinner */
.stSpinner p { font-size: 15px !important; color: #8b949e !important; }

/* ── Shared card styles ── */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
}
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #f0f6fc;
    margin: 0 0 16px;
}
.section-label {
    font-size: 12px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 8px;
}

/* Transaction rows */
.txn-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid #21262d;
}
.txn-row:last-child { border-bottom: none; }
.avatar {
    width: 40px; height: 40px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 600;
    flex-shrink: 0;
}
.txn-info { flex: 1; }
.txn-name { font-size: 15px; font-weight: 500; color: #f0f6fc; margin: 0 0 3px; }
.txn-meta { font-size: 13px; color: #8b949e; margin: 0; }
.txn-right { text-align: right; }
.txn-amt { font-size: 15px; font-weight: 600; color: #f85149; margin: 0; }
.txn-amt.credit { color: #3fb950; }

/* Category badges */
.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-green  { background: rgba(63,185,80,0.15);  color: #3fb950; }
.badge-purple { background: rgba(139,92,246,0.15); color: #a78bfa; }
.badge-amber  { background: rgba(245,158,11,0.15); color: #fbbf24; }
.badge-blue   { background: rgba(56,139,253,0.15); color: #58a6ff; }
.badge-red    { background: rgba(248,81,73,0.15);  color: #f85149; }
.badge-gray   { background: rgba(139,148,158,0.15);color: #8b949e; }
.badge-cyan   { background: rgba(34,211,238,0.15); color: #22d3ee; }

/* Stat cards */
.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 22px;
}
.stat-label {
    font-size: 12px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 10px;
}
.stat-value { font-size: 32px; font-weight: 700; color: #f0f6fc; margin: 0; }
.stat-value.red   { color: #f85149; }
.stat-value.green { color: #3fb950; }
.stat-sub { font-size: 13px; color: #8b949e; margin: 8px 0 0; }

/* Budget hero */
.hero-amount { font-size: 44px; font-weight: 700; color: #f0f6fc; margin: 4px 0 18px; }
.progress-track { height: 5px; background: #21262d; border-radius: 99px; overflow: hidden; margin: 14px 0 8px; }
.progress-fill  { height: 100%; border-radius: 99px; }

/* Top border utilities */
.top-border-green { border-top: 2px solid #3fb950; }
.top-border-red   { border-top: 2px solid #f85149; }
.top-border-blue  { border-top: 2px solid #58a6ff; }
</style>
"""

CATEGORY_BADGES = {
    "Food":          ("badge-green",  "FOOD"),
    "Rent":          ("badge-purple", "RENT"),
    "Utilities":     ("badge-blue",   "UTILITIES"),
    "Entertainment": ("badge-cyan",   "ENTERTAINMENT"),
    "Transport":     ("badge-amber",  "TRANSPORT"),
    "Other":         ("badge-gray",   "OTHER"),
}

AVATAR_COLORS = {
    "Food":          ("#1a3a2a", "#3fb950"),
    "Rent":          ("#2d1f4a", "#a78bfa"),
    "Utilities":     ("#1a2a3a", "#58a6ff"),
    "Entertainment": ("#1a3a3a", "#22d3ee"),
    "Transport":     ("#3a2a1a", "#fbbf24"),
    "Other":         ("#2a2a2a", "#8b949e"),
}

def get_badge(category):
    cls, label = CATEGORY_BADGES.get(category, ("badge-gray", category.upper()))
    return f'<span class="badge {cls}">{label}</span>'

def get_avatar(category, letter="?"):
    bg, fg = AVATAR_COLORS.get(category, ("#2a2a2a", "#8b949e"))
    return f'<div class="avatar" style="background:{bg};color:{fg};">{letter}</div>'