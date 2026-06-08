import csv
import os
from bitget_data import get_bitget_price

FILE_NAME = "signals.csv"

SYMBOL_MAP = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
    "DOGE": "DOGEUSDT",
    "ADA": "ADAUSDT",
    "BNB": "BNBUSDT",
    "AVAX": "AVAXUSDT",
    "DOT": "DOTUSDT",
    "LINK": "LINKUSDT",
    "SUI": "SUIUSDT",
    "APT": "APTUSDT",
    "ARB": "ARBUSDT",
    "OP": "OPUSDT",
    "TRX": "TRXUSDT"
}

TAKE_PROFIT = 1.00
STOP_LOSS = -1.00

rows = []

print("\n====================================")
print("      AlphaLens Trade Tracker")
print("====================================\n")

if not os.path.exists(FILE_NAME):
    print(f"ERROR: {FILE_NAME} not found.")
    exit()

with open(FILE_NAME, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        # Skip completely empty rows
        if not row:
            continue

        status = str(
            row.get("status") or "OPEN"
        ).strip().upper()

        coin = str(
            row.get("coin") or ""
        ).strip().upper()

        signal = str(
            row.get("signal") or ""
        ).strip().upper()

        # Skip already closed trades
        if status == "CLOSED":
            rows.append(row)
            continue

        if coin not in SYMBOL_MAP:
            print(f"Skipping {coin} - Unsupported coin")
            rows.append(row)
            continue

        try:
            entry_price = float(
                row.get("entry_price") or 0
            )
        except ValueError:
            print(f"Invalid entry price for {coin}")
            rows.append(row)
            continue

        current_price = get_bitget_price(
            SYMBOL_MAP[coin]
        )

        if current_price is None:
            print(f"Could not fetch price for {coin}")
            rows.append(row)
            continue

        try:
            current_price = float(current_price)
        except:
            print(f"Invalid current price for {coin}")
            rows.append(row)
            continue

        print(f"\nChecking {coin}")
        print(f"Signal: {signal}")
        print(f"Entry Price: {entry_price}")
        print(f"Current Price: {current_price}")

        # BUY signal
        if signal == "BUY":

            pnl = (
                (current_price - entry_price)
                / entry_price
            ) * 100

        # REDUCE = short/demo sell
        elif signal == "REDUCE":

            pnl = (
                (entry_price - current_price)
                / entry_price
            ) * 100

        else:

            pnl = 0

        print(f"PnL: {pnl:.2f}%")

        # Trade close logic

        if pnl >= TAKE_PROFIT:

            row["status"] = "CLOSED"
            row["exit_price"] = str(current_price)
            row["pnl_percent"] = f"{pnl:.2f}"

            print("✅ PROFIT TARGET HIT")
            print("Trade CLOSED")

        elif pnl <= STOP_LOSS:

            row["status"] = "CLOSED"
            row["exit_price"] = str(current_price)
            row["pnl_percent"] = f"{pnl:.2f}"

            print("❌ STOP LOSS HIT")
            print("Trade CLOSED")

        else:

            row["status"] = "OPEN"
            row["exit_price"] = row.get(
                "exit_price", ""
            )
            row["pnl_percent"] = row.get(
                "pnl_percent", ""
            )

            print("⏳ Trade still OPEN")

        rows.append(row)

# Save updated CSV

fieldnames = [
    "timestamp",
    "coin",
    "signal",
    "confidence",
    "entry_price",
    "exit_price",
    "pnl_percent",
    "status"
]

with open(
    FILE_NAME,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for row in rows:

        clean_row = {
            "timestamp": row.get("timestamp", ""),
            "coin": row.get("coin", ""),
            "signal": row.get("signal", ""),
            "confidence": row.get("confidence", ""),
            "entry_price": row.get("entry_price", ""),
            "exit_price": row.get("exit_price", ""),
            "pnl_percent": row.get("pnl_percent", ""),
            "status": row.get("status", "OPEN")
        }

        writer.writerow(clean_row)

print("\n====================================")
print("Trade scan complete.")
print("CSV updated successfully.")
print("====================================\n")