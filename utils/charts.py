import plotly.express as px
import pandas as pd

def plot_exchange_rate(df, base, target):
    fig = px.line(
        df, x="date", y=target,
        title=f"{base} → {target} Exchange Rate",
        labels={"date": "Date", target: "Rate"}
    )
    fig.update_traces(line_color="#007BFF")
    fig.update_layout(yaxis_tickformat=".2f", height=400)
    return fig


def plot_inflation(df, country):
    if df.empty:
        return None
    fig = px.bar(
        df, x="year", y="inflation_rate",
        title=f"Inflation Rate in {country}",
        labels={"inflation_rate": "Inflation (%)", "year": "Year"},
    )
    fig.update_traces(marker_color="#28A745")
    fig.update_layout(yaxis_tickformat=".1f", height=400)
    return fig

def plot_inflation_comparison(df1, df2, country1, country2):
    """Return a bar chart comparing inflation between two countries."""
    df1 = df1.copy(); df1["Country"] = country1
    df2 = df2.copy(); df2["Country"] = country2
    merged = pd.concat([df1, df2])
    fig = px.bar(
        merged, x="year", y="inflation_rate", color="Country",
        barmode="group",
        title=f"Inflation Comparison: {country1} vs {country2}",
        labels={"inflation_rate": "Inflation (%)", "year": "Year"}
    )
    fig.update_layout(height=400)
    return fig
