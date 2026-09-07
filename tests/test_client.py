import httpx
import respx
import pytest
from client import FXApiClient, FXApiHTTPError, FXApiNetworkError
from models import FXApiResponse


@pytest.fixture
def mock_api_response():
    """Provides a standard mock JSON payload returned by Frankfurter API."""
    return {
        "amount": 1.0,
        "base": "USD",
        "start_date": "2026-01-01",
        "end_date": "2026-01-07",
        "rates": {
            "2026-01-02": {"EUR": 0.92, "GBP": 0.79},
            "2026-01-05": {"EUR": 0.91, "GBP": 0.78},
        },
    }


@respx.mock
def test_fetch_rates_success(mock_api_response):
    """Test successful fetching and parsing of FX rates using respx."""
    # Mock the specific API route and query params
    route = respx.get("https://api.frankfurter.app/2026-01-01..2026-01-07").mock(
        return_value=httpx.Response(200, json=mock_api_response)
    )

    with FXApiClient() as client:
        result = client.fetch_rates(
            start_date="2026-01-01",
            end_date="2026-01-07",
            base_currency="USD",
            symbols=["EUR", "GBP"],
        )

    # Verify request matching and return object
    assert route.called # Verifies that client actually made the web request
    assert route.calls.last.request.url.query == b"from=USD&to=EUR%2CGBP" # Verifies that Pydantic converted it to the right class
    assert isinstance(result, FXApiResponse) # Verifies that the internal data parsed correctly
    assert result.base == "USD"
    assert len(result.rates) == 2


@respx.mock
def test_fetch_rates_http_error():
    """Test client handling of HTTP status errors (e.g., 404)."""
    respx.get("https://api.frankfurter.app/2026-01-01..2026-01-07").mock(
        return_value=httpx.Response(404, text="Not Found")
    )

    with FXApiClient() as client:
        with pytest.raises(FXApiHTTPError) as exc_info:
            client.fetch_rates()

    assert "404" in str(exc_info.value) # Checks if 404 is in the error risen


@respx.mock
def test_fetch_rates_network_error():
    """Test client handling of transport/network failure."""
    respx.get("https://api.frankfurter.app/2026-01-01..2026-01-07").mock(
        side_effect=httpx.ConnectError("Network unreachable")
    )

    with FXApiClient() as client:
        with pytest.raises(FXApiNetworkError) as exc_info:
            client.fetch_rates()

    assert "Network error occurred" in str(exc_info.value) # Checks if "network error occurred" is in the error risen