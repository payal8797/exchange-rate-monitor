import streamlit as st

# -------------------------------------------------------------------
# 🔹 Helper: Metric with hover tooltip
# -------------------------------------------------------------------
def metric_with_tooltip(label, value, delta=None, tip=""):
    """Render a metric with tooltip visible only when hovering on ℹ️ icon."""
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


