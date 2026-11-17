import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

USER_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:5000")
PRODUCT_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service:5000")

orders = {}
next_id = 1


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "order-service"})


@app.route("/orders")
def list_orders():
    return jsonify(list(orders.values()))


@app.route("/orders/<int:order_id>")
def get_order(order_id):
    order = orders.get(order_id)
    if order is None:
        return jsonify({"error": "order not found"}), 404
    return jsonify(order)


@app.route("/orders", methods=["POST"])
def create_order():
    global next_id
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    # Step 1: user check (call to user-service)
    try:
        user_resp = requests.get(USER_URL + "/users/" + str(user_id), timeout=3)
    except requests.exceptions.RequestException:
        return jsonify({"error": "user-service unavailable"}), 503
    if user_resp.status_code != 200:
        return jsonify({"error": "user not found"}), 400
    user = user_resp.json()

    # Step 2: product check (call to product-service)
    try:
        product_resp = requests.get(PRODUCT_URL + "/products/" + str(product_id), timeout=3)
    except requests.exceptions.RequestException:
        return jsonify({"error": "product-service unavailable"}), 503
    if product_resp.status_code != 200:
        return jsonify({"error": "product not found"}), 400
    product = product_resp.json()

    if product["stock"] < quantity:
        return jsonify({"error": "not enough stock"}), 400

    # Step 3: order save
    order = {
        "id": next_id,
        "user": user["name"],
        "product": product["name"],
        "quantity": quantity,
        "total": product["price"] * quantity,
        "status": "created",
    }
    orders[next_id] = order
    next_id = next_id + 1
    return jsonify(order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)