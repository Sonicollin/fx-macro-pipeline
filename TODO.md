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
- [ ] **Configuration Engine** (`src/config.py`)
  - [ ] Manage directory paths (`data/raw/`, `data/processed/`) and environment variables
- [ ] **Parquet Storage Engine**
  - [ ] Save processed Polars DataFrames as partitioned Parquet files (`partition_by=['base_currency', 'year']`)
- [ ] **CLI Entrypoint** (`main.py`)
  - [ ] Wire together API Client, Transformer, and Storage Engine into an end-to-end executable pipeline

---

## 📄 Phase 5: Documentation & Final Polish
- [ ] **Documentation (`README.md`)**
  - [ ] Architecture diagram & overview
  - [ ] Setup & execution guide using Poetry
- [ ] **Integration Testing**
  - [ ] Execute full pipeline test run from CLI to Parquet output