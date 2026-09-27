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
    .header-banner {
        background: linear-gradient(135deg, #ff9a3c 0%, #d35400 100%);
        padding: 2rem 1rem;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(211, 84, 0, 0.35);
    }
    .header-banner h1 {
        color: white !important;
        font-size: 2.3rem;
        margin: 0;
    }
    .header-banner p {
        color: #ffe8d1 !important;
        margin: 0.3rem 0 0 0;
        font-size: 1.05rem;
    }
    .section-heading {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1rem 0 0.7rem 0;
        color: #d35400 !important;
    }
    .menu-card {
        background: #fff3e0;
        border-left: 5px solid #d35400;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .menu-card .item-name {
        color: #3e2723 !important;
        font-weight: 600;
        font-size: 1.05rem;
    }
    .menu-card .item-price {
        color: #d35400 !important;
        font-weight: 800;
        font-size: 1.1rem;
    }
    .total-card {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.35);
    }
    .total-card h2 {
        color: white !important;
        margin: 0;
        font-size: 1.8rem;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #ff9a3c 0%, #d35400 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        width: 100%;
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
    st.markdown("""
        <div class="header-banner">
            <h1>🍛 Jai Balaji</h1>
            <p>Veg Biryani Stall</p>
        </div>
    """, unsafe_allow_html=True)

    menu = {
        "Full Plate": {"price": 50, "icon": "🍚"},
        "Half Plate": {"price": 30, "icon": "🥘"},
        "Small Plate": {"price": 20, "icon": "🍛"},
    }

    st.markdown('<div class="section-heading">📋 Menu</div>', unsafe_allow_html=True)
    for item, info in menu.items():
        st.markdown(f"""
            <div class="menu-card">
                <span class="item-name">{info['icon']} {item}</span>
                <span class="item-price">₹{info['price']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">🛒 Order Karein</div>', unsafe_allow_html=True)

    # Order form ke liye default values (order confirm hone ke baad reset ho jayenge)
    if "full_qty" not in st.session_state:
        st.session_state.full_qty = 0
    if "half_qty" not in st.session_state:
        st.session_state.half_qty = 0
    if "small_qty" not in st.session_state:
        st.session_state.small_qty = 0
    if "order_placed" not in st.session_state:
        st.session_state.order_placed = False

    if st.session_state.order_placed:
        st.balloons()
        st.success("🎉 Order safaltapoorvak place ho gaya hai!")
        st.session_state.order_placed = False

    col1, col2, col3 = st.columns(3)
    with col1:
        full_qty = st.number_input("🍚 Full Plate", min_value=0, step=1, key="full_qty")
    with col2:
        half_qty = st.number_input("🥘 Half Plate", min_value=0, step=1, key="half_qty")
    with col3:
        small_qty = st.number_input("🍛 Small Plate", min_value=0, step=1, key="small_qty")

    total = (full_qty * menu["Full Plate"]["price"]) + (half_qty * menu["Half Plate"]["price"]) + (small_qty * menu["Small Plate"]["price"])

    if total > 0:
        st.markdown(f"""
            <div class="total-card">
                <h2>💰 Total Bill: ₹{total}</h2>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("🧾 Order Details Dekhein"):
            if full_qty > 0:
                st.write(f"🍚 Full Plate x {full_qty} = ₹{full_qty * menu['Full Plate']['price']}")
            if half_qty > 0:
                st.write(f"🥘 Half Plate x {half_qty} = ₹{half_qty * menu['Half Plate']['price']}")
            if small_qty > 0:
                st.write(f"🍛 Small Plate x {small_qty} = ₹{small_qty * menu['Small Plate']['price']}")

        if st.button("✅ Order Confirm Karein"):
            save_order(full_qty, half_qty, small_qty, total)
            st.session_state.full_qty = 0
            st.session_state.half_qty = 0
            st.session_state.small_qty = 0
            st.session_state.order_placed = True
            st.rerun()
    else:
        st.info("Order karne ke liye quantity select karein.")

    st.markdown("---")
    st.caption("Made with ❤️ | Jai Balaji Veg Biryani Stall")
