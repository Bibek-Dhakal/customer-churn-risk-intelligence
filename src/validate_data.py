from pathlib import Path

import pandas as pd

EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]


def load_and_validate_data(data_path: Path) -> pd.DataFrame:
    """Load the raw customer churn dataset and validate its structure."""

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}\n"
            "Place the downloaded CSV inside data/raw/."
        )

    df = pd.read_csv(data_path)

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing expected columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Dataset contains no rows.")

    if df["customerID"].duplicated().any():
        raise ValueError("Duplicate customerID values detected.")

    return df


def prepare_target(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the target column and convert it to binary values."""

    df = df.copy()

    df["Churn"] = (
        df["Churn"]
        .astype(str)
        .str.strip()
        .map({"No": 0, "Yes": 1})
    )

    if df["Churn"].isna().any():
        raise ValueError(
            "Unexpected values found in Churn column."
        )

    return df


def prepare_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric columns to appropriate numeric types."""

    df = df.copy()

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce",
    )

    if df["TotalCharges"].isna().any():
        # Blank TotalCharges values occur for customers with very short tenure.
        # Fill them conservatively using MonthlyCharges.
        df["TotalCharges"] = df["TotalCharges"].fillna(
            df["MonthlyCharges"]
        )

    return df


def load_prepared_data(data_path: Path) -> pd.DataFrame:
    """Load and prepare the complete raw dataset."""

    df = load_and_validate_data(data_path)
    df = prepare_target(df)
    df = prepare_numeric_columns(df)

    return df


if __name__ == "__main__":
    from src.config import RAW_DATA_PATH

    data = load_prepared_data(RAW_DATA_PATH)

    print("Data validation successful.")
    print(f"Rows: {data.shape[0]:,}")
    print(f"Columns: {data.shape[1]}")
    print(f"Churn rate: {data['Churn'].mean():.2%}")
