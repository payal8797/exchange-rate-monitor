import streamlit as st
import numpy as np
from utils.api_handler import get_available_currencies, get_exchange_rate
from utils.data_loader import fetch_inflation_data
from utils.charts import plot_exchange_rate, plot_inflation

def metric_with_tooltip(label, value, delta=None, tip=""):
    """Metric with tooltip that appears when hovering over ℹ️ icon."""
    html = f"""
    <style>
        .metric-container {{
            display: inline-block;
            position: relative;
            margin: 10px 0;
            padding: 5px 10px;
        }}
        .tooltip-icon {{
            cursor: help;
            color: #888;
            font-size: 14px;
            margin-left: 4px;
        }}
        .tooltip-box {{
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.3s;
            position: absolute;
            top: -5px;
            left: 105%;
            background-color: #333;
            color: #fff;
            text-align: left;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 13px;
            width: 220px;
            z-index: 999;
        }}
        .tooltip-icon:hover + .tooltip-box {{
            visibility: visible;
            opacity: 1;
        }}
    </style>

    <div class="metric-container">
        <div style="font-weight:600; font-size:16px; display:flex; align-items:center;">
            {label}
            <span class="tooltip-icon">ℹ️</span>
            <div class="tooltip-box">{tip}</div>
        </div>
        <div style="font-size:22px;">{value}</div>
        {'<div style="font-size:14px; color:gray;">' + delta + '</div>' if delta else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- Page Config ---
st.set_page_config(
    page_title="Exchange Rate & Inflation Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title & Description ---
st.title("💱 Global Exchange Rate & Inflation Monitor")
st.caption("Live currency data from Frankfurter API & inflation data from World Bank API.")


# --- Sidebar Controls ---
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


# --- Main Section ---
st.subheader(f"💹 {base} → {target} Exchange Rate Trend")

try:
    exchange_df = get_exchange_rate(base, target)
    current_rate = exchange_df[target].iloc[-1]
    first_rate = exchange_df[target].iloc[0]
    rate_change = ((current_rate - first_rate) / first_rate) * 100
    volatility = exchange_df[target].std()

    # --- Smart color logic ---
    if rate_change > 0:
        delta_color = "inverse"  # green
        direction_note = "📈 Base currency strengthened."
    else:
        delta_color = "normal"   # red
        direction_note = "📉 Base currency weakened."

    # --- Key Metrics Row ---
    st.markdown("### 📊 Key Metrics Overview")
    col1, col2, col3, col4 = st.columns(4)

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
            tip=f"Change calculated over the past 6 months. {direction_note}"
        )

    with col3:
        metric_with_tooltip(
            label="Volatility (Std Dev)",
            value=f"{volatility:.2f}",
            tip="Higher volatility = more fluctuation in exchange rate."
        )

    with col4:
        if show_inflation:
            with st.spinner(f"Fetching inflation data for {selected_country}..."):
                inflation_df = fetch_inflation_data(selected_country)
            if not inflation_df.empty:
                avg_infl = inflation_df["inflation_rate"].tail(5).mean()
                metric_with_tooltip(
                    label="Avg Inflation (5 yrs)",
                    value=f"{avg_infl:.2f}%",
                    tip=f"Average annual inflation in {selected_country} for the last 5 years."
                )
            else:
                metric_with_tooltip(
                    label="Avg Inflation (5 yrs)",
                    value="N/A",
                    tip="Inflation data unavailable for selected country."
                )
        else:
            metric_with_tooltip(
                label="Avg Inflation (5 yrs)",
                value="Hidden",
                tip="Inflation display disabled."
            )

    # --- Charts ---
    st.plotly_chart(plot_exchange_rate(exchange_df, base, target), use_container_width=True)

    if show_inflation and 'inflation_df' in locals() and not inflation_df.empty:
        st.plotly_chart(plot_inflation(inflation_df, selected_country), use_container_width=True)

    # --- Insights ---
    st.markdown("### 🧠 Insights")
    st.write(f"- Over the selected period, **{base}** changed by **{rate_change:.2f}%** against **{target}**.")
    if show_inflation and 'inflation_df' in locals() and not inflation_df.empty:
        st.write(f"- Inflation in **{selected_country}** averaged **{avg_infl:.2f}%** over the last 5 years.")

except Exception as e:
    st.error(f"⚠️ Could not load exchange data: {e}")

st.markdown("---")
st.caption("Data Sources: [Frankfurter API](https://www.frankfurter.app/) and [World Bank](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG)")
