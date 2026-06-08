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

# ALPHALENS MARKET BRIEF

# =========================

print("\n====================")
print(" AlphaLens AI Market Brief")
print("====================\n")

prompt = """
Act as a professional crypto market strategist.

Generate an AlphaLens Daily Market Brief.

Use EXACTLY the following format:

1. Market Mood

2. Confidence Score (0-100)

3. Top Opportunity

4. Highest Risk Asset

5. Market Narrative

6. Key Risk

7. Actionable Insight

8. Executive Summary

Rules:

* Keep each section concise.
* Do not add extra sections.
* Do not change the order.
* Use professional language suitable for traders.
* Keep the entire report under 250 words.
  """

print("Generating market brief...\n")

response = client.chat.completions.create(
model="qwen3.6-plus",
messages=[
{
"role": "user",
"content": prompt
}
]
)

brief = response.choices[0].message.content

print("====================")
print(" AlphaLens Daily Brief")
print("====================\n")

print(brief)

# Save report

with open("market_brief.txt", "w", encoding="utf-8") as file:
    file.write(brief)

print("\nMarket brief saved to market_brief.txt")