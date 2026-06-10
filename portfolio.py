import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from bitget_data import get_bitget_price

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# =========================
# SYMBOL MAP
# =========================

SYMBOL_MAP = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "solana": "SOLUSDT",
    "sui": "SUIUSDT",
    "xrp": "XRPUSDT",
    "dogecoin": "DOGEUSDT",
    "cardano": "ADAUSDT",
    "binancecoin": "BNBUSDT",
    "avalanche-2": "AVAXUSDT",
    "polkadot": "DOTUSDT",
    "chainlink": "LINKUSDT"
}

# =========================
# BITGET PRICE FUNCTION
# =========================

def get_price(coin_id):
    symbol = SYMBOL_MAP.get(coin_id.lower())

    if not symbol:
        return None

    return get_bitget_price(symbol)

# =========================
# TRENDING COINS
# =========================

def get_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"

    try:
        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return [
            coin["item"]["symbol"].upper()
            for coin in data["coins"][:5]
        ]

    except Exception:
        return []

# =========================
# GLOBAL MARKET DATA
# =========================

def get_global_market():
    url = "https://api.coingecko.com/api/v3/global"

    try:
        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()["data"]

        return {
            "market_cap": data["total_market_cap"]["usd"],
            "volume": data["total_volume"]["usd"],
            "btc_dominance": data["market_cap_percentage"]["btc"]
        }

    except Exception:
        return None

# =========================
# FEAR & GREED
# =========================

def get_fear_greed():
    url = "https://api.alternative.me/fng/"

    try:
        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        value = data["data"][0]["value"]

        classification = data["data"][0]["value_classification"]

        return value, classification

    except Exception:
        return None, "Unavailable"

# =========================
# DASHBOARD
# =========================

print("\n====================================")
print(" AlphaLens Portfolio Intelligence")
print("====================================\n")

# =========================
# TRENDING
# =========================

trending = get_trending_coins()

if trending:
    print("🔥 Trending Coins")
    print("----------------------------")

    for idx, coin in enumerate(
        trending,
        start=1
    ):
        print(f"{idx}. {coin}")

    print()

# =========================
# GLOBAL MARKET
# =========================

global_data = get_global_market()

market_cap_t = 0
volume_b = 0
market_structure = "Unknown"
market_sentiment = "Neutral"

if global_data:
    market_cap_t = (
        global_data["market_cap"]
        / 1_000_000_000_000
    )

    volume_b = (
        global_data["volume"]
        / 1_000_000_000
    )

    btc_dom = global_data["btc_dominance"]

    if btc_dom >= 55:
        market_structure = "Bitcoin-Led Market"
        market_sentiment = "Risk-Off"

    elif btc_dom >= 50:
        market_structure = "Balanced Market"
        market_sentiment = "Neutral"

    else:
        market_structure = "Altcoin-Friendly Market"
        market_sentiment = "Risk-On"

    print("🌍 Global Market Overview")
    print("----------------------------")

    print(
        f"💰 Total Market Cap : "
        f"${market_cap_t:.2f}T"
    )

    print(
        f"📊 24h Volume       : "
        f"${volume_b:.2f}B"
    )

    print(
        f"₿ BTC Dominance     : "
        f"{btc_dom:.2f}%"
    )

    print(
        f"📈 Market Structure : "
        f"{market_structure}"
    )

    print(
        f"🔥 Market Sentiment : "
        f"{market_sentiment}"
    )

    print()

# =========================
# FEAR & GREED
# =========================

fear_value, fear_classification = get_fear_greed()

if fear_value:
    print("😨 Fear & Greed Index")
    print("----------------------------")

    print(
        f"Score : {fear_value}"
    )

    print(
        f"Sentiment : "
        f"{fear_classification}"
    )

    print()

# =========================
# PORTFOLIO INPUT
# =========================

import pandas as pd

portfolio_prompt_data = []

print("\n📊 Portfolio Summary")
print("----------------------------")

if not os.path.exists("signals.csv"):

    report = """
No active portfolio positions found.

Generate and place trades from the
dashboard before running Portfolio
Analysis.
"""

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        "reports/portfolio_report.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    print(report)

    exit()

df = pd.read_csv("signals.csv")

open_trades = df[
    df["status"] == "OPEN"
]

if len(open_trades) == 0:

    report = """
No active portfolio positions found.

Generate and place trades from the
dashboard before running Portfolio
Analysis.
"""

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        "reports/portfolio_report.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    print(report)

    exit()

unique_coins = (
    open_trades["coin"]
    .dropna()
    .unique()
    .tolist()
)

for coin in unique_coins:

    symbol = coin.upper()

    try:

        price = get_bitget_price(
            f"{symbol}USDT"
        )

        if price:

            print(
                f"{symbol:<12}"
                f"${price:,.4f}"
            )

            portfolio_prompt_data.append(
                f"{symbol}: ${price:,.4f}"
            )

    except Exception:

        print(
            f"{symbol:<12}"
            f"Price unavailable"
        )

# =========================
# AI PROMPT
# =========================

prompt = f"""
You are AlphaLens AI.

You are an institutional-grade crypto
portfolio analyst, market strategist,
and risk manager.

Portfolio Data:

{chr(10).join(portfolio_prompt_data)}

Trending Coins:

{', '.join(trending) if trending else 'None'}

Market Cap:
${market_cap_t:.2f}T

24h Volume:
${volume_b:.2f}B

Market Structure:
{market_structure}

Market Sentiment:
{market_sentiment}

Fear & Greed:
{fear_classification}

Provide:

1. Portfolio Health Score

2. Portfolio Risk Score

3. Diversification Score

4. Market Sentiment

5. Strongest Asset

6. Highest Risk Asset

7. Buy / Hold / Reduce
   for each asset

8. Recommended Allocation

9. Opportunity Watchlist

10. Market Narrative

11. Risk Management Advice

12. AI Confidence Score

13. Executive Summary

14. Final Trading Stance

Choose one:

Strong Buy
Buy
Selective Buy
Hold
Rebalance
Reduce Risk
Defensive

Keep response under 700 words.
"""

# =========================
# AI ANALYSIS
# =========================

print("\n🤖 Generating AI Analysis...\n")

try:
    response = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=[
            {
                "role": "system",
                "content": "You are AlphaLens AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1200
    )

    report = (
        response
        .choices[0]
        .message
        .content
    )

except Exception as e:
    report = (
        "AI Analysis unavailable.\n\n"
        f"Error: {str(e)}"
    )

# =========================
# DISPLAY REPORT
# =========================

print("\n====================================")
print(" AlphaLens Portfolio Analysis")
print("====================================\n")

print(report)

# =========================
# SAVE REPORT
# =========================

os.makedirs(
    "reports",
    exist_ok=True
)

with open(
    "reports/portfolio_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print(
    "\n✅ Portfolio report saved to "
    "reports/portfolio_report.txt"
)