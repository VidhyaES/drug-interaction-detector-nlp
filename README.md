# Drug Interaction Detector (NLP-Based Risk Checker) (Ongoing)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat&logo=huggingface)](https://huggingface.co/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=flat&logo=spacy)](https://spacy.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)

Real-time NLP system that parses drug names from user input, queries a knowledge base for potential interactions, and returns clear safety warnings — designed to help prevent dangerous drug-drug interactions in clinical settings.

## 🎯 Project Highlights
- Parses free-text or structured drug input with high-precision Named Entity Recognition (NER)
- Uses BioClinicalBERT for biomedical entity extraction (drugs, dosages, etc.)
- Integrates vector search for semantic matching + rule-based + graph queries
- Delivers safety-critical outputs with risk levels and explanations
- Deployed as an interactive web app via Streamlit

**Built as part of ongoing healthcare AI contributions during iHub Robotics internship.**

## 🛠️ Tech Stack
- **Core Language**: Python
- **NLP & Entity Extraction**: spaCy, BioClinicalBERT (Hugging Face), rule-based matchers
- **Search & Knowledge Base**: Vector embeddings, graph-based queries
- **Deployment/UI**: Streamlit
- **Others**: Hugging Face Transformers, potential RxNorm/DrugBank API integration

## ✨ Features
- Biomedical NER for accurate drug name identification
- Real-time interaction lookup from knowledge base
- Risk classification with warnings and explanations
- User-friendly web interface for quick checks
- High precision on medical term matching

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- GPU recommended for BioClinicalBERT inference

### Installation
```bash
# Clone the repository
git clone https://github.com/VidhyaES/drug-interaction-detector-nlp.git
cd drug-interaction-detector-nlp

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
