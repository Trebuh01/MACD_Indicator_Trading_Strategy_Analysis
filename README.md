# MACD Indicator Trading Strategy Analysis

## Description
This project analyzes the use of the MACD (Moving Average Convergence Divergence) indicator for trading strategies involving the cryptocurrency Litecoin (LTC) against USD Tether (USDT). The analysis spans different market conditions including bullish (hossa), sideways (boczny), and general market conditions, incorporating the use of additional indicators like RSI (Relative Strength Index) to enhance decision-making.
A more detailed report is available in the file `sprawozdanie.pdf`.

## Files
- `macd.py`: General analysis of the MACD indicator over a period from 01.01.2018.
- `macd_hossa.py`: Analysis of the MACD indicator during a bullish market phase from December 2018 to November 2021.
- `macd_boczny.py`: Analysis of the MACD indicator during a sideways market.
- `macd_rsi.py`: Combined analysis using both MACD and RSI indicators.

# Analysis Methods
## MACD Calculation
The MACD is calculated using the following steps:

- Calculate the 12-day EMA (Exponential Moving Average).
- Calculate the 26-day EMA.
- Subtract the 26-day EMA from the 12-day EMA to get the MACD line.
- Calculate the 9-day EMA of the MACD line to get the Signal line.

## Trading Signals
- Buy Signal: When the MACD line crosses above the Signal line.
- Sell Signal: When the MACD line crosses below the Signal line.

## RSI Calculation (used in macd_rsi.py)
- Calculate the change in price.
- Separate the gains and losses.
- Calculate the average gain and average loss over a 14-day period.
- Calculate the RS (Relative Strength) by dividing the average gain by the average loss.
- Calculate the RSI using the formula: `RSI = 100 - (100 / (1 + RS))`.

# Functions
## General Functions
- `calculate_ema(prices, days, smoothing=2)`: Computes the Exponential Moving Average.
- `load_and_calculate_indicators(file_path)`: Loads data from a CSV file and calculates MACD and Signal lines.
- `plot_with_signals2(data)`: Plots MACD and Signal lines with buy and sell signals.
- `simulate_trading(data, positions_limit)`: Simulates trading based on MACD signals and returns transactions and final capital.

## Combined Analysis Functions (macd_rsi.py)
- `simulate_trading_with_rsi(data, investment_per_trade)`: Simulates trading using both MACD and RSI indicators.
- `plot_with_signals(data, buy_dates, sell_dates)`: Plots closing prices with buy and sell signals, as well as MACD and RSI indicators.

# Results Summary
## General Analysis
- **Profitability**: The MACD-based strategy demonstrated profitability under different market conditions.
- **Risk Management**: Dividing the capital into multiple positions reduced risk but also potential returns.
- **Bullish Market**: Higher profits were observed when investing the entire capital in a single position during a bullish market phase.
## Combined MACD and RSI Analysis
- **Signal Filtration**: Using RSI alongside MACD helped filter signals, potentially reducing false positives.
- **Market Conditions**: Both indicators showed strengths and weaknesses depending on market conditions, with combined use improving decision accuracy.
