import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AlphaLens AI",
    page_icon="🚀",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🚀 AlphaLens AI Dashboard")
st.subheader("Bitget × Qwen Hackathon")

st.markdown("---")

# =========================
# SIGNALS
# =========================

st.header("📡 Signal History")

if os.path.exists("signals.csv"):

    signals = pd.read_csv("signals.csv")

    st.dataframe(
        signals,
        use_container_width=True
    )

    st.metric(
        "Total Signals",
        len(signals)
    )

else:

    st.warning(
        "signals.csv not found"
    )

st.markdown("---")

# =========================
# PERFORMANCE
# =========================

st.header("📊 Trading Performance")

if os.path.exists("signals.csv"):

    df = pd.read_csv("signals.csv")

    if "status" in df.columns:

        closed = df[
            df["status"] == "CLOSED"
        ]

        if len(closed) > 0:

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
                wins / len(closed)
            ) * 100

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(
                "Trades",
                len(closed)
            )

            col2.metric(
                "Wins",
                wins
            )

            col3.metric(
                "Losses",
                losses
            )

            col4.metric(
                "Win Rate",
                f"{win_rate:.2f}%"
            )

            st.line_chart(
                pnl.reset_index(
                    drop=True
                )
            )

        else:

            st.info(
                "No closed trades yet."
            )

st.markdown("---")

# =========================
# REPORTS
# =========================

st.header("📄 Reports")

if os.path.exists("reports"):

    reports = sorted(
        os.listdir("reports"),
        reverse=True
    )

    for report in reports[:10]:

        st.write(
            f"📄 {report}"
        )

else:

    st.warning(
        "reports folder not found"
    )

st.markdown("---")

# =========================
# FOOTER
# =========================

st.success(
    "AlphaLens AI Dashboard Online"
)