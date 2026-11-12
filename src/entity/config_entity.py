# src/entity/config_entity.py
"""
Data classes representing configuration entities for the pipeline components.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path
    data_ingestion_dir: Path
    ingested_raw_data_path: Path
    train_data_path: Path
    test_data_path: Path
    test_size: float
    random_state: int

