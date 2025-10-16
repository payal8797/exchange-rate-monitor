import streamlit as st
from utils.api_handler import get_available_currencies, get_exchange_rate
from utils.data_loader import fetch_inflation_data
from utils.charts import plot_exchange_rate, plot_inflation

st.set_page_config(page_title="Exchange Rate & Inflation Monitor", layout="wide")

st.title("💱 Global Exchange Rate & Inflation Monitor")
st.markdown("Explore real-time exchange rates and live inflation trends from global sources.")

# --- Currency Data ---
with st.spinner("Loading available currencies..."):
    currency_dict = get_available_currencies()
    currency_list = sorted(currency_dict.keys())

st.sidebar.header("🔧 Controls")
base = st.sidebar.selectbox("Base Currency", currency_list, index=currency_list.index("USD"))
target = st.sidebar.selectbox("Target Currency", currency_list, index=currency_list.index("EUR"))
show_inflation = st.sidebar.checkbox("Show Inflation Data", True)

# --- Exchange Rate Section ---
st.subheader(f"💹 {base} → {target} Exchange Rate Trend")
try:
    exchange_df = get_exchange_rate(base, target)
    st.plotly_chart(plot_exchange_rate(exchange_df, base, target), use_container_width=True)

    current_rate = exchange_df[target].iloc[-1]
    change = ((exchange_df[target].iloc[-1] - exchange_df[target].iloc[0]) / exchange_df[target].iloc[0]) * 100
    st.metric(label=f"Current {base} → {target}", value=f"{current_rate:.2f}", delta=f"{change:.2f}%")

except Exception as e:
    st.warning(f"⚠️ Could not load exchange data: {e}")

# --- Inflation Section ---
if show_inflation:
    st.subheader("📈 Inflation Trends (Live from World Bank)")
    selected_country = st.selectbox("Select Country", ["India", "Germany", "United States", "Japan", "France", "Brazil", "United Kingdom", "China", "Canada", "Australia"])

    with st.spinner(f"Fetching inflation data for {selected_country}..."):
        inflation_df = fetch_inflation_data(selected_country)

    if not inflation_df.empty:
        st.plotly_chart(plot_inflation(inflation_df, selected_country), use_container_width=True)
        avg_infl = inflation_df["inflation_rate"].tail(5).mean()
        st.metric(label=f"Avg Inflation (last 5 yrs)", value=f"{avg_infl:.2f}%")

# --- Insights ---
st.markdown("### 🧠 Insights")
st.write(f"- Over the selected period, **{base}** changed by **{change:.2f}%** against **{target}**.")
if show_inflation and not inflation_df.empty:
    st.write(f"- Inflation in **{selected_country}** shows an average of **{avg_infl:.2f}%** over recent years.")

st.markdown("---")
st.caption("Data Sources: [Frankfurter API](https://www.frankfurter.app/) for exchange rates and [World Bank](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG) for inflation data.")
