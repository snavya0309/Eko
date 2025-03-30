from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append('../scoring_engine')  # Adjust path if needed

from score_engine import score_product
from product_mappings import PRODUCT_URLS  # Hardcoded product data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend use

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

        # Debug print
        print("📦 Using hardcoded data:", parsed)

        result = score_product(parsed)
        result["title"] = parsed.get("title", "Your fashion choice")
        return jsonify(result)
    else:
        return jsonify({"error": "Product not found in demo list"}), 404

if __name__ == "__main__":
    app.run(debug=True)
