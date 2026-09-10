# Customer Churn Risk Intelligence

An end-to-end machine learning project for identifying customers who are at higher risk of churn and understanding the
customer characteristics associated with retention.

## Overview

Customer churn is a critical business problem for subscription-based services. Being able to identify customers who may
leave allows organizations to prioritize retention efforts, improve customer experience, and make better use of limited
intervention resources.

This project develops a machine learning workflow that uses customer demographics, service usage, contract information,
tenure, and billing characteristics to estimate churn probability.

Rather than focusing only on a single predictive model, the project explores the complete modeling process—from data
quality and exploratory analysis through feature engineering, model comparison, validation, and prediction.

## Objectives

* Explore customer characteristics associated with churn.
* Identify important patterns in customer tenure, contracts, services, and billing.
* Engineer meaningful features that represent customer behavior and commercial relationships.
* Compare multiple classification algorithms using a consistent validation strategy.
* Evaluate models using probability-based classification metrics.
* Produce churn probabilities that can be used to prioritize customers for retention efforts.
* Build a reproducible and leakage-aware machine learning workflow.

## Project Workflow

```text
Raw Customer Data
       │
       ▼
Data Quality & Validation
       │
       ▼
Exploratory Data Analysis
       │
       ▼
Feature Engineering
       │
       ▼
Preprocessing
       │
       ▼
Model Development
       │
       ├── Logistic Regression
       ├── Random Forest
       └── LightGBM
       │
       ▼
Stratified Cross-Validation
       │
       ▼
Model Comparison
       │
       ▼
Best-Model Selection
       │
       ▼
Churn Probability Predictions
```

## Machine Learning Approach

The project compares models with different modeling assumptions and levels of complexity.

### Logistic Regression

Provides a relatively interpretable linear baseline and establishes how well churn can be modeled from a conventional
statistical classification perspective.

### Random Forest

Provides a nonlinear ensemble approach capable of capturing interactions and more complex relationships between customer
characteristics.

### LightGBM

Provides a gradient-boosted decision-tree approach designed for efficient modeling of structured tabular data.

The models are evaluated using the same cross-validation framework so that their results can be compared on a consistent
basis.

## Feature Engineering

The project derives additional customer-level signals from the original attributes where appropriate.

Examples include measures representing:

* customer lifetime spending relative to tenure;
* accumulated customer value;
* service adoption;
* proportion of available services adopted;
* contract stability;
* early-stage customers on rolling contracts;
* electronic payment behavior;
* monthly cost exposure.

These features are designed to represent business concepts rather than simply increasing the number of columns.

## Validation

Model evaluation uses **stratified cross-validation**, preserving the approximate target distribution across validation
folds.

The primary ranking metric is **ROC-AUC**, allowing the models to be evaluated on their ability to distinguish customers
with different levels of churn risk across probability thresholds.

Additional metrics are considered to provide a broader view of model behavior, including:

* Average Precision
* Log Loss
* Accuracy at a 0.5 classification threshold

The final performance values are generated from the executed experiments rather than being predetermined.

## Results

Model performance is evaluated experimentally during training, with the strongest candidate selected according to
validation ROC-AUC.

The repository does not rely on a predefined benchmark score: results depend on the dataset and execution environment
used for the experiment.

This makes the project reproducible while avoiding unsupported claims about model performance.

## Outputs

The modeling workflow produces:

* model comparison results;
* customer-level churn probability predictions;
* the selected trained model;
* experiment metadata.

The prediction output represents **probability of churn**, rather than simply assigning every customer to a binary
churn/non-churn class.

This makes the output suitable for ranking customers by relative retention risk.

## How to Run

For environment setup, dataset placement, dependency installation, and notebook execution instructions, see the
**[Usage Guide](docs/usage.md)**.

The project notebooks are located in:

```text
notebooks/
├── 01_customer_retention_eda.ipynb
└── 02_customer_retention_modeling.ipynb
```

Run the notebooks from top to bottom after completing the setup described in the usage guide.

## Repository Structure

```text
## Repository Structure

```text
customer-churn-risk-intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── artifacts/
│
├── docs/
│   └── usage.md
│
├── notebooks/
│   ├── 01_customer_retention_eda.ipynb
│   └── 02_customer_retention_modeling.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── features.py
│   ├── modeling.py
│   ├── train.py
│   └── validate_data.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.min.txt
```

## Key Design Considerations

### Leakage-aware processing

Transformations that depend on the observed training data are performed within the modeling workflow so that validation
information is not inadvertently used to construct training features.

### Reproducibility

Random states and major modeling parameters are explicitly defined, allowing experiments to be repeated under the same
conditions.

### Model comparison

Instead of assuming that a particular algorithm is optimal, multiple approaches are evaluated using a common validation
framework.

### Probability-based predictions

The output preserves continuous churn probabilities, making it possible to prioritize customers according to risk rather
than relying solely on an arbitrary classification threshold.

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* LightGBM
* Matplotlib
* Seaborn
* Jupyter

## Project Focus

This project combines **predictive modeling with practical customer-retention analysis**.

The goal is not simply to build a model that predicts churn, but to create a workflow where the resulting predictions
can support questions such as:

* Which customers appear most vulnerable to churn?
* What customer characteristics are associated with increased risk?
* How does contract structure relate to retention?
* Does service adoption provide useful predictive information?
* How can churn probabilities be used to prioritize retention activity?

## Disclaimer

This project is intended for educational, analytical, and portfolio purposes. Model predictions represent statistical
estimates from the available dataset and should not be interpreted as certain predictions of individual customer
behavior.

The dataset and its associated usage rights remain subject to their original licensing or competition terms.
