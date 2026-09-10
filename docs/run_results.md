# Pipeline Execution & Experimentation Report

This document records the data validation, exploratory data analysis (EDA), model cross-validation comparison, terminal
logs, and test performance metadata for the **Customer Churn Risk Intelligence** pipeline.

---

## 1. Terminal Execution Logs

Executed via PowerShell 7.6.6 in the project virtual environment:

```text
(.venv) PS D:\00-ml-projects\customer-churn-risk-intelligence> python -m src.validate_data
Data validation successful.
Rows: 7,043
Columns: 21
Churn rate: 26.54%

(.venv) PS D:\00-ml-projects\customer-churn-risk-intelligence> python -m src.train
Training completed successfully.
Dataset: WA_Fn-UseC_-Telco-Customer-Churn.csv
Training rows: 5,634
Test rows: 1,409
Selected model: Logistic Regression

Test metrics:
ROC_AUC: 0.8482
Average_Precision: 0.6670
Log_Loss: 0.4858
Accuracy_At_0.5: 0.7374

```

---

## 2. Model Cross-Validation Results

The pipeline evaluated three algorithm families across **5-Fold Stratified Cross-Validation** on the training set (5,634
samples):

| Model                   | Mean CV ROC-AUC | Std CV ROC-AUC | Mean CV Avg Precision | Mean CV Log Loss | Mean CV Accuracy |
|-------------------------|-----------------|----------------|-----------------------|------------------|------------------|
| **Logistic Regression** | **0.8501**      | **0.0116**     | **0.6718**            | **0.4831**       | **0.7508**       |
| **Random Forest**       | 0.8426          | 0.0083         | 0.6467                | 0.4624           | 0.7725           |
| **LightGBM**            | 0.8393          | 0.0072         | 0.6478                | 0.4634           | 0.7772           |

### Selection Rationale & Interpretation

* **Logistic Regression** achieved the highest **Mean CV ROC-AUC (0.8501)** and **Average Precision (0.6718)**, making
  it the most robust candidate for probability-based risk ranking on imbalanced target data (26.54% churn).
* While tree-based ensembles (Random Forest, LightGBM) yielded slightly higher raw accuracy at default threshold `0.5`,
  Logistic Regression provided superior ranking sensitivity across varying risk thresholds.

---

## 3. Run Metadata (`run_metadata.json`)

```json
{
  "dataset": "WA_Fn-UseC_-Telco-Customer-Churn.csv",
  "total_rows": 7043,
  "total_columns": 30,
  "train_rows": 5634,
  "test_rows": 1409,
  "test_size": 0.2,
  "random_state": 42,
  "cv_folds": 5,
  "target": "Churn",
  "selected_model": "Logistic Regression",
  "test_metrics": {
    "ROC_AUC": 0.8482110103593479,
    "Average_Precision": 0.6669548301964747,
    "Log_Loss": 0.4857611356568524,
    "Accuracy_At_0.5": 0.7374024130589071
  }
}

```

---

## 4. Key EDA & Visual Insights

* **Target Class Imbalance:** **26.54%** churn rate across 7,043 total records (5,174 retained vs. 1,869 churned).
* **Payment Method Vulnerability:** Customers using **Electronic check** experience the highest churn rate (>45%),
  compared to ~15–19% for automated payments and mailed checks.
* **Tenure Decay:** The **0–6 months tenure** band has a churn rate of **52.94%**, dropping steadily below **10%** for
  customers in the **49–72 months** band.
* **Monthly Charge Sensitivity:** Churned users show a significantly higher median monthly
  cost (~$80) compared to retained users (~$65).

---
