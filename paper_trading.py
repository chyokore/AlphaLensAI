import csv
import time
import requests

# =========================
# SYMBOL → COINGECKO ID
# =========================

COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "BNB": "binancecoin",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "SUI": "sui",
    "APT": "aptos",
    "ARB": "arbitrum",
    "OP": "optimism",
    "TRX": "tron"
}

# =========================
# PRICE FETCHER
# =========================

def get_price(symbol):
    symbol = symbol.upper()

    coin_id = COIN_MAP.get(symbol)

    if not coin_id:
        return None

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies=usd"
    )

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "AlphaLens/4.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        if coin_id not in data:
            return None

        return float(data[coin_id]["usd"])

    except requests.exceptions.RequestException:
        return None

    except Exception:
        return None


# =========================
# DASHBOARD
# =========================

print("\n==============================")
print(" AlphaLens Paper Trading V4")
print("==============================\n")

winning_trades = 0
losing_trades = 0
trade_count = 0
open_trades = 0

total_pnl = 0

best_trade_coin = None
best_trade_pnl = float("-inf")

worst_trade_coin = None
worst_trade_pnl = float("inf")

report_lines = []

try:

    with open(
        "paper_trades.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for trade in reader:

            try:

                coin = trade["coin"].upper().strip()
                signal = trade["signal"].upper().strip()

                entry_price = float(
                    trade["entry_price"]
                )

                if entry_price <= 0:
                    print(
                        f"⚠ Invalid entry price for {coin}"
                    )
                    continue

            except (
                KeyError,
                ValueError,
                TypeError
            ):

                print(
                    "⚠ Skipping invalid trade row"
                )
                continue

            current_price = get_price(
                coin
            )

            time.sleep(1)

            if current_price is None:

                print(
                    f"⚠ Price unavailable for {coin}"
                )
                continue

            price_change = (
                current_price
                - entry_price
            )

            pnl = (
                price_change
                / entry_price
            ) * 100

            status = (
                "WINNING"
                if pnl >= 0
                else "LOSING"
            )

            trade_count += 1
            open_trades += 1
            total_pnl += pnl

            if pnl >= 0:
                winning_trades += 1
            else:
                losing_trades += 1

            if pnl > best_trade_pnl:
                best_trade_pnl = pnl
                best_trade_coin = coin

            if pnl < worst_trade_pnl:
                worst_trade_pnl = pnl
                worst_trade_coin = coin

            print("------------------------------")
            print(f"Coin: {coin}")
            print(f"Signal: {signal}")

            print(
                f"Entry Price: "
                f"${entry_price:,.2f}"
            )

            print(
                f"Current Price: "
                f"${current_price:,.2f}"
            )

            print(
                f"PnL: "
                f"{pnl:.2f}%"
            )

            print(
                f"Status: "
                f"{status}"
            )

    print("\n==============================")
    print(" PORTFOLIO SUMMARY")
    print("==============================")

    report_lines.append(
        "AlphaLens Paper Trading Report"
    )

    if trade_count == 0:

        print("No valid trades found.")

        report_lines.append(
            "No valid trades found."
        )

    else:

        average_pnl = (
            total_pnl
            / trade_count
        )

        win_rate = (
            winning_trades
            / trade_count
        ) * 100

        # =========================
        # RISK ENGINE
        # =========================

        if win_rate >= 70:
            risk_rating = "LOW"
        elif win_rate >= 50:
            risk_rating = "MEDIUM"
        else:
            risk_rating = "HIGH"

        # =========================
        # HEALTH SCORE
        # =========================

        health_score = (
            (win_rate * 0.7)
            +
            (max(average_pnl, 0) * 0.3)
        )

        health_score = min(
            round(
                health_score,
                2
            ),
            100
        )

        if health_score >= 75:
            portfolio_status = "EXCELLENT 🚀"
        elif health_score >= 50:
            portfolio_status = "GOOD ✅"
        elif health_score >= 30:
            portfolio_status = "NEUTRAL ⚠"
        else:
            portfolio_status = "WEAK ❌"

        print(
            f"\nTrades Analyzed: "
            f"{trade_count}"
        )

        print(
            f"Open Trades: "
            f"{open_trades}"
        )

        print(
            f"Winning Trades: "
            f"{winning_trades}"
        )

        print(
            f"Losing Trades: "
            f"{losing_trades}"
        )

        print(
            f"Win Rate: "
            f"{win_rate:.2f}%"
        )

        print(
            f"Average PnL: "
            f"{average_pnl:.2f}%"
        )

        print(
            f"Total Portfolio PnL: "
            f"{total_pnl:.2f}%"
        )

        print(
            f"Best Trade: "
            f"{best_trade_coin} "
            f"({best_trade_pnl:.2f}%)"
        )

        print(
            f"Worst Trade: "
            f"{worst_trade_coin} "
            f"({worst_trade_pnl:.2f}%)"
        )

        print(
            f"Risk Rating: "
            f"{risk_rating}"
        )

        print(
            f"Health Score: "
            f"{health_score}/100"
        )

        print(
            f"Portfolio Status: "
            f"{portfolio_status}"
        )

        report_lines.extend([
            f"Trades Analyzed: {trade_count}",
            f"Open Trades: {open_trades}",
            f"Winning Trades: {winning_trades}",
            f"Losing Trades: {losing_trades}",
            f"Win Rate: {win_rate:.2f}%",
            f"Average PnL: {average_pnl:.2f}%",
            f"Total Portfolio PnL: {total_pnl:.2f}%",
            f"Best Trade: {best_trade_coin} ({best_trade_pnl:.2f}%)",
            f"Worst Trade: {worst_trade_coin} ({worst_trade_pnl:.2f}%)",
            f"Risk Rating: {risk_rating}",
            f"Health Score: {health_score}/100",
            f"Portfolio Status: {portfolio_status}"
        ])

        with open(
            "paper_trading_report.txt",
            "w",
            encoding="utf-8"
        ) as report_file:

            report_file.write(
                "\n".join(report_lines)
            )

        print(
            "\n✅ Report saved as "
            "'paper_trading_report.txt'"
        )

except FileNotFoundError:

    print(
        "❌ paper_trades.csv not found."
    )

except Exception as e:

    print(
        f"❌ Unexpected error: {e}"
    )