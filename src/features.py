import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer-level features for churn modeling."""

    data = df.copy()

    # Financial exposure relative to customer tenure.
    data["LifetimeSpendPerTenure"] = (
            data["TotalCharges"]
            / data["tenure"].clip(lower=1)
    )

    # Monthly charges relative to accumulated customer value.
    data["MonthlyCostExposure"] = (
            data["MonthlyCharges"]
            / data["TotalCharges"].clip(lower=1)
    )

    # Count adopted optional services.
    service_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]

    data["ServiceAdoptionCount"] = (
            data[service_columns] == "Yes"
    ).sum(axis=1)

    data["ServiceAdoptionRate"] = (
            data["ServiceAdoptionCount"] / len(service_columns)
    )

    # Contract structure.
    data["IsRollingContract"] = (
            data["Contract"] == "Month-to-month"
    ).astype(int)

    data["IsLongContract"] = (
            data["Contract"] == "Two year"
    ).astype(int)

    # Customers early in their lifecycle and still on a rolling contract.
    data["EarlyLifecycleRolling"] = (
            (data["tenure"] <= 12)
            & (data["Contract"] == "Month-to-month")
    ).astype(int)

    # Relationship between accumulated spend and monthly cost.
    data["AccumulatedValueRatio"] = (
            data["TotalCharges"]
            / (data["MonthlyCharges"].clip(lower=1) * data["tenure"].clip(lower=1))
    )

    # Payment behavior.
    data["UsesElectronicPayment"] = (
            data["PaymentMethod"] == "Electronic check"
    ).astype(int)

    return data
