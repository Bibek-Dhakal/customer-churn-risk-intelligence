from __future__ import annotations

import json

import joblib
import pandas as pd

from .config import (
    ARTIFACT_DIR,
    ID_COLUMN,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_PATH,
    TRAIN_PATH,
    CV_SPLITS,
)
from .modeling import build_candidates, cross_validate_candidates


def normalize_target(series: pd.Series) -> pd.Series:
    values = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

    mapping = {
        "yes": 1,
        "no": 0,
        "1": 1,
        "0": 0,
    }

    converted = values.map(mapping)

    if converted.isna().any():
        bad = sorted(values[converted.isna()].unique())
        raise ValueError(
            f"Unsupported target values: {bad}"
        )

    return converted.astype(int)


def main():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)

    y = normalize_target(train[TARGET_COLUMN])

    X = train.drop(columns=[TARGET_COLUMN])
    X_test = test.copy()

    if ID_COLUMN in X.columns:
        X = X.drop(columns=[ID_COLUMN])

    if ID_COLUMN in X_test.columns:
        X_test = X_test.drop(columns=[ID_COLUMN])

    candidates = build_candidates(X)

    comparison = cross_validate_candidates(
        X=X,
        y=y,
        candidates=candidates,
        cv=CV_SPLITS,
    )

    mean_scores = (
        comparison[comparison["fold"] == "mean"]
        .sort_values("roc_auc", ascending=False)
        .reset_index(drop=True)
    )

    if mean_scores.empty:
        raise RuntimeError("No model comparison results were produced.")

    selected_name = str(mean_scores.iloc[0]["model"])
    selected_model = candidates[selected_name]

    selected_model.fit(X, y)

    probabilities = selected_model.predict_proba(X_test)[:, 1]

    predictions = pd.DataFrame(
        {
            ID_COLUMN: test[ID_COLUMN],
            TARGET_COLUMN: probabilities,
        }
    )

    comparison.to_csv(
        ARTIFACT_DIR / "model_comparison.csv",
        index=False,
    )

    predictions.to_csv(
        ARTIFACT_DIR / "predictions.csv",
        index=False,
    )

    joblib.dump(
        selected_model,
        ARTIFACT_DIR / "selected_model.joblib",
    )

    metadata = {
        "selected_model": selected_name,
        "random_state": RANDOM_STATE,
        "cv_splits": CV_SPLITS,
        "training_rows": int(len(X)),
        "test_rows": int(len(X_test)),
        "target": TARGET_COLUMN,
    }

    (ARTIFACT_DIR / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\nModel comparison:")
    print(
        mean_scores[
            ["model", "roc_auc"]
        ].to_string(index=False)
    )

    print(f"\nSelected model: {selected_name}")
    print(
        f"Prediction file: "
        f"{ARTIFACT_DIR / 'predictions.csv'}"
    )


if __name__ == "__main__":
    main()