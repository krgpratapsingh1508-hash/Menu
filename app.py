import streamlit as st

# Page setup
st.set_page_config(page_title="Jai Balaji", page_icon="🍛", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        color: #d35400;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        text-align: center;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .price-box {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 Jai Balaji</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Veg Biryani Stall</div>', unsafe_allow_html=True)

# --- MENU DATA ---
menu = {
    "Full Plate": 50,
    "Half Plate": 30,
    "Small Plate": 20
}

st.subheader("📋 Menu")
for item, price in menu.items():
    st.markdown(f'<div class="price-box">🍽️ <b>{item}</b> — ₹{price}</div>', unsafe_allow_html=True)

st.markdown("---")

# --- ORDER SECTION ---
st.subheader("🛒 Order Karein")

col1, col2, col3 = st.columns(3)
with col1:
    full_qty = st.number_input("Full Plate", min_value=0, value=0, step=1)
with col2:
    half_qty = st.number_input("Half Plate", min_value=0, value=0, step=1)
with col3:
    small_qty = st.number_input("Small Plate", min_value=0, value=0, step=1)

total = (full_qty * menu["Full Plate"]) + (half_qty * menu["Half Plate"]) + (small_qty * menu["Small Plate"])

st.markdown("---")

if total > 0:
    st.success(f"💰 Total Bill: ₹{total}")
    with st.expander("🧾 Order Details"):
        if full_qty > 0:
            st.write(f"Full Plate x {full_qty} = ₹{full_qty * menu['Full Plate']}")
        if half_qty > 0:
            st.write(f"Half Plate x {half_qty} = ₹{half_qty * menu['Half Plate']}")
        if small_qty > 0:
            st.write(f"Small Plate x {small_qty} = ₹{small_qty * menu['Small Plate']}")
else:
    st.info("Order karne ke liye quantity select karein.")

st.markdown("---")
st.caption("Made with ❤️ | Jai Balaji Veg Biryani Stall")
