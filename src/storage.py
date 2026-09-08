from pathlib import Path
import polars as pl
from config import PROCESSED_DATA_DIR, ensure_directories_exist


class ParquetStorageEngine:
    """Handles saving Polars DataFrames into partitioned Parquet files."""

    def __init__(self, output_dir: Path = PROCESSED_DATA_DIR) -> None:
        self.output_dir = output_dir
        ensure_directories_exist()

    def save_dataframe(
        self,
        df: pl.DataFrame,
        filename: str = "fx_rates.parquet",
        partition_by: list[str] | None = None,
    ) -> Path:
        """
        Saves a Polars DataFrame to Parquet format.
        
        Args:
            df: The Polars DataFrame to write.
            filename: Target file name if not partitioning.
            partition_by: List of column names to partition disk storage by (e.g., ['base_currency']).
            
        Returns:
            Path to the saved directory or file.
        """
        if df.is_empty():
            raise ValueError("Cannot write an empty DataFrame to Parquet.")

        if partition_by:
            # Writes dataset into hive-partitioned subdirectories
            df.write_parquet(
                self.output_dir,
                use_pyarrow=True,
                pyarrow_options={"partition_cols": partition_by},
            )
            return self.output_dir

        target_path = self.output_dir / filename
        df.write_parquet(target_path)
        return target_path