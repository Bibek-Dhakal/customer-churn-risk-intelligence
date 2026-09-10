import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
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


def build_preprocessor(
        X: pd.DataFrame,
) -> ColumnTransformer:
    """Build preprocessing for numerical and categorical features."""

    numeric_features = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            (
                "categorical",
                categorical_pipeline,
                categorical_features,
            ),
        ],
        remainder="drop",
    )


def build_candidates(
        X: pd.DataFrame,
        random_state: int = 42,
) -> dict:
    """Build candidate churn classification pipelines."""

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=random_state,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=400,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=400,
            learning_rate=0.03,
            num_leaves=31,
            subsample=0.85,
            colsample_bytree=0.85,
            class_weight="balanced",
            random_state=random_state,
            verbosity=-1,
        ),
    }

    pipelines = {}

    for name, model in models.items():
        pipelines[name] = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(X)),
                ("model", model),
            ]
        )

    return pipelines


def evaluate_predictions(
        y_true,
        probabilities,
        threshold: float = 0.5,
) -> dict:
    """Calculate model evaluation metrics."""

    predictions = (
            np.asarray(probabilities) >= threshold
    ).astype(int)

    return {
        "ROC_AUC": roc_auc_score(y_true, probabilities),
        "Average_Precision": average_precision_score(
            y_true,
            probabilities,
        ),
        "Log_Loss": log_loss(
            y_true,
            probabilities,
        ),
        "Accuracy_At_0.5": accuracy_score(
            y_true,
            predictions,
        ),
    }
