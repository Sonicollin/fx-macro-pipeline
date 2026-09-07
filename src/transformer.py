import polars as pl
from models import FXApiResponse


class FXTransformer:
    """Transforms FXApiResponse Pydantic objects into tabular Polars DataFrames with analytical metrics."""

    @staticmethod
    def transform(api_response: FXApiResponse) -> pl.DataFrame:
        """
        Flattens nested FXApiResponse rates dictionary and computes rolling aggregations.
        
        Schema:
            date (pl.Date)
            base_currency (pl.Categorical)
            target_currency (pl.Categorical)
            rate (pl.Float64)
            pct_change_1d (pl.Float64)
            rolling_avg_7d (pl.Float64)
            rolling_avg_30d (pl.Float64)
        """
        # Handle empty API response gracefully
        if not api_response.rates:
            return pl.DataFrame(
                schema={
                    "date": pl.Date,
                    "base_currency": pl.Categorical,
                    "target_currency": pl.Categorical,
                    "rate": pl.Float64,
                    "pct_change_1d": pl.Float64,
                    "rolling_avg_7d": pl.Float64,
                    "rolling_avg_30d": pl.Float64,
                }
            )

        # 1. Unnest Dict[date, Dict[str, float]] into flat records
        records = [
            {
                "date": dt,
                "base_currency": api_response.base,
                "target_currency": target_currency,
                "rate": float(rate),
            }
            for dt, rates in api_response.rates.items()
            for target_currency, rate in rates.items()
        ]

        # 2. Build initial Polars DataFrame and enforce categorical types
        df = pl.DataFrame(records).with_columns(
            [
                pl.col("date").cast(pl.Date),
                pl.col("base_currency").cast(pl.Categorical),
                pl.col("target_currency").cast(pl.Categorical),
                pl.col("rate").cast(pl.Float64),
            ]
        )

        # 3. Sort chronologically by currency group before window operations
        df = df.sort(["target_currency", "date"])

        # 4. Compute vectorized rolling transformations partitioned by target currency
        df_transformed = df.with_columns(
            [
                # Daily percentage change: (current - previous) / previous
                (
                    (pl.col("rate") - pl.col("rate").shift(1).over("target_currency"))
                    / pl.col("rate").shift(1).over("target_currency")
                ).alias("pct_change_1d"),
                # 7-day rolling moving average
                pl.col("rate")
                .rolling_mean(window_size=7)
                .over("target_currency")
                .alias("rolling_avg_7d"),
                # 30-day rolling moving average
                pl.col("rate")
                .rolling_mean(window_size=30)
                .over("target_currency")
                .alias("rolling_avg_30d"),
            ]
        )

        return df_transformed