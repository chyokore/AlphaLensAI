import csv
import os
from datetime import datetime

FILE_NAME = "signals.csv"

def save_signal(
    coin,
    signal,
    confidence,
    entry_price
):
    file_exists = os.path.isfile(FILE_NAME)

    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "coin",
                "signal",
                "confidence",
                "entry_price",
                "exit_price",
                "pnl_percent",
                "status"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            coin,
            signal,
            confidence,
            entry_price,
            "",
            "",
            "OPEN"
        ])

    print(
        f"✅ Trade logged: "
        f"{coin} | {signal} | "
        f"Entry: {entry_price} | OPEN"
    )