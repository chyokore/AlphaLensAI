import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

import pandas as pd

from market_data import (
    get_trending_coins,
    get_global_market,
    get_fear_greed
)

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# =========================
# ALPHALENS MARKET BRIEF
# =========================

print("\n====================================")
print("      AlphaLens Market Brief")
print("====================================\n")

# =========================
# MARKET CONTEXT
# =========================

portfolio_coins = []

if os.path.exists("signals.csv"):

    try:

        df = pd.read_csv(
            "signals.csv"
        )

        open_trades = df[
            df["status"] == "OPEN"
        ]

        portfolio_coins = (
            open_trades["coin"]
            .dropna()
            .unique()
            .tolist()
        )

    except Exception:

        portfolio_coins = []

trending = get_trending_coins()

market = get_global_market()

fear_value, fear_classification = (
    get_fear_greed()
)

market_cap = "Unknown"
volume = "Unknown"
btc_dom = "Unknown"

if market:

    market_cap = (
        f"${market['market_cap']/1_000_000_000_000:.2f}T"
    )

    volume = (
        f"${market['volume']/1_000_000_000:.2f}B"
    )

    btc_dom = (
        f"{market['btc_dominance']:.2f}%"
    )

prompt = f"""
You are AlphaLens AI.

You are an institutional-grade
crypto strategist.

Current Portfolio:

{', '.join(portfolio_coins) if portfolio_coins else 'No Open Positions'}

Trending Coins:

{', '.join(trending) if trending else 'Unavailable'}

Market Cap:
{market_cap}

24h Volume:
{volume}

BTC Dominance:
{btc_dom}

Fear & Greed:
{fear_classification}

Generate a Daily Market Brief.

Provide:

1. Market Mood

Choose one:

Strongly Bullish
Bullish
Neutral
Cautiously Bullish
Cautiously Bearish
Bearish

2. Confidence Score

Format exactly:

Confidence Score: XX/100

3. Top Opportunity

4. Highest Risk Asset

5. Market Narrative

Cover:

• Bitcoin Trend
• Altcoin Trend
• Liquidity Conditions
• Market Structure

6. Key Risk

7. Actionable Insight

8. Executive Summary

9. Final Market Stance

Choose one:

Strong Buy
Buy
Selective Buy
Hold
Reduce Risk
Defensive

Reference the portfolio holdings
when relevant.

Keep under 500 words.
"""

print("🤖 Generating AI Market Brief...\n")

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
        max_tokens=1000
    )

    report = (
        response
        .choices[0]
        .message
        .content
    )

except Exception as e:
    report = (
        "Market Brief unavailable.\n\n"
        f"Error: {str(e)}"
    )

# =========================
# DISPLAY REPORT
# =========================

print("====================================")
print("      AlphaLens Market Brief")
print("====================================\n")

print(report)

# =========================
# SAVE REPORT
# =========================

os.makedirs(
    "reports",
    exist_ok=True
)

filename = (
    "reports/market_brief_"
    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)

with open(
    filename,
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

print(
    f"\n✅ Market brief saved to "
    f"{filename}"
)