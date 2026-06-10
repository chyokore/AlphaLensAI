import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from bitget_data import get_bitget_price
from market_data import get_trending_coins

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

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


def generate_signal(symbol):

    symbol = symbol.upper()

    if symbol not in SYMBOL_MAP:
        return None

    market_symbol = SYMBOL_MAP[symbol]

    price = get_bitget_price(
        market_symbol
    )

    if not price:
        return None

    prompt = f"""
You are AlphaLens AI.

Market Symbol:
{market_symbol}

Current Price:
${price}

Act as a professional crypto analyst.

Provide:

Trading Signal: BUY

or

Trading Signal: REDUCE

Confidence Score: XX/100

Keep response concise.
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

    report = response.choices[0].message.content

    signal = "BUY"
    confidence = 70

    signal_match = re.search(
        r"TRADING SIGNAL\s*:\s*(BUY|REDUCE)",
        report.upper()
    )

    if signal_match:
        signal = signal_match.group(1)

    confidence_match = re.search(
        r"CONFIDENCE\s*SCORE\s*:?\s*([0-9]{1,3})",
        report.upper()
    )

    if confidence_match:
        confidence = int(
            confidence_match.group(1)
        )

    return {
        "coin": symbol,
        "signal": signal,
        "confidence": confidence,
        "entry_price": price,
        "report": report
    }


def get_best_opportunity():

    trending = get_trending_coins()

    for coin in trending:

        coin = coin.upper()

        if coin in SYMBOL_MAP:

            result = generate_signal(
                coin
            )

            if result:
                return result

    return generate_signal("BTC")