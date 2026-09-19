# Project Roadmap & Future Extensions

While the core pipeline has been upgraded with an enterprise MLOps scaffold (FastAPI, MLflow, Pandera Contracts, Docker), the following enhancements represent technical next steps for future iterations:

### 1. Explainability & Feature Selection

* **Coefficient Extraction:** Extract and visualize the final Logistic Regression coefficients (odds ratios) to provide clear interpretability on which features most aggressively drive customer churn log-odds.
* **SHAP Values for API:** Expose SHAP (SHapley Additive exPlanations) values in the FastAPI `/predict` response so CRM users can see the "top reasons" for a customer's specific risk score.

### 2. Advanced Model Tuning & Auto-Retraining

* **Hyperparameter Optimization:** Implement systematic hyperparameter search (`GridSearchCV` or `Optuna`) integrated with MLflow tracking for tree-based models to evaluate whether fine-tuned gradient boosting outperforms the linear baseline.
* **Orchestration:** Introduce Apache Airflow or Dagster to orchestrate scheduled data extraction and automated retraining pipelines if the source dataset transitions from a static CSV to a live Cloud Data Warehouse (e.g., Snowflake/BigQuery).

### 3. Business Logic Optimization

* **Decision Threshold Optimization:** Standard classification defaults to `0.5`. By tuning the decision threshold down to `0.30 – 0.35`, we can significantly improve **Recall** for high-risk customers, ensuring retention campaigns capture more at-risk users before they leave.

### 4. Cloud Native Deployment

* **Kubernetes/Cloud Run:** Migrate the provided Docker container to AWS ECS, GCP Cloud Run, or a managed Kubernetes cluster to enable horizontal auto-scaling during peak CRM querying periods.
* **Drift Observability:** Integrate Evidently AI or NannyML into the serving microservice to continuously monitor input payload distributions against the training baseline to detect data drift.