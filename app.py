import os
import re
import sys
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from signal_logger import save_signal
from bitget_data import get_bitget_price

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

# =========================
# SYMBOL MAP
# =========================

SYMBOL_MAP = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
    "DOGE": "DOGEUSDT",
    "ADA": "ADAUSDT",
    "BNB": "BNBUSDT",
    "AVAX": "AVAXUSDT",
    "DOT": "DOTUSDT",
    "LINK": "LINKUSDT",
    "SUI": "SUIUSDT",
    "APT": "APTUSDT",
    "ARB": "ARBUSDT",
    "OP": "OPUSDT",
    "TRX": "TRXUSDT"
}

# =========================
# HEADER
# =========================

print("\n====================================")
print("        AlphaLens AI V9")
print("====================================\n")

symbol = input(
    "Enter symbol (BTC, ETH, SOL, XRP, SUI, DOGE): "
).upper()

language = input(
    "\nChoose language "
    "(English, Chinese, Spanish, Portuguese, French): "
)

if symbol not in SYMBOL_MAP:
    print("\n❌ Unsupported symbol.")
    sys.exit()

market_symbol = SYMBOL_MAP[symbol]

# =========================
# MARKET DATA
# =========================

print("\nFetching Bitget market data...\n")

price = get_bitget_price(market_symbol)

if price is None:
    print("\n❌ Unable to fetch Bitget price.")
    sys.exit()

print(
    f"{market_symbol} Price: "
    f"${price:,.4f}"
)

# =========================
# AI ANALYSIS
# =========================

print("\nGenerating AlphaLens Analysis...\n")

prompt = f"""
You are AlphaLens AI.

Market Symbol:
{market_symbol}

Current Price:
${price}

Act as a professional crypto analyst.

Provide:

1. Market Sentiment

2. Short-Term Outlook

3. Risk Level

4. Trading Signal

Format exactly as:

Trading Signal: BUY

or

Trading Signal: HOLD

or

Trading Signal: REDUCE

5. Confidence Score

Format exactly as:

Confidence Score: XX/100

6. Suggested Entry Price

7. Suggested Stop Loss

8. Suggested Take Profit

9. AI Market Narrative

10. Key Risk Factors

Respond entirely in {language}.

IMPORTANT:
Always keep these two fields in English:

For simulation purposes, always return either BUY or REDUCE.
Do not return HOLD.
Confidence Score: XX/100

Keep the report concise,
professional,
and easy to understand.
"""

try:
    response = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    report = response.choices[0].message.content

    print("\n===== RAW AI RESPONSE =====")
    print(report)
    print("==========================\n")

except Exception as e:
    report = (
        f"AI analysis unavailable.\n\n"
        f"Error: {str(e)}"
    )

# =========================
# DISPLAY REPORT
# =========================

print("\n====================================")
print("      AlphaLens Report")
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
    "reports/report_"
    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)

with open(
    filename,
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

print(
    f"\n✅ Report saved to "
    f"{filename}"
)

# =========================
# SIGNAL EXTRACTION
# =========================

signal = "UNKNOWN"
confidence = "0"

try:
    report_upper = report.upper()

    # =========================
    # SIGNAL
    # =========================

    signal_patterns = [
        r"TRADING SIGNAL\s*:\s*(BUY)",
        r"TRADING SIGNAL\s*:\s*(HOLD)",
        r"TRADING SIGNAL\s*:\s*(REDUCE)"
    ]

    for pattern in signal_patterns:
        signal_match = re.search(
            pattern,
            report_upper,
            re.IGNORECASE
        )

        if signal_match:
            signal = signal_match.group(1).upper()
            break

    # =========================
    # CONFIDENCE
    # =========================

    confidence_patterns = [
        r"CONFIDENCE\s*SCORE\s*:?\s*([0-9]{1,3})\s*/\s*100",
        r"CONFIDENCE\s*SCORE\s*:?\s*([0-9]{1,3})",
        r"CONFIDENCE\s*:?\s*([0-9]{1,3})"
    ]

    confidence_match = None

    for pattern in confidence_patterns:
        confidence_match = re.search(
            pattern,
            report_upper,
            re.IGNORECASE | re.DOTALL
        )

        if confidence_match:
            score = int(confidence_match.group(1))

            if 0 <= score <= 100:
                confidence = str(score)
                break

    # =========================
    # DEBUG
    # =========================

    print("\n===== CONFIDENCE DEBUG =====")

    if confidence_match:
        print("✅ Match found")
        print("Pattern:", pattern)
        print("Extracted:", confidence_match.group(1))
    else:
        print("❌ No confidence match found")

        print("\nFirst 1000 chars of report:")
        print(report_upper[:1000])

        print("\nPattern Tests:")

        for test_pattern in confidence_patterns:
            test_match = re.search(
                test_pattern,
                report_upper,
                re.IGNORECASE | re.DOTALL
            )

            print(f"Testing: {test_pattern}")

            if test_match:
                print("✅ MATCH")
                print("Value:", test_match.group(1))
            else:
                print("❌ No Match")

    print("============================\n")

except Exception as e:
    print(f"\nConfidence extraction error: {e}")
# =========================
# SAVE SIGNAL
# =========================

print("\n===== EXTRACTED SIGNAL =====")
print(f"Coin: {symbol}")
print(f"Signal: {signal}")
print(f"Confidence: {confidence}")
print("============================\n")

save_signal(
    coin=symbol,
    signal=signal,
    confidence=confidence,
    entry_price=price
)

print("\n✅ Signal saved successfully!")
print(f"Signal: {signal}")
print(f"Confidence: {confidence}")