# Project Roadmap & Future Extensions

While the baseline modeling pipeline and exploratory data analysis (EDA) yield production-ready baseline results, the
following enhancements represent key technical next steps for future iterations:

### 1. Explainability & Feature Selection

* **Coefficient Extraction:** Extract and visualize the final Logistic Regression coefficients (odds ratios) to provide
  clear interpretability on which features most aggressively drive customer churn log-odds.

### 2. Decision Threshold Optimization

* **Business-Centric Thresholding:** Standard classification defaults to `0.5`. By tuning the decision threshold down to
  `0.30 – 0.35`, we can significantly improve **Recall** for high-risk customers, ensuring retention campaigns capture
  more at-risk users before they leave.

### 3. Advanced Model Tuning

* **Hyperparameter Optimization:** Implement systematic hyperparameter search (`GridSearchCV` or `Optuna`) for the
  tree-based models (LightGBM and Random Forest) to evaluate whether fine-tuned gradient boosting outperforms the linear
  baseline.

---
