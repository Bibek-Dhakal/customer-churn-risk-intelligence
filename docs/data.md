# Data Documentation

This document describes the dataset used by the **Customer Churn Risk Intelligence** project, including its source,
structure, preparation process, local folder organization, and data-handling considerations.

## Data Source

The project uses the Telco Customer Churn dataset.

The source dataset is available through the Kaggle dataset, commonly identified as **Telco Customer Churn** and
attributed to BlastChar.

The dataset is based on IBM's customer churn sample data.

For the original dataset and source context, refer to:

- [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

The repository does not redistribute the original raw dataset.

## Dataset Structure

The source CSV contains:

- **7,043 customer records**
- **21 columns**
- One row per customer
- A binary churn outcome

### Target

| Column  | Description                           |
|---------|---------------------------------------|
| `Churn` | Whether the customer left the service |

## Local Data Folder

The project expects the downloaded CSV to be placed under:

```text
data/
└── raw/
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv
```

## Data Flow

```text
Original Source CSV & Real-Time API Payloads
        |
        v
Pandera / Pydantic Data Contracts (Schema Enforcement)
        |
        v
Type Conversion & Cleaning
        |
        v
Feature Engineering
        |
        v
Stratified Train/Test Split
        |
        +----------------------+
        |                      |
        v                      v
Training Data             Test Data
        |                      |
        v                      |
Cross-Validation              |
        |                      |
        v                      |
Selected Model                |
        |                      |
        +----------+-----------+
                   |
                   v
          Final Test Evaluation
                   |
                   v
       Customer Churn Probabilities
```

## Data Preparation & Contracts

The raw dataset is governed by strict declarative data contracts defined in:

```text
src/schema.py
```

Validation is performed in `src/validate_data.py`. The preparation workflow includes:

1. Confirming that the source file exists.
2. Loading the CSV with pandas.
3. Enforcing the **Pandera Schema** to guarantee strict column types and constraints.
4. Checking for duplicate customer IDs.
5. Converting the `Churn` target from `Yes` / `No` to `1` / `0`.
6. Converting `TotalCharges` from text to numeric.

## Feature Engineering

The project creates additional customer-level features in:

```text
src/features.py
```

These features include: `LifetimeSpendPerTenure`, `MonthlyCostExposure`, `ServiceAdoptionCount`, `ServiceAdoptionRate`, `IsRollingContract`, `IsLongContract`, `EarlyLifecycleRolling`, `AccumulatedValueRatio`, and `UsesElectronicPayment`.

These transformations are verified automatically by tests in `tests/test_features.py`.

## Train/Test Split & Cross Validation

The modeling workflow creates a stratified train/test split (Test size: 20%, Random state: 42). Model comparison uses stratified K-fold cross-validation (5 folds) heavily tracked by **MLflow**.

## Generated Artifacts

Model execution generates files tracked by MLflow and persisted securely using **Skops** under:

```text
artifacts/
├── predictions.csv
├── model_comparison.csv
├── selected_model.skops      # Secure Skops model format
└── run_metadata.json
```

These files are generated outputs rather than source data. The `.skops` file format is deliberately chosen over `.joblib` or `.pkl` as it prevents arbitrary code execution vulnerabilities during API inference.

## Data Responsibility

Model predictions describe patterns learned from historical data. They do not establish why an individual customer will churn. Predictions should be calibrated alongside business intervention costs before being operationalized.