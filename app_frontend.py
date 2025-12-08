# app_frontend.py
from flask import Flask, jsonify, send_from_directory
from pathlib import Path

from src.firewall_ga.simulation import run_baseline_and_ga  # you adjust this import
# Create a helper in your code that returns all metrics as a dict.

app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/results")
def api_results():
    # You need to implement this helper in your Python code
    # so it returns a dict with all metrics.
    results = run_baseline_and_ga()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
