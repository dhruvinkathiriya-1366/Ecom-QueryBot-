# configuration/setting.py
"""
Configuration settings and constants for the Ecom-QueryBot project.
Contains base parameters and file names required for data ingestion and pipeline execution.
"""

# Directory Names
DATA_DIR_NAME = "data"
RAW_DATA_DIR_NAME = "raw"
RAW_DATA_FILE_NAME = "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"

ARTIFACTS_DIR_NAME = "artifacts"
DATA_INGESTION_DIR_NAME = "data_ingestion"

# Data Ingestion Output File Names
RAW_DATA_COPY_FILE_NAME = "raw.csv"
TRAIN_DATA_FILE_NAME = "train.csv"
TEST_DATA_FILE_NAME = "test.csv"

# Split Parameters for Data Ingestion
TEST_SIZE = 0.2
RANDOM_STATE = 42

