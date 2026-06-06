import csv
import os
from datetime import datetime
from time import perf_counter

start = perf_counter()

print("\n====================")
print(" AlphaLens Trade Journal")
print("====================\n")

coin = input("Coin: ").strip().lower()

signal = input(
    "Signal (BUY/HOLD/REDUCE): "
).strip().upper()

confidence = input(
    "Confidence Score (0-100): "
).strip()

entry_price = input(
    "Entry Price (USD): "
).strip()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

file_name = "paper_trades.csv"

# Create header if file doesn't exist
file_exists = os.path.isfile(file_name)

with open(
    file_name,
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
            "status"
        ])

    writer.writerow([
        timestamp,
        coin,
        signal,
        confidence,
        entry_price,
        "OPEN"
    ])

print("\n✅ Trade saved successfully!")

print("\nTrade Details")
print("--------------------")

print(f"Coin: {coin.upper()}")
print(f"Signal: {signal}")
print(f"Confidence: {confidence}%")
print(f"Entry Price: ${entry_price}")
print("Status: OPEN")
end = perf_counter()

print(f"\nExecution Time: {end - start:.4f} seconds")