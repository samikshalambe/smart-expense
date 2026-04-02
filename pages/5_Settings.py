"""Settings — modern category and budget management."""
import streamlit as st
from utils.db_manager import get_categories, execute_query, clear_all_expenses

st.markdown("""
<style>
    .settings-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .settings-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 28px !important;
    }
    .settings-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 8px 0 0 0 !important;
        font-size: 14px !important;
    }
    .danger-zone {
        background: linear-gradient(135deg, rgba(248,113,113,0.1) 0%, rgba(239,68,68,0.05) 100%);
        border: 1px solid rgba(248,113,113,0.2);
        border-radius: 12px;
        padding: 20px;
        margin-top: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="settings-header"><h2>⚙️ Settings</h2><p>Manage budgets and expense categories</p></div>', unsafe_allow_html=True)

# ── Category budgets ──────────────────────────────────────────────────
st.markdown("**💼 Category Budgets**")
categories = get_categories() or []

if categories:
    with st.form("budget_form"):
        cols = st.columns(2)
        new_limits = {}
        for i, cat in enumerate(categories):
            with cols[i % 2]:
                new_limits[cat["name"]] = st.number_input(
                    cat["name"],
                    min_value=0.0, max_value=500_000.0,
                    value=float(cat["budget_limit"]),
                    step=100.0,
                    key=f"bl_{cat['id']}",
                )
        st.write("")
        if st.form_submit_button("💾 Save Budget Changes", use_container_width=True, type="primary"):
            for name, limit in new_limits.items():
                execute_query(
                    "UPDATE categories SET budget_limit=%s WHERE name=%s",
                    (limit, name),
                )
            st.success("✅ Budget limits updated!")
            st.rerun()
else:
    st.info("📌 No categories found. Create one below!")

st.divider()

# ── Add new category ──────────────────────────────────────────────────
st.markdown("**➕ Add New Category**")
with st.form("add_cat_form", clear_on_submit=True):
    cc1, cc2 = st.columns(2)
    with cc1:
        new_name  = st.text_input("Category name", placeholder="e.g. Groceries")
    with cc2:
        new_limit = st.number_input("Monthly budget (₹)", min_value=0.0, step=100.0)
    st.write("")
    if st.form_submit_button("✨ Add Category", use_container_width=True, type="primary"):
        if new_name.strip():
            execute_query(
                "INSERT INTO categories (name, budget_limit) VALUES (%s, %s)",
                (new_name.strip(), new_limit),
            )
            st.success(f"✅ Category **{new_name}** added!")
            st.rerun()
        else:
            st.warning("📝 Please enter a category name.")

st.divider()

# ── Danger zone ───────────────────────────────────────────────────────
st.markdown('<div class="danger-zone"><h3 style="color: #f87171; margin-top: 0;">🚨 Danger Zone</h3><p style="color: #cbd5e1; font-size: 13px; margin: 8px 0 0 0;">This action is irreversible and cannot be undone.</p>', unsafe_allow_html=True)

confirm = st.text_input("Type 'DELETE' to confirm deletion", placeholder="DELETE", key="confirm_del")
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🗑  Delete All", type="secondary", use_container_width=True):
        if confirm == "DELETE":
            clear_all_expenses()
            st.success("✅ All expense records have been deleted.")
            st.rerun()
        else:
            st.error("❌ Type DELETE exactly to confirm.")
with col2:
    st.write("")
st.markdown("</div>", unsafe_allow_html=True)
