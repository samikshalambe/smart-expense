"""Modern light gradient UI with pastel purple theme."""
import streamlit as st

_CSS = """
<style>
/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8dff5 0%, #f3ebf8 50%, #dfe1f0 100%) !important;
    min-height: 100vh;
}

/* ── Sidebar with gradient ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f9f7ff 100%) !important;
    border-right: 1px solid rgba(200, 180, 220, 0.3) !important;
}
[data-testid="stSidebarContent"] { 
    padding: 1.5rem 0.8rem;
}

/* ── Main content ── */
.main { background: transparent !important; }

/* ── Headers ── */
h1, h2, h3 { 
    color: #4a3f72 !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* ── Body text ── */
body, p, span { color: #6b5b8a !important; }

/* ── Metric cards with gradient ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, rgba(248,245,252,0.9) 100%) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(171, 131, 201, 0.25) !important;
    padding: 20px 24px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(166, 108, 205, 0.08) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(171, 131, 201, 0.4) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(166, 108, 205, 0.12) !important;
}
[data-testid="stMetricLabel"] { 
    font-size: 12px !important; 
    color: #a685d0 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.1em;
    font-weight: 600;
}
[data-testid="stMetricValue"] { 
    font-size: 32px !important; 
    font-weight: 800 !important;
    color: #7c5ca8 !important;
}

/* ── Form styling ── */
[data-testid="stForm"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, rgba(248,245,252,0.8) 100%) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(171, 131, 201, 0.2) !important;
    padding: 28px 32px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(166, 108, 205, 0.06) !important;
}

/* ── Input fields ── */
.stTextInput input, .stNumberInput input, .stDateInput input, 
.stSelectbox select, .stTextArea textarea {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid rgba(171, 131, 201, 0.2) !important;
    border-radius: 10px !important;
    color: #4a3f72 !important;
    padding: 10px 14px !important;
    transition: all 0.3s ease !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus,
.stSelectbox select:focus, .stTextArea textarea:focus {
    border-color: #a685d0 !important;
    box-shadow: 0 0 0 3px rgba(166, 108, 205, 0.1) !important;
    background: white !important;
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
    background: linear-gradient(135deg, #b29fe8 0%, #a685d0 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(166, 108, 205, 0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 25px rgba(166, 108, 205, 0.4) !important;
    transform: translateY(-2px);
}
.stButton > button:hover { 
    opacity: 1 !important;
    transform: translateY(-2px);
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: rgba(248, 245, 252, 0.5) !important;
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
    color: #a685d0 !important;
    transition: all 0.3s ease !important;
}
[aria-selected="true"] { 
    background: linear-gradient(135deg, #b29fe8 0%, #a685d0 100%) !important; 
    color: white !important;
    font-weight: 600;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed rgba(171, 131, 201, 0.3) !important;
    border-radius: 14px !important;
    background: rgba(182, 159, 232, 0.05) !important;
    padding: 28px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(171, 131, 201, 0.6) !important;
    background: rgba(182, 159, 232, 0.1) !important;
}

/* ── Dividers ── */
hr { 
    border-color: rgba(171, 131, 201, 0.15) !important; 
    margin: 1.5rem 0 !important;
}

/* ── Alert boxes ── */
.stAlert { 
    border-radius: 12px !important; 
    border: 1px solid rgba(171, 131, 201, 0.15) !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px);
}
.st-alert > div { background: rgba(248, 245, 252, 0.6) !important; }

/* ── Page links (sidebar nav) ── */
[data-testid="stPageLink"] a {
    font-size: 14px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    display: block !important;
    transition: all 0.3s ease !important;
    color: #6b5b8a !important;
}
[data-testid="stPageLink"] a:hover { 
    background: rgba(182, 159, 232, 0.15) !important;
    color: #a685d0 !important;
    padding-left: 16px;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] > div, [data-testid="stDataEditor"] > div {
    border-radius: 12px !important;
    border: 1px solid rgba(171, 131, 201, 0.1) !important;
    background: rgba(255, 255, 255, 0.5) !important;
}

/* ── Containers ── */
[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

/* ── Radio buttons (horizontal) ── */
[data-testid="stHorizontalBlock"] [data-testid="stRadioGroup"] label {
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(171, 131, 201, 0.15);
    border-radius: 20px;
    padding: 6px 16px;
    margin: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.3s;
    color: #6b5b8a;
}
[data-testid="stHorizontalBlock"] [data-testid="stRadioGroup"] label:hover {
    border-color: rgba(171, 131, 201, 0.4);
    background: rgba(182, 159, 232, 0.1);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(248, 245, 252, 0.4); border-radius: 10px; }
::-webkit-scrollbar-thumb { 
    background: rgba(182, 159, 232, 0.4);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(182, 159, 232, 0.6); }

/* ── Caption ── */
.stCaption { color: #a685d0 !important; font-size: 13px !important; }

/* ── Success/Error/Warning ── */
.stSuccess { border-left: 4px solid #34d399 !important; }
.stError { border-left: 4px solid #f87171 !important; }
.stWarning { border-left: 4px solid #fbbf24 !important; }
</style>
"""


def inject_styles():
    st.markdown(_CSS, unsafe_allow_html=True)
