# 📊 Customer Churn Risk Intelligence

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)

An enterprise-grade Machine Learning pipeline designed to predict customer churn, evaluate model families via cross-validation, and deliver actionable risk segmentation through a real-time REST API.

---

## 📌 Executive Summary

Customer churn severely impacts Customer Lifetime Value (CLV) and recurring revenue models. This production-ready pipeline identifies at-risk users, analyzes primary churn drivers, and stratifies predictions into actionable risk tiers to optimize business interventions.

* **Selected Model:** Logistic Regression
* **Test Performance:** `0.8482 ROC-AUC` | `0.6670 PR-AUC` | `0.7374 Accuracy`
* **Key Risk Factors:** Electronic check payments, short tenure (0–6 months), and elevated monthly charges.

### MLOps Infrastructure
This project implements a robust **Data-Agnostic MLOps Core**:
* **Data Contracts:** `Pandera` strictly enforces raw data schemas.
* **Experiment Tracking:** `MLflow` logs hyperparameters, cross-validation metrics, and model artifacts.
* **Secure Serialization:** Models are persisted using `Skops` to prevent arbitrary code execution vulnerabilities.
* **Real-time Serving:** A `FastAPI` microservice exposes the model via Docker for seamless CRM integration.
* **CI/CD & Testing:** Automated `Pytest` suites and GitHub actions ensure pipeline integrity.

---

## 🔗 Project Documentation & Artifacts

| Category              | Resource / Artifact Link                                                                           | Description                                                             |
|:----------------------|:---------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| **Usage Guide**       | [`docs/usage.md`](docs/usage.md)                                                                   | Setup, testing, MLflow tracking, and Docker API serving                 |
| **Dataset Details**   | [`docs/data.md`](docs/data.md)                                                                     | Data contracts, feature definitions, and target class distribution      |
| **Pipeline Runs**     | [`docs/run_results.md`](docs/run_results.md)                                                       | Execution outputs, cross-validation tables, and run logs                |
| **Project Roadmap**   | [`docs/future_roadmap.md`](docs/future_roadmap.md)                                                 | Technical backlog, threshold tuning, and optimization plans             |
| **EDA Notebook**      | [`notebooks/01_customer_retention_eda.ipynb`](notebooks/01_customer_retention_eda.ipynb)           | Exploratory analysis, feature distributions, and initial visualizations |
| **Modeling Notebook** | [`notebooks/02_customer_retention_modeling.ipynb`](notebooks/02_customer_retention_modeling.ipynb) | Cross-validation workflows, model selection, and diagnostic evaluation  |

---

## 🛠️ Architecture & Workflow

```text
Raw CSV ──► Pandera Data Contract ──► Feature Engineering ──► Stratified CV ──► MLflow Registry
                                                                                      │
                                                                                      ▼
CRM / Web App ◄── JSON Payload ── FastAPI REST API ◄── Docker Container ◄── Skops Serialization
```

---

## 📈 Model Performance Overview

Model selection prioritized probability ranking under class imbalance (~26.5% baseline churn rate):

| Model                   | Mean CV ROC-AUC | Mean CV PR-AUC | Mean CV Accuracy | Status       |
|-------------------------|-----------------|----------------|------------------|--------------|
| **Logistic Regression** | **0.8501**      | **0.6718**     | **0.7508**       | **Selected** |
| **Random Forest**       | 0.8426          | 0.6467         | 0.7725           | Evaluated    |
| **LightGBM**            | 0.8393          | 0.6478         | 0.7772           | Evaluated    |

---

## ⚡ Quickstart & Reproducibility

### 1. Environment Setup

```bash
git clone <repo_url>
cd <repo_name>

python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate # Linux/macOS

pip install -r requirements.min.txt
```

### 2. Validate Data Contract & Run Tests

```bash
pytest tests/
python -m src.validate_data
```

### 3. Run Training Pipeline & MLflow

```bash
python -m src.train
mlflow ui
```

### 4. Serve Model API (Local)

```bash
uvicorn src.serve:app --reload --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000/docs` to test predictions.

### 5. Serve via Docker

```bash
docker build -t customer-churn-api .
docker run -p 8000:8000 customer-churn-api
```

---

## 📂 Repository Layout

```text
├── data/
│   └── raw/                                      # Source CSV files
├── docs/                                         # Architecture, data, and usage documentation
├── notebooks/                                    # EDA and modeling Jupyter notebooks
├── src/
│   ├── config.py                                 # Configuration and constants
│   ├── schema.py                                 # Pandera and Pydantic data contracts
│   ├── features.py                               # Preprocessing and feature engineering
│   ├── modeling.py                               # Scikit-learn pipelines and model definitions
│   ├── train.py                                  # Training execution and MLflow registry
│   ├── validate_data.py                          # Schema validation module
│   └── serve.py                                  # FastAPI inference microservice
├── tests/                                        # Pytest unit tests for pipeline logic
├── .github/workflows/                            # CI/CD pipelines
├── Dockerfile                                    # API containerization config
├── requirements.min.txt                          # Python dependencies
└── README.md                                     # Project main landing page
```