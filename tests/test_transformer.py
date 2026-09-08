from client import FXApiClient
from transformer import FXTransformer

with FXApiClient() as client:
    # Fetch a wider range (30+ days) to see window metrics populate
    data = client.fetch_rates(
        start_date="2026-01-01",
        end_date="2026-02-15",
        base_currency="USD",
        symbols=["EUR", "JPY"],
    )

df = FXTransformer.transform(data)
print(df)
print("\nDataFrame Schema:")
print(df.schema)