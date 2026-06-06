import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
api_key=os.getenv("QWEN_API_KEY"),
base_url="https://hackathon.bitgetops.com/v1"
)

response = client.chat.completions.create(
model="qwen3.6-plus",
messages=[
{
"role": "user",
"content": "Give me a short analysis of Bitcoin market sentiment."
}
]
)

print(response.choices[0].message.content)
