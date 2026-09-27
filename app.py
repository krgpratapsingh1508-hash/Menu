import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# Page setup
st.set_page_config(page_title="Jai Balaji", page_icon="🍛", layout="centered")

# --- FILES ---
ORDERS_FILE = "orders.csv"
MENU_FILE = "menu.json"
PIN_FILE = "pin.txt"

DEFAULT_MENU = {
    "Full Plate": {"price": 50, "icon": "🍚"},
    "Half Plate": {"price": 30, "icon": "🥘"},
    "Small Plate": {"price": 20, "icon": "🍛"},
}
DEFAULT_PIN = "1234"

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

# --- HELPERS: Orders ---
def load_orders():
    if os.path.exists(ORDERS_FILE):
        return pd.read_csv(ORDERS_FILE)
    return pd.DataFrame(columns=["Timestamp", "Name", "Mobile", "Address", "Full Plate", "Half Plate", "Small Plate", "Total"])

def save_order(customer, quantities, total):
    df = load_orders()
    new_row = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    new_row.update(customer)
    new_row.update(quantities)
    new_row["Total"] = total
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(ORDERS_FILE, index=False)

# --- HELPERS: Menu ---
def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_MENU.copy()

def save_menu(menu):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)

# --- HELPERS: PIN ---
def load_pin():
    if os.path.exists(PIN_FILE):
        with open(PIN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return DEFAULT_PIN

def save_pin(new_pin):
    with open(PIN_FILE, "w", encoding="utf-8") as f:
        f.write(new_pin)

CURRENT_PIN = load_pin()

# --- SIDEBAR: Owner Panel Access ---
with st.sidebar:
    st.subheader("🔒 Owner Panel")
    pin_input = st.text_input("PIN daalein", type="password")
    show_owner_panel = pin_input == CURRENT_PIN

# --- OWNER PANEL VIEW ---
if show_owner_panel:
    st.title("📊 Owner Panel")

    tab_orders, tab_menu, tab_settings = st.tabs(["📦 Orders", "🍽️ Menu Manage Karein", "⚙️ Settings"])

    # --- TAB 1: ORDERS ---
    with tab_orders:
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

    # --- TAB 2: MENU MANAGEMENT ---
    with tab_menu:
        menu = load_menu()

        st.subheader("Current Menu")
        for item, info in list(menu.items()):
            col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])
            col1.write(f"{info['icon']} **{item}**")
            new_price = col2.number_input(
                "Rate", min_value=0, value=int(info["price"]),
                key=f"price_{item}", label_visibility="collapsed"
            )
            if col3.button("💾", key=f"save_{item}", help="Rate save karein"):
                menu[item]["price"] = new_price
                save_menu(menu)
                st.success(f"{item} ka rate ₹{new_price} update ho gaya.")
                st.rerun()
            if col4.button("🗑️", key=f"del_{item}", help="Item hatayein"):
                del menu[item]
                save_menu(menu)
                st.success(f"{item} menu se hata diya gaya.")
                st.rerun()

        st.markdown("---")
        st.subheader("➕ Naya Item Add Karein")
        with st.form("add_item_form", clear_on_submit=True):
            new_name = st.text_input("Item ka naam")
            new_icon = st.text_input("Emoji (optional)", value="🍽️")
            new_item_price = st.number_input("Rate (₹)", min_value=0, value=0, step=1)
            submitted = st.form_submit_button("Add Karein")
            if submitted:
                if new_name.strip() == "":
                    st.error("Item ka naam daalna zaroori hai.")
                elif new_name in menu:
                    st.error("Ye item pehle se menu mein hai.")
                else:
                    menu[new_name] = {"price": new_item_price, "icon": new_icon or "🍽️"}
                    save_menu(menu)
                    st.success(f"{new_name} menu mein add ho gaya.")
                    st.rerun()

    # --- TAB 3: SETTINGS (Change PIN) ---
    with tab_settings:
        st.subheader("🔑 PIN Badlein")
        with st.form("change_pin_form", clear_on_submit=True):
            new_pin = st.text_input("Naya PIN", type="password")
            confirm_pin = st.text_input("Naya PIN dobara daalein", type="password")
            pin_submitted = st.form_submit_button("PIN Update Karein")
            if pin_submitted:
                if new_pin.strip() == "":
                    st.error("PIN khali nahi ho sakta.")
                elif new_pin != confirm_pin:
                    st.error("Dono PIN match nahi ho rahe.")
                else:
                    save_pin(new_pin.strip())
                    st.success("PIN safaltapoorvak update ho gaya. Agli baar naya PIN use karein.")

# --- CUSTOMER VIEW ---
else:
    menu = load_menu()

    st.markdown("""
        <div class="header-banner">
            <h1>🍛 Jai Balaji</h1>
            <p>Veg Biryani Stall</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">📋 Menu</div>', unsafe_allow_html=True)
    for item, info in menu.items():
        st.markdown(f"""
            <div class="menu-card">
                <span class="item-name">{info['icon']} {item}</span>
                <span class="item-price">₹{info['price']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">🛒 Order Karein</div>', unsafe_allow_html=True)

    if not menu:
        st.warning("Abhi menu khali hai. Owner Panel se items add karein.")
    else:
        # Session state defaults for each menu item
        for item in menu:
            key = f"qty_{item}"
            if key not in st.session_state:
                st.session_state[key] = 0

        for field_key in ["cust_name", "cust_mobile", "cust_address"]:
            if field_key not in st.session_state:
                st.session_state[field_key] = ""

        if "order_placed" not in st.session_state:
            st.session_state.order_placed = False

        # Reset BEFORE widgets are created (avoids widget-key error)
        if st.session_state.get("do_reset", False):
            for item in menu:
                st.session_state[f"qty_{item}"] = 0
            st.session_state.cust_name = ""
            st.session_state.cust_mobile = ""
            st.session_state.cust_address = ""
            st.session_state.do_reset = False

        if st.session_state.order_placed:
            st.balloons()
            st.success("🎉 Order safaltapoorvak place ho gaya hai!")
            st.session_state.order_placed = False

        st.markdown("**👤 Aapki Details**")
        cust_name = st.text_input("Naam", key="cust_name")
        cust_mobile = st.text_input("Mobile No.", key="cust_mobile")
        cust_address = st.text_area("Address", key="cust_address", height=80)

        st.markdown("**🍽️ Quantity Chunein**")
        quantities = {}
        cols = st.columns(len(menu))
        for col, (item, info) in zip(cols, menu.items()):
            with col:
                quantities[item] = st.number_input(
                    f"{info['icon']} {item}", min_value=0, step=1, key=f"qty_{item}"
                )

        total = sum(quantities[item] * menu[item]["price"] for item in menu)

        if total > 0:
            st.markdown(f"""
                <div class="total-card">
                    <h2>💰 Total Bill: ₹{total}</h2>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("🧾 Order Details Dekhein"):
                for item, qty in quantities.items():
                    if qty > 0:
                        st.write(f"{menu[item]['icon']} {item} x {qty} = ₹{qty * menu[item]['price']}")

            if st.button("✅ Order Confirm Karein"):
                if cust_name.strip() == "" or cust_mobile.strip() == "" or cust_address.strip() == "":
                    st.error("Order confirm karne se pehle Naam, Mobile No. aur Address zaroor bharein.")
                else:
                    customer = {
                        "Name": cust_name.strip(),
                        "Mobile": cust_mobile.strip(),
                        "Address": cust_address.strip()
                    }
                    save_order(customer, quantities, total)
                    st.session_state.do_reset = True
                    st.session_state.order_placed = True
                    st.rerun()
        else:
            st.info("Order karne ke liye quantity select karein.")

    st.markdown("---")
    st.caption("Made with ❤️ | Jai Balaji Veg Biryani Stall")
