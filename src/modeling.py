from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier

from .config import CV_SPLITS, RANDOM_STATE
from .features import RetentionFeatureBuilder


def make_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = X.select_dtypes(exclude="number").columns.tolist()

    numeric_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    min_frequency=5,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        [
            ("numeric", numeric_pipe, numeric),
            ("categorical", categorical_pipe, categorical),
        ],
        remainder="drop",
    )


def build_candidates(X: pd.DataFrame) -> dict[str, Pipeline]:
    preprocessor = make_preprocessor(X)

    return {
        "logistic_regression": Pipeline(
            [
                ("features", RetentionFeatureBuilder()),
                ("preprocessor", clone(preprocessor)),
                (
                    "model",
                    LogisticRegression(
                        max_iter=1200,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("features", RetentionFeatureBuilder()),
                ("preprocessor", clone(preprocessor)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=350,
                        min_samples_leaf=5,
                        max_features="sqrt",
                        class_weight="balanced_subsample",
                        n_jobs=-1,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "lightgbm": Pipeline(
            [
                ("features", RetentionFeatureBuilder()),
                ("preprocessor", clone(preprocessor)),
                (
                    "model",
                    LGBMClassifier(
                        n_estimators=500,
                        learning_rate=0.035,
                        num_leaves=31,
                        subsample=0.85,
                        colsample_bytree=0.85,
                        reg_lambda=1.0,
                        objective="binary",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                        verbosity=-1,
                    ),
                ),
            ]
        ),
    }


def evaluate_predictions(y_true, probabilities, threshold=0.5):
    labels = (probabilities >= threshold).astype(int)

    return {
        "roc_auc": roc_auc_score(y_true, probabilities),
        "average_precision": average_precision_score(
            y_true, probabilities
        ),
        "log_loss": log_loss(y_true, probabilities),
        "accuracy_at_0_5": accuracy_score(y_true, labels),
    }


def cross_validate_candidates(X, y, candidates, cv):
    from sklearn.model_selection import StratifiedKFold

    splitter = StratifiedKFold(
        n_splits=cv,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    rows = []

    for model_name, estimator in candidates.items():
        fold_scores = []

        for fold_number, (train_idx, valid_idx) in enumerate(
            splitter.split(X, y),
            start=1,
        ):
            model = clone(estimator)

            X_train = X.iloc[train_idx]
            X_valid = X.iloc[valid_idx]
            y_train = y.iloc[train_idx]
            y_valid = y.iloc[valid_idx]

            model.fit(X_train, y_train)

            probabilities = model.predict_proba(X_valid)[:, 1]
            metrics = evaluate_predictions(y_valid, probabilities)

            fold_scores.append(metrics["roc_auc"])

            rows.append(
                {
                    "model": model_name,
                    "fold": fold_number,
                    **metrics,
                }
            )

        rows.append(
            {
                "model": model_name,
                "fold": "mean",
                "roc_auc": float(np.mean(fold_scores)),
                "average_precision": np.nan,
                "log_loss": np.nan,
                "accuracy_at_0_5": np.nan,
            }
        )

    return pd.DataFrame(rows)