import os
from datetime import datetime
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

print("\n====================================")
print("      AlphaLens Market Brief")
print("====================================\n")

prompt = """
You are AlphaLens AI.

You are an institutional-grade crypto
market strategist.

Generate a professional Daily Market Brief.

Provide:

1. Market Mood

Choose one:

* Strongly Bullish
* Bullish
* Neutral
* Cautiously Bullish
* Cautiously Bearish
* Bearish

2. Confidence Score

Format exactly as:

Confidence Score: XX/100

3. Top Opportunity

4. Highest Risk Asset

5. Market Narrative

Cover:

* Bitcoin trend
* Altcoin trend
* Liquidity conditions
* Market structure

6. Key Risk

7. Actionable Insight

8. One-Sentence Executive Summary

9. Final Market Stance

Choose one:

Strong Buy
Buy
Selective Buy
Hold
Reduce Risk
Defensive

Keep the report concise,
professional,
institutional-grade,
and under 500 words.
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