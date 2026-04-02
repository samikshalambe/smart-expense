import streamlit as st

# set_page_config, inject_styles, sidebar, and login guard handled by app.py

st.title("🎨 Theme")
st.write("Choose your preferred appearance.")

current = st.session_state.get("theme", "dark")

col1, col2 = st.columns(2)

with col1:
    is_dark = current == "dark"
    st.markdown(
        f"""
        <div class="theme-card {'active' if is_dark else ''}">
          <p style="font-size:32px;margin:0 0 8px;">🌙</p>
          <p style="font-size:15px;font-weight:600;margin:0 0 4px;">Dark Mode</p>
          <p style="font-size:12px;color:#64748b;margin:0;">Easy on the eyes at night.<br>Deep indigo gradient background.</p>
          {"<p style='font-size:11px;color:#818cf8;margin:8px 0 0;font-weight:500;'>✓ Currently active</p>" if is_dark else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not is_dark:
        if st.button("Switch to Dark", use_container_width=True, key="btn_dark"):
            st.session_state["theme"] = "dark"
            st.rerun()

with col2:
    is_light = current == "light"
    st.markdown(
        f"""
        <div class="theme-card {'active' if is_light else ''}">
          <p style="font-size:32px;margin:0 0 8px;">☀️</p>
          <p style="font-size:15px;font-weight:600;margin:0 0 4px;">Light Mode</p>
          <p style="font-size:12px;color:#64748b;margin:0;">Clean and bright for daytime.<br>White cards, soft indigo accents.</p>
          {"<p style='font-size:11px;color:#6366f1;margin:8px 0 0;font-weight:500;'>✓ Currently active</p>" if is_light else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not is_light:
        if st.button("Switch to Light", use_container_width=True, key="btn_light"):
            st.session_state["theme"] = "light"
            st.rerun()
