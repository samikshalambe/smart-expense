"""Modern gradient UI with minimal, clean design."""
import streamlit as st

_CSS = """
<style>
/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
    min-height: 100vh;
}

/* ── Sidebar with gradient ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    border-right: 1px solid rgba(148,163,184,0.1) !important;
}
[data-testid="stSidebarContent"] { 
    padding: 1.5rem 0.8rem;
}

/* ── Main content ── */
.main { background: transparent !important; }

/* ── Headers ── */
h1, h2, h3 { 
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* ── Body text ── */
body, p, span { color: #cbd5e1 !important; }

/* ── Metric cards with gradient ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.8) 0%, rgba(15,23,42,0.6) 100%) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    padding: 20px 24px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(148,163,184,0.3) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
}
[data-testid="stMetricLabel"] { 
    font-size: 12px !important; 
    color: #94a3b8 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.1em;
    font-weight: 600;
}
[data-testid="stMetricValue"] { 
    font-size: 32px !important; 
    font-weight: 800 !important;
    background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Form styling ── */
[data-testid="stForm"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.7) 0%, rgba(15,23,42,0.5) 100%) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(148,163,184,0.12) !important;
    padding: 28px 32px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
}

/* ── Input fields ── */
.stTextInput input, .stNumberInput input, .stDateInput input, 
.stSelectbox select, .stTextArea textarea {
    background: rgba(15,23,42,0.6) !important;
    border: 1.5px solid rgba(148,163,184,0.15) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    padding: 10px 14px !important;
    transition: all 0.3s ease !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus,
.stSelectbox select:focus, .stTextArea textarea:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.1) !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    border: none !important;
    transition: all 0.3s ease !important;
    text-transform: none;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 25px rgba(59,130,246,0.4) !important;
    transform: translateY(-2px);
}
.stButton > button:hover { 
    opacity: 1 !important;
    transform: translateY(-2px);
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.5) !important;
    border-radius: 12px !important;
    padding: 6px !important;
    gap: 4px !important;
    border-bottom: none !important;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    border-bottom: none !important;
    padding: 8px 18px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    transition: all 0.3s ease !important;
}
[aria-selected="true"] { 
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important; 
    color: white !important;
    font-weight: 600;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed rgba(96,165,250,0.3) !important;
    border-radius: 14px !important;
    background: rgba(59,130,246,0.05) !important;
    padding: 28px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(96,165,250,0.6) !important;
    background: rgba(59,130,246,0.1) !important;
}

/* ── Dividers ── */
hr { 
    border-color: rgba(148,163,184,0.1) !important; 
    margin: 1.5rem 0 !important;
}

/* ── Alert boxes ── */
.stAlert { 
    border-radius: 12px !important; 
    border: 1px solid rgba(148,163,184,0.15) !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px);
}
.st-alert > div { background: rgba(15,23,42,0.5) !important; }

/* ── Page links (sidebar nav) ── */
[data-testid="stPageLink"] a {
    font-size: 14px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    display: block !important;
    transition: all 0.3s ease !important;
    color: #cbd5e1 !important;
}
[data-testid="stPageLink"] a:hover { 
    background: rgba(59,130,246,0.15) !important;
    color: #60a5fa !important;
    padding-left: 16px;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] > div, [data-testid="stDataEditor"] > div {
    border-radius: 12px !important;
    border: 1px solid rgba(148,163,184,0.1) !important;
    background: rgba(15,23,42,0.4) !important;
}

/* ── Containers ── */
[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

/* ── Radio buttons (horizontal) ── */
[data-testid="stHorizontalBlock"] [data-testid="stRadioGroup"] label {
    background: rgba(30,41,59,0.6);
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 20px;
    padding: 6px 16px;
    margin: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.3s;
    color: #cbd5e1;
}
[data-testid="stHorizontalBlock"] [data-testid="stRadioGroup"] label:hover {
    border-color: rgba(96,165,250,0.4);
    background: rgba(59,130,246,0.1);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(15,23,42,0.4); border-radius: 10px; }
::-webkit-scrollbar-thumb { 
    background: rgba(96,165,250,0.4);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(96,165,250,0.6); }

/* ── Caption ── */
.stCaption { color: #94a3b8 !important; font-size: 13px !important; }

/* ── Success/Error/Warning ── */
.stSuccess { border-left: 4px solid #34d399 !important; }
.stError { border-left: 4px solid #f87171 !important; }
.stWarning { border-left: 4px solid #fbbf24 !important; }
</style>
"""


def inject_styles():
    st.markdown(_CSS, unsafe_allow_html=True)
