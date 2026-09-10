from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"

TRAIN_PATH = RAW_DIR / "train.csv"
TEST_PATH = RAW_DIR / "test.csv"

TARGET_COLUMN = "Churn"
ID_COLUMN = "id"

RANDOM_STATE = 2026
CV_SPLITS = 5

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
