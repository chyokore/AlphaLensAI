import os
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
# ALPHALENS DAILY BRIEF
# =========================

print("\n====================")
print(" AlphaLens Daily Brief")
print("====================\n")

prompt = """
Act as a professional crypto market strategist.

Generate a Daily Market Brief.

Provide:

1. Market Mood
2. Confidence Score (0-100)
3. Top Opportunity
4. Highest Risk Asset
5. Market Narrative
6. Key Risk
7. Actionable Insight
8. One-Sentence Executive Summary

Keep the response concise, professional, and suitable for traders.
"""

print("Generating AI Market Brief...\n")

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
print(" AlphaLens Daily Brief")
print("====================\n")

print(response.choices[0].message.content)