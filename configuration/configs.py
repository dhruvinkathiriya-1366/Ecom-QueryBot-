# configuration/configs.py
"""
Configuration manager that combines settings and paths to supply
component-specific configuration objects.
"""
import sys
from pathlib import Path

# Ensure project root is available in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configuration.setting import TEST_SIZE, RANDOM_STATE
from configuration.path import (
    RAW_DATA_PATH,
    DATA_INGESTION_DIR,
    INGESTED_RAW_DATA_PATH,
    TRAIN_DATA_PATH,
    TEST_DATA_PATH,
)
from src.entity.config_entity import DataIngestionConfig
from src.logger import logger
from src.exception import MyException


class DataConfig:
    """
    Configuration manager for creating configuration entities required by pipeline components.
    """

    def __init__(self):
        self.raw_data_path: Path = RAW_DATA_PATH
        self.data_ingestion_dir: Path = DATA_INGESTION_DIR
        self.ingested_raw_data_path: Path = INGESTED_RAW_DATA_PATH
        self.train_data_path: Path = TRAIN_DATA_PATH
        self.test_data_path: Path = TEST_DATA_PATH
        self.test_size: float = TEST_SIZE
        self.random_state: int = RANDOM_STATE

    def dataingession_config(self) -> DataIngestionConfig:
        """
        Builds and returns the DataIngestionConfig entity containing
        all required paths and parameters for data ingestion.
        """
        try:
            logger.info("Initializing DataIngestionConfig...")
            data_ingestion_config = DataIngestionConfig(
                raw_data_path=self.raw_data_path,
                data_ingestion_dir=self.data_ingestion_dir,
                ingested_raw_data_path=self.ingested_raw_data_path,
                train_data_path=self.train_data_path,
                test_data_path=self.test_data_path,
                test_size=self.test_size,
                random_state=self.random_state,
            )
            logger.info("DataIngestionConfig created successfully.")
            return data_ingestion_config

        except Exception as e:
            logger.error(f"Error while creating DataIngestionConfig: {e}")
            raise MyException(e, sys)

    # Aliases to accommodate alternative conventions (with underscore and standard spelling)
    def data_ingession_config(self) -> DataIngestionConfig:
        return self.dataingession_config()

    def data_ingestion_config(self) -> DataIngestionConfig:
        return self.dataingession_config()
