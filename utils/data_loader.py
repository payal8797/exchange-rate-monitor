import requests
import pandas as pd
import streamlit as st

# Mapping between country names and ISO2 codes (for top countries)
COUNTRY_CODES = {
    "Germany": "DE",
    "India": "IN",
    "United States": "US",
    "Japan": "JP",
    "France": "FR",
    "Brazil": "BR",
    "United Kingdom": "GB",
    "China": "CN",
    "Canada": "CA",
    "Australia": "AU"
}

@st.cache_data
def fetch_inflation_data(country_name: str):
    """Fetch live inflation data (CPI, annual %) from World Bank API."""
    code = COUNTRY_CODES.get(country_name)
    if not code:
        st.warning(f"No ISO code found for {country_name}.")
        return pd.DataFrame()

    url = f"https://api.worldbank.org/v2/country/{code}/indicator/FP.CPI.TOTL.ZG?format=json"
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data for {country_name}: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    if not data or len(data) < 2 or not data[1]:
        st.warning(f"No inflation data found for {country_name}.")
        return pd.DataFrame()

    df = pd.DataFrame(data[1])
    df = df[["date", "value"]].dropna()
    df.columns = ["year", "inflation_rate"]
    df["year"] = df["year"].astype(int)
    df["inflation_rate"] = df["inflation_rate"].astype(float)
    df = df.sort_values("year")

    return df
