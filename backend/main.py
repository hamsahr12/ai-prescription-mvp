from fastapi import FastAPI
from pydantic import BaseModel
import re, json, os
from typing import List

app = FastAPI(title="Prescription Verification MVP")

# load dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "interactions.json")
with open(DATA_PATH) as f:
    DB = json.load(f)

DRUG_NAMES = [d["name"] for d in DB["drugs"]]

class AnalyzeRequest(BaseModel):
    text: str
    age: int

def extract_drugs(text: str):
    found = []
    text_l = text.lower()
    dose_pattern = re.compile(r"(\d+(?:\.\d+)?)\s?(mg|g|ml|mcg)")
    for name in DRUG_NAMES:
        if name in text_l:
            idx = text_l.find(name)
            nearby = text_l[idx: idx+80]
            dose_match = dose_pattern.search(nearby)
            dose = f"{dose_match.group(1)}{dose_match.group(2)}" if dose_match else None
            found.append({"drug": name, "dose": dose, "raw_text_snippet": nearby.strip()})
    return found

def check_interactions(drug_list: List[str]):
    issues = []
    for i in range(len(drug_list)):
        for j in range(i+1, len(drug_list)):
            a = drug_list[i]
            b = drug_list[j]
            for rec in DB["interactions"]:
                if (rec["a"]==a and rec["b"]==b) or (rec["a"]==b and rec["b"]==a):
                    issues.append({"pair": [a,b], "risk": rec["risk"], "advice": rec["advice"]})
    return issues

def get_alternatives(drug_name: str):
    for d in DB["drugs"]:
        if d["name"]==drug_name:
            return d.get("alternatives", [])
    return []

def age_dosage_hint(age: int, drug_name: str):
    if age < 12:
        return "Pediatric: consider ~50% adult dose or consult pediatrician."
    elif age > 65:
        return "Elderly: consider ~25% lower dose and monitor."
    else:
        return "Adult standard dose."

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    extracted = extract_drugs(req.text)
    drug_names = [d["drug"] for d in extracted]
    interactions = check_interactions(drug_names)
    return {
        "extracted": extracted,
        "interactions": interactions,
        "age_hints": {d: age_dosage_hint(req.age, d) for d in drug_names},
        "alternatives": {d: get_alternatives(d) for d in drug_names}
    }

@app.get("/")
def root():
    return {"status": "ok"}
