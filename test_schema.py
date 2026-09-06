import httpx
from pydantic import ValidationError
from src.models import FXApiResponse

URL = "https://api.frankfurter.app/2026-01-01..2026-01-07"
params = {"from": "USD", "to": "EUR,JPY,GBP"}

print("1. Fetching live raw JSON from API...")
response = httpx.get(URL, params=params, follow_redirects=True, timeout=10.0)
response.raise_for_status()
raw_data = response.json()

print("\n2. Validating payload against FXApiResponse schema...")
try:
    # Pass raw dictionary to Pydantic for parsing & validation
    validated_data: FXApiResponse = FXApiResponse.model_validate(raw_data)

    print("Validation successful!")
    print(f"Base Currency : {validated_data.base}")
    print(f"Start Date    : {validated_data.start_date} (Type: {type(validated_data.start_date)})")
    print(f"Total Dates   : {len(validated_data.rates)}")

    # Peek at the parsed rates dictionary
    first_date = list(validated_data.rates.keys())[0]
    print(f"Rates on {first_date}: {validated_data.rates[first_date]}")

except httpx.RequestError as e:
    print(f"\n❌ Network Error: Could not connect to API.")
    print(f"Details: {e}")

except ValidationError as e:
    print("\n❌ Validation Error: API response didn't match Pydantic schema!")
    print(e)