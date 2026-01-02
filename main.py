import json
from datetime import datetime

# --- Load Menu from JSON ---
def load_menu(path="menu.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ menu.json not found!")
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

# --- CLI UI ---
print("🍽️ Welcome to Python Cafe 🍽️")
print("\nHere is our menu:")
for item, price in menu.items():
    print(f"- {item}: Rs {price}")

order_list = []
order_total = 0

while True:
    item = input("\n👉 Select an item (or type 'done' to finish): ")
    if item.lower() == "done":
        break
    if item not in menu:
        print("❌ Item not found in menu!")
        continue

    try:
        qty = int(input(f"How many {item} do you want? "))
    except ValueError:
        print("❌ Please enter a valid number!")
        continue

    order_list.append((item, menu[item], qty))
    order_total += menu[item] * qty
    print(f"✅ {qty} {item} added to your order (Rs {menu[item] * qty})")

# --- Order Summary ---
if order_list:
    print("\n🧾 Order Summary")
    for ordered_item, price, qty in order_list:
        print(f"{ordered_item:<10} x {qty:<3} : Rs {price * qty}")

    discount = 0
    if order_total > 200:
        discount = order_total * 0.10
        print(f"🎉 Discount Applied: Rs {discount:.2f}")
        order_total -= discount

    print(f"\n💰 Total Amount to Pay: Rs {order_total:.2f}")

    confirm = input("\nDo you want to confirm & save order? (yes/no): ")
    if confirm.lower() == "yes":
        for ordered_item, price, qty in order_list:
            save_order({
                "item": ordered_item,
                "qty": qty,
                "price": price,
                "total": price * qty
            })
        print("✅ Order saved to orders.json")
else:
    print("\n🛑 No items ordered.")