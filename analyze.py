from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    prompt = data.get("prompt", "")

    print("🧪 DEBUG: Prompt recibido:", prompt)
    print("🧪 DEBUG: API_KEY presente:", "Sí" if API_KEY else "No")

    if not prompt or not API_KEY:
        return jsonify({"error": "Missing prompt or API key."}), 400

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent?key={API_KEY}"
    print("🧪 DEBUG: URL construida:", url)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = { "Content-Type": "application/json" }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        print("🧪 DEBUG: Respuesta bruta de Gemini:", result)

        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "⚠️ Sin respuesta")
        return jsonify({"response": text})
    except Exception as e:
        print("🧪 DEBUG: Error en llamada a Gemini:", str(e))
        return jsonify({"error": "Internal server error"}), 500
