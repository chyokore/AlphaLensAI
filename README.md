# AlphaLens AI

AlphaLens AI is a multilingual crypto intelligence platform built for the Bitget × Qwen Hackathon.

The platform combines real-time market data, AI-powered analysis, portfolio intelligence, paper trading analytics, and market narratives to help traders make more informed decisions.

## Overview

AlphaLens AI acts as an AI-powered crypto copilot that helps users:

* Analyze crypto assets
* Generate AI trading signals
* Evaluate portfolio risk
* Monitor market conditions
* Track paper trading performance
* Generate institutional-style market reports

## Features

### AI Trading Signals

* Real-time crypto market analysis
* BUY / HOLD / REDUCE recommendations
* AI-generated confidence scores
* Risk assessment
* Multi-language support

### Portfolio Intelligence

* Portfolio Health Score
* Portfolio Risk Score
* Diversification Analysis
* AI Portfolio Recommendations
* Opportunity Watchlists
* Executive Portfolio Summaries

### Daily Market Briefs

* Market Mood Analysis
* Market Narratives
* Key Risk Monitoring
* Executive Summaries
* Actionable Trading Insights

### Paper Trading Engine

* Trade Tracking
* Win Rate Analysis
* Portfolio PnL Monitoring
* Portfolio Health Scoring
* Risk Ratings
* Trade Recommendations

### Market Intelligence

* Bitget Market Data Integration
* Trending Asset Monitoring
* Fear & Greed Index Tracking
* Global Market Overview

## Architecture

AlphaLens AI combines multiple systems:

* Bitget API for real-time market data
* Qwen AI for analysis and signal generation
* MuleRun for workflow orchestration
* CoinGecko API for market intelligence data
* Python analytics engine for portfolio and trading intelligence

### Workflow

Bitget Market Data

↓

AlphaLens Analytics Engine

↓

Qwen AI Analysis

↓

Signal Generation

↓

Portfolio Intelligence

↓

Paper Trading Analytics

↓

Report Generation

## Tech Stack

* Python
* Qwen AI
* Bitget Market Data API
* CoinGecko API
* MuleRun
* GitHub

## Project Structure

```text
AlphaLensAI/

app.py
portfolio.py
market_brief.py
paper_trading.py
trade_journal.py

bitget_data.py
bitget_market.py
signal_logger.py

signals.csv
paper_trades.csv

reports/
├── portfolio_report.txt
├── market_brief_*.txt
├── report_*.txt
└── paper_trading_report.txt
```

## How To Run

### AI Trading Signals

```bash
python app.py
```

### Portfolio Intelligence

```bash
python portfolio.py
```

### Daily Market Brief

```bash
python market_brief.py
```

### Paper Trading Dashboard

```bash
python paper_trading.py
```

### Trade Journal

```bash
python trade_journal.py
```

## Example Capabilities

* Generate AI-powered crypto market reports
* Analyze portfolio risk and diversification
* Produce institutional-style market briefs
* Track paper trading performance
* Generate confidence-scored trading signals
* Export reports for review and analysis

## Current Modules

### AlphaLens AI Core

Generates:

* Market Sentiment
* Trading Signals
* Confidence Scores
* Entry, Stop Loss, and Take Profit Levels
* AI Market Narratives

### Portfolio Intelligence

Generates:

* Health Scores
* Risk Scores
* Allocation Recommendations
* Opportunity Watchlists
* Portfolio Narratives

### Paper Trading Analytics

Generates:

* Win Rate
* Portfolio PnL
* Health Scores
* Risk Ratings
* Best and Worst Trade Analysis
* Trade Recommendations

### Market Brief Engine

Generates:

* Daily Market Mood
* Confidence Scores
* Top Opportunities
* Market Narratives
* Executive Summaries

## Vision

AlphaLens AI aims to become a complete AI-powered crypto intelligence platform that combines market analytics, portfolio management, risk monitoring, and trading intelligence into a single experience powered by Qwen AI and Bitget market data.

## Built For

Bitget × Qwen Hackathon 2026
