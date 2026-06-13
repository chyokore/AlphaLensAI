import os
import re
import random

from dotenv import load_dotenv
from openai import OpenAI

from bitget_data import get_bitget_price

load_dotenv()

client = OpenAI(
api_key=os.getenv("QWEN_API_KEY"),
base_url="https://hackathon.bitgetops.com/v1"
)

# =========================

# SUPPORTED COINS

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

# HIGH-CONVICTION WATCHLIST

# =========================

WATCHLIST = [
"BTC",
"ETH",
"SOL",
"XRP",
"BNB",
"SUI"
]

# =========================

# SIGNAL GENERATION

# =========================

def generate_signal(symbol):
    symbol = symbol.upper()

    if symbol not in SYMBOL_MAP:
        return None

    market_symbol = SYMBOL_MAP[symbol]

    price = get_bitget_price(market_symbol)

    if not price:
        return None

    prompt = f"""
You are AlphaLens AI.

Market Symbol:
{market_symbol}

Current Price:
${price}

Act as a professional crypto analyst.

Provide exactly:

Trading Signal: BUY

or

Trading Signal: REDUCE

Confidence Score: XX/100

Keep response concise.
"""

    try:
        response = client.chat.completions.create(
            model="qwen3.6-plus",
            messages=[{"role": "user", "content": prompt}]
        )

        report = response.choices[0].message.content

    except Exception as e:
        print(f"Signal generation error for {symbol}: {e}")
        return None

    signal = "BUY"
    confidence = 70

    signal_match = re.search(r"TRADING SIGNAL\s*:\s*(BUY|REDUCE)", report.upper())
    if signal_match:
        signal = signal_match.group(1)

    confidence_match = re.search(r"CONFIDENCE\s*SCORE\s*:\s*([0-9]{1,3})", report.upper())
    if confidence_match:
        confidence = int(confidence_match.group(1))

    return {"coin": symbol, "signal": signal, "confidence": confidence, "entry_price": price, "report": report}


# =========================

# BEST OPPORTUNITY

# =========================

def get_best_opportunity():
    coin = random.choice(WATCHLIST)
    print(f"Selected Coin: {coin}")
    return generate_signal(coin)

