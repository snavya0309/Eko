from flask import Flask, request, jsonify
from flask_cors import CORS
from product_mappings import PRODUCT_URLS  # NEW: Your hardcoded URL data
import sys
sys.path.append('../scoring_engine')  # Ensure path to score engine
from score_engine import score_product

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Eko API is live!"

@app.route("/analyze-url", methods=["POST"])
def analyze_url():
    data = request.json
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    if url in PRODUCT_URLS:
        parsed = PRODUCT_URLS[url]
        result = score_product(parsed)
        return jsonify(result)
    else:
        return jsonify({"error": "Product not found in demo list"}), 404

if __name__ == "__main__":
    app.run(debug=True)