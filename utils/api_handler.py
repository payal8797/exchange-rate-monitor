import requests
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = "https://api.frankfurter.app"


def get_available_currencies():
    """Fetch available currencies dynamically from Frankfurter API."""
    url = f"{BASE_URL}/currencies"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch currency list from API.")
    
    data = response.json()  # Returns dict like {"USD": "United States Dollar", ...}
    return data

def get_exchange_rate(base="USD", target="EUR", start_date=None, end_date=None):
    """Fetch historical exchange rates from Frankfurter API."""
    if base == target:
        # Handle same-currency case
        return pd.DataFrame({
            "date": pd.date_range(end=datetime.now(), periods=10),
            target: [1.0] * 10
        })
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/{start_date}..{end_date}?from={base}&to={target}"
    response = requests.get(url)
    
    # Check if the request succeeded
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")
    
    data = response.json()
    
    # Defensive check for missing 'rates' key
    if "rates" not in data or not data["rates"]:
        raise Exception(f"No rate data available for {base}->{target}. Response: {data}")
    
    # Build DataFrame
    rates = pd.DataFrame(data["rates"]).T.reset_index()
    rates.columns = ["date", target]
    rates["date"] = pd.to_datetime(rates["date"])
    
    return rates.sort_values("date")
