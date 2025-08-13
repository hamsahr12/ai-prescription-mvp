# AI Medical Prescription Verification — MVP

## Overview
This project verifies prescriptions for:
- Harmful drug interactions
- Age-based dosage adjustments
- Safer alternatives

## Setup & Run

### Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/ai-prescription-mvp.git
cd ai-prescription-mvp
```

### Run Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend
```bash
cd ../frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Example Test
Age: 70
Prescription: Aspirin 100mg once daily; Ibuprofen 200 mg twice daily

Expected:
- Detect drugs & dosages
- Warn about interactions
- Suggest alternative
- Age-based dosing hint
