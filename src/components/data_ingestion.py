# src/components/data_ingestion.py
"""
Data Ingestion Component for Ecom-QueryBot.
Reads raw customer support query dataset, creates artifact directories,
saves a copy of raw data, splits data into train/test sets, and persists them.
"""
import sys
from pathlib import Path
from sklearn.model_selection import train_test_split

# Ensure project root is available in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logger import logger
from src.exception import MyException
from src.utils.common import create_dir, read_csv, load_csv
from configuration.configs import DataConfig
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:
    """
    Component responsible for ingesting raw data and generating train/test splits.
    """

    def __init__(self, config: DataIngestionConfig = None):
        try:
            if config is None:
               
                data_config = DataConfig()
                self.config = data_config.data_ingession_config()
            else:
                self.config = config

            logger.info("DataIngestion component initialized with configuration.")
        except Exception as e:
            logger.error(f"Error during DataIngestion initialization: {e}")
            raise MyException(e, sys)

    def initiate_data_ingestion(self):
       
        logger.info(">>>>> Starting Data Ingestion Stage <<<<<")
        try:
            # 1. Read raw CSV using common utility function
            logger.info(f"Reading raw data from: {self.config.raw_data_path}")
            df = read_csv(self.config.raw_data_path)
            logger.info(f"Raw data successfully read. Dataset shape: {df.shape}")

            # 2. Create directory for data ingestion artifacts
            logger.info(f"Ensuring artifact directory exists: {self.config.data_ingestion_dir}")
            create_dir(self.config.data_ingestion_dir)

            # 3. Save raw data copy in artifacts directory
            logger.info(f"Exporting raw data backup to: {self.config.ingested_raw_data_path}")
            load_csv(self.config.ingested_raw_data_path, df)

            # 4. Perform train-test split
            logger.info(
                f"Splitting dataset: test_size={self.config.test_size}, "
                f"random_state={self.config.random_state}"
            )
            train_set, test_set = train_test_split(
                df,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
            )
            logger.info(f"Train split shape: {train_set.shape} | Test split shape: {test_set.shape}")

            # 5. Save train and test splits to artifacts directory
            logger.info(f"Saving train dataset to: {self.config.train_data_path}")
            load_csv(self.config.train_data_path, train_set)

            logger.info(f"Saving test dataset to: {self.config.test_data_path}")
            load_csv(self.config.test_data_path, test_set)

            logger.info(">>>>> Data Ingestion Stage Completed Successfully <<<<<")

            return self.config.train_data_path, self.config.test_data_path

        except Exception as e:
            logger.error(f"Exception occurred in Data Ingestion: {str(e)}")
            raise MyException(e, sys)


if __name__ == "__main__":
    try:
        # Initialize configuration using DataConfig and dataingession_config
        config_manager = DataConfig()
        ingestion_config = config_manager.dataingession_config()

        # Run Data Ingestion component
        ingestion = DataIngestion(config=ingestion_config)
        train_file_path, test_file_path = ingestion.initiate_data_ingestion()

        print(f"Data Ingestion successfully executed!")
        print(f"Train file path: {train_file_path}")
        print(f"Test file path:  {test_file_path}")

    except Exception as e:
        print(f"Data Ingestion execution failed: {e}")
