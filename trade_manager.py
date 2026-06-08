import csv
from bitget_data import get_bitget_price

rows = []

with open("signals.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row["status"] == "OPEN":

            coin = row["coin"]

            symbol = f"{coin}USDT"

            current_price = get_bitget_price(symbol)

            entry_price = float(row["entry_price"])

            if current_price is None:
                rows.append(row)
                continue

            pnl = (
                (current_price - entry_price)
                / entry_price
            ) * 100

            if abs(pnl) >= 2:
                row["status"] = "CLOSED"

            rows.append(row)

with open("signals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "timestamp",
            "coin",
            "signal",
            "confidence",
            "entry_price",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("Trade update complete")