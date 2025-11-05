from flask import Flask, request, jsonify, send_from_directory
from g4f.client import Client
import os

app = Flask(__name__)
client = Client()

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt")
    try:
        result = client.images.generate(
            model="flux",
            prompt=prompt,
            response_format="b64_json"
        )
        image_data = result.data[0].b64_json
        return jsonify({"image": image_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
