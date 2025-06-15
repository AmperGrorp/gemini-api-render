from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt or not API_KEY:
        return jsonify({"error": "Missing prompt or API key."}), 400

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = { "Content-Type": "application/json" }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()

    text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "⚠️ Sin respuesta")
    return jsonify({"response": text})

if __name__ == "__main__":
    app.run(debug=True)
