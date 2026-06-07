
# AlphaLens Paper Trading V7
# Full replacement file generated for CSV schema:
# timestamp,coin,signal,confidence,entry_price,status

import os
import csv
import time
import statistics
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "BNB": "binancecoin",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "SUI": "sui",
    "APT": "aptos",
    "ARB": "arbitrum",
    "OP": "optimism",
    "TRX": "tron"
}

def get_price(symbol):
    coin_id = COIN_MAP.get(symbol.upper())
    if not coin_id:
        return None
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd",
            timeout=10,
            headers={"User-Agent":"AlphaLens-V7"}
        )
        r.raise_for_status()
        return float(r.json()[coin_id]["usd"])
    except Exception:
        return None

def ai_review(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen3.6-plus",
            messages=[{"role":"user","content":prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI unavailable: {e}"

print("\n===== ALPHALENS V7 =====\n")

trades = []

with open("paper_trades.csv","r",encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:

        coin = row["coin"].upper().strip()
        signal = row["signal"].upper().strip()
        confidence = float(row["confidence"])
        entry = float(row["entry_price"])
        status = row["status"].upper().strip()

        current = get_price(coin)

        if current is None:
            continue

        pnl = ((current-entry)/entry)*100

        trades.append({
            "timestamp": row["timestamp"],
            "coin": coin,
            "signal": signal,
            "confidence": confidence,
            "entry": entry,
            "current": current,
            "status": status,
            "pnl": pnl
        })

        time.sleep(1)

if not trades:
    print("No valid trades found.")
    raise SystemExit

winning = len([t for t in trades if t["pnl"] >= 0])
losing = len([t for t in trades if t["pnl"] < 0])

win_rate = (winning / len(trades)) * 100
avg_pnl = statistics.mean([t["pnl"] for t in trades])
avg_confidence = statistics.mean([t["confidence"] for t in trades])
total_pnl = sum([t["pnl"] for t in trades])

best_trade = max(trades, key=lambda x:x["pnl"])
worst_trade = min(trades, key=lambda x:x["pnl"])

risk = "LOW" if win_rate >= 70 else "MEDIUM" if win_rate >= 50 else "HIGH"

health_score = min(
    round((win_rate * 0.5) + (avg_confidence * 0.3) + (max(avg_pnl,0) * 0.2),2),
    100
)

portfolio_status = (
    "EXCELLENT"
    if health_score >= 80 else
    "GOOD"
    if health_score >= 60 else
    "NEUTRAL"
    if health_score >= 40 else
    "WEAK"
)

leaderboard = sorted(
    trades,
    key=lambda x:x["pnl"],
    reverse=True
)

with open("leaderboard.txt","w",encoding="utf-8") as f:
    for i, trade in enumerate(leaderboard, start=1):
        f.write(
            f"{i}. {trade['coin']} | "
            f"PnL {trade['pnl']:.2f}% | "
            f"Confidence {trade['confidence']}\n"
        )

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

with open("trade_recommendations.txt","w",encoding="utf-8") as f:
    f.write("\n".join(recommendations))

metrics = f'''
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
'''

with open("portfolio_metrics.txt","w",encoding="utf-8") as f:
    f.write(metrics)

portfolio_prompt = f'''
Analyze this portfolio.

Trades: {len(trades)}
Win Rate: {win_rate:.2f}%
Average PnL: {avg_pnl:.2f}%
Average Confidence: {avg_confidence:.2f}
Risk Rating: {risk}
Health Score: {health_score}

Provide assessment, strengths, weaknesses,
risk analysis and actions.
'''

review = ai_review(portfolio_prompt)

with open("trade_review.txt","w",encoding="utf-8") as f:
    f.write(review)

report = []
report.append("AlphaLens V7 Report")
report.append("="*40)
report.append(metrics)
report.append(f"Best Trade: {best_trade['coin']} ({best_trade['pnl']:.2f}%)")
report.append(f"Worst Trade: {worst_trade['coin']} ({worst_trade['pnl']:.2f}%)")
report.append("")
report.append("Recommendations")
report.extend(recommendations)

with open("paper_trading_report.txt","w",encoding="utf-8") as f:
    f.write("\n".join(report))

print(metrics)
print("\nBest Trade:", best_trade["coin"])
print("Worst Trade:", worst_trade["coin"])
print("\nFiles generated successfully.")

# AlphaLens Paper Trading V7
# Full replacement file generated for CSV schema:
# timestamp,coin,signal,confidence,entry_price,status

import os
import csv
import time
import statistics
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "BNB": "binancecoin",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "SUI": "sui",
    "APT": "aptos",
    "ARB": "arbitrum",
    "OP": "optimism",
    "TRX": "tron"
}

def get_price(symbol):
    coin_id = COIN_MAP.get(symbol.upper())
    if not coin_id:
        return None
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd",
            timeout=10,
            headers={"User-Agent":"AlphaLens-V7"}
        )
        r.raise_for_status()
        return float(r.json()[coin_id]["usd"])
    except Exception:
        return None

def ai_review(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen3.6-plus",
            messages=[{"role":"user","content":prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI unavailable: {e}"

print("\n===== ALPHALENS V7 =====\n")

trades = []

with open("paper_trades.csv","r",encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:

        coin = row["coin"].upper().strip()
        signal = row["signal"].upper().strip()
        confidence = float(row["confidence"])
        entry = float(row["entry_price"])
        status = row["status"].upper().strip()

        current = get_price(coin)

        if current is None:
            continue

        pnl = ((current-entry)/entry)*100

        trades.append({
            "timestamp": row["timestamp"],
            "coin": coin,
            "signal": signal,
            "confidence": confidence,
            "entry": entry,
            "current": current,
            "status": status,
            "pnl": pnl
        })

        time.sleep(1)

if not trades:
    print("No valid trades found.")
    raise SystemExit

winning = len([t for t in trades if t["pnl"] >= 0])
losing = len([t for t in trades if t["pnl"] < 0])

win_rate = (winning / len(trades)) * 100
avg_pnl = statistics.mean([t["pnl"] for t in trades])
avg_confidence = statistics.mean([t["confidence"] for t in trades])
total_pnl = sum([t["pnl"] for t in trades])

best_trade = max(trades, key=lambda x:x["pnl"])
worst_trade = min(trades, key=lambda x:x["pnl"])

risk = "LOW" if win_rate >= 70 else "MEDIUM" if win_rate >= 50 else "HIGH"

health_score = min(
    round((win_rate * 0.5) + (avg_confidence * 0.3) + (max(avg_pnl,0) * 0.2),2),
    100
)

portfolio_status = (
    "EXCELLENT"
    if health_score >= 80 else
    "GOOD"
    if health_score >= 60 else
    "NEUTRAL"
    if health_score >= 40 else
    "WEAK"
)

leaderboard = sorted(
    trades,
    key=lambda x:x["pnl"],
    reverse=True
)

with open("leaderboard.txt","w",encoding="utf-8") as f:
    for i, trade in enumerate(leaderboard, start=1):
        f.write(
            f"{i}. {trade['coin']} | "
            f"PnL {trade['pnl']:.2f}% | "
            f"Confidence {trade['confidence']}\n"
        )

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

with open("trade_recommendations.txt","w",encoding="utf-8") as f:
    f.write("\n".join(recommendations))

metrics = f'''
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
'''

with open("portfolio_metrics.txt","w",encoding="utf-8") as f:
    f.write(metrics)

portfolio_prompt = f'''
Analyze this portfolio.

Trades: {len(trades)}
Win Rate: {win_rate:.2f}%
Average PnL: {avg_pnl:.2f}%
Average Confidence: {avg_confidence:.2f}
Risk Rating: {risk}
Health Score: {health_score}

Provide assessment, strengths, weaknesses,
risk analysis and actions.
'''

review = ai_review(portfolio_prompt)

with open("trade_review.txt","w",encoding="utf-8") as f:
    f.write(review)

report = []
report.append("AlphaLens V7 Report")
report.append("="*40)
report.append(metrics)
report.append(f"Best Trade: {best_trade['coin']} ({best_trade['pnl']:.2f}%)")
report.append(f"Worst Trade: {worst_trade['coin']} ({worst_trade['pnl']:.2f}%)")
report.append("")
report.append("Recommendations")
report.extend(recommendations)

with open("paper_trading_report.txt","w",encoding="utf-8") as f:
    f.write("\n".join(report))

print(metrics)
print("\nBest Trade:", best_trade["coin"])
print("Worst Trade:", worst_trade["coin"])
print("\nFiles generated successfully.")
