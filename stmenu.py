import streamlit as st
import json
from datetime import datetime

# --- Load Menu from JSON ---
def load_menu(path="menu.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ menu.json not found!")
        return {}

menu = load_menu()

# --- Save Orders to JSON ---
def save_order(order, path="orders.json"):
    try:
        with open(path, "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

    order["timestamp"] = datetime.now().isoformat(timespec="seconds")
    orders.append(order)

    with open(path, "w") as f:
        json.dump(orders, f, indent=4)

# --- Streamlit UI ---
st.set_page_config(page_title="Python Café", page_icon="🍽️", layout="centered")

st.title("🍽️ Welcome to Python Café")
st.subheader("Here is our menu:")

# Show menu table
st.table({"Item": list(menu.keys()), "Price (Rs)": list(menu.values())})

# Session state for orders
if "order_list" not in st.session_state:
    st.session_state.order_list = []
if "order_total" not in st.session_state:
    st.session_state.order_total = 0

st.header("🛒 Place Your Order")
item = st.selectbox("👉 Select an item:", list(menu.keys()))
qty = st.number_input(f"How many {item} do you want?", min_value=1, step=1)

if st.button("Add to Order"):
    st.session_state.order_list.append((item, menu[item], qty))
    st.session_state.order_total += menu[item] * qty
    st.success(f"✅ {qty} {item} added to your order (Rs {menu[item] * qty})")

# --- Order Summary ---
if st.session_state.order_list:
    st.header("🧾 Order Summary")
    for ordered_item, price, qty in st.session_state.order_list:
        st.write(f"{ordered_item:<10} x {qty:<3} : Rs {price * qty}")

    discount = 0
    if st.session_state.order_total > 200:
        discount = st.session_state.order_total * 0.10
        st.info(f"🎉 Discount Applied: Rs {discount:.2f}")
        st.session_state.order_total -= discount

    st.subheader(f"💰 Total Amount to Pay: Rs {st.session_state.order_total:.2f}")

    if st.button("Confirm & Save Order"):
        for ordered_item, price, qty in st.session_state.order_list:
            save_order({
                "item": ordered_item,
                "qty": qty,
                "price": price,
                "total": price * qty
            })
        st.success("✅ Order saved to orders.json")
        st.session_state.order_list = []
        st.session_state.order_total = 0