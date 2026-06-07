import requests

def get_bitget_price(symbol):

    url = (
        "https://api.bitget.com"
        "/api/v2/spot/market/tickers"
    )

    try:
        response = requests.get(
            url,
            params={"symbol": symbol},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("data"):
            return float(
                data["data"][0]["lastPr"]
            )

        return None

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None