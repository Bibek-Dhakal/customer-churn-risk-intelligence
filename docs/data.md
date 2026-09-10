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

The target variable is:

```text
Churn
````

where:

```text
No  -> 0
Yes -> 1
```

### Customer Information

| Column          | Description                         |
|-----------------|-------------------------------------|
| `customerID`    | Unique customer identifier          |
| `gender`        | Customer gender                     |
| `SeniorCitizen` | Senior-citizen indicator            |
| `Partner`       | Whether the customer has a partner  |
| `Dependents`    | Whether the customer has dependents |

### Service Information

| Column             | Description                                                 |
|--------------------|-------------------------------------------------------------|
| `tenure`           | Number of months the customer has remained with the company |
| `PhoneService`     | Whether phone service is subscribed                         |
| `MultipleLines`    | Multiple-line phone service status                          |
| `InternetService`  | Internet service type                                       |
| `OnlineSecurity`   | Online security service status                              |
| `OnlineBackup`     | Online backup service status                                |
| `DeviceProtection` | Device protection service status                            |
| `TechSupport`      | Technical support service status                            |
| `StreamingTV`      | Streaming TV service status                                 |
| `StreamingMovies`  | Streaming movie service status                              |

### Account and Billing Information

| Column             | Description                          |
|--------------------|--------------------------------------|
| `Contract`         | Contract term                        |
| `PaperlessBilling` | Paperless billing indicator          |
| `PaymentMethod`    | Customer payment method              |
| `MonthlyCharges`   | Current monthly customer charge      |
| `TotalCharges`     | Total amount charged to the customer |

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

The raw CSV should not be committed to the Git repository unless the dataset's applicable license explicitly permits
redistribution and the project intentionally chooses to do so.

## Why There Is Only One CSV

The downloaded source dataset is a single customer-level CSV.

The project therefore does **not** require manually creating separate:

```text
train.csv
test.csv
```

files.

Instead, the modeling workflow loads the complete source CSV and creates a reproducible stratified train/test split
during execution.

This keeps the original source data unchanged and makes the modeling split controlled by the project's configuration.

## Data Flow

```text
Original Source CSV
        |
        v
Data Validation
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
Model Comparison              |
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

## Data Preparation

The raw dataset is prepared through reusable functions in:

```text
src/validate_data.py
```

The preparation workflow includes:

1. Confirming that the source file exists.
2. Loading the CSV with pandas.
3. Checking that the expected columns are present.
4. Checking for duplicate customer IDs.
5. Converting the `Churn` target from `Yes` / `No` to `1` / `0`.
6. Converting `TotalCharges` from text to numeric.
7. Handling values that cannot be converted to numeric values.
8. Returning the prepared dataset for analysis and modeling.

## TotalCharges

The source dataset stores `TotalCharges` as a text field.

The project converts it to numeric values before modeling:

```python
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce",
)
```

Values that cannot be converted are handled during preparation using the customer's monthly charge as a conservative
fallback.

This transformation is implemented in the shared validation/preparation module rather than independently in each
notebook.

## Feature Engineering

The project creates additional customer-level features in:

```text
src/features.py
```

The engineered features include:

| Feature                  | Purpose                                               |
|--------------------------|-------------------------------------------------------|
| `LifetimeSpendPerTenure` | Approximate accumulated spend per month of tenure     |
| `MonthlyCostExposure`    | Relative monthly charge exposure                      |
| `ServiceAdoptionCount`   | Number of optional services adopted                   |
| `ServiceAdoptionRate`    | Share of optional services adopted                    |
| `IsRollingContract`      | Indicator for month-to-month contracts                |
| `IsLongContract`         | Indicator for two-year contracts                      |
| `EarlyLifecycleRolling`  | Indicator for newer customers on rolling contracts    |
| `AccumulatedValueRatio`  | Relationship between accumulated and expected charges |
| `UsesElectronicPayment`  | Indicator for electronic-check payment                |

These features are intended to represent customer lifecycle, service adoption, contract structure, billing exposure, and
payment behavior.

They are modeling features, not claims of causal relationships.

## Train/Test Split

The modeling workflow creates a stratified train/test split using the configuration values in:

```text
src/config.py
```

The default configuration uses:

```text
Test size: 20%
Random state: 42
```

Stratification is applied using the churn target so that the training and test partitions maintain similar target
proportions.

The split is performed after loading and feature preparation and before model fitting.

## Cross-Validation

Model comparison uses stratified K-fold cross-validation.

The default configuration uses:

```text
5 folds
shuffle = True
random_state = 42
```

The primary model-comparison metric is ROC-AUC.

Additional metrics include:

* Average Precision
* Log Loss
* Accuracy

Performance numbers are calculated when the project is executed rather than stored as fixed claims in the documentation.

## Data Quality Considerations

The source dataset contains customer-level information and several categorical service fields.

Important considerations include:

* `customerID` is an identifier and is excluded from model predictors.
* Categorical variables require encoding before model training.
* `TotalCharges` requires numeric conversion.
* The churn target is imbalanced, so stratified validation is used.
* Some service columns contain values such as `No internet service` or `No phone service`.
* The project preserves these categorical distinctions rather than treating them as ordinary missing values.

## Dataset Licensing and Attribution

The repository's software license applies to the original project code and documentation, not automatically to the
external dataset.

The dataset remains subject to the terms, attribution requirements, and rights applicable to its original source.

The Kaggle dataset page currently identifies its data files as belonging to the original authors. Users should review
the current source terms before redistributing the data.

For this reason:

* The raw dataset is not included in this repository.
* Users should obtain the dataset directly from its source.
* The repository documents the source for reproducibility.
* The repository's MIT license does not grant rights to the external dataset.

## Reproducibility

To reproduce the project:

1. Obtain the source dataset.
2. Place the CSV in:

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

3. Install the project dependencies.
4. Run data validation.
5. Run the modeling workflow.
6. Review the generated artifacts.

The project uses a fixed random seed for the train/test split and cross-validation so that repeated runs use the same
partitioning configuration.

## Generated Artifacts

Model execution can generate files under:

```text
artifacts/
```

Typical outputs include:

```text
artifacts/
├── predictions.csv
├── model_comparison.csv
├── selected_model.joblib
└── run_metadata.json
```

These files are generated outputs rather than source data.

The raw dataset and generated model artifacts should normally remain outside version control unless there is a
deliberate reason to publish them.

## Data Responsibility

This project is intended for educational, portfolio, and analytical purposes.

Churn predictions should not automatically be treated as decisions about individual customers.

Before using a churn-risk model operationally, an organization should consider:

* Prediction calibration
* Intervention costs
* Retention campaign capacity
* False-positive and false-negative costs
* Fairness and subgroup performance
* Privacy and data governance
* Model monitoring
* Data drift
* Appropriate customer communication

Model predictions describe patterns learned from historical data. They do not establish why an individual customer will
churn.

---
