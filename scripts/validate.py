import json

def load_drugs(path="data/drugs.json"):
    with open(path) as f:
        return json.load(f)

def validate(prescription, drugs):
    drug_name = prescription["drug"].lower()
    match = next((d for d in drugs if d["name"] == drug_name or drug_name in d["aliases"]), None)
    
    if not match:
        return {"status": "unknown", "message": f"Drug '{drug_name}' not in database"}
    
    dose = prescription["dosage"]
    if dose < match["min_dose_mg"]:
        return {"status": "underdose", "message": f"Dose {dose}mg below minimum {match['min_dose_mg']}mg"}
    elif dose > match["max_dose_mg"]:
        return {"status": "overdose", "message": f"Dose {dose}mg above maximum {match['max_dose_mg']}mg"}
    else:
        return {"status": "safe", "message": f"Dose {dose}mg is within safe range"}

if __name__ == "__main__":
    drugs = load_drugs()
    with open("data/samples/prescription_001.json") as f:
        rx = json.load(f)
    result = validate(rx, drugs)
    print(json.dumps(result, indent=2))