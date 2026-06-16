import streamlit as st
from datetime import datetime


def get_economic_events():
    return [

    {
        "event": "Consumer Price Index (CPI)",
        "impact": "🔴 High",
        "date": "2026-06-15",
        "time": "12:30 UTC",
        "description":
            "Inflation data affecting interest rate expectations.",

        "crypto_impact":
            "Higher inflation may pressure risk assets including crypto.",

        "alphalens_view":
            "Expect elevated BTC and ETH volatility around the release."
    },

    {
        "event": "Producer Price Index (PPI)",
        "impact": "🟠 Medium",
        "date": "2026-06-16",
        "time": "12:30 UTC",
        "description":
            "Measures wholesale inflation pressures.",

        "crypto_impact":
            "Can influence inflation expectations and market sentiment.",

        "alphalens_view":
            "Moderate impact expected unless results significantly surprise."
    },

    {
        "event": "FOMC Interest Rate Decision",
        "impact": "🔴 High",
        "date": "2026-06-18",
        "time": "18:00 UTC",
        "description":
            "Federal Reserve interest rate announcement.",

        "crypto_impact":
            "One of the most important drivers of crypto market volatility.",

        "alphalens_view":
            "Risk level elevated. Monitor liquidity and price reactions."
    },

    {
        "event": "Non-Farm Payrolls (NFP)",
        "impact": "🔴 High",
        "date": "2026-07-03",
        "time": "12:30 UTC",
        "description":
            "Monthly US employment report.",

        "crypto_impact":
            "Strong employment data can influence interest rate expectations.",

        "alphalens_view":
            "Expect short-term volatility across major crypto assets."
    }

]
