import streamlit as st
import pandas as pd
import os   
import sys

from signal_engine import (
    get_best_opportunity
)
from signal_logger import save_signal
from translations import TRANSLATIONS
from translator import translate_text
from market_data import (
get_trending_coins,
get_global_market,
get_fear_greed
)

# =========================

# PAGE CONFIG

# =========================

st.set_page_config(
page_title="AlphaLens AI",
page_icon="🚀",
layout="wide"
)

# =========================

# LANGUAGE

# =========================

language = st.sidebar.selectbox(
"🌐 Language",
[
"English",
"Chinese",
"Portuguese",
"Spanish",
"French"
]
)

T = TRANSLATIONS[language]

# =========================

# HEADER

# =========================

st.title(f"🚀 {T['title']}")
st.subheader(T["subtitle"])

st.markdown("---")

# =========================
# AI ACTION CENTER
# =========================

import csv
from datetime import datetime

# =========================
# ACTION BUTTONS
# =========================

st.markdown("---")
st.header("⚡ AI Action Center")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button("📊 Portfolio Analysis"):

        with st.spinner(
            "Generating portfolio analysis..."
        ):

            os.system(
    f"{sys.executable} portfolio.py"
)

        st.success(
            "Portfolio report updated."
        )

        st.rerun()

with col2:

    if st.button("📰 Market Brief"):

        with st.spinner(
            "Generating market brief..."
        ):

            os.system(
                f"{sys.executable} market_brief.py"
            )

        st.success(
            "Market brief updated."
        )

        st.rerun()

with col3:

    if st.button("📈 Update Trades"):

        with st.spinner(
            "Updating trades..."
        ):

            os.system(
                f"{sys.executable} trade_tracker.py"
            )

        st.success(
            "Trades updated."
        )

        st.rerun()

with col4:

    if st.button("🤖 Generate Signal"):

        

        with st.spinner(
            "Generating AI signal..."
        ):

            signal = (
                get_best_opportunity()
            )

            st.session_state[
                "pending_signal"
            ] = signal

        st.success(
            "Signal generated."
        )

        st.rerun()

# =========================
# REFRESH
# =========================

if st.button(
    "🔄 Refresh Dashboard"
):

    st.rerun()

# =========================
# PENDING TRADE
# =========================

st.markdown("---")

st.header(
    "📋 Pending Trade"
)

pending = st.session_state.get(
    "pending_signal"
)

if pending:

    col1, col2 = st.columns(2)

    col1.metric(
        "Coin",
        pending["coin"]
    )

    col2.metric(
        "Signal",
        pending["signal"]
    )

    col1.metric(
        "Confidence",
        pending["confidence"]
    )

    col2.metric(
        "Entry Price",
        f"${pending['entry_price']:.4f}"
    )

    st.text_area(
        "AI Report",
        pending["report"],
        height=150
    )

    col1, col2 = st.columns(2)

with col1:

    if st.button(
        "✅ Place Order"
    ):

        save_signal(
            coin=pending["coin"],
            signal=pending["signal"],
            confidence=pending["confidence"],
            entry_price=pending["entry_price"]
        )

        os.system(
            f"{sys.executable} portfolio.py"
        )

        os.system(
            f"{sys.executable} market_brief.py"
        )

        del st.session_state[
            "pending_signal"
        ]

        st.success(
            "Trade placed successfully."
        )

        st.rerun()

    with col2:

        if st.button(
            "🔄 Generate New Signal"
        ):

            st.session_state[
                "pending_signal"
            ] = (
                get_best_opportunity()
            )

            st.rerun()

else:

    st.info(
        "Generate a signal to create a pending trade."
    )

# =========================
# LOAD SIGNALS
# =========================

df = pd.DataFrame()

if os.path.exists(
    "signals.csv"
):
    try:
        df = pd.read_csv(
            "signals.csv"
        )
    except Exception:
        df = pd.DataFrame()

# =========================
# PLATFORM OVERVIEW
# =========================

st.header(f"📊 {T['overview']}")

if not df.empty:
    closed = df[
        df["status"] == "CLOSED"
    ]

    total_signals = len(df)

    total_closed = len(closed)

    open_trades_count = len(
        df[df["status"] == "OPEN"]
    )

    wins = 0
    losses = 0
    win_rate = 0
    avg_pnl = 0
    health_score = 0

    if total_closed > 0:

        pnl = pd.to_numeric(
            closed["pnl_percent"],
            errors="coerce"
        )

        wins = len(
            pnl[pnl >= 0]
        )

        losses = len(
            pnl[pnl < 0]
        )

        win_rate = (
            wins / total_closed
        ) * 100

        avg_pnl = pnl.mean()

        health_score = min(
            round(
                (
                    win_rate * 0.7
                )
                +
                (
                    max(avg_pnl, 0)
                    * 0.3
                ),
                2
            ),
            100
        )

    avg_confidence = round(
        pd.to_numeric(
            df["confidence"],
            errors="coerce"
        ).mean(),
        2
    )

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric(
        T["signals"],
        total_signals
    )

    col2.metric(
        T["closed_trades"],
        total_closed
    )

    col3.metric(
        T["open_trades"],
        open_trades_count
    )

    col4.metric(
        T["win_rate"],
        f"{win_rate:.2f}%"
    )

    col5.metric(
    "Average Confidence",
    avg_confidence
)

    col6.metric(
        T["health_score"],
        health_score
    )
else:
    st.warning(
    "signals.csv not found"
)


# =========================
# ACTIVE SIGNALS
# =========================

st.markdown("---")

st.header("🔴 Active Signals")

if not df.empty:

    open_trades = df[
        df["status"] == "OPEN"
    ]

    if len(open_trades) > 0:

        st.dataframe(
            open_trades,
            width="stretch"
        )

    else:

        st.info(
            "No active signals."
        )
# =========================

# CAPABILITIES

# =========================

st.markdown("---")

st.header(f"🤖 {T['capabilities']}")

capabilities = """
✅ AI Trading Signals
✅ Confidence Scoring
✅ Bitget Market Data
✅ Portfolio Intelligence
✅ Daily Market Brief
✅ Trade Tracking
✅ Paper Trading Analytics
✅ Trending Coin Analysis
✅ Fear & Greed Monitoring
✅ Multi-Language Support
✅ Risk Management
✅ Market Narratives
"""

st.markdown(
translate_text(
capabilities,
language
)
)

# =========================

# TRENDING COINS

# =========================

st.markdown("---")

st.header(f"🔥 {T['trending']}")

try:
    trending = get_trending_coins()

    if trending:

        cols = st.columns(
            len(trending)
        )

        for i, coin in enumerate(
            trending
        ):

            cols[i].metric(
                f"#{i+1}",
                coin
            )

except Exception:
    st.warning(
        "Trending coins unavailable"
    )


# =========================

# GLOBAL MARKET

# =========================

st.markdown("---")

st.header(f"🌍 {T['market']}")

try:
    market = get_global_market()

    if market:
        market_cap = (
            market["market_cap"]
            / 1_000_000_000_000
        )

        volume = (
            market["volume"]
            / 1_000_000_000
        )

        btc_dom = (
            market["btc_dominance"]
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        col1.metric(
    "Market Cap",
    f"${market_cap:.2f}T"
)

        col2.metric(
    "24h Volume",
    f"${volume:.2f}B"
)

        col3.metric(
    "BTC Dominance",
    f"{btc_dom:.2f}%"
)


except Exception:
    st.warning(
        "Market data unavailable"
    )


# =========================

# FEAR & GREED

# =========================

st.markdown("---")

st.header(f"😨 {T['fear_greed']}")

try:
    value, sentiment = (
        get_fear_greed()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Score",
        value
    )

    col2.metric(
    "Sentiment",
    sentiment
)

except Exception:
    st.warning(
    "Fear & Greed unavailable"
)


# =========================

# SIGNAL HISTORY

# =========================

st.markdown("---")

st.header(
f"📡 {T['signal_history']}"
)

if not df.empty:
    st.dataframe(
    df,
    width="stretch"
)


# =========================

# TRADE PERFORMANCE

# =========================

st.markdown("---")

st.header(
    f"📈 {T['trade_performance']}"
)

if not df.empty:
    closed = df[
        df["status"] == "CLOSED"
    ]

    if len(closed) > 0:
        pnl = pd.to_numeric(
            closed["pnl_percent"],
            errors="coerce"
        )

        st.line_chart(
            pnl.reset_index(
                drop=True
            )
        )

# =========================
# LEADERBOARD
# =========================

st.markdown("---")

st.header(
    f"🏆 {T['leaderboard']}"
)

if not df.empty:

    closed = df[
        df["status"] == "CLOSED"
    ].copy()

    if len(closed) > 0:

        closed["pnl_percent"] = (
            pd.to_numeric(
                closed["pnl_percent"],
                errors="coerce"
            )
        )

        leaderboard = (
            closed.sort_values(
                by="pnl_percent",
                ascending=False
            )
        )

        st.dataframe(
            leaderboard[
                [
                    "coin",
                    "signal",
                    "confidence",
                    "pnl_percent"
                ]
            ],
            width="stretch"
        )
# =========================

# PORTFOLIO

# =========================

st.markdown("---")

st.header(
f"💼 {T['portfolio']}"
)

portfolio_file = "reports/portfolio_report.txt"

if os.path.exists(portfolio_file):

    with open(
        portfolio_file,
        "r",
        encoding="utf-8"
    ) as f:

        portfolio_text = f.read()

    display_text = (
        portfolio_text
        if language == "English"
        else translate_text(
            portfolio_text,
            language
        )
    )

    st.text_area(
        "Portfolio Report",
        value=display_text,
        height=400,
        key=f"portfolio_{os.path.getmtime(portfolio_file)}",
        label_visibility="collapsed"
    )

else:

    st.text_area(
        "Portfolio Report",
        value="Portfolio report not available",
        height=400,
        label_visibility="collapsed"
    )

# =========================
# MARKET BRIEF
# =========================

st.markdown("---")

st.header(
    f"📰 {T['market_brief']}"
)

latest_brief = None
briefs = []

if os.path.exists("reports"):

    briefs = sorted(
        [
            file
            for file in os.listdir("reports")
            if file.startswith(
                "market_brief"
            )
        ],
        reverse=True
    )

if len(briefs) > 0:

    latest_brief = os.path.join(
        "reports",
        briefs[0]
    )

if latest_brief:

    with open(
        latest_brief,
        "r",
        encoding="utf-8"
    ) as f:

        brief = f.read()

    display_brief = (
        brief
        if language == "English"
        else translate_text(
            brief,
            language
        )
    )

    st.text_area(
        "Market Brief",
        value=display_brief,
        height=400,
        key=f"brief_{os.path.getmtime(latest_brief)}",
        label_visibility="collapsed"
    )

else:

    st.info(
        "Run market_brief.py first."
    )
# =========================

# SUMMARY

# =========================

st.markdown("---")

st.header(
f"🚀 {T['summary']}"
)

summary = """
AlphaLens AI combines Bitget Market Data,
Qwen AI Analysis,
Portfolio Intelligence,
Paper Trading Analytics,
Daily Market Briefs,
Trending Coin Monitoring,
Fear & Greed Analysis,
and Multi-Language Support
into a unified crypto intelligence platform.
"""

st.info(
translate_text(
summary,
language
)
)

# =========================

# FOOTER

# =========================

st.markdown("---")

st.success(
"✅ AlphaLens AI Dashboard Online"
)
