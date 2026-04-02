"""Bill Splitter — modern UI with bill splitting and UPI QR generation."""
import streamlit as st
from utils.upi_helper import generate_upi_qr

st.markdown("""
<style>
    .form-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .form-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 28px !important;
    }
    .form-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 8px 0 0 0 !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="form-header"><h2>👥 Bill Splitter</h2><p>Split bills instantly with UPI payment links</p></div>', unsafe_allow_html=True)

# ── Bill details ──────────────────────────────────────────────────────
_, center, _ = st.columns([1, 2, 1])
with center:
    total_amount = st.number_input(
        "💵 Total Bill Amount (₹)",
        min_value=0.0, max_value=1_000_000.0,
        step=10.0, format="%.2f",
        placeholder="2400.00",
    )
    description = st.text_input("📝 Description", placeholder="e.g. Monthly Rent · April 2026")
    upi_id      = st.text_input("🏦 Your UPI ID", placeholder="name@bank")
    biller_name = st.text_input("👤 Your Name",   value="Biller")

st.write("")
st.markdown("**👥 Split Between**")

# ── ± People counter ─────────────────────────────────────────────────
if "num_people" not in st.session_state:
    st.session_state["num_people"] = 2

_, col_m, col_n, col_p, _ = st.columns([2, 1, 1, 1, 2])
with col_m:
    if st.button("  ➖  ", use_container_width=True, key="minus"):
        if st.session_state["num_people"] > 1:
            st.session_state["num_people"] -= 1
with col_n:
    st.metric("People", st.session_state["num_people"])
with col_p:
    if st.button("  ➕  ", use_container_width=True, key="plus"):
        if st.session_state["num_people"] < 20:
            st.session_state["num_people"] += 1

num_people = st.session_state["num_people"]

# ── Result card ───────────────────────────────────────────────────────
st.write("")
if total_amount > 0:
    split = total_amount / num_people
    st.divider()

    _, res_col, _ = st.columns([1, 2, 1])
    with res_col:
        st.metric("💰 Per Person", f"₹{split:,.2f}",
                  f"{num_people} people · total ₹{total_amount:,.2f}")

    st.write("")

    if upi_id:
        _, qr_col, info_col, _ = st.columns([1, 1, 2, 1])
        try:
            qr_bytes = generate_upi_qr(upi_id, biller_name, split, description)
            with qr_col:
                st.image(qr_bytes, use_container_width=True)
            with info_col:
                st.write("")
                st.write(f"**₹{split:,.2f} / person**")
                st.caption("Scan with any UPI app — PhonePe, GooglePay, Paytm")
                st.caption(f"To: {biller_name}  ·  {upi_id}")
                st.download_button(
                    "📥 Download QR",
                    data=qr_bytes,
                    file_name="split_qr.png",
                    mime="image/png",
                    use_container_width=True,
                )
        except Exception as e:
            st.error(f"Could not generate QR: {e}")
    else:
        st.info("Enter your UPI ID above to generate the payment QR code.", icon="📱")
else:
    st.info("Enter the total bill amount to calculate the split.", icon="💡")
