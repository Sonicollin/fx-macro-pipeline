import httpx
import json

# 1. Define the macroeconomic API endpoint
# Frankfurter API endpoint for standard historical USD exchange rates
URL = "https://api.frankfurter.app/2026-01-01..2026-01-07"

params = {
    "from": "USD",
    "to": "EUR,JPY,GBP"
}

print(f"Fetching data from: {URL}...")

try:
    # 2. Make an HTTP GET request to the public API
    response = httpx.get(URL, params=params, timeout=10.0, follow_redirects=True)

    # 3. Check if the request was successful (Status code 200)
    response.raise_for_status()

    # 4. Parse the raw JSON response into a native Python dictionary
    data = response.json()

    print("\n--- Successful Ingestion ---")
    print(f"Base Currency: {data['base']}")
    print(f"Start Date: {data['start_date']}")

    print("\n--- Raw Nested Payload Structure ---")
    # Pretty-print the nested dictionary so you can inspect the JSON structure
    print(json.dumps(data, indent=2))

except httpx.HTTPStatusError as e:
    print(f"HTTP Error occurred: {e.response.status_code}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")