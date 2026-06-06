from openai import OpenAI
from market_data import get_btc_price

client = OpenAI(
    api_key="h1MsqprV9PxTxk9",
    base_url="https://hackathon.bitgetops.com/v1"
)

price = get_btc_price()

prompt = f"""
Current Bitcoin price is ${price}.

Give:
1. Market sentiment
2. Short-term outlook
3. Risk level

Keep response under 100 words.
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

print(response.choices[0].message.content)