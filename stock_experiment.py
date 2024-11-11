import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import ta
stocks = ['AAPL', 'MSFT', 'GOOGL']  # Example: Apple, Microsoft, Alphabet
data = yf.download(stocks, start='2020-01-01', end='2024-11-11')
adj_close = data['Adj Close']
# Initialize the DataFrame to store indicators
indicators = pd.DataFrame(index=adj_close.index)

for stock in stocks:
    indicators[f'{stock}_SMA_50'] = ta.trend.sma_indicator(adj_close[stock], window=50)
    indicators[f'{stock}_SMA_200'] = ta.trend.sma_indicator(adj_close[stock], window=200)
    indicators[f'{stock}_RSI'] = ta.momentum.rsi(adj_close[stock], window=14)
plt.figure(figsize=(14, 7))

for stock in stocks:
    plt.plot(adj_close[stock], label=f'{stock} Adj Close')
    plt.plot(indicators[f'{stock}_SMA_50'], label=f'{stock} 50-day SMA')
    plt.plot(indicators[f'{stock}_SMA_200'], label=f'{stock} 200-day SMA')

plt.title('Stock Prices and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
