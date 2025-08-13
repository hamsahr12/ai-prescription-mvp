import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="AI Prescription Verifier (MVP)")

st.title("AI Medical Prescription Verification — MVP")
st.write("Paste a prescription and enter patient age.")

with st.form("presc_form"):
    age = st.number_input("Patient age", min_value=0, max_value=120, value=30)
    text = st.text_area("Prescription text", height=200)
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not text.strip():
        st.error("Please paste prescription text.")
    else:
        with st.spinner("Analyzing..."):
            payload = {"text": text, "age": int(age)}
            try:
                resp = requests.post(BACKEND_URL, json=payload, timeout=15)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                st.error(f"Error contacting backend: {e}")
                st.stop()

        st.subheader("Extracted Drugs")
        if not data["extracted"]:
            st.warning("No known drugs detected.")
        else:
            for d in data["extracted"]:
                st.write(f"**{d['drug'].title()}** — dose: {d['dose'] or 'not found'}")
                st.caption(d.get("raw_text_snippet",""))

        st.subheader("Interactions")
        if not data["interactions"]:
            st.success("No flagged interactions.")
        else:
            for it in data["interactions"]:
                pair = " + ".join([p.title() for p in it["pair"]])
                st.error(f"{pair}: {it['risk']}")
                st.write(f"Advice: {it['advice']}")

        st.subheader("Age-based Hints")
        for drug, hint in data["age_hints"].items():
            st.info(f"{drug.title()}: {hint}")

        st.subheader("Alternatives")
        for drug, alts in data["alternatives"].items():
            if alts:
                st.write(f"{drug.title()}: {', '.join([a.title() for a in alts])}")
            else:
                st.write(f"{drug.title()}: No alternatives available.")
