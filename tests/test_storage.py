from pathlib import Path
import polars as pl
import pytest
from storage import ParquetStorageEngine


@pytest.fixture
def sample_dataframe() -> pl.DataFrame:
    """Provides a sample transformed Polars DataFrame for testing."""
    return pl.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-02"],
            "base_currency": ["USD", "USD"],
            "target_currency": ["EUR", "EUR"],
            "rate": [0.92, 0.93],
            "pct_change_1d": [None, 0.01087],
            "rolling_avg_7d": [0.92, 0.925],
            "rolling_avg_30d": [0.92, 0.925],
        }
    ).with_columns(
        [
            pl.col("date").str.to_date(),
            pl.col("base_currency").cast(pl.Categorical),
            pl.col("target_currency").cast(pl.Categorical),
            pl.col("rate").cast(pl.Float64),
        ]
    )


def test_save_dataframe_single_file(tmp_path: Path, sample_dataframe: pl.DataFrame):
    """Test writing a DataFrame to a single Parquet file."""
    storage = ParquetStorageEngine(output_dir=tmp_path)
    target_filename = "test_rates.parquet"

    saved_path = storage.save_dataframe(sample_dataframe, filename=target_filename)

    assert saved_path.exists()
    assert saved_path.is_file()
    assert saved_path.name == target_filename

    # Read back the Parquet file and verify contents match
    df_read = pl.read_parquet(saved_path)
    assert df_read.shape == sample_dataframe.shape
    assert df_read.columns == sample_dataframe.columns


def test_save_dataframe_partitioned(tmp_path: Path, sample_dataframe: pl.DataFrame):
    """Test writing a DataFrame with hive-style partitioning."""
    storage = ParquetStorageEngine(output_dir=tmp_path)

    saved_path = storage.save_dataframe(
        sample_dataframe, partition_by=["base_currency"]
    )

    assert saved_path.exists()
    assert saved_path.is_dir()

    # Verify that the partitioned subdirectory structure was created
    partition_folder = tmp_path / "base_currency=USD"
    assert partition_folder.exists()
    assert partition_folder.is_dir()

    # Read back partitioned dataset using Polars
    df_read = pl.read_parquet(tmp_path / "**/*.parquet")
    assert df_read.shape[0] == sample_dataframe.shape[0]


def test_save_empty_dataframe_raises_error(tmp_path: Path):
    """Test that attempting to write an empty DataFrame raises a ValueError."""
    storage = ParquetStorageEngine(output_dir=tmp_path)
    empty_df = pl.DataFrame()

    with pytest.raises(ValueError) as exc_info:
        storage.save_dataframe(empty_df)

    assert "Cannot write an empty DataFrame" in str(exc_info.value)