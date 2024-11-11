import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import ta
from datetime import datetime, timedelta
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Function to get user input for stocks and date range
def get_user_input():
    stocks = input("Enter stock symbols separated by commas (e.g., AAPL,MSFT,GOOGL): ").split(',')
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) or 'today' for current date: ")
    if end_date.lower() == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    return stocks, start_date, end_date

# Get user input
stocks, start_date, end_date = get_user_input()

# Download data
data = yf.download(stocks, start=start_date, end=end_date)
adj_close = data['Adj Close']

# Initialize the DataFrame to store indicators
indicators = pd.DataFrame(index=adj_close.index)

# Calculate indicators
for stock in stocks:
    indicators[f'{stock}_SMA_50'] = ta.trend.sma_indicator(adj_close[stock], window=50)
    indicators[f'{stock}_SMA_200'] = ta.trend.sma_indicator(adj_close[stock], window=200)
    indicators[f'{stock}_RSI'] = ta.momentum.rsi(adj_close[stock], window=14)
    indicators[f'{stock}_MACD'] = ta.trend.macd_diff(adj_close[stock])
    indicators[f'{stock}_BB_upper'], indicators[f'{stock}_BB_middle'], indicators[f'{stock}_BB_lower'] = ta.volatility.bollinger_hband_indicator(adj_close[stock]), ta.volatility.bollinger_mavg(adj_close[stock]), ta.volatility.bollinger_lband_indicator(adj_close[stock])

# Calculate returns
returns = adj_close.pct_change()

# Plot function for stock prices and indicators
def plot_stock_indicators(stock):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 16), sharex=True)
    
    # Price and MAs
    ax1.plot(adj_close[stock], label=f'{stock} Adj Close')
    ax1.plot(indicators[f'{stock}_SMA_50'], label='50-day SMA')
    ax1.plot(indicators[f'{stock}_SMA_200'], label='200-day SMA')
    ax1.fill_between(indicators.index, indicators[f'{stock}_BB_lower'], indicators[f'{stock}_BB_upper'], alpha=0.1)
    ax1.set_title(f'{stock} Price and Indicators')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    # RSI
    ax2.plot(indicators[f'{stock}_RSI'], label='RSI')
    ax2.axhline(70, color='r', linestyle='--')
    ax2.axhline(30, color='g', linestyle='--')
    ax2.set_ylabel('RSI')
    ax2.legend()
    
    # MACD
    ax3.plot(indicators[f'{stock}_MACD'], label='MACD')
    ax3.axhline(0, color='r', linestyle='--')
    ax3.set_ylabel('MACD')
    ax3.legend()
    
    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()

# Plot correlation heatmap
def plot_correlation_heatmap(returns):
    plt.figure(figsize=(10, 8))
    sns.heatmap(returns.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Heatmap of Stock Returns')
    plt.show()

# Calculate and print performance metrics
def print_performance_metrics(stock):
    total_return = (adj_close[stock][-1] / adj_close[stock][0] - 1) * 100
    annualized_return = ((1 + total_return/100)**(365/len(adj_close))) - 1
    volatility = returns[stock].std() * np.sqrt(252) * 100
    sharpe_ratio = annualized_return / volatility if volatility != 0 else 0
    
    print(f"\nPerformance Metrics for {stock}:")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Annualized Return: {annualized_return:.2f}%")
    print(f"Annualized Volatility: {volatility:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Main execution
for stock in stocks:
    plot_stock_indicators(stock)
    print_performance_metrics(stock)

plot_correlation_heatmap(returns)

# Print buy/sell signals based on SMA crossover
for stock in stocks:
    signal = np.where(indicators[f'{stock}_SMA_50'] > indicators[f'{stock}_SMA_200'], 1, 0)
    signal_changes = np.diff(signal)
    buy_signals = adj_close.index[1:][signal_changes == 1]
    sell_signals = adj_close.index[1:][signal_changes == -1]
    
    print(f"\nTrading Signals for {stock}:")
    print("Buy Signals:", ', '.join(buy_signals.strftime('%Y-%m-%d')))
    print("Sell Signals:", ', '.join(sell_signals.strftime('%Y-%m-%d')))

# Plot comparison of normalized stock prices
scaler = MinMaxScaler()
normalized_prices = pd.DataFrame(scaler.fit_transform(adj_close), columns=adj_close.columns, index=adj_close.index)

plt.figure(figsize=(14, 7))
for stock in stocks:
    plt.plot(normalized_prices[stock], label=stock)

plt.title('Comparison of Normalized Stock Prices')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend()
plt.show()
