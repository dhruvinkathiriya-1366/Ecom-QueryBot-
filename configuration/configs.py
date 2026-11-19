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
from configuration.path import *
from src.entity.config_entity import *
from src.logger import logger
from src.exception import MyException


class DataConfig:
    """
    Configuration manager for creating configuration entities required by pipeline components.
    """

      

    def data_ingestion_config(self) -> DataIngestionConfig:
        """
        Builds and returns the DataIngestionConfig entity containing
        all required paths and parameters for data ingestion.
        """
        try:
            logger.info("Initializing DataIngestionConfig...")
            data_ingestion_config = DataIngestionConfig(
                raw_data_path=RAW_DATA_PATH,
                data_ingestion_dir=DATA_INGESTION_DIR,
                ingested_raw_data_path=INGESTED_RAW_DATA_PATH,
                train_data_path=TRAIN_DATA_PATH,
                test_data_path=TEST_DATA_PATH,
                test_size=TEST_SIZE,
                random_state=RANDOM_STATE,
            )
            logger.info("DataIngestionConfig created successfully.")
            return data_ingestion_config

        except Exception as e:
            logger.error(f"Error while creating DataIngestionConfig: {e}")
            raise MyException(e, sys)

    # Aliases to accommodate alternative conventions / spelling
    def dataingession_config(self) -> DataIngestionConfig:
        return self.data_ingestion_config()

    def data_ingession_config(self) -> DataIngestionConfig:
        return self.data_ingestion_config()

    def data_preprocessing_config(self) -> DataPreprocessingConfig:
        try:
            logger.info("Initializing DataPreprocessingConfig...")
            data_preprocessing_config = DataPreprocessingConfig(
                data_preprocessing_dir=DATA_PREPROCESSING_DIR,
                preprocessed_train_data_path=PREPROCESSED_TRAIN_DATA_PATH,
                preprocessed_test_data_path=PREPROCESSED_TEST_DATA_PATH
            )
            logger.info("DataPreprocessingConfig created successfully.")
            return data_preprocessing_config
        except Exception as e:
            logger.error(f"Error while creating DataPreprocessingConfig: {e}")
            raise MyException(e, sys)
