import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    response = requests.get(url)

    data = response.json()

    if coin_id not in data:
        return None

    return data[coin_id]["usd"]


print("\n====================")
print(" Portfolio Mode")
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

prompt = f"""
Analyze this crypto portfolio:

{portfolio_data}

Provide:

1. Portfolio Health Score (0-100)
2. Strongest Asset
3. Highest Risk Asset
4. Overall Outlook
5. Short Narrative Analysis

Keep response concise.
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
print(" Portfolio Analysis")
print("====================\n")

print(response.choices[0].message.content)