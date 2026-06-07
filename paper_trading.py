import csv
import requests

# =========================
# COINGECKO PRICE FETCHER
# =========================

def get_price(coin_id):
    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies=usd"
    )

    response = requests.get(url)
    data = response.json()

    if coin_id not in data:
        return None

    return data[coin_id]["usd"]


# =========================
# PAPER TRADING
# =========================

print("\n====================")
print(" AlphaLens Paper Trading")
print("====================\n")

try:
    with open(
        "paper_trades.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for trade in reader:

            coin = trade["coin"]
            signal = trade["signal"]
            entry_price = float(trade["entry_price"])

            current_price = get_price(coin)

            if current_price is None:
                continue

            pnl = (
                (current_price - entry_price)
                / entry_price
            ) * 100

            status = (
                "WINNING"
                if pnl >= 0
                else "LOSING"
            )

            print("--------------------")
            print(f"Coin: {coin.upper()}")
            print(f"Signal: {signal}")
            print(f"Entry Price: ${entry_price:,.2f}")
            print(f"Current Price: ${current_price:,.2f}")
            print(f"PnL: {pnl:.2f}%")
            print(f"Status: {status}")

except FileNotFoundError:
    print("paper_trades.csv not found.")