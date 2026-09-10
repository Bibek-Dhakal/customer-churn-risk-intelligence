# Customer Churn Risk Intelligence

An end-to-end machine learning project for identifying customers who are at higher risk of churn and understanding the
customer characteristics associated with retention.

The project combines exploratory analysis, reusable feature engineering, model comparison, stratified cross-validation,
and probability-based churn-risk scoring.

## Overview

Customer churn is an important business problem because retaining an existing customer can be more efficient than
acquiring a replacement.

This project develops a reproducible machine learning workflow that:

* Validates and prepares customer data
* Explores churn patterns across customer segments
* Creates business-oriented customer features
* Compares multiple classification models
* Uses stratified cross-validation for model selection
* Evaluates the selected model on a held-out test set
* Produces customer-level churn probabilities
* Groups customers into practical risk segments

The project is designed as a portfolio-quality example of applied machine learning and business analytics.

## Objectives

The main objectives are to:

1. Understand observable characteristics associated with customer churn.
2. Build a reliable churn classification workflow.
3. Compare different modeling approaches under a consistent evaluation framework.
4. Produce probability-based customer risk scores.
5. Translate model outputs into retention-oriented insights.

## Project Workflow

```text
Raw Customer Data
        |
        v
Data Quality & Validation
        |
        v
Exploratory Data Analysis
        |
        v
Feature Engineering
        |
        v
Preprocessing
        |
        v
Model Development
   |       |       |
   v       v       v
Logistic  Random  LightGBM
Regression Forest
   |       |       |
   +-------+-------+
           |
           v
Stratified Cross-Validation
           |
           v
Model Comparison
           |
           v
Best-Model Selection
           |
           v
Held-Out Test Evaluation
           |
           v
Churn Probability Predictions
           |
           v
Customer Risk Segmentation
```

## Machine Learning Approach

Three candidate classification approaches are evaluated:

### Logistic Regression

Provides an interpretable linear baseline and establishes a useful benchmark for more complex models.

### Random Forest

Captures nonlinear relationships through an ensemble of decision trees.

### LightGBM

Uses gradient-boosted decision trees and provides a strong candidate for tabular classification.

All models are evaluated using the same overall data-splitting and validation strategy.

## Feature Engineering

The project creates several customer-level features designed to capture different aspects of the customer relationship.

Examples include:

* `LifetimeSpendPerTenure`
* `MonthlyCostExposure`
* `ServiceAdoptionCount`
* `ServiceAdoptionRate`
* `IsRollingContract`
* `IsLongContract`
* `EarlyLifecycleRolling`
* `AccumulatedValueRatio`
* `UsesElectronicPayment`

These features represent customer lifecycle, service adoption, contract structure, payment behavior, and financial
exposure.

They are predictive features rather than claims of causal relationships.

## Validation

The project uses a reproducible stratified train/test split.

The default configuration is:

* Test size: 20%
* Cross-validation: 5 stratified folds
* Random state: 42
* Primary model-selection metric: ROC-AUC

Additional evaluation metrics include:

* Average Precision
* Log Loss
* Accuracy

The final selected model is evaluated on an untouched test set after model selection.

## Results

Model performance is calculated when the project is executed.

The repository does not hard-code model performance numbers because results should be reproducible from the source data
and project configuration.

Generated model-comparison results are saved to:

```text
artifacts/model_comparison.csv
```

Final test metrics are also recorded in:

```text
artifacts/run_metadata.json
```

## Outputs

Running the modeling pipeline can produce:

```text
artifacts/
├── predictions.csv
├── model_comparison.csv
├── selected_model.joblib
└── run_metadata.json
```

### `predictions.csv`

Contains customer-level predictions for the held-out test set, including:

* Customer identifier
* Actual churn outcome
* Churn probability
* Binary churn prediction

### `model_comparison.csv`

Contains cross-validation results for the candidate models.

### `selected_model.joblib`

Contains the fitted selected model pipeline.

### `run_metadata.json`

Contains run configuration, dataset dimensions, selected model information, and final test metrics.

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd customer-churn-risk-intelligence
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Download the source dataset and place the CSV at:

```text
data/
└── raw/
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv
```

The raw dataset is not included in this repository.

For dataset provenance, structure, licensing information, and data-handling details, see the *
*[Data Documentation](docs/data.md)**.

### 5. Validate the data

```bash
python -m src.validate_data
```

### 6. Run the modeling pipeline

```bash
python -m src.train
```

### 7. Explore the notebooks

Open:

```text
notebooks/01_customer_retention_eda.ipynb
notebooks/02_customer_retention_modeling.ipynb
```

For detailed setup, execution, troubleshooting, and workflow instructions, see the **[Usage Guide](docs/usage.md)**.

## Repository Structure

```text
customer-churn-risk-intelligence/
│
├── data/
│   └── raw/
│       └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── docs/
│   ├── data.md
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
├── artifacts/
│   └── .gitkeep
│
├── LICENSE
├── README.md
└── requirements.txt
```

## Key Design Considerations

### Reproducibility

The project uses explicit random seeds for train/test splitting and cross-validation.

### Reusable Code

Data preparation, feature engineering, preprocessing, model construction, and evaluation logic are maintained under
`src/` so that notebooks do not become the only source of project logic.

### Probability-Based Risk

The model produces churn probabilities rather than relying only on binary predictions. This supports prioritization and
risk segmentation.

### Avoiding Data Leakage

The final test set is held out from model selection and is used only for final evaluation.

### Business Interpretation

Model outputs are intended to support retention analysis and prioritization. They should not automatically be
interpreted as causal explanations for individual customer behavior.

## Technologies

* Python
* pandas
* NumPy
* scikit-learn
* LightGBM
* Matplotlib
* Jupyter Notebook
* joblib

## Project Focus

This project demonstrates practical skills in:

* Data validation
* Exploratory data analysis
* Feature engineering
* Classification
* Cross-validation
* Model comparison
* Probability-based prediction
* Business-oriented risk segmentation
* Reproducible machine learning workflows

## Disclaimer

This project is intended for educational, portfolio, and analytical purposes.

The dataset is externally sourced and is not owned by this repository.

The repository's software license applies to the original project code and documentation, not automatically to the
external dataset.

Churn predictions are model-based estimates and should not be treated as causal conclusions or automated decisions about
individual customers.

````

## `docs/usage.md`

# Usage Guide

This guide explains how to set up, validate, run, and explore the **Customer Churn Risk Intelligence** project.

## 1. Prerequisites

Recommended environment:

- Python 3.10+
- Git
- Jupyter Notebook or JupyterLab

The project is designed to run on Windows, macOS, and Linux.

## 2. Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone <your-repository-url>
cd customer-churn-risk-intelligence
````

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal should indicate that the virtual environment is active.

## 4. Install Dependencies

Install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The main dependencies include:

* pandas
* NumPy
* scikit-learn
* LightGBM
* Matplotlib
* joblib
* Jupyter

## 5. Dataset

The project requires the source Telco Customer Churn CSV.

Place the downloaded dataset at:

```text
data/
└── raw/
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv
```

The project uses a **single source CSV**.

You do not need to create separate `train.csv` and `test.csv` files.

The modeling pipeline creates the train/test split programmatically.

For dataset source, structure, licensing, preparation, and reproducibility details, see the *
*[Data Documentation](data.md)**.

## 6. Validate the Dataset

From the project root, run:

```bash
python -m src.validate_data
```

The validation process checks that:

* The dataset exists.
* Expected columns are present.
* The dataset contains rows.
* Customer IDs are unique.
* The churn target contains expected values.
* Numeric fields can be prepared for modeling.

A successful run should print a validation confirmation together with dataset dimensions and the churn rate.

## 7. Run the Modeling Pipeline

Run:

```bash
python -m src.train
```

The training workflow performs the following steps:

1. Loads the single source CSV.
2. Validates and prepares the dataset.
3. Converts the churn target to binary form.
4. Converts `TotalCharges` to numeric.
5. Creates engineered features.
6. Separates the customer identifier from predictors.
7. Creates a stratified train/test split.
8. Builds candidate model pipelines.
9. Runs stratified cross-validation.
10. Compares candidate models.
11. Selects the strongest model using mean CV ROC-AUC.
12. Fits the selected model.
13. Evaluates the model on the held-out test set.
14. Generates customer-level churn probabilities.
15. Saves model outputs and metadata.

## 8. Generated Artifacts

After successful training, the following files may appear under:

```text
artifacts/
```

### Model comparison

```text
artifacts/model_comparison.csv
```

Contains cross-validation results for the candidate models.

### Predictions

```text
artifacts/predictions.csv
```

Contains predictions for customers in the held-out test set.

Typical columns include:

```text
customerID
ActualChurn
ChurnProbability
PredictedChurn
```

### Selected model

```text
artifacts/selected_model.joblib
```

Contains the fitted preprocessing and model pipeline.

### Run metadata

```text
artifacts/run_metadata.json
```

Contains information such as:

* Dataset name
* Dataset dimensions
* Training/test sizes
* Random seed
* Number of cross-validation folds
* Selected model
* Final test metrics

## 9. Running the Notebooks

The repository contains two notebooks.

### Notebook 1 — Exploratory Data Analysis

```text
notebooks/01_customer_retention_eda.ipynb
```

This notebook examines:

* Dataset structure
* Data types
* Missing values
* Churn distribution
* Contract characteristics
* Payment methods
* Internet services
* Customer tenure
* Monthly charges
* Service adoption
* Engineered features
* Descriptive churn patterns

### Notebook 2 — Modeling

```text
notebooks/02_customer_retention_modeling.ipynb
```

This notebook demonstrates:

* Dataset preparation
* Feature engineering
* Stratified train/test splitting
* Candidate model construction
* Cross-validation
* Model comparison
* Best-model selection
* Held-out test evaluation
* Customer churn probabilities
* Risk segmentation

## 10. Start Jupyter

From the project root:

```bash
jupyter notebook
```

or:

```bash
jupyter lab
```

Open the notebooks under:

```text
notebooks/
```

Run the cells from top to bottom.

## 11. Notebook Imports

The notebooks use project code from `src/`.

For example:

```python
from src.config import RAW_DATA_PATH
from src.features import add_features
from src.validate_data import load_prepared_data
```

This keeps data preparation and feature logic centralized rather than duplicating the implementation across notebooks.

## 12. Project Configuration

Core project settings are maintained in:

```text
src/config.py
```

Important settings include:

```text
TEST_SIZE = 0.20
CV_FOLDS = 5
RANDOM_STATE = 42
```

Changing these values changes the experimental configuration.

For reproducible comparisons, keep the random state fixed.

## 13. Evaluation Strategy

ROC-AUC is the primary model-selection metric.

The project also records:

* Average Precision
* Log Loss
* Accuracy

The model is selected using cross-validation on the training partition.

The held-out test partition is reserved for final evaluation.

## 14. Risk Segmentation

The modeling notebook demonstrates four illustrative risk groups:

```text
Probability < 0.25      Low
0.25 - <0.50            Moderate
0.50 - <0.75            High
>= 0.75                 Very High
```

These thresholds are not production recommendations.

In a real retention program, thresholds should be selected using business considerations such as:

* Cost of contacting customers
* Expected retention value
* Available campaign capacity
* False-positive costs
* False-negative costs
* Model calibration

## 15. Troubleshooting

### Dataset not found

If you receive an error indicating that the dataset cannot be found, confirm that the file exists at:

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Also confirm that you are running commands from the project root.

### Import errors

If Python cannot import `src`, run commands from the repository root:

```bash
python -m src.validate_data
```

rather than executing source files directly.

### LightGBM installation problems

Try upgrading pip:

```bash
python -m pip install --upgrade pip
```

Then reinstall the dependencies:

```bash
pip install -r requirements.txt
```

### Notebook cannot import `src`

Restart the notebook kernel and ensure the notebook is being run from the project repository.

The notebooks also include project-root path handling to make imports more reliable.

## 16. Reproducibility Checklist

For a reproducible run:

1. Use the documented source dataset.
2. Keep the project configuration unchanged.
3. Use the same Python dependency versions where possible.
4. Keep `RANDOM_STATE = 42`.
5. Run validation before training.
6. Run the modeling pipeline from the project root.
7. Record the generated metadata and model-comparison results.

## 17. Recommended Execution Order

For a fresh project setup:

```text
1. Download dataset
        ↓
2. Place CSV in data/raw/
        ↓
3. Create virtual environment
        ↓
4. Install requirements
        ↓
5. Run src.validate_data
        ↓
6. Run Notebook 01
        ↓
7. Run Notebook 02
        ↓
8. Run src.train
        ↓
9. Review artifacts
```

The notebooks are intended for exploration and presentation, while the reusable implementation under `src/` provides the
project's core data and modeling workflow.

````

## Then check everything before committing

Run:

```bash
python -m src.validate_data
````

Then:

```bash
python -m src.train
```

Then open and run both notebooks.

After that, check:

```bash
git status
```

### Recommended commit

Because you're correcting the project structure and documentation together, I'd use:

```bash
git add README.md docs/data.md docs/usage.md notebooks/01_customer_retention_eda.ipynb notebooks/02_customer_retention_modeling.ipynb src/config.py src/validate_data.py src/features.py src/modeling.py src/train.py
git commit -m "refactor: align project with single source dataset"
git push
```

If you **already pushed the previous incorrect commit and reset it**, use:

```bash
git push --force-with-lease
```

instead of the final `git push`.

**Don't use `git add .` here** if you have the downloaded CSV or generated artifacts sitting in the repository, unless
your `.gitignore` is definitely configured correctly.
