# AlphaLens Paper Trading V7
# CSV Schema:
# timestamp,coin,signal,confidence,entry_price,status

import os
import csv
import time
import statistics
from dotenv import load_dotenv
from openai import OpenAI
from bitget_data import get_bitget_price

# =========================
# LOAD ENV
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# =========================
# AI REVIEW
# =========================

def ai_review(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen3.6-plus",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI unavailable: {e}"

# =========================
# START
# =========================

print("\n====================")
print(" ALPHALENS V7")
print("====================\n")

CSV_FILE = "paper_trades.csv"

if not os.path.exists(CSV_FILE):
    print("paper_trades.csv not found.")
    raise SystemExit

trades = []

# =========================
# LOAD TRADES
# =========================

with open(CSV_FILE, "r", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        try:

            coin = row["coin"].upper().strip()
            signal = row["signal"].upper().strip()
            confidence = float(row["confidence"])
            entry_price = float(row["entry_price"])
            status = row["status"].upper().strip()

            symbol = f"{coin}USDT"

            current_price = get_bitget_price(symbol)

            if current_price is None:
                print(f"Skipping {coin} (price unavailable)")
                continue

            pnl = (
                (current_price - entry_price)
                / entry_price
            ) * 100

            trades.append(
                {
                    "timestamp": row["timestamp"],
                    "coin": coin,
                    "signal": signal,
                    "confidence": confidence,
                    "entry": entry_price,
                    "current": current_price,
                    "status": status,
                    "pnl": pnl
                }
            )

            time.sleep(1)

        except Exception as e:
            print(f"Error processing row: {e}")

# =========================
# VALIDATION
# =========================

if len(trades) == 0:
    print("No valid trades found.")
    raise SystemExit

# =========================
# METRICS
# =========================

winning = len(
    [t for t in trades if t["pnl"] >= 0]
)

losing = len(
    [t for t in trades if t["pnl"] < 0]
)

win_rate = (winning / len(trades)) * 100

avg_pnl = statistics.mean(
    [t["pnl"] for t in trades]
)

avg_confidence = statistics.mean(
    [t["confidence"] for t in trades]
)

total_pnl = sum(
    [t["pnl"] for t in trades]
)

best_trade = max(
    trades,
    key=lambda x: x["pnl"]
)

worst_trade = min(
    trades,
    key=lambda x: x["pnl"]
)

# =========================
# RISK ENGINE
# =========================

if win_rate >= 70:
    risk = "LOW"
elif win_rate >= 50:
    risk = "MEDIUM"
else:
    risk = "HIGH"

health_score = min(
    round(
        (win_rate * 0.5)
        + (avg_confidence * 0.3)
        + (max(avg_pnl, 0) * 0.2),
        2
    ),
    100
)

if health_score >= 80:
    portfolio_status = "EXCELLENT"
elif health_score >= 60:
    portfolio_status = "GOOD"
elif health_score >= 40:
    portfolio_status = "NEUTRAL"
else:
    portfolio_status = "WEAK"

# =========================
# LEADERBOARD
# =========================

leaderboard = sorted(
    trades,
    key=lambda x: x["pnl"],
    reverse=True
)

with open(
    "leaderboard.txt",
    "w",
    encoding="utf-8"
) as f:

    for i, trade in enumerate(
        leaderboard,
        start=1
    ):

        f.write(
            f"{i}. "
            f"{trade['coin']} | "
            f"PnL {trade['pnl']:.2f}% | "
            f"Confidence {trade['confidence']}\n"
        )

# =========================
# RECOMMENDATIONS
# =========================

recommendations = []

for trade in trades:

    if trade["pnl"] > 10:
        action = "REDUCE"

    elif trade["pnl"] >= 0:
        action = "HOLD"

    else:
        action = "BUY"

    recommendations.append(
        f"{trade['coin']} | "
        f"Signal={trade['signal']} | "
        f"Confidence={trade['confidence']} | "
        f"PnL={trade['pnl']:.2f}% | "
        f"Action={action}"
    )

with open(
    "trade_recommendations.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(recommendations)
    )

# =========================
# PORTFOLIO METRICS
# =========================

metrics = f"""
Trades Analyzed: {len(trades)}
Winning Trades: {winning}
Losing Trades: {losing}
Win Rate: {win_rate:.2f}%
Average PnL: {avg_pnl:.2f}%
Total Portfolio PnL: {total_pnl:.2f}%
Average Confidence: {avg_confidence:.2f}
Risk Rating: {risk}
Health Score: {health_score}/100
Portfolio Status: {portfolio_status}
"""

with open(
    "portfolio_metrics.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(metrics)

# =========================
# AI REVIEW
# =========================

portfolio_prompt = f"""
Analyze this portfolio.

Trades: {len(trades)}
Win Rate: {win_rate:.2f}%
Average PnL: {avg_pnl:.2f}%
Average Confidence: {avg_confidence:.2f}
Risk Rating: {risk}
Health Score: {health_score}

Provide:
1. Assessment
2. Strengths
3. Weaknesses
4. Risk Analysis
5. Recommended Actions
"""

review = ai_review(
    portfolio_prompt
)

with open(
    "trade_review.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(review)

# =========================
# FINAL REPORT
# =========================

report = []

report.append("AlphaLens V7 Report")
report.append("=" * 40)
report.append(metrics)

report.append(
    f"Best Trade: "
    f"{best_trade['coin']} "
    f"({best_trade['pnl']:.2f}%)"
)

report.append(
    f"Worst Trade: "
    f"{worst_trade['coin']} "
    f"({worst_trade['pnl']:.2f}%)"
)

report.append("")
report.append("Recommendations")
report.extend(recommendations)

with open(
    "paper_trading_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(report)
    )

# =========================
# OUTPUT
# =========================

print(metrics)

print(
    f"\nBest Trade: "
    f"{best_trade['coin']} "
    f"({best_trade['pnl']:.2f}%)"
)

print(
    f"Worst Trade: "
    f"{worst_trade['coin']} "
    f"({worst_trade['pnl']:.2f}%)"
)

print("\nFiles generated successfully.")
print("leaderboard.txt")
print("trade_recommendations.txt")
print("portfolio_metrics.txt")
print("trade_review.txt")
print("paper_trading_report.txt")