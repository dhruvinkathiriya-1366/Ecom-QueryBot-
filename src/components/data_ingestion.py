# src/components/data_ingestion.py
"""
Data Ingestion Component for Ecom-QueryBot.
Reads raw customer support query dataset, creates artifact directories,
and saves an ingested copy of raw data.
"""
import sys
from pathlib import Path
from pandas import DataFrame

# Ensure project root is available in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logger import logger
from src.exception import MyException
from src.utils.common import create_dir, read_csv, load_csv
from configuration.configs import DataConfig
from src.entity.config_entity import DataIngestionConfig, DataIngessionConfig


class DataIngestion:
    """
    Component responsible for ingesting raw data.
    """

    def __init__(self, config: DataIngestionConfig = None):
        try:
            if config is None:
                data_config = DataConfig()
                self.config = data_config.data_ingestion_config()
            else:
                self.config = config

            logger.info("DataIngestion component initialized with configuration.")
        except Exception as e:
            logger.error(f"Error during DataIngestion initialization: {e}")
            raise MyException(e, sys)

    def data_ingestion(self) -> DataFrame:
        """
        Method 1: Reads raw data from configured raw_data_path.

        Returns:
            DataFrame: Ingested raw dataset as pandas DataFrame.
        """
        try:
            logger.info(f"Reading raw data from: {self.config.raw_data_path}")
            df = read_csv(self.config.raw_data_path)
            df = df[['instruction', 'intent']]
            logger.info(f"Raw data successfully read. Dataset shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error occurred during data ingestion/reading: {e}")
            raise MyException(e, sys)

    # Alias for backward compatibility
    def data_ingession(self) -> DataFrame:
        return self.data_ingestion()

    def initiate_data_ingestion(self):
        """
        Initiates data ingestion stage:
        1. Ensures artifact directory exists.
        2. Ingests raw data.
        3. Saves ingested data copy to CSV in artifacts directory.

        Returns:
            Path: Path to ingested raw CSV file.
        """
        logger.info(">>>>> Starting Data Ingestion Stage <<<<<")
        try:
            # 1. Create directory for data ingestion artifacts
            logger.info(f"Ensuring artifact directory exists: {self.config.data_ingestion_dir}")
            create_dir(self.config.data_ingestion_dir)

            # 2. Ingest raw data
            df = self.data_ingestion()

            # 3. Save raw data copy in artifacts directory as CSV
            logger.info(f"Exporting raw data backup to: {self.config.ingested_raw_data_path}")
            load_csv(self.config.ingested_raw_data_path, df)

            logger.info(">>>>> Data Ingestion Stage Completed Successfully <<<<<")

            return self.config.ingested_raw_data_path

        except Exception as e:
            logger.error(f"Exception occurred in Data Ingestion initiation: {str(e)}")
            raise MyException(e, sys)

    # Aliases for naming flexibility and backward compatibility
    def data_ingestion_initiate(self):
        return self.initiate_data_ingestion()

    def data_ingession_intiate(self):
        return self.initiate_data_ingestion()


# Alias for backward compatibility
DataIngession = DataIngestion


if __name__ == "__main__":
    try:
        # Initialize configuration using DataConfig
        config_manager = DataConfig()
        ingestion_config = config_manager.data_ingestion_config()

        # Run Data Ingestion component
        ingestion = DataIngestion(config=ingestion_config)
        ingested_file_path = ingestion.initiate_data_ingestion()

        print("Data Ingestion successfully executed!")
        print(f"Ingested file path: {ingested_file_path}")

    except Exception as e:
        print(f"Data Ingestion execution failed: {e}")
