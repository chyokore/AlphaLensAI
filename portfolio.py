
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# =========================
# COINGECKO FUNCTIONS
# =========================

def get_price(coin_id):
    """
    Fetch current USD price for a coin.
    """
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies=usd"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if coin_id not in data:
            return None

        return data[coin_id]["usd"]

    except Exception:
        return None


def get_trending_coins():
    """
    Fetch top trending coins.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        return [
            coin["item"]["symbol"].upper()
            for coin in data["coins"][:5]
        ]

    except Exception:
        return []


def get_global_market():
    """
    Fetch global crypto market data.
    """
    url = "https://api.coingecko.com/api/v3/global"

    try:
        response = requests.get(url, timeout=10)

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


def get_fear_greed():
    """
    Fetch Fear & Greed Index.
    """
    url = "https://api.alternative.me/fng/"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        value = data["data"][0]["value"]
        classification = (
            data["data"][0]["value_classification"]
        )

        return value, classification

    except Exception:
        return None, "Unavailable"


# =========================
# ALPHALENS DASHBOARD
# =========================

print("\n====================================")
print("   AlphaLens Portfolio Intelligence")
print("====================================\n")

# =========================
# TRENDING COINS
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
# GLOBAL MARKET DATA
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
# FEAR & GREED INDEX
# =========================

fear_value, fear_classification = (
    get_fear_greed()
)

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
# USER PORTFOLIO INPUT
# =========================

coins = input(
    "Enter coins separated by commas "
    "(bitcoin,ethereum,sui,solana): "
).strip()

if not coins:
    print("❌ No coins entered.")
    exit()

coin_list = [
    coin.strip().lower()
    for coin in coins.split(",")
    if coin.strip()
]

portfolio_data = []
portfolio_prompt_data = []

print("\n📊 Portfolio Summary")
print("----------------------------")

for coin in coin_list:

    price = get_price(coin)

    if price:

        print(
            f"{coin.upper():<12} "
            f"${price:,.4f}"
        )

        portfolio_data.append({
            "coin": coin,
            "price": price
        })

        portfolio_prompt_data.append(
            f"{coin.upper()} : "
            f"${price:,.4f}"
        )

    else:

        print(
            f"{coin.upper():<12} "
            f"Coin not found"
        )

# =========================
# BUILD AI PROMPT
# =========================

prompt = f"""
You are AlphaLens AI.

You are an institutional-grade crypto portfolio analyst,
market strategist,
and risk manager.

Portfolio Data:

{chr(10).join(portfolio_prompt_data)}

Trending Coins:

{', '.join(trending) if trending else 'None'}

Global Market Data:

Market Cap:
${market_cap_t:.2f}T

24h Volume:
${volume_b:.2f}B

BTC Dominance:
{global_data['btc_dominance']:.2f}%

Market Structure:
{market_structure}

Market Sentiment:
{market_sentiment}

Fear & Greed:
{fear_classification}

Provide:

1. Portfolio Health Score (0-100)

2. Portfolio Risk Score (0-100)

3. Diversification Score (0-100)

4. Market Sentiment
(Bullish, Neutral, Bearish)

5. Strongest Asset
(Explain why)

6. Highest Risk Asset
(Explain why)

7. Buy / Hold / Reduce signal
for each asset

8. Recommended Allocation

Example:

BTC: 40%
ETH: 25%
SOL: 15%
SUI: 10%
USDT: 10%

9. Opportunity Watchlist

Suggest 3 assets worth monitoring.

Explain:
- upside potential
- risks
- narrative

10. Market Narrative

Cover:
- Bitcoin trend
- Altcoin trend
- Risk appetite
- Macro environment

11. Risk Management Advice

12. AI Confidence Score

13. Executive Summary

14. Final Trading Stance

Choose ONE:

Strong Buy
Buy
Selective Buy
Hold
Rebalance
Reduce Risk
Defensive

Keep the report concise,
professional,
institutional-grade,
and under 700 words.
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
                "content": (
                    "You are AlphaLens AI, "
                    "an institutional-grade "
                    "crypto portfolio strategist."
                )
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
print("      AlphaLens Portfolio Analysis")
print("====================================\n")

print(report)

# =========================
# SAVE REPORT
# =========================

try:

    with open(
        "portfolio_report.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    print(
        "\n✅ Portfolio report saved as "
        "'portfolio_report.txt'"
    )

except Exception as e:

    print(
        f"\n❌ Failed to save report: {e}"
    )
