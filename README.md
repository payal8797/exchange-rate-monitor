# 💱 Global Exchange Rate & Inflation Monitor

A lightweight and interactive **Streamlit dashboard** that visualizes **currency exchange rates** and **inflation trends** using live data from the **Frankfurter API** and the **World Bank API**.  
It helps users quickly understand how global currencies and inflation correlate — with smart insights, comparison views, and hover-based tooltips.


---

## 🧰 Tech Stack

| Category | Technologies |
|-----------|---------------|
| **Frontend / UI** | Streamlit, Plotly Express |
| **Backend / Data Fetching** | Python (Requests, Pandas) |
| **Data Sources** | [Frankfurter API](https://www.frankfurter.app/) for exchange rates, [World Bank API](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG) for inflation |
| **Visualization** | Plotly (line + bar charts) |
| **Structure** | Modular Python (`utils/` folder for APIs, charts, insights) |


---

## ⚙️ Installation & Running Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/exchange-rate-monitor.git
cd exchange-rate-monitor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
---

## 🌟 Current Features

### 💹 1. **Exchange Rate Tracker**
- 📊 Fetches **live currency exchange rates** via the [Frankfurter API](https://www.frankfurter.app/).  
- 🕒 Displays **6-month historical trends** with daily resolution.  
- ⚡ Calculates **% Change** and **Volatility (Standard Deviation)** to measure currency stability.  
- 🧠 Smart tooltips explain each metric (hover over ℹ️ for contextual hints).

---

### 📈 2. **Inflation Monitor**
- 🌍 Retrieves **Consumer Price Index (CPI, Annual %)** data from the [World Bank API](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG).  
- 🧾 Displays the **5-year average inflation rate** with informative tooltips.  
- 📊 Visualizes year-wise inflation trends through interactive **bar charts**.  
- 🧩 Dynamic country selection automatically updates data and visuals.

---

### 🌍 3. **Global Inflation Map**
- 🗺️ Interactive **world map (choropleth)** highlighting inflation by country.  
- 🔴 Higher inflation → darker red; 🟢 lower inflation → lighter shades.  
- 💬 Hover to view each country’s inflation % and data year.  
- ⚙️ Option to include the **latest available data** for all reporting countries.

---

### 🔁 4. **Two-Country Comparison Mode**
- ⚖️ Compare **inflation trends** between any two countries side-by-side.  
- 📊 Dual-color **grouped bar chart** shows clear year-to-year differences.  
- 🧮 Displays an **average inflation comparison metric**, e.g. `India: 5.3% vs Germany: 2.7%`.  

---

### 🧠 5. **Smart Insights**
- 🗣️ Automatically generates **natural-language summaries** such as:  
  > “USD strengthened by 2.8% against INR in the last six months, while India’s average inflation was 5.3%.”  
- 💡 Helps non-technical users quickly interpret data relationships.

---

### 💬 6. **Interactive Tooltips**
- ℹ️ Hover-based explanations beside every key metric (no clutter).  
- Consistent tooltip style across **exchange rate, volatility, and inflation** sections.  

---

### 🧭 7. **User Experience & Performance**
- 🧱 Modular architecture (`utils/` folder for APIs, charts, and insights).  
- ⚡ Cached API calls using `@st.cache_data` for faster reloads.  
- 🎨 Clean Streamlit interface optimized for both desktop and mobile users.  


## 🚀 Checkout here
https://exchange-rate-monitor.streamlit.app/
---