# Usage Guide

This guide explains how to set up, validate, run, and explore the **Customer Churn Risk Intelligence** project.

## 1. Prerequisites

Recommended environment:

* Python 3.10+
* Git
* Jupyter Notebook or JupyterLab

The project is designed to run on Windows, macOS, and Linux.

## 2. Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone <your-repository-url>
cd customer-churn-risk-intelligence
```

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

Install the packages listed in `requirements.min.txt`:

```bash
pip install -r requirements.min.txt
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
pip install -r requirements.min.txt
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
