import streamlit as st
import spacy
import pandas as pd
from pathlib import Path
import re

# ── Models ───────────────────────────────────────────────────────────────
nlp_base = spacy.load("en_core_web_sm")
nlp_bio = spacy.load("en_ner_bc5cdr_md")

# ── Data ─────────────────────────────────────────────────────────────────
DRUG_LIST_PATH = Path(r"C:\Users\user\Documents\project\drug-interaction-detector-nlp\data\drug_names_simple.txt")
INTERACTIONS_PATH = Path(r"C:\Users\user\Documents\project\drug-interaction-detector-nlp\data\interactions.csv")

try:
    custom_drugs = [line.strip().lower() for line in DRUG_LIST_PATH.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
except Exception as e:
    st.error(f"Drug list failed: {e}")
    custom_drugs = []

try:
    interactions_df = pd.read_csv(INTERACTIONS_PATH)
    interactions_df['drug1_normalized'] = interactions_df['drug1_normalized'].str.lower()
    interactions_df['drug2_normalized'] = interactions_df['drug2_normalized'].str.lower()
except Exception as e:
    st.error(f"Interactions CSV failed: {e}")
    interactions_df = pd.DataFrame()

# Expanded normalization map (brand → generic)
NORMALIZATION_MAP = {
    "dolo650": "paracetamol",
    "dolo": "paracetamol",
    "crocin": "paracetamol",
    "paracetomol": "paracetamol",
    "paracatamol": "paracetamol",
    "metformmin": "metformin",
    "pantocid": "pantoprazole",
    "pantoc": "pantoprazole",
    "glimepiride": "glimepiride",
    "glimi": "glimepiride",
    "atorva": "atorvastatin",
    "atorlip": "atorvastatin",
}

# ── Detection ────────────────────────────────────────────────────────────
def detect_drugs(text):
    doc_bio = nlp_bio(text)
    bio_entities = {ent.text.strip().lower() for ent in doc_bio.ents if ent.label_ == "CHEMICAL"}
    
    doc_base = nlp_base(text.lower())
    custom_entities = set()
    for token in doc_base:
        tok = token.text.lower()
        if any(tok.startswith(d) or d in tok for d in custom_drugs):
            custom_entities.add(token.text.lower())
    
    for prefix in ["tab", "tablet", "cap", "inj", "syp"]:
        for token in doc_base:
            if token.text.lower().startswith(prefix):
                next_t = token.nbor(1) if token.i + 1 < len(doc_base) else None
                if next_t:
                    custom_entities.add(f"{token.text.lower()} {next_t.text.lower()}")

    all_entities = bio_entities | custom_entities
    
    # Normalize
    normalized = set()
    for ent in all_entities:
        base = NORMALIZATION_MAP.get(ent, ent)
        normalized.add(base)
    
    return list(normalized)

# ── Interaction Check ────────────────────────────────────────────────────
def check_interactions(detected_drugs):
    warnings = []
    detected_lower = {d.lower() for d in detected_drugs}
    
    for _, row in interactions_df.iterrows():
        d1 = row['drug1_normalized']
        d2 = row['drug2_normalized']
        if d1 in detected_lower and d2 in detected_lower and d1 != d2:
            warnings.append({
                "drugs": f"{row['drug1_normalized'].title()} + {row['drug2_normalized'].title()}",
                "severity": row['severity'],
                "description": row['description']
            })
    
    return warnings

# ── UI ───────────────────────────────────────────────────────────────────
import streamlit as st
import time  # For simulating loading

# Placeholder functions (replace with actual implementations)
def detect_drugs(text):
    # Simulated detection
    return ["crocin", "dolo650", "pantocid dsr", "metformin", "glimepiride", "paracetamol"]

def check_interactions(drugs):
    # Simulated interactions
    return [
        {"severity": "major", "drugs": "Metformin + Glimepiride", "description": "Risk of hypoglycemia."},
        {"severity": "moderate", "drugs": "Paracetamol + Crocin", "description": "Potential liver strain."}
    ]

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {background-color: #f9fafb;}
    .stButton>button {background-color: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 500;}
    .stButton>button:hover {background-color: #2563eb;}
    .stTextArea textarea {border-radius: 6px; border: 1px solid #d1d5db; padding: 12px;}
    .stSuccess {background-color: #dcfce7; border-left: 4px solid #22c55e; padding: 12px; border-radius: 6px;}
    .stError {background-color: #fee2e2; border-left: 4px solid #ef4444; padding: 12px; border-radius: 6px;}
    .stWarning {background-color: #fef9c3; border-left: 4px solid #eab308; padding: 12px; border-radius: 6px;}
    .sidebar .sidebar-content {background-color: #f3f4f6;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# App header with bigger, balanced logo
col1, col2 = st.columns([1, 4])  # Slightly less space for logo column → bigger visual impact

with col1:
    st.image(
        "data\Screenshot 2026-01-17 163955.png",         
        width=120                 # ← Increased from 80 → looks more substantial
    )

with col2:
    st.title("Drug Interaction Checker")
    st.caption("AI-Powered Medication Safety Analysis • Professional Edition")
# Sidebar for additional features
with st.sidebar:
    st.header("App Settings")
    confidence_threshold = st.slider("Detection Confidence Threshold", 0.5, 1.0, 0.8, 0.05)
    include_minor = st.checkbox("Include Minor Interactions", value=False)
    st.divider()
    st.header("About")
    st.markdown("""
    This app detects drugs from your input text and checks for interactions using a comprehensive database.
    - **Version:** 1.0
    - **Developed by:** VIDHYA
    - **Contact:** [LinkedIn Profile](https://linkedin.com/in/yourprofile)
    """)
    st.divider()
    st.header("Resources")
    st.markdown("- [Drug Database API](https://example.com)")
    st.markdown("- [Privacy Policy](https://example.com/privacy)")

# Main content
st.subheader("Enter Your Prescription")
user_text = st.text_area(
    "Paste your medications or prescription text here:",
    value="I take Tab Crocin 650 at night, Dolo650 for fever, Pantocid DSR morning, Tab Metformin 500mg + Glimepiride 2mg BD, paracetamol when headache",
    height=160,
    help="Enter drug names, dosages, and frequencies for accurate detection."
)

# Analyze button with loading spinner
if st.button("Analyze Interactions", key="analyze_btn"):
    if not user_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing your prescription..."):
            time.sleep(2)  # Simulate processing time
            detected = detect_drugs(user_text)
            warnings = check_interactions(detected)
        
        # Display results in columns for better layout
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Detected Drugs")
            if detected:
                st.success(f"Detected {len(detected)} drug(s):")
                for drug in sorted(detected):
                    st.markdown(f"- **{drug.title()}**")
            else:
                st.info("No drugs detected in the provided text.")
        
        with col_b:
            st.subheader("Interaction Warnings")
            if warnings:
                st.error("⚠️ **Potential Interactions Detected!**")
                for w in warnings:
                    color = "#ef4444" if w['severity'] == "major" else "#f59e0b" if w['severity'] == "moderate" else "#eab308"
                    st.markdown(
                        f"<div style='padding:12px;border-radius:6px;background-color:{color}10;border:1px solid {color}40;color:{color};margin:8px 0;'>"
                        f"<strong>{w['severity'].upper()}</strong>: {w['drugs']} – {w['description']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.success("✅ No known major or moderate interactions found.")
        
        # Additional professional features
        st.divider()
        st.subheader("Recommendations")
        st.info("Always consult a healthcare professional before changing your medication regimen.")
        
        # Export results
        results_md = f"### Detected Drugs\n{', '.join(detected)}\n\n### Interactions\n"
        for w in warnings:
            results_md += f"- {w['severity'].upper()}: {w['drugs']} – {w['description']}\n"
        st.download_button(
            label="Download Report",
            data=results_md,
            file_name="drug_interaction_report.md",
            mime="text/markdown"
        )
        
        # Debug expander
        with st.expander("Debug & Advanced Details"):
            st.write("Normalized detected drugs:", detected)
            st.write("Found interactions:", warnings)
            st.write("Confidence threshold used:", confidence_threshold)

# Footer
st.markdown("---")
st.caption("© 2026 VIDHYA | Built with Streamlit | For demonstration purposes only. Not for medical advice.")