import json

import joblib
import pandas as pd
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    train_test_split,
)

from src.config import (
    ARTIFACTS_DIR,
    CV_FOLDS,
    ID_COLUMN,
    MODEL_COMPARISON_PATH,
    PREDICTIONS_PATH,
    RANDOM_STATE,
    RAW_DATA_PATH,
    RUN_METADATA_PATH,
    SELECTED_MODEL_PATH,
    TARGET_COLUMN,
    TEST_SIZE,
)
from src.features import add_features
from src.modeling import build_candidates, evaluate_predictions
from src.validate_data import load_prepared_data


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Load and prepare the single source dataset.
    # ------------------------------------------------------------------
    df = load_prepared_data(RAW_DATA_PATH)

    # ------------------------------------------------------------------
    # Feature engineering.
    # ------------------------------------------------------------------
    df = add_features(df)

    # ------------------------------------------------------------------
    # Separate identifier, target, and predictors.
    # ------------------------------------------------------------------
    customer_ids = df[ID_COLUMN].copy()

    X = df.drop(
        columns=[TARGET_COLUMN, ID_COLUMN]
    )

    y = df[TARGET_COLUMN]

    # ------------------------------------------------------------------
    # Reproducible stratified train/test split.
    # ------------------------------------------------------------------
    X_train, X_test, y_train, y_test, ids_train, ids_test = (
        train_test_split(
            X,
            y,
            customer_ids,
            test_size=TEST_SIZE,
            stratify=y,
            random_state=RANDOM_STATE,
        )
    )

    # ------------------------------------------------------------------
    # Candidate models.
    # ------------------------------------------------------------------
    candidates = build_candidates(
        X_train,
        random_state=RANDOM_STATE,
    )

    cv = StratifiedKFold(
        n_splits=CV_FOLDS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    scoring = {
        "roc_auc": "roc_auc",
        "average_precision": "average_precision",
        "neg_log_loss": "neg_log_loss",
        "accuracy": "accuracy",
    }

    results = []

    # ------------------------------------------------------------------
    # Cross-validation model comparison.
    # ------------------------------------------------------------------
    for name, pipeline in candidates.items():
        cv_results = cross_validate(
            pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )

        results.append(
            {
                "Model": name,
                "CV_ROC_AUC_Mean": cv_results[
                    "test_roc_auc"
                ].mean(),
                "CV_ROC_AUC_Std": cv_results[
                    "test_roc_auc"
                ].std(),
                "CV_Average_Precision_Mean": cv_results[
                    "test_average_precision"
                ].mean(),
                "CV_Log_Loss_Mean": -cv_results[
                    "test_neg_log_loss"
                ].mean(),
                "CV_Accuracy_Mean": cv_results[
                    "test_accuracy"
                ].mean(),
            }
        )

    comparison = (
        pd.DataFrame(results)
        .sort_values(
            "CV_ROC_AUC_Mean",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    comparison.to_csv(
        MODEL_COMPARISON_PATH,
        index=False,
    )

    # ------------------------------------------------------------------
    # Select the model with the strongest mean CV ROC-AUC.
    # ------------------------------------------------------------------
    best_model_name = comparison.iloc[0]["Model"]

    best_model = candidates[best_model_name]

    best_model.fit(
        X_train,
        y_train,
    )

    # ------------------------------------------------------------------
    # Evaluate on untouched test data.
    # ------------------------------------------------------------------
    test_probabilities = best_model.predict_proba(
        X_test
    )[:, 1]

    test_metrics = evaluate_predictions(
        y_test,
        test_probabilities,
    )

    # ------------------------------------------------------------------
    # Save customer-level predictions.
    # ------------------------------------------------------------------
    predictions = pd.DataFrame(
        {
            ID_COLUMN: ids_test.values,
            "ActualChurn": y_test.values,
            "ChurnProbability": test_probabilities,
            "PredictedChurn": (
                    test_probabilities >= 0.5
            ).astype(int),
        }
    )

    predictions.to_csv(
        PREDICTIONS_PATH,
        index=False,
    )

    # ------------------------------------------------------------------
    # Save selected model.
    # ------------------------------------------------------------------
    joblib.dump(
        best_model,
        SELECTED_MODEL_PATH,
    )

    # ------------------------------------------------------------------
    # Save run metadata.
    # ------------------------------------------------------------------
    metadata = {
        "dataset": RAW_DATA_PATH.name,
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "train_rows": int(X_train.shape[0]),
        "test_rows": int(X_test.shape[0]),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "cv_folds": CV_FOLDS,
        "target": TARGET_COLUMN,
        "selected_model": best_model_name,
        "test_metrics": {
            key: float(value)
            for key, value in test_metrics.items()
        },
    }

    with open(
            RUN_METADATA_PATH,
            "w",
            encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )

    print("\nTraining completed successfully.")
    print(f"Dataset: {RAW_DATA_PATH.name}")
    print(f"Training rows: {len(X_train):,}")
    print(f"Test rows: {len(X_test):,}")
    print(f"Selected model: {best_model_name}")

    print("\nTest metrics:")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")


if __name__ == "__main__":
    main()
