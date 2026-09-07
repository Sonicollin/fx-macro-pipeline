from typing import List, Optional
import httpx
from models import FXApiResponse


class FXApiClientError(Exception):
    """Base exception for FXApiClient errors."""
    pass


class FXApiNetworkError(FXApiClientError):
    """Raised on connection failures or timeouts."""
    pass


class FXApiHTTPError(FXApiClientError):
    """Raised when API returns a non-2xx status code."""
    pass


class FXApiClient:
    def __init__(
        self,
        incoming_url: str = "https://api.frankfurter.app",
        max_wait_time: float = 10.0,
        max_retries: int = 3,
    ) -> None:
        self.base_url = incoming_url.rstrip("/")
        self.timeout = max_wait_time

        # Configure automatic retries for transient transport failures
        transport = httpx.HTTPTransport(retries=max_retries)
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            transport=transport,
            follow_redirects=True,
        )

    def fetch_rates(
        self,
        start_date: str = "2026-01-01",
        end_date: str = "2026-01-07",
        base_currency: str = "USD",
        symbols: Optional[List[str]] = None,
    ) -> FXApiResponse:
        endpoint = f"/{start_date}..{end_date}"
        params = {"from": base_currency}
        if symbols:
            params["to"] = ",".join(symbols)

        try:
            response = self.client.get(endpoint, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise FXApiHTTPError(
                f"API request failed with status code {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except httpx.RequestError as exc:
            raise FXApiNetworkError(f"Network error occurred while fetching FX data: {exc}") from exc

        return FXApiResponse.model_validate(response.json())

    def close(self) -> None:
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()