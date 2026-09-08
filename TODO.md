# FX-Macro-Pipeline: Project Todo List & Roadmap

## 📌 Project Overview
`fx-macro-pipeline` is an end-to-end macroeconomic data engine built with Python 3.12+, Pydantic v2, Polars, and Parquet.

---

## 🛠️ Phase 1: Environment & Schema Validation
- [x] **Setup Basic Ingestion** (`fetch_rates.py`)
  - [x] Fetch exchange rates from Frankfurter API using `httpx`
- [x] **Define Pydantic Schemas** (`src/models.py`)
  - [x] Define `FXApiResponse` model with strict type annotations
  - [x] Resolve string-to-date type coercion (disabled `strict=True` for JSON date strings)
- [x] **Test Validation Pipeline** (`test_schema.py`)
  - [x] Verify live API payload parsing and type conversion

---

## 🌐 Phase 2: Production-Grade API Client (`src/client.py`)
- [ ] **Implement `FXApiClient` Class**
  - [x] Encapsulate `httpx` requests with configurable base URL, timeout, and retry logic
  - [x] Implement robust error handling (`httpx.RequestError`, HTTP status codes)
  - [x] Integrate `FXApiResponse` Pydantic model into client return type
- [x] **Write Unit Tests for API Client** (`tests/test_client.py`)
  - [x] Test successful fetching with mocked responses
  - [x] Test client handling of non-200 responses and connection failures

---

## ⚡ Phase 3: Polars ETL & Vectorized Transformations (`src/transformer.py`)
- [ ] **Implement `FXTransformer` Class**
  - [x] Convert validated Pydantic models into flat Polars DataFrames
  - [x] Unnest and reshape nested `rates` dictionary into tabular schema (`date`, `base_currency`, `target_currency`, `exchange_rate`)
  - [x] Compute rolling aggregations (7-day & 30-day moving averages, percentage changes)
- [x] **Write Unit Tests for Transformer** (`tests/test_transformer.py`)
  - [x] Verify schema correctness, null handling, and rolling calculations

---

## 💾 Phase 4: Storage & CLI Driver (`src/config.py`, `main.py`)
- [x] **Implement Central Configuration** (`src/config.py`)
  - [x] Set up environment-agnostic filesystem paths using `pathlib`
  - [x] Configure automatic directory creation (`data/raw/`, `data/processed/`)
- [x] **Implement Parquet Storage Engine**
  - [x] Write Polars DataFrames to Parquet format using `PyArrow`
  - [x] Support hierarchical, multi-level Hive partitioning (`base_currency` -> `target_currency`)
- [x] **Write Storage Unit Tests** (`tests/test_storage.py`)
  - [x] Verify single=file and partitioned Parquet writes using `pytest` and `tmp_path` fixtures
- [x] **Built CLI Pipeline Orchestrator** (`main.py`)
  - [x] Configure `argeparse` CLI options for date ranges, base currencies, target symbols, and storage           partitioning
  - [x] Wire end-to-end flow: Extraction (`FXApiClient`) -> Transformation (`FXTransformer`) -> Load/Store    (`ParquetStorageEngine`)

---

## 📑 Phase 5: Documentation & Final Polish
- [x] **Project Hygiene & Code Quality**
  - [x] Add clear type annotations and docstrings across all modules
  - [x] Ensure test suite coverage across ingestion, transformation, and storage
- [x] **Environment & Dependency Management**
  - [x] Freeze environment dependencies into `requirements.txt`
  - [x] Provide clean, reproducible setup instructions
- [x] **Portfolio README & Architecture Documentation**
  - [x] Write a comprehensive `README.md` with architecture diagrams and CLI usage
  - [x] Add `.gitignore` safety rules