import streamlit as st

from utils.styles import inject_styles, require_login
from utils.db_manager import get_categories, execute_query, clear_all_expenses
from utils.auth import get_user_details

st.set_page_config(page_title="Settings · SmartExpense", page_icon="⚙", layout="wide")
inject_styles()
require_login()

# ── Sidebar logout ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:20px 16px 12px;">
          <p style="font-size:20px;font-weight:600;color:#e0e7ff;margin:0;">✨ SmartExpense</p>
          <p style="font-size:12px;color:#64748b;margin:4px 0 0;">{get_user_details(st.session_state['username'])}</p>
        </div>
        <hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 16px 12px;">
        """,
        unsafe_allow_html=True,
    )
    if st.button("↩  Log Out", key="logout_sidebar"):
        st.session_state["logged_in"] = False
        st.session_state["username"]  = None
        st.switch_page("app.py")

# ── Page content ───────────────────────────────────────────────────
st.title("Settings")

# Category budgets ──────────────────────────────────────────────────
st.markdown('<p class="section-head">Category budgets</p>', unsafe_allow_html=True)
categories = get_categories()
with st.form("budget_form"):
    cols = st.columns(2)
    new_limits = {}
    for i, cat in enumerate(categories):
        with cols[i % 2]:
            new_limits[cat["name"]] = st.number_input(
                cat["name"],
                min_value=0.0, max_value=500000.0,
                value=float(cat["budget_limit"]), step=100.0,
                key=f"budget_{cat['id']}",
            )
    if st.form_submit_button("Save Budget Changes", use_container_width=True):
        for name, limit in new_limits.items():
            execute_query("UPDATE categories SET budget_limit = %s WHERE name = %s", (limit, name))
        st.success("Budget limits updated!")
        st.rerun()

# Add new category ──────────────────────────────────────────────────
st.markdown('<p class="section-head">Add new category</p>', unsafe_allow_html=True)
with st.form("add_category_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1: new_cat_name  = st.text_input("Category name")
    with c2: new_cat_limit = st.number_input("Monthly budget (₹)", min_value=0.0, step=100.0)
    if st.form_submit_button("Add Category", use_container_width=True):
        if new_cat_name.strip():
            execute_query(
                "INSERT INTO categories (name, budget_limit) VALUES (%s, %s)",
                (new_cat_name.strip(), new_cat_limit),
            )
            st.success(f"Category '{new_cat_name}' added!")
            st.rerun()
        else:
            st.warning("Please enter a category name.")

# Danger zone ───────────────────────────────────────────────────────
st.markdown('<p class="section-head" style="color:#f87171;">Danger zone</p>', unsafe_allow_html=True)
st.markdown(
    '<div class="settings-card">'
    '<p class="settings-label">Clear all expenses</p>'
    '<p class="settings-sub">Permanently deletes every expense record. This cannot be undone.</p>'
    '</div>',
    unsafe_allow_html=True,
)
confirm_text = st.text_input("Type DELETE to confirm", key="danger_confirm")
if st.button("Clear All Data", key="clear_data"):
    if confirm_text == "DELETE":
        clear_all_expenses()
        st.success("All expense data cleared.")
        st.rerun()
    else:
        st.error("Please type DELETE exactly to confirm.")

# Account ───────────────────────────────────────────────────────────
st.markdown('<p class="section-head">Account</p>', unsafe_allow_html=True)
if st.button("↩  Log Out", key="logout_settings"):
    st.session_state["logged_in"] = False
    st.session_state["username"]  = None
    st.switch_page("app.py")
