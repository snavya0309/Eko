import json
from pathlib import Path

# Load all scoring data
base_path = Path(__file__).parent

def load_json(file_name):
    with open(base_path / file_name, "r") as f:
        return json.load(f)

rules = load_json("scoring_rules.json")
material_care_map = load_json("material_care_map.json")
brand_country_map = load_json("brand_country_map.json")
brand_certifications = load_json("brand_certifications.json")

# Define max possible values for normalization
MAX_SCORES = {
    "material_impact": 30,
    "labor_ethics": 20,
    "transparency": 20,
    "skin_safety": 20,
    "toxicity": 20,
    "durability": 18
}

def score_product(product):
    material = product.get("material", "").lower()
    care = product.get("care")
    brand = product.get("brand", "")
    product_certs = [c.strip() for c in product.get("certifications", [])]

    # Step 1: Fallback care if missing
    if not care and material in material_care_map:
        care = material_care_map[material]

    # Step 2: Initialize subscores
    scores = {
        "material_impact": 0,
        "labor_ethics": 0,
        "transparency": 0,
        "skin_safety": 0,
        "toxicity": 0,
        "durability": 0
    }

    # Step 3: Score from material
    if material in rules["materials"]:
        for key, value in rules["materials"][material].items():
            scores[key] += value

    # Step 4: Score from care instructions
    if care and care in rules["care_instructions"]:
        for key, value in rules["care_instructions"][care].items():
            scores[key] += value

    # Step 5: Score from certifications (brand + product level)
    all_certs = set(product_certs)
    if brand in brand_certifications:
        all_certs.update(brand_certifications[brand])

    for cert in all_certs:
        if cert in rules["certifications"]:
            for key, value in rules["certifications"][cert].items():
                scores[key] += value

    # Step 6: Normalize to [0, 100]
    normalized_scores = {
    k: min(round((v / MAX_SCORES[k]) * 100), 100) if MAX_SCORES[k] > 0 else 0
    for k, v in scores.items()
}


    # Step 7: Compute ring scores
    impact_index = round((normalized_scores["material_impact"] +
                          normalized_scores["labor_ethics"] +
                          normalized_scores["transparency"]) / 3)

    wellness_index = round((normalized_scores["skin_safety"] +
                            normalized_scores["toxicity"] +
                            normalized_scores["durability"]) / 3)

    overall_score = round((impact_index + wellness_index) / 2)

    return {
        "impact_index": impact_index,
        "wellness_index": wellness_index,
        "overall_score": overall_score,
        "subscores": normalized_scores
    }

# Optional: Run a sample test
if __name__ == "__main__":
    sample_product = {
        "brand": "H&M",
        "material": "polyester",
        "care": None,
        "certifications": []
    }

    result = score_product(sample_product)
    print(json.dumps(result, indent=2))
