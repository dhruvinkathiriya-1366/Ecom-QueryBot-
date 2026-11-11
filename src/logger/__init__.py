import logging
import os
from pathlib import Path
from datetime import datetime



logger = logging.getLogger("Ecom-quaryBoat")
logger.setLevel(logging.INFO)
logger.propagate = False


formatter = logging.Formatter(
    "[%(asctime)s] "
    "%(levelname)s "
    "[%(filename)s:%(lineno)d] "
    "%(funcName)s() - "
    "%(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


try:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    print("Project root path:", PROJECT_ROOT)
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    LOG_FILE = LOG_DIR / f"{current_time}.log"
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except (OSError, PermissionError):
    # Read-only filesystem (e.g. Vercel serverless) — console logging only
    pass
