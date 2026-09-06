import httpx
from typing import List, Optional
from models import FXApiResponse


class FXApiClient:
    """HTTP Client for interacting with the Frankfurter Macroeconomic FX API."""

    def __init__(
        self,
        base_url: str = "https://api.frankfurter.app",
        timeout: float = 10.0
    ) -> None:
        """
        Initialize the API client.
        
        :param base_url: The root URL for the Frankfurter API endpoints.
        :param timeout: Network request timeout limit in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # Create a persistent HTTPX client session with default timeout configuration
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True
        )
    def fetch_rates(
        self,
        start_date: str = "2026-01-01",
        end_date: str = "2026-01-07",
        base_currency: str = "USD",
        symbols: Optional[List[str]] = None
    ) -> FXApiResponse:
        """
        Fetch time-series exchange rate data and validate it using FXApiResponse.

        :param start_date: Start date string (YYYY-MM-DD)
        :param end_date: End date string (YYYY-MM-DD)
        :param base_currency: Base currency code (e.g., 'USD')
        :param symbols: Optional list of target currency codes (e.g., ['EUR', 'JPY'])
        :return: Validated FXApiResponse Pydantic model instance
        """
        endpoint = f"/{start_date}..{end_date}"
        params = {"from": base_currency}

        if symbols:
            params["to"] = ",".join(symbols)

        response = self.client.get(endpoint, params=params)
        response.raise_for_status()

        # Parse and validate raw JSON through Pydantic
        raw_json = response.json()
        return FXApiResponse.model_validate(raw_json)
    
    def close(self) -> None:
        """Close the underlying HTTPX client connection pool."""
        self.client.close()

    def __enter__(self):
        """Context manager support to auto-close connections using 'with' blocks."""
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    # Quick sanity check run directly
    with FXApiClient() as client:
        data = client.fetch_rates(
            start_date="2026-01-01",
            end_date="2026-01-07",
            base_currency="USD",
            symbols=["EUR", "JPY", "GBP"]
        )
        print("✅ Success!")
        print(f"Base: {data.base}")
        print(f"Fetched {len(data.rates)} days of rate data.")+