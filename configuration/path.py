# configuration/path.py
"""
Defines and resolves all filesystem paths for the Ecom-QueryBot project
by combining base settings from configuration/setting.py with the project root.
"""
import sys
from pathlib import Path

# Resolve project root (parent directory of configuration)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configuration.setting import (
    DATA_DIR_NAME,
    RAW_DATA_DIR_NAME,
    RAW_DATA_FILE_NAME,
    ARTIFACTS_DIR_NAME,
    DATA_INGESTION_DIR_NAME,
    RAW_DATA_COPY_FILE_NAME,
    TRAIN_DATA_FILE_NAME,
    TEST_DATA_FILE_NAME,
)

# Raw Data Source Path
RAW_DATA_PATH = PROJECT_ROOT / DATA_DIR_NAME / RAW_DATA_DIR_NAME / RAW_DATA_FILE_NAME

# Artifacts Directory Paths
ARTIFACTS_DIR = PROJECT_ROOT / ARTIFACTS_DIR_NAME
DATA_INGESTION_DIR = ARTIFACTS_DIR / DATA_INGESTION_DIR_NAME

# Data Ingestion Output Paths
INGESTED_RAW_DATA_PATH = DATA_INGESTION_DIR / RAW_DATA_COPY_FILE_NAME
TRAIN_DATA_PATH = DATA_INGESTION_DIR / TRAIN_DATA_FILE_NAME
TEST_DATA_PATH = DATA_INGESTION_DIR / TEST_DATA_FILE_NAME

