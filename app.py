import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create Qwen client
client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# Get crypto price from CoinGecko
def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    response = requests.get(url)

    data = response.json()

    if coin_id not in data:
        return None

    return data[coin_id]["usd"]


print("\n====================")
print("     AlphaLens AI")
print("====================\n")

coin = input(
    "Enter CoinGecko coin id (bitcoin, ethereum, solana, sui, dogecoin, etc): "
).lower()

language = input(
    "\nChoose language (English, Chinese, Spanish, Portuguese, French): "
)

print("\nFetching market data...\n")

price = get_price(coin)

if price is None:
    print("Coin not found.")
    exit()

print(f"Current price: ${price}")

print("\nAnalyzing market...\n")

prompt = f"""
Current {coin} price is ${price}.

Act as a professional crypto analyst.

Provide:

1. Market Sentiment
2. Short-Term Outlook
3. Risk Level
4. Trading Signal (BUY, SELL, HOLD)
5. Confidence Score (0-100)
6. Suggested Entry Price
7. Suggested Stop Loss
8. Suggested Take Profit
9. Key Risk Factors

Respond entirely in {language}.

Keep the response concise and structured.
"""

response = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\n====================")
print("  AlphaLens Report")
print("====================\n")

print(response.choices[0].message.content)