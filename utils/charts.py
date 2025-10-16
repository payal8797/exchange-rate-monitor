import plotly.express as px

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
