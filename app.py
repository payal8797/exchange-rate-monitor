import streamlit as st
import numpy as np
from utils.api_handler import get_available_currencies, get_exchange_rate
from utils.data_loader import fetch_inflation_data
from utils.charts import plot_exchange_rate, plot_inflation, plot_inflation_comparison, plot_global_inflation_map
from utils.insights import generate_insights
from utils.metric_tooltip import metric_with_tooltip
from utils.global_data import fetch_global_inflation

# -------------------------------------------------------------------
# 🔹 Streamlit Page Config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Exchange Rate & Inflation Monitor",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("💱 Global Exchange Rate & Inflation Monitor")
st.caption("Live currency data from Frankfurter API & inflation data from World Bank API.")


# -------------------------------------------------------------------
# 🔹 Sidebar Controls
# -------------------------------------------------------------------
with st.sidebar:
    st.header("🔧 Controls")
    with st.spinner("Loading currencies..."):
        try:
            currency_dict = get_available_currencies()
            currency_list = sorted(currency_dict.keys())
        except Exception as e:
            st.error(f"Failed to load currencies: {e}")
            st.stop()

    base = st.selectbox("Base Currency", currency_list, index=currency_list.index("USD"))
    target = st.selectbox("Target Currency", currency_list, index=currency_list.index("EUR"))
    show_inflation = st.checkbox("Show Inflation Data", True)

    if show_inflation:
        selected_country = st.selectbox(
            "Select Country",
            ["India", "Germany", "United States", "Japan", "France", "Brazil",
             "United Kingdom", "China", "Canada", "Australia"]
        )
    else:
        selected_country = None


# -------------------------------------------------------------------
# 🔹 Exchange Rate Section
# -------------------------------------------------------------------
st.subheader(f"💹 {base} → {target} Exchange Rate Trend")

try:
    exchange_df = get_exchange_rate(base, target)
    current_rate = exchange_df[target].iloc[-1]
    first_rate = exchange_df[target].iloc[0]
    rate_change = ((current_rate - first_rate) / first_rate) * 100
    volatility = exchange_df[target].std()

    # Smart color logic for direction
    if rate_change > 0:
        direction_note = "📈 Base currency strengthened."
    elif rate_change < 0:
        direction_note = "📉 Base currency weakened."
    else:
        direction_note = "⚖️ Exchange rate stable."

    # --- Key Metrics Row ---
    st.markdown("### 📊 Key Metrics Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        metric_with_tooltip(
            label="Current Rate",
            value=f"{current_rate:.2f}",
            tip="Current exchange value of base to target currency."
        )

    with col2:
        metric_with_tooltip(
            label="Change (%)",
            value=f"{rate_change:.2f}%",
            tip=f"Overall % change over the last 6 months. {direction_note}"
        )

    with col3:
        metric_with_tooltip(
            label="Volatility (Std Dev)",
            value=f"{volatility:.2f}",
            tip="Higher volatility means more fluctuations in exchange rate."
        )

    st.plotly_chart(plot_exchange_rate(exchange_df, base, target), use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Could not load exchange data: {e}")
    exchange_df = None
    rate_change = None


# -------------------------------------------------------------------
# 🔹 Inflation Section
# -------------------------------------------------------------------
avg_infl = None
if show_inflation:
    st.subheader("📈 Inflation Trends (Live from World Bank)")
    with st.spinner(f"Fetching inflation data for {selected_country}..."):
        inflation_df = fetch_inflation_data(selected_country)

    if not inflation_df.empty:
        avg_infl = inflation_df["inflation_rate"].tail(5).mean()

        # Tooltip metric for average inflation
        st.markdown("### 📊 Inflation Summary")
        metric_with_tooltip(
            label="Avg Inflation (5 yrs)",
            value=f"{avg_infl:.2f}%",
            tip=f"Average annual inflation in {selected_country} for the last five years."
        )

        # Inflation chart
        st.plotly_chart(plot_inflation(inflation_df, selected_country), use_container_width=True)

        # Comparison mode
        compare_toggle = st.checkbox("Compare Inflation with Another Country")
        if compare_toggle:
            comp_country = st.selectbox(
                "Compare With",
                [c for c in ["India", "Germany", "United States", "Japan", "France", "Brazil",
                             "United Kingdom", "China", "Canada", "Australia"]
                 if c != selected_country]
            )
            with st.spinner(f"Fetching inflation data for {comp_country}..."):
                comp_df = fetch_inflation_data(comp_country)
            if not comp_df.empty:
                st.plotly_chart(
                    plot_inflation_comparison(inflation_df, comp_df, selected_country, comp_country),
                    use_container_width=True
                )
                comp_avg = comp_df["inflation_rate"].tail(5).mean()
                metric_with_tooltip(
                    label=f"Avg Inflation Comparison ({selected_country} vs {comp_country})",
                    value=f"{avg_infl:.2f}% vs {comp_avg:.2f}%",
                    tip=f"Average inflation comparison over last 5 years: {selected_country} vs {comp_country}."
                )

    else:
        st.warning(f"No inflation data found for {selected_country}.")


# -------------------------------------------------------------------
# 🔹 Smart Insights Section
# -------------------------------------------------------------------
st.markdown("### 🧠 Smart Insights")
if rate_change is not None:
    insights_text = generate_insights(base, target, rate_change, selected_country, avg_infl)
    st.markdown(insights_text)
else:
    st.info("Exchange rate data unavailable. Cannot generate insights.")


# -------------------------------------------------------------------
# 🔹 Footer
# -------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Data Sources: [Frankfurter API](https://www.frankfurter.app/) for exchange rates and "
    "[World Bank](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG) for inflation data."
)


# -------------------------------------------------------------------
# 🌍 Global Inflation Map
# -------------------------------------------------------------------
st.markdown("### 🌍 Global Inflation Overview")

if st.button("Load Global Inflation Map"):
    with st.spinner("Fetching global inflation data..."):
        global_df = fetch_global_inflation()
    if not global_df.empty:
        st.plotly_chart(plot_global_inflation_map(global_df), use_container_width=True)
        st.caption("Data Source: World Bank (Annual CPI %)")
    else:
        st.warning("No global data available at the moment.")
