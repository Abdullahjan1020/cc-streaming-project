from flask import Flask, jsonify

app = Flask(__name__)

products = {
    1: {"id": 1, "name": "Laptop", "price": 120000, "stock": 10},
    2: {"id": 2, "name": "Headphones", "price": 8000, "stock": 50},
    3: {"id": 3, "name": "Keyboard", "price": 5000, "stock": 30},
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "product-service"})


@app.route("/products")
def list_products():
    return jsonify(list(products.values()))


@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({"error": "product not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)