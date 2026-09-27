import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Jai Balaji", page_icon="🍛", layout="centered")

# --- SETTINGS ---
OWNER_PIN = "1234"  # <-- Yaha apna PIN badal sakte hain
ORDERS_FILE = "orders.csv"

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

# --- HELPER: Orders file ---
def load_orders():
    if os.path.exists(ORDERS_FILE):
        return pd.read_csv(ORDERS_FILE)
    return pd.DataFrame(columns=["Timestamp", "Full Plate", "Half Plate", "Small Plate", "Total"])

def save_order(full_qty, half_qty, small_qty, total):
    df = load_orders()
    new_row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Full Plate": full_qty,
        "Half Plate": half_qty,
        "Small Plate": small_qty,
        "Total": total
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(ORDERS_FILE, index=False)

# --- SIDEBAR: Owner Panel Access ---
with st.sidebar:
    st.subheader("🔒 Owner Panel")
    pin_input = st.text_input("PIN daalein", type="password")
    show_owner_panel = pin_input == OWNER_PIN

# --- OWNER PANEL VIEW ---
if show_owner_panel:
    st.title("📊 Owner Panel — Saare Orders")
    orders_df = load_orders()

    if orders_df.empty:
        st.info("Abhi tak koi order nahi aaya hai.")
    else:
        st.dataframe(orders_df, use_container_width=True)

        total_orders = len(orders_df)
        total_revenue = orders_df["Total"].sum()
        col1, col2 = st.columns(2)
        col1.metric("Total Orders", total_orders)
        col2.metric("Total Kamai", f"₹{total_revenue}")

        st.download_button(
            "⬇️ Orders CSV Download Karein",
            data=orders_df.to_csv(index=False),
            file_name="jai_balaji_orders.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Saare Orders Clear Karein"):
            os.remove(ORDERS_FILE)
            st.success("Saare orders clear ho gaye hain.")
            st.rerun()

# --- CUSTOMER VIEW ---
else:
    st.markdown('<div class="main-title">🍛 Jai Balaji</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Veg Biryani Stall</div>', unsafe_allow_html=True)

    menu = {
        "Full Plate": 50,
        "Half Plate": 30,
        "Small Plate": 20
    }

    st.subheader("📋 Menu")
    for item, price in menu.items():
        st.markdown(f'<div class="price-box">🍽️ <b>{item}</b> — ₹{price}</div>', unsafe_allow_html=True)

    st.markdown("---")
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

        if st.button("✅ Order Confirm Karein"):
            save_order(full_qty, half_qty, small_qty, total)
            st.balloons()
            st.success("Order safaltapoorvak place ho gaya hai!")
    else:
        st.info("Order karne ke liye quantity select karein.")

    st.markdown("---")
    st.caption("Made with ❤️ | Jai Balaji Veg Biryani Stall")
