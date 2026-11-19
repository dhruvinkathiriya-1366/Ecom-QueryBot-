# src/components/data_preprocess.py
"""
Data Preprocessing Component for Ecom-QueryBot.
Responsible for cleaning instruction text, extracting intent labels,
and returning/persisting preprocessed train and test DataFrames.
"""         
import sys
from pathlib import Path
from pandas import DataFrame
import spacy as sp
import re 

# Ensure project root is available in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logger import logger
from src.exception import MyException
from src.utils.common import create_dir, read_csv, load_csv
from configuration.configs import DataConfig
from src.entity.config_entity import DataPreprocessingConfig, DataIngestionConfig


class DataPreprocessing:
    """
    Component responsible for preprocessing text instructions and intent labels.
    """

    def __init__(
        self,
        config: DataPreprocessingConfig = None,
        ingestion_config: DataIngestionConfig = None,
    ):
        try:
            data_config = DataConfig()
            self.config = config if config else data_config.data_preprocessing_config()
            self.ingestion_config = (
                ingestion_config if ingestion_config else data_config.data_ingestion_config()
            )
            self.nlp = sp.load("en_core_web_sm", disable=["parser", "ner"])
            
            logger.info("DataPreprocessing component initialized with configuration.")
        except Exception as e:
            logger.error(f"Error during DataPreprocessing initialization: {e}")
            raise MyException(e, sys)

    def preprocessing(self, df: DataFrame) -> DataFrame:
        """
        Preprocesses instructions by standardizing slot placeholders,
        lemmatizing and tokenizing text, and filters the DataFrame
        to retain only ['instruction', 'intent'].
        """
        try:
            cleane_instruction = []
            logger.info("Starting instruction preprocessing...")
            
            # Standardize slot placeholders: e.g. {{Order Number}} -> Order_Number
            df['instruction'] = df['instruction'].astype(str).str.replace(
                r"\{\{(.*?)\}\}",
                lambda m: m.group(1).strip().replace(" ", "_"),
                regex=True
            )

            # Process with spaCy pipe
            for doc in self.nlp.pipe(df['instruction'], batch_size=500):
                tokens = [
                    token.lemma_.lower()
                    for token in doc
                    if not token.is_punct and not token.is_space
                ]
                cleane_instruction.append(tokens)

            logger.info("Instruction preprocessing completed.")
            df['instruction'] = cleane_instruction

            # Filter DataFrame to keep preprocessed instruction with intent
            df = df[['instruction', 'intent']]
            return df

        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            raise MyException(e, sys)

    # Aliases for backward compatibility
    def instruction_preprocessing(self, df: DataFrame) -> DataFrame:
        return self.preprocessing(df)

    def intent_preprocessing(self, df: DataFrame) -> DataFrame:
        return df

    def initiate_data_preprocessing(
        self,
        train_path: Path = None,
        test_path: Path = None,
    ) -> tuple[DataFrame, DataFrame]:
        """
        Initiates the data preprocessing pipeline:
        1. Ensures artifact directory exists.
        2. Loads train and test datasets.
        3. Preprocesses instructions and retains intent column.
        4. Saves preprocessed datasets to CSV.
        5. Returns preprocessed train and test DataFrames.

        Returns:
            tuple[DataFrame, DataFrame]: (train_df, test_df) containing ['instruction', 'intent']
        """
        logger.info(">>>>> Starting Data Preprocessing Stage <<<<<")
        try:
            train_path = train_path or self.ingestion_config.train_data_path
            test_path = test_path or self.ingestion_config.test_data_path

            # 1. Ensure artifact directory exists
            logger.info(f"Ensuring preprocessing artifact directory exists: {self.config.data_preprocessing_dir}")
            create_dir(self.config.data_preprocessing_dir)

            # 2. Read train and test data
            logger.info(f"Loading train data from: {train_path}")
            train_df = read_csv(train_path)

            logger.info(f"Loading test data from: {test_path}")
            test_df = read_csv(test_path)
        
            # 3. Apply preprocessing to both train and test sets
            train_df = self.preprocessing(train_df)
            test_df = self.preprocessing(test_df)
        
            # 4. Save preprocessed datasets as CSV files in artifacts directory
            logger.info(
                f"Saving preprocessed train data to: {self.config.preprocessed_train_data_path}"
            )
            load_csv(self.config.preprocessed_train_data_path, train_df)
        
            logger.info(
                f"Saving preprocessed test data to: {self.config.preprocessed_test_data_path}"
            )
            load_csv(self.config.preprocessed_test_data_path, test_df)

            logger.info(">>>>> Data Preprocessing Stage Completed Successfully <<<<<")

            # Return the preprocessed DataFrames containing ['instruction', 'intent']
            return train_df, test_df

        except Exception as e:
            logger.error(f"Error in initiate_data_preprocessing: {e}")
            raise MyException(e, sys)


if __name__ == "__main__":
    try:
        preprocessing = DataPreprocessing()
        train_df, test_df = preprocessing.initiate_data_preprocessing()
        print("Data Preprocessing successfully executed!")
        print(f"Train DataFrame shape: {train_df.shape}")
        print(f"Test DataFrame shape:  {test_df.shape}")
        print("\nPreprocessed Train DataFrame sample (instruction & intent):")
        print(train_df.head())
    except Exception as e:
        print(f"Data Preprocessing execution failed: {e}")
