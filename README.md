# 📈 FX Macro Data Pipeline (`fx-macro-pipeline`)

A simple macroeconomic data pipeline built in Python. Fetches foreign exchange rates, performs vectorized window calculations, and stores datasets in multi-level Hive-partitioned Parquet files.

## 🏗️ Architecture & Data Flow

```text
┌────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────────────┐
│  Frankfurter   │ ──► │   FXApiClient    │ ──► │   FXTransformer   │ ──► │ ParquetStorageEngine │
│  REST API      │     │(httpx + Pydantic)│     │  (Polars Vector)  │     │  (PyArrow / Parquet) │
└────────────────┘     └──────────────────┘     └───────────────────┘     └──────────────────────┘
                                                                                     │
                                                                                     ▼
                                                                        data/processed/
                                                                        └── base_currency=USD/
                                                                            └── target_currency=EUR/
                                                                                └── data.parquet
```

### Key Features

Robust Ingestion: Async/sync httpx client wrapped with Pydantic runtime schema validation.

High-Performance ETL: Polars vectorized transformations computing daily % change and 7/30-day rolling averages.

Granular Storage: Hive-style multi-level directory partitioning (base_currency → target_currency) with PyArrow.

Path-Safe Execution: Dynamic path resolution via pathlib for cross-platform reliability.

#### Quick Start
1. Installation
-- Bash --
git clone [https://github.com/Sonicollin/fx-macro-pipeline.git](https://github.com/Sonicollin/fx-macro-pipeline.git)
cd fx-macro-pipeline
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

2. Run Pipeline
-- Bash --
*Run with default 30-day window*
python main.py

*Custom date range with multi-level partitioning*
python main.py --start-date 2026-01-01 --end-date 2026-03-01 --base USD --symbols EUR JPY GBP --partition

##### Tech Stack
Language: Python 3.12+
HTTP Client: httpx
Data Validation: Pydantic v2
Data Transformation and Storage: Polars & PyArrow
Testing: pytest