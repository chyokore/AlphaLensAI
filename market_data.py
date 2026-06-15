import requests
import streamlit as st

# =========================
# TRENDING COINS
# =========================

@st.cache_data(ttl=300)
def get_trending_coins():

    url = "https://api.coingecko.com/api/v3/search/trending"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return [
            coin["item"]["symbol"].upper()
            for coin in data["coins"][:5]
        ]

    except Exception as e:

        print(
            f"Trending Coins Error: {e}"
        )

        return []
# =========================
# GLOBAL MARKET DATA
# =========================

@st.cache_data(ttl=300)
def get_global_market():
    url = "https://api.coingecko.com/api/v3/global"

    try:
        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()["data"]

        return {
            "market_cap": data["total_market_cap"]["usd"],
            "volume": data["total_volume"]["usd"],
            "btc_dominance": data["market_cap_percentage"]["btc"]
        }

    except Exception:
        return None

# =========================
# FEAR & GREED
# =========================

@st.cache_data(ttl=300)
def get_fear_greed():

    url = "https://api.alternative.me/fng/"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        value = data["data"][0]["value"]

        classification = (
            data["data"][0]
            ["value_classification"]
        )

        return value, classification

    except Exception as e:

        print(
            f"Fear & Greed Error: {e}"
        )

        return "N/A", "Unavailable"
        def get_fear_greed():

    url = "https://api.alternative.me/fng/"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text[:500])

        data = response.json()

        value = data["data"][0]["value"]

        classification = (
            data["data"][0]["value_classification"]
        )

        return value, classification

    except Exception as e:

        print(
            f"Fear & Greed Error: {e}"
        )

        return "N/A", "Unavailable"