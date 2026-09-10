# 📊 Customer Churn Risk Intelligence

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An end-to-end Machine Learning pipeline designed to predict customer churn, evaluate model families via 5-fold
cross-validation, and deliver actionable risk segmentation for retention campaigns.

---

## 📌 Executive Summary

Customer churn severely impacts Customer Lifetime Value (CLV) and recurring revenue models. This production-ready
pipeline identifies at-risk users, analyzes primary churn drivers, and stratifies predictions into actionable risk tiers
to optimize business interventions.

* **Selected Model:** Logistic Regression
* **Test Performance:** `0.8482 ROC-AUC` | `0.6670 PR-AUC` | `0.7374 Accuracy`
* **Key Risk Factors:** Electronic check payments, short tenure (0–6 months), and elevated monthly charges.

For pipeline execution logs and cross-validation comparisons, see [`docs/run_results.md`](docs/run_results.md).

---

## 🔗 Project Documentation & Artifacts

| Category              | Resource / Artifact Link                                                                           | Description                                                             |
|:----------------------|:---------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| **Pipeline Runs**     | [`docs/run_results.md`](docs/run_results.md)                                                       | Execution outputs, cross-validation tables, and `run_metadata.json`     |
| **Dataset Details**   | [`docs/data.md`](docs/data.md)                                                                     | Data schema, feature definitions, and target class distribution         |
| **Usage Guide**       | [`docs/usage.md`](docs/usage.md)                                                                   | Step-by-step instructions for setup, validation, and training           |
| **Project Roadmap**   | [`docs/future_roadmap.md`](docs/future_roadmap.md)                                                 | Technical backlog, threshold tuning, and optimization plans             |
| **Dataset Storage**   | [`data/README.md`](data/README.md)                                                                 | Information on raw data placement and schema expectations               |
| **EDA Notebook**      | [`notebooks/01_customer_retention_eda.ipynb`](notebooks/01_customer_retention_eda.ipynb)           | Exploratory analysis, feature distributions, and initial visualizations |
| **Modeling Notebook** | [`notebooks/02_customer_retention_modeling.ipynb`](notebooks/02_customer_retention_modeling.ipynb) | Cross-validation workflows, model selection, and diagnostic evaluation  |

---

## 🛠️ Architecture & Workflow

```text
Raw CSV Data ──► Validation Script ──► Preprocessing & Encoding ──► 5-Fold Stratified CV ──► Test Evaluation ──► Risk Stratification

```

The pipeline systematically processes raw customer attributes, validates input schemas, evaluates models (Logistic
Regression, Random Forest, LightGBM), and outputs trained model artifacts alongside execution metadata.

---

## 📈 Model Performance Overview

Model selection prioritized probability ranking under class imbalance (~26.5% baseline churn rate):

| Model                   | Mean CV ROC-AUC | Mean CV PR-AUC | Mean CV Accuracy | Status       |
|-------------------------|-----------------|----------------|------------------|--------------|
| **Logistic Regression** | **0.8501**      | **0.6718**     | **0.7508**       | **Selected** |
| **Random Forest**       | 0.8426          | 0.6467         | 0.7725           | Evaluated    |
| **LightGBM**            | 0.8393          | 0.6478         | 0.7772           | Evaluated    |

Detailed metric distributions, standard deviations, and log-loss comparisons are documented in [
`docs/run_results.md`](docs/run_results.md).

---

## ⚡ Quickstart & Reproducibility

### 1. Environment Setup

```bash
# Clone the repository
git clone <repo_url>
cd <repo_name>

# Initialize virtual environment (Python 3.12+)
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.min.txt

```

### 2. Validate Dataset

```bash
python -m src.validate_data

```

### 3. Run Pipeline Training

```bash
python -m src.train

```

For complete CLI options and customization, refer to [`docs/usage.md`](docs/usage.md).

---

## 📂 Repository Layout

```text
├── data/
│   └── README.md                                 # Data folder guidelines
├── docs/
│   ├── data.md                                   # Schema and dataset details
│   ├── future_roadmap.md                         # Technical roadmap and backlog
│   ├── run_results.md                            # Execution logs, CV metrics, and metadata
│   └── usage.md                                  # Execution and setup guide
├── notebooks/
│   ├── 01_customer_retention_eda.ipynb           # Exploratory data analysis notebook
│   └── 02_customer_retention_modeling.ipynb      # Model training & validation notebook
├── src/
│   ├── __init__.py                               # Package entry
│   ├── config.py                                 # Configuration and constants
│   ├── features.py                               # Preprocessing and feature engineering
│   ├── modeling.py                               # Model definitions and cross-validation
│   ├── train.py                                  # Training execution pipeline
│   └── validate_data.py                          # Schema validation module
├── .gitignore                                    # Git exclusion rules
├── PATCH.md                                      # Patch and version history
├── requirements.min.txt                          # Minimal Python 3.12 dependencies
└── README.md                                     # Project main landing page

```

---
