import sys
from pathlib import Path

# Add 'src' directory to Python module search path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import argparse
from datetime import date, timedelta
import sys

from config import DEFAULT_BASE_CURRENCY, DEFAULT_TARGET_SYMBOLS, PROCESSED_DATA_DIR
from client import FXApiClient, FXApiClientError
from transformer import FXTransformer
from storage import ParquetStorageEngine


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments for the FX macro pipeline."""
    # Default date values
    today = date.today() # --> Default end date
    default_start = today - timedelta(days=30) # --> Default start date 30 days ago

    parser = argparse.ArgumentParser(
        description="FX Macro Data Pipeline: Fetch, transform, and store exchange rate data."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=default_start.isoformat(),
        help=f"Start date (YYYY-MM-DD). Default: {default_start.isoformat()} (30 days ago)",     
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=today.isoformat(),
        help=f"End date (YYYY-MM-DD). Default: {today.isoformat()} (today)",
    )
    parser.add_argument(
        "--base",
        type=str,
        default=DEFAULT_BASE_CURRENCY,
        help=f"Base currency code (e.g. USD, EUR). Default: {DEFAULT_BASE_CURRENCY}",
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=DEFAULT_TARGET_SYMBOLS,
        help=f"Target currency symbols separated by space. Default: {' '.join(DEFAULT_TARGET_SYMBOLS)}",
    )
    parser.add_argument(
        "--partition",
        action="store_true",
        help="Partition Parquet output directory by target currency.",
    )
    return parser.parse_args()

def run_pipeline(
    start_date: str,
    end_date: str,
    base_currency: str,
    symbols: list[str],
    partition: bool = False, 
) -> None:
    """Executes the end-to-end ingestion, transformation, and storage workflow."""
    print("🚀 Initializing FX Macro Data Pipeline...")
    print(f"  • Date Range: {start_date} -> {end_date}")
    print(f"  • Base Currency: {base_currency}")
    print(f"  • Target Symbols: {', '.join(symbols)}")

    # 1. Fetch
    print("\n[1/3] Fetching exchange rates from API...")
    try:
        with FXApiClient() as client:
            api_response = client.fetch_rates(
                start_date=start_date,
                end_date=end_date,
                base_currency=base_currency,
                symbols=symbols
            )
        print(f"  ✓ Successfully retrieved records for base '{api_response.base}'.")
    except FXApiClientError as err:
        print(f"  ❌ API Error: {err}", file=sys.stderr)
        sys.exit(1)

    # 2. Transform
    print("\n[2/3] Transforming data and computing rolling metrics (Polars)...")
    df = FXTransformer.transform(api_response)
    print(f"  ✓ Generated Polars DataFrame: {df.shape[0]} rows x {df.shape[1]} columns.")

    # 3. Store
    print("\n[3/3] Saving dataset to Parquet storage engine...")
    storage = ParquetStorageEngine(output_dir=PROCESSED_DATA_DIR)

    if partition:
        saved_path = storage.save_dataframe(df, partition_by=["target_currency"])
        print(f"  ✓ Saved partitioned dataset to directory: {saved_path}")
    else:
        filename = f"fx_{base_currency.lower()}_{start_date}_to_{end_date}.parquet"
        saved_path = storage.save_dataframe(df, filename=filename)
        print(f"  ✓ Saved Parquet file to: {saved_path}")

    print("\n Pipeline execution completed successfully!")


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        start_date = args.start_date,
        end_date = args.end_date,
        base_currency = args.base,
        symbols = args.symbols,
        partition = args.partition
    )
    