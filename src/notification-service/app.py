from flask import Flask, jsonify, request

app = Flask(__name__)

notifications = []


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "notification-service"})


@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    note = {
        "id": len(notifications) + 1,
        "user": data.get("user"),
        "message": data.get("message"),
        "status": "sent",
    }
    notifications.append(note)
    return jsonify(note), 201


@app.route("/notifications")
def list_notifications():
    return jsonify(notifications)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)