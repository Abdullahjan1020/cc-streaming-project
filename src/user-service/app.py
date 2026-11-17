from flask import Flask, jsonify

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Ali", "email": "ali@example.com"},
    2: {"id": 2, "name": "Sara", "email": "sara@example.com"},
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "user-service"})


@app.route("/users")
def list_users():
    return jsonify(list(users.values()))


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)