# Data Documentation

This document describes the dataset used by the Customer Churn Risk Intelligence project, its source, structure,
preparation, and storage conventions.

## Data Source

The project uses the **Telco Customer Churn** dataset originally published as part of IBM Sample Data Sets and
distributed through Kaggle.

**Primary dataset source:**

[Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

The dataset contains customer-level information covering demographics, services, account characteristics, contract
information, tenure, billing, and churn status. The original dataset contains **7,043 customer records and 21 columns**.

The Kaggle dataset describes the source context as a fictional telecommunications company providing home phone and
Internet services.

### IBM Source

The Kaggle dataset also points to IBM's related sample-data material:

[IBM Telco Customer Churn — IBM Community](https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113)

The IBM material provides additional background on the Telco Customer Churn sample data.

## Dataset Licensing and Attribution

The dataset is an external data source and is **not covered by this project's MIT License**.

The Kaggle dataset page currently identifies the data files as **© Original Authors** rather than granting the
repository's MIT license to the dataset.

Therefore:

* The MIT License in the repository applies to the project's original source code and documentation.
* The dataset remains subject to the terms and rights associated with its original source.
* The raw dataset is not redistributed as part of this repository.
* Users reproducing the project should obtain the dataset from the original source and review its current terms before
  use or redistribution.

## Dataset Structure

The original dataset contains one row per customer.

The main target variable is:

| Column  | Description                                                                    |
|---------|--------------------------------------------------------------------------------|
| `Churn` | Indicates whether the customer left during the observed period (`Yes` / `No`). |

The original dataset includes several groups of customer attributes.

### Customer Demographics

| Column          | Description                                         |
|-----------------|-----------------------------------------------------|
| `customerID`    | Unique identifier for the customer.                 |
| `gender`        | Customer gender.                                    |
| `SeniorCitizen` | Indicates whether the customer is a senior citizen. |
| `Partner`       | Indicates whether the customer has a partner.       |
| `Dependents`    | Indicates whether the customer has dependents.      |

### Tenure and Services

| Column             | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `tenure`           | Number of months the customer has remained with the service. |
| `PhoneService`     | Indicates whether the customer has phone service.            |
| `MultipleLines`    | Indicates the customer's multiple-line service status.       |
| `InternetService`  | Type of Internet service.                                    |
| `OnlineSecurity`   | Online security service status.                              |
| `OnlineBackup`     | Online backup service status.                                |
| `DeviceProtection` | Device protection service status.                            |
| `TechSupport`      | Technical support service status.                            |
| `StreamingTV`      | Streaming television service status.                         |
| `StreamingMovies`  | Streaming movie service status.                              |

### Account and Billing

| Column             | Description                                            |
|--------------------|--------------------------------------------------------|
| `Contract`         | Customer contract type.                                |
| `PaperlessBilling` | Indicates whether the customer uses paperless billing. |
| `PaymentMethod`    | Customer payment method.                               |
| `MonthlyCharges`   | Monthly amount charged to the customer.                |
| `TotalCharges`     | Total amount charged to the customer.                  |

### Target

| Column  | Description                                        |
|---------|----------------------------------------------------|
| `Churn` | Binary churn outcome represented as `Yes` or `No`. |

The dataset documentation describes the services, account information, demographic information, and churn field as the
primary categories of information available for each customer.

## Project Data Preparation

The original source data is prepared for this project before modeling.

The project workflow separates:

1. Raw external data
2. Project training data
3. Project test data
4. Derived/processed data

The target variable is converted into a binary representation for machine-learning workflows:

```text
Yes → 1
No  → 0
```

The customer identifier is retained where needed for identification and prediction outputs but is not used as a
predictive feature.

Additional features are created by the project's feature-engineering workflow. These are derived from the original
customer attributes and are documented through the modeling implementation.

## Project Data Folder

The repository follows this structure:

```text
data/
├── raw/
│   ├── train.csv
│   └── test.csv
│
└── processed/
```

### `data/raw/`

Contains the input datasets used by the project.

```text
data/raw/
├── train.csv
└── test.csv
```

These files are expected to be available locally when running the notebooks.

The raw data is intentionally not redistributed with the repository.

### `data/processed/`

Reserved for derived datasets created during preprocessing or feature-engineering workflows.

Processed files should be treated as generated project artifacts rather than original source data.

## Training and Test Data

The modeling workflow expects:

```text
train.csv
```

to contain the target column:

```text
Churn
```

The test dataset is used for generating customer-level churn probability predictions.

The exact number of rows in the project-specific `train.csv` and `test.csv` depends on how the source data was prepared
for the project. The notebooks calculate their actual dimensions at runtime rather than relying on hard-coded values.

## Data Flow

```text
External Dataset
      │
      ▼
data/raw/
      │
      ├── train.csv
      └── test.csv
      │
      ▼
Data Validation
      │
      ▼
Cleaning & Feature Engineering
      │
      ▼
Modeling Pipeline
      │
      ▼
Predictions / Analysis
      │
      ▼
artifacts/
```

## Data Quality Considerations

The dataset should be validated before modeling to confirm:

* expected columns are present;
* the target variable contains valid values;
* customer identifiers are handled correctly;
* numerical fields are represented using appropriate data types;
* categorical fields contain expected categories;
* missing or malformed values are handled consistently.

The project includes validation logic in:

```text
src/validate_data.py
```

## Feature Engineering

The project derives customer-level signals from the original attributes.

Examples include:

* lifetime spending relative to tenure;
* monthly cost exposure;
* service adoption count;
* service adoption rate;
* contract stability;
* early lifecycle and rolling-contract status;
* accumulated customer value;
* electronic payment behavior.

These variables are project-derived features and are not part of the original external dataset.

## Reproducibility

To reproduce the project:

1. Obtain the dataset from the documented source.
2. Place the required files under `data/raw/`.
3. Follow the instructions in [`usage.md`](usage.md).
4. Run the notebooks from top to bottom.
5. Allow the notebooks and source modules to calculate dataset dimensions, validation results, model performance, and
   predictions at runtime.

No model performance values are stored as predetermined claims in this documentation.

## Data Responsibility

This project is intended for educational, analytical, and portfolio purposes.

The dataset represents a fictional telecommunications business scenario. It should not be interpreted as a source of
real-world customer records or as evidence about the behavior of any particular real customer.

The repository's code and documentation are the author's project work; the underlying dataset remains subject to its
original source terms and rights.
