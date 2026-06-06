import csv
import os
from datetime import datetime

FILE_NAME = "signals.csv"

def save_signal(coin, signal, confidence):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "coin",
                "signal",
                "confidence"
            ])

        writer.writerow([
            datetime.now(),
            coin,
            signal,
            confidence
        ])