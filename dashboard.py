import streamlit as st
import pandas as pd
import os   
import sys

from signal_engine import (
    get_best_opportunity
)
from economic_calendar import (
    get_economic_events
)
from signal_logger import save_signal
from translations import TRANSLATIONS
from translator import translate_text
from market_data import (
get_trending_coins,
get_global_market,
get_fear_greed
)
from datetime import datetime

if (
    "last_trade_check"
    not in st.session_state
):

    st.session_state[
        "last_trade_check"
    ] = datetime.now()

    os.system(
        f"{sys.executable} trade_tracker.py"
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

header_col1, header_col2 = st.columns([1, 6])

with header_col1:

    try:

        st.image(
            "logo.png",
            width=90
        )

    except Exception:

        st.markdown("# 🚀")

with header_col2:

    st.title("AlphaLens AI")

    st.caption(
        "Built for Bitget AI Base Camp Hackathon S1 2026"
    )

    st.subheader(
        "Multilingual AI-Powered Crypto Intelligence Platform"
    )

st.markdown(
    """
🤖 AI Signals • 📊 Portfolio Intelligence • 📰 Market Briefs • 📅 Economic Calendar • 🌍 Market Intelligence • 🌐 Multi-Language Support
"""
)

st.markdown("---")

# =========================
# HEADER
# =========================

st.markdown("---")

# =========================
# LOAD SIGNALS
# =========================

df = pd.DataFrame()

if os.path.exists("signals.csv"):

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

# CAPABILITIES

# =========================

st.markdown("---")

st.header(f"🤖 {T['capabilities']}")

capabilities = """
🤖 AI Trading Signals
📊 Portfolio Intelligence
📰 AI Market Briefs
📅 Economic Calendar
📈 Bitget Market Data
🌍 Global Market Intelligence
😨 Fear & Greed Analysis
🔥 Trending Coin Discovery
🎯 Confidence Scoring
⚠️ Risk Management
📋 Pending Trade Workflow
🔄 Automated Trade Monitoring
🏆 Trade Performance Analytics
📊 Trade Leaderboards
💼 Portfolio Health Scoring
🧠 Market Narrative Generation
🌐 Multi-Language Support
"""

st.markdown(
translate_text(
capabilities,
language
)
)

# =========================
# MARKET OVERVIEW
# =========================

st.markdown("---")

market_col, fear_col = st.columns([4, 1])

# ==================================
# MARKET PULSE
# ==================================

with market_col:

    st.subheader("🔥 Market Pulse")

    st.caption(
        "Real-time trending assets across the crypto market."
    )

    try:

        trending = get_trending_coins()

        if trending:

            cols = st.columns(5)

            for i, coin in enumerate(
                trending[:5]
            ):

                cols[i].metric(
                    label=f"#{i+1}",
                    value=coin,
                    delta="Trending"
                )

        else:

            st.info(
                "No trending coins available."
            )

    except Exception:

        st.warning(
            "Trending coins unavailable."
        )

# ==================================
# FEAR & GREED
# ==================================

with fear_col:

    st.subheader("😨 Fear & Greed")

    try:

        value, sentiment = (
            get_fear_greed()
        )

        st.metric(
            label="Score",
            value=value
        )

        st.metric(
            label="Sentiment",
            value=sentiment
        )

    except Exception:

        st.warning(
            "Unavailable"
        )

# =========================
# ECONOMIC CALENDAR
# =========================

st.markdown("---")

st.header(translate_text("📅 Economic Calendar", language))

events = get_economic_events()

high_impact = [
    e for e in events
    if "🔴" in e["impact"]
]

if high_impact:

    st.warning(
        f"⚠️ {len(high_impact)} high-impact economic events scheduled."
    )

for event in events:

    with st.expander(
        f"{event['impact']} {event['event']}"
    ):

        st.write(
            f"📅 Date: {event['date']}"
        )

        st.write(
            f"⏰ Time: {event['time']}"
        )

        st.write(
            event["description"]
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
# AI ACTION CENTER
# =========================

import csv
from datetime import datetime
import subprocess

# =========================
# AI COMMAND CENTER
# =========================

st.markdown("---")

st.header("⚡ AI Command Center")

st.caption(
    "Launch AlphaLens AI agents and intelligence workflows."
)

col1, col2 = st.columns(2)

# ==================================
# LEFT SIDE
# ==================================

with col1:

    if st.button(
        "📊 Generate Portfolio Intelligence",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing portfolio..."
        ):

            subprocess.run(
                [sys.executable, "portfolio.py"],
                check=False
            )

        st.success(
            "Portfolio Intelligence Updated"
        )

        st.rerun()

    if st.button(
        "📰 Generate Market Brief",
        use_container_width=True
    ):

        with st.spinner(
            "Building market brief..."
        ):

            subprocess.run(
                [sys.executable, "market_brief.py"],
                check=False
            )

        st.success(
            "Market Brief Updated"
        )

        st.rerun()

# ==================================
# RIGHT SIDE
# ==================================

with col2:

    if st.button(
        "📈 Update Trade Tracker",
        use_container_width=True
    ):

        with st.spinner(
            "Scanning open trades..."
        ):

            subprocess.run(
                [sys.executable, "trade_tracker.py"],
                check=False
            )

        st.success(
            "Trade Tracker Updated"
        )

        st.rerun()

    if st.button(
        "🤖 Generate AI Signal",
        use_container_width=True
    ):

        with st.spinner(
            "Searching for alpha..."
        ):

            signal = get_best_opportunity()

            if signal:

                st.session_state[
                    "pending_signal"
                ] = signal

                st.success(
                    f"{signal['coin']} opportunity detected"
                )

                st.rerun()

            else:

                st.error(
                    "No opportunity found."
                )

# ==================================
# DASHBOARD REFRESH
# ==================================

st.markdown("")

if st.button(
    "🔄 Refresh Intelligence Hub",
    use_container_width=True
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
        pending.get("coin", "N/A")
    )

    col2.metric(
        "Signal",
        pending.get("signal", "N/A")
    )

    col1.metric(
        "Confidence",
        pending.get("confidence", "N/A")
    )

    col2.metric(
        "Entry Price",
        f"${pending.get('entry_price', 0):.4f}"
    )

    st.text_area(
        "🤖 AI Analysis",
        pending.get(
            "report",
            "Analysis unavailable."
        ),
        height=180
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Place Order",
            use_container_width=True
        ):

            save_signal(
                coin=pending["coin"],
                signal=pending["signal"],
                confidence=pending["confidence"],
                entry_price=pending["entry_price"]
            )

            subprocess.run(
                [sys.executable, "portfolio.py"],
                check=False
            )

            subprocess.run(
                [sys.executable, "market_brief.py"],
                check=False
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
            "🔄 Generate New Signal",
            use_container_width=True
        ):

            new_signal = (
                get_best_opportunity()
            )

            if new_signal:

                st.session_state[
                    "pending_signal"
                ] = new_signal

            st.rerun()

else:

    st.info(
        "Generate a signal to create a pending trade."
    )

    # =========================
# ACTIVE SIGNALS
# =========================

st.markdown("---")

st.header("🔴 Active Signals")

# Ensure df is defined before use (it may be loaded later in the file)
if "df" not in locals():
    df = pd.DataFrame()

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
# PLATFORM SUMMARY
# =========================

st.markdown("---")

st.header("🚀 AlphaLens Mission")

summary = """
AlphaLens AI bridges the gap between raw market data and intelligent decision-making.

By combining Bitget Market Data, Qwen AI, Portfolio Intelligence,
Economic Calendar Monitoring, AI Market Briefs, Paper Trading Analytics,
and Multi-Language Accessibility, AlphaLens delivers institutional-grade
crypto intelligence through a single streamlined experience.
"""

st.success(
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
