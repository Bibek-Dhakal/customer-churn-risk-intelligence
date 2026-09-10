from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data paths
RAW_DATA_PATH = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

# Output paths
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

PREDICTIONS_PATH = ARTIFACTS_DIR / "predictions.csv"
MODEL_COMPARISON_PATH = ARTIFACTS_DIR / "model_comparison.csv"
SELECTED_MODEL_PATH = ARTIFACTS_DIR / "selected_model.joblib"
RUN_METADATA_PATH = ARTIFACTS_DIR / "run_metadata.json"

# Reproducibility
RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

# Target / identifier
TARGET_COLUMN = "Churn"
ID_COLUMN = "customerID"
