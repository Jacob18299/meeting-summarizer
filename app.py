from __future__ import annotations
from flask import Flask, request, jsonify, send_from_directory
from summarizer import summarize_transcript

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    data = request.get_json(silent=True) or {}
    transcript = (data.get("transcript") or "").strip()
    if not transcript:
        return jsonify({"error": "Please paste a meeting transcript first."}), 400
    try:
        summary = summarize_transcript(transcript)
        return jsonify(summary)
    except Exception as exc:
        return jsonify({"error": f"Could not summarize: {exc}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
