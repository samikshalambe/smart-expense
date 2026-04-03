import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.nav import require_login, navbar
from utils.styles import SHARED_CSS
from utils.db_manager import execute_query, get_categories, clear_all_expenses
from utils.auth import get_user_details

st.set_page_config(page_title="Settings · SmartExpense", layout="wide", page_icon="💰", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
require_login()
navbar("Settings")

user_name = get_user_details(st.session_state["username"])

col_l, col_r = st.columns(2)

with col_l:
    # ── Budget limits ──────────────────────────────────────────
    st.markdown('<div class="card"><p class="card-title">Category budgets</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#8b949e;margin-bottom:16px;">Set your monthly spending limit for each category.</p>', unsafe_allow_html=True)

    categories = get_categories()
    with st.form("budget_form"):
        new_limits = {}
        cols = st.columns(2)
        for i, cat in enumerate(categories):
            with cols[i % 2]:
                new_limits[cat["name"]] = st.number_input(
                    cat["name"], min_value=0.0, max_value=500000.0,
                    value=float(cat["budget_limit"]), step=100.0,
                    key=f"budget_{cat['id']}")
        if st.form_submit_button("Save budget changes →"):
            for name, limit in new_limits.items():
                execute_query("UPDATE categories SET budget_limit = %s WHERE name = %s", (limit, name))
            st.success("Budget limits updated!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Add category ───────────────────────────────────────────
    st.markdown('<div class="card"><p class="card-title">Add new category</p>', unsafe_allow_html=True)
    with st.form("add_cat_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1: new_cat_name  = st.text_input("Category name")
        with c2: new_cat_limit = st.number_input("Monthly budget (₹)", min_value=0.0, step=100.0)
        if st.form_submit_button("Add category →"):
            if new_cat_name.strip():
                execute_query("INSERT INTO categories (name, budget_limit) VALUES (%s, %s)",
                              (new_cat_name.strip(), new_cat_limit))
                st.success(f"'{new_cat_name}' added!")
                st.rerun()
            else:
                st.warning("Please enter a category name.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    # ── Account ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card">
      <p class="card-title">Account</p>
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;">
        <div style="width:48px;height:48px;border-radius:50%;background:#1f6feb33;
                    display:flex;align-items:center;justify-content:center;
                    font-size:16px;font-weight:700;color:#58a6ff;">
          {user_name[:2].upper()}
        </div>
        <div>
          <p style="font-size:16px;font-weight:600;color:#f0f6fc;margin:0;">{user_name}</p>
          <p style="font-size:13px;color:#8b949e;margin:2px 0 0;">@{st.session_state['username']}</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("↩  Log out", key="logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"]  = None
        st.markdown('<script>window.location.href = "/";</script>', unsafe_allow_html=True)
        st.stop()

    # ── Danger zone ────────────────────────────────────────────
    st.markdown("""
    <div class="card" style="border-color:#f85149;">
      <p class="card-title" style="color:#f85149;">Danger zone</p>
      <p style="font-size:13px;color:#8b949e;margin-bottom:16px;">
        Permanently delete all expense records. This cannot be undone.
      </p>
    </div>""", unsafe_allow_html=True)

    confirm = st.text_input("Type DELETE to confirm", key="danger_confirm")
    if st.button("Clear all expense data", key="clear_btn"):
        if confirm == "DELETE":
            clear_all_expenses()
            st.success("All expense data cleared.")
            st.rerun()
        else:
            st.error("Please type DELETE exactly to confirm.")