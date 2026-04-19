import os
from flask import Flask, request, jsonify

from config import WEBHOOK_SECRET
from main import process_update

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_secret = request.headers.get("X-Max-Bot-Api-Secret")
    if incoming_secret != WEBHOOK_SECRET:
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400

    try:
        process_update(data)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return jsonify({"error": "internal error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)