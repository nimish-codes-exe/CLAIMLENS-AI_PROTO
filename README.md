# 🔬 ClaimLens AI

### Misinformation Detection & Trust Scoring Platform

ClaimLens AI is an intelligent misinformation analysis platform that evaluates claims, headlines, social media posts, URLs, and images using semantic similarity, linguistic pattern detection, evidence retrieval, and trust scoring.

The system helps users assess the credibility of information by comparing claims against a curated evidence database and generating a detailed analytical report.

---

## 🚀 Features

### 📝 Multi-Source Input

* Text Claims
* News Headlines
* Social Media Posts
* URL Analysis (Demo Mode)
* Screenshot/Image OCR Extraction

### 🧠 Semantic Analysis

* Sentence Embedding Similarity Search
* Evidence Retrieval Engine
* Context-Aware Matching

### ⚠️ Risk Detection

* Clickbait Detection
* Manipulation Language Detection
* Sensationalism Detection
* CAPS & Exclamation Analysis

### 🎯 Trust Scoring Engine

* Semantic Similarity Score
* Source Reliability Score
* Credibility Indicators
* Risk Penalties
* Final Trust Score (0–100)

### 📊 Interactive Dashboard

* Trust Score Gauge
* Similarity Gauge
* Signal Meters
* Score Breakdown
* Text Analytics

### 📋 Report Generation

* PDF Export
* Evidence CSV Export
* Detailed AI Analysis Report

---

## 🏗️ System Architecture

Input Source
↓
OCR / Text Extraction
↓
Semantic Analysis
↓
Risk Detection
↓
Trust Score Computation
↓
Evidence Matching
↓
Report Generation

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Programming Language

* Python

### Machine Learning & NLP

* Sentence Transformers
* Scikit-Learn
* NumPy
* Pandas

### Visualization

* Plotly

### OCR

* Pillow
* OCR Module

### Reporting

* ReportLab

---

## 📂 Project Structure

```text
CLAIMLENS-AI_PROTO/
│
├── app.py
├── evidence.csv
├── requirements.txt
│
├── utils/
│   ├── detectors.py
│   ├── ocr.py
│   ├── similarity.py
│   ├── scoring.py
│   └── report_generator.py
│
└── reports/
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/nimish-codes-exe/CLAIMLENS-AI_PROTO.git
cd CLAIMLENS-AI_PROTO
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🎯 Use Cases

* Fact Checking
* Misinformation Detection
* News Verification
* Social Media Analysis
* Educational Research
* Cybersecurity Awareness
* Digital Literacy Programs

---

## 🔮 Future Enhancements

* Real-Time Fact Checking APIs
* RAG-Based Evidence Retrieval
* LLM-Powered Explanations
* Multilingual Support
* Browser Extension
* Social Media Integration
* Live News Verification

---

## 📈 Current MVP Capabilities

* Offline Semantic Verification
* No External AI API Dependency
* Evidence-Based Analysis
* Interactive Dashboard
* OCR Support
* PDF Report Generation

---

## 👨‍💻 Developed By

Nilesh Kumar Mishra

B.Tech Computer Science Engineering

Focused on AI, Cybersecurity, Data Science, and Trustworthy Information Systems.

---

## 📜 License

This project is developed for educational, research, and hackathon purposes.
