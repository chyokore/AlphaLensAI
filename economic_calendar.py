import streamlit as st
from datetime import datetime

@st.cache_data(ttl=3600)
def get_economic_events():

    return [

        {
            "event": "Consumer Price Index (CPI)",
            "impact": "🔴 High",
            "date": "2026-06-15",
            "time": "12:30 UTC",
            "description": "Inflation data affecting interest rate expectations."
        },

        {
            "event": "Producer Price Index (PPI)",
            "impact": "🟠 Medium",
            "date": "2026-06-16",
            "time": "12:30 UTC",
            "description": "Measures wholesale inflation pressures."
        },

        {
            "event": "FOMC Interest Rate Decision",
            "impact": "🔴 High",
            "date": "2026-06-18",
            "time": "18:00 UTC",
            "description": "Federal Reserve interest rate announcement."
        },

        {
            "event": "Non-Farm Payrolls (NFP)",
            "impact": "🔴 High",
            "date": "2026-07-03",
            "time": "12:30 UTC",
            "description": "Monthly US employment report."
        }

    ]