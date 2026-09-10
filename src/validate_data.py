from __future__ import annotations

import sys

import pandas as pd

from .config import ID_COLUMN, TARGET_COLUMN, TEST_PATH, TRAIN_PATH


def main() -> int:
    if not TRAIN_PATH.exists():
        print(f"Missing training file: {TRAIN_PATH}")
        return 1

    if not TEST_PATH.exists():
        print(f"Missing test file: {TEST_PATH}")
        return 1

    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)

    problems = []

    if TARGET_COLUMN not in train.columns:
        problems.append(
            f"Training data does not contain target column '{TARGET_COLUMN}'."
        )

    if ID_COLUMN not in train.columns:
        problems.append(
            f"Training data does not contain identifier '{ID_COLUMN}'."
        )

    if ID_COLUMN not in test.columns:
        problems.append(
            f"Test data does not contain identifier '{ID_COLUMN}'."
        )

    if TARGET_COLUMN in train.columns:
        values = set(
            train[TARGET_COLUMN]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
        )
        expected = {"yes", "no", "0", "1"}
        unexpected = values - expected

        if unexpected:
            problems.append(
                "Unexpected target values: "
                + ", ".join(sorted(unexpected))
            )

    train_features = set(train.columns) - {TARGET_COLUMN}
    test_features = set(test.columns)

    missing_from_test = train_features - test_features
    unexpected_in_test = test_features - train_features

    if missing_from_test:
        problems.append(
            "Columns present in training but missing from test: "
            + ", ".join(sorted(missing_from_test))
        )

    if unexpected_in_test:
        problems.append(
            "Columns present in test but absent from training: "
            + ", ".join(sorted(unexpected_in_test))
        )

    if ID_COLUMN in train.columns:
        duplicate_ids = int(train[ID_COLUMN].duplicated().sum())
        if duplicate_ids:
            print(
                f"Warning: training data contains {duplicate_ids} "
                "duplicate identifiers."
            )

    print(f"Training shape: {train.shape}")
    print(f"Test shape: {test.shape}")
    print(f"Training missing cells: {int(train.isna().sum().sum())}")
    print(f"Test missing cells: {int(test.isna().sum().sum())}")

    if problems:
        print("\nValidation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("\nSchema validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())