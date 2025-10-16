import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=86400)
def fetch_global_inflation():
    """
    Fetch latest inflation data for all countries (CPI Annual %).
    Returns a DataFrame with Country, Country Code, and Latest Inflation Rate.
    """
    url = "https://api.worldbank.org/v2/country/all/indicator/FP.CPI.TOTL.ZG?format=json&per_page=4000"
    res = requests.get(url)

    if res.status_code != 200:
        st.warning("Could not fetch global inflation data.")
        return pd.DataFrame()

    data = res.json()
    if len(data) < 2 or not isinstance(data[1], list):
        st.warning("No inflation data received from World Bank API.")
        return pd.DataFrame()

    df = pd.DataFrame(data[1])

    # Extract nested country info safely
    df["Country"] = df["country"].apply(lambda x: x["value"] if isinstance(x, dict) else str(x))
    df["Country Code"] = df["countryiso3code"]
    df["Year"] = pd.to_numeric(df["date"], errors="coerce")
    df["Inflation Rate"] = pd.to_numeric(df["value"], errors="coerce")

    df = df[["Country", "Country Code", "Year", "Inflation Rate"]].dropna()

    # Keep only latest year per country
    df = df.sort_values(["Country", "Year"], ascending=[True, False])
    latest = df.groupby("Country").head(1).reset_index(drop=True)
    latest = latest[latest["Inflation Rate"].notnull()]
    return latest
