from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class RetentionFeatureBuilder(BaseEstimator, TransformerMixin):
    """Create retention-oriented features from the customer table.

    The transformer deliberately keeps feature construction inside the sklearn
    workflow so transformations applied during validation are based only on
    information available to the corresponding training fold.
    """

    def __init__(self):
        self.numeric_fill_values_: dict[str, float] = {}
        self.categorical_fill_values_: dict[str, str] = {}

    def fit(self, X, y=None):
        X = X.copy()

        numeric_columns = X.select_dtypes(include=np.number).columns
        for column in numeric_columns:
            self.numeric_fill_values_[column] = float(X[column].median())

        categorical_columns = X.select_dtypes(exclude=np.number).columns
        for column in categorical_columns:
            mode = X[column].mode(dropna=True)
            self.categorical_fill_values_[column] = (
                str(mode.iloc[0]) if not mode.empty else "Unknown"
            )

        return self

    @staticmethod
    def _numeric(series: pd.Series) -> pd.Series:
        return pd.to_numeric(series, errors="coerce")

    def transform(self, X):
        X = X.copy()

        for column, value in self.numeric_fill_values_.items():
            if column in X.columns:
                X[column] = self._numeric(X[column]).fillna(value)

        for column, value in self.categorical_fill_values_.items():
            if column in X.columns:
                X[column] = X[column].astype("string").fillna(value)

        if "TotalCharges" in X.columns:
            X["TotalCharges"] = self._numeric(X["TotalCharges"]).fillna(0)

        if {"TotalCharges", "tenure"}.issubset(X.columns):
            tenure = self._numeric(X["tenure"]).clip(lower=0)
            X["LifetimeSpendPerTenure"] = X["TotalCharges"] / (tenure + 1.0)

        if {"MonthlyCharges", "tenure"}.issubset(X.columns):
            tenure = self._numeric(X["tenure"]).clip(lower=0)
            X["MonthlyCostExposure"] = X["MonthlyCharges"] * np.log1p(tenure)

        service_columns = [
            "PhoneService",
            "MultipleLines",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
        ]

        present_services = [
            column for column in service_columns if column in X.columns
        ]

        if present_services:
            service_matrix = X[present_services].apply(
                lambda column: column.astype("string")
                .str.strip()
                .str.lower()
                .map({"yes": 1, "no": 0})
                .fillna(0)
            )
            X["ServiceAdoptionCount"] = service_matrix.sum(axis=1)
            X["ServiceAdoptionRate"] = (
                X["ServiceAdoptionCount"] / len(present_services)
            )

        if {"Contract", "tenure"}.issubset(X.columns):
            contract = X["Contract"].astype("string").str.strip().str.lower()
            tenure = self._numeric(X["tenure"]).clip(lower=0)

            X["IsRollingContract"] = contract.eq("month-to-month").astype(int)
            X["IsLongContract"] = contract.isin(
                ["one year", "two year"]
            ).astype(int)
            X["EarlyLifecycleRolling"] = (
                X["IsRollingContract"] * (tenure < 12).astype(int)
            )

        if {"MonthlyCharges", "TotalCharges"}.issubset(X.columns):
            monthly = self._numeric(X["MonthlyCharges"]).clip(lower=0)
            total = self._numeric(X["TotalCharges"]).clip(lower=0)

            X["AccumulatedValueRatio"] = total / (monthly + 1.0)

        if {"PaymentMethod"}.issubset(X.columns):
            payment = (
                X["PaymentMethod"]
                .astype("string")
                .str.strip()
                .str.lower()
            )
            X["UsesElectronicPayment"] = payment.eq("electronic check").astype(int)

        return X


class TabularPreprocessor(BaseEstimator, TransformerMixin):
    """Convert engineered mixed-type data into a numeric model matrix."""

    def __init__(self):
        self.numeric_columns_: list[str] = []
        self.categorical_columns_: list[str] = []
        self.category_maps_: dict[str, dict[str, int]] = {}
        self.medians_: dict[str, float] = {}

    def fit(self, X, y=None):
        X = X.copy()

        self.numeric_columns_ = X.select_dtypes(
            include=np.number
        ).columns.tolist()

        self.categorical_columns_ = X.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        for column in self.numeric_columns_:
            self.medians_[column] = float(
                pd.to_numeric(X[column], errors="coerce").median()
            )

        for column in self.categorical_columns_:
            values = (
                X[column]
                .astype("string")
                .fillna("Unknown")
                .astype(str)
                .unique()
                .tolist()
            )
            self.category_maps_[column] = {
                value: index for index, value in enumerate(sorted(values))
            }

        return self

    def transform(self, X):
        X = X.copy()

        result = pd.DataFrame(index=X.index)

        for column in self.numeric_columns_:
            values = pd.to_numeric(
                X[column], errors="coerce"
            ).fillna(self.medians_[column])
            result[column] = values.astype(np.float32)

        for column in self.categorical_columns_:
            values = (
                X[column]
                .astype("string")
                .fillna("Unknown")
                .astype(str)
            )
            result[column] = (
                values.map(self.category_maps_[column])
                .fillna(-1)
                .astype(np.float32)
            )

        return result