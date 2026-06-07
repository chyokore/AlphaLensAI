import requests

print("\n====================")
print(" Bitget Market Data")
print("====================\n")

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]

for symbol in symbols:

    url = (
        "https://api.bitget.com"
        "/api/v2/spot/market/tickers"
        f"?symbol={symbol}"
    )

    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if (
            "data" in data
            and len(data["data"]) > 0
        ):

            ticker = data["data"][0]

            print(f"{symbol}")
            print(
                f"Price: "
                f"${ticker['lastPr']}"
            )
            print()

        else:
            print(
                f"{symbol}: "
                "No data"
            )

    except Exception as e:
        print(
            f"{symbol}: "
            f"Error - {e}"
        )