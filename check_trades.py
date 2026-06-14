import pandas as pd

df = pd.read_csv("signals.csv")

print("\n===== OPEN TRADES =====\n")

print(
    df[
        df["status"] == "OPEN"
    ]
)

print("\n=======================\n")