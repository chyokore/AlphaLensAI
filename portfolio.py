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
# MARKET DATA
# =========================

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    response = requests.get(url)
    data = response.json()

    if coin_id not in data:
        return None

    return data[coin_id]["usd"]


# =========================
# PORTFOLIO MODE
# =========================

print("\n====================")
print(" AlphaLens Portfolio Mode")
print("====================\n")

coins = input(
    "Enter coins separated by commas (bitcoin,ethereum,sui): "
)

coin_list = [coin.strip().lower() for coin in coins.split(",")]

portfolio_data = []

print("\nPortfolio Summary")
print("--------------------")

for coin in coin_list:
    price = get_price(coin)

    if price:
        print(f"{coin.upper()}: ${price}")
        portfolio_data.append(f"{coin}: ${price}")
    else:
        print(f"{coin.upper()}: Coin not found")

prompt = f"""
Analyze this crypto portfolio:

{portfolio_data}

Act as a professional crypto portfolio manager.

Provide:

1. Portfolio Health Score (0-100)

2. Overall Portfolio Sentiment
   (Bullish, Neutral, Bearish)

3. Strongest Asset
   (Explain why)

4. Highest Risk Asset
   (Explain why)

5. Portfolio Diversification Score
   (0-100)

6. AI Market Narrative
   (Summarize the current market environment)

7. Suggested Portfolio Actions
   (Buy, Hold, Reduce, Rebalance)

8. Risk Management Recommendations

9. Confidence Score (0-100)

Keep the response concise, professional, and easy to understand.
"""

print("\nGenerating AI Portfolio Analysis...\n")

response = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("====================")
print(" AlphaLens Portfolio Analysis")
print("====================\n")

report = response.choices[0].message.content

print("====================")
print(" AlphaLens Portfolio Analysis")
print("====================\n")

print(report)

with open("portfolio_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\nPortfolio report saved to portfolio_report.txt")