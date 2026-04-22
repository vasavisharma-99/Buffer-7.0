from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "suswaad_secret"

# NEW MENU STRUCTURE (with images)
menu = [
    {"name": "Samosa", "price": 15, "image": "samosa.jpg"},
    {"name": "Vada Pav", "price": 20, "image": "vada_pav.jpg"},
    {"name": "Tea", "price": 10, "image": "tea.jpg"},
    {"name": "Coffee", "price": 15, "image": "coffee.jpg"},
    {"name": "Sandwich", "price": 30, "image": "sandwich.jpg"}
]

orders = []

STAFF_USERNAME = "admin"
STAFF_PASSWORD = "suswaad123"

@app.route("/")
def home():
    return render_template("menu.html", menu=menu)

@app.route("/place_order", methods=["POST"])
def place_order():
    name = request.form.get("name")
    selected_items = request.form.getlist("items")

    if not selected_items:
        return "⚠️ Please select at least one item!"

    order = {
        "name": name,
        "items": selected_items,
        "time": datetime.now().strftime("%H:%M:%S"),
        "status": "pending"
    }

    orders.append(order)

    token_number = len(orders)
    pending_ahead = len([o for o in orders if o["status"] == "pending"]) - 1

    return render_template("order.html", name=name, token_number=token_number, pending_ahead=pending_ahead)

@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        if request.form["username"] == STAFF_USERNAME and request.form["password"] == STAFF_PASSWORD:
            session["staff_logged_in"] = True
            return redirect(url_for("staff_dashboard"))
        else:
            return "❌ Invalid credentials"

    return render_template("staff_login.html")

@app.route("/staff_dashboard")
def staff_dashboard():
    if not session.get("staff_logged_in"):
        return redirect(url_for("staff_login"))

    price_map = {item["name"]: item["price"] for item in menu}

    total_sales = sum(
        price_map[item]
        for o in orders if o["status"] == "completed"
        for item in o["items"]
    )

    return render_template("staff_dashboard.html", orders=orders, total_sales=total_sales)

@app.route("/complete_order/<int:order_id>")
def complete_order(order_id):
    if 0 < order_id <= len(orders):
        orders[order_id - 1]["status"] = "completed"
    return redirect(url_for("staff_dashboard"))

@app.route("/logout")
def logout():
    session.pop("staff_logged_in", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)