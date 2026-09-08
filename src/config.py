import os
from pathlib import Path

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Storage Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

def ensure_directories_exist() -> None:
    """Ensures that all required data directories exist on the filesystem."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# Default Pipeline Configurations
DEFAULT_BASE_CURRENCY = os.getenv("FX_BASE_CURRENCY", "USD")
DEFAULT_TARGET_SYMBOLS = ["EUR", "GBP", "JPY", "CAD", "AUD"]