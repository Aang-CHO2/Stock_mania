This code provides a visual comparison of the stock prices and their moving averages for multiple stocks on a single chart. 
It allows for easy identification of trends and potential buy/sell signals based on moving average crossovers. 
The RSI indicator is calculated but not plotted in this version of the code.
This code creates a stock price chart with technical indicators for multiple stocks. Here's a breakdown of its functionality:

Import necessary libraries:
- pandas for data manipulation
- numpy for numerical operations
- matplotlib for plotting
- yfinance for downloading stock data
- ta for technical analysis indicators

Define a list of stock symbols to analyze (AAPL, MSFT, GOOGL).
Download historical stock data from Yahoo Finance using yfinance, from January 1, 2020, to November 11, 2024.
Extract the adjusted closing prices for each stock.
Create a new DataFrame called 'indicators' to store technical indicators.

For each stock, calculate and store the following indicators:
- 50-day Simple Moving Average (SMA)
- 200-day Simple Moving Average (SMA)
- 14-day Relative Strength Index (RSI)

Create a plot using matplotlib:
- Set the figure size to 14x7 inches

For each stock:
- Plot the adjusted closing price
- Plot the 50-day SMA
- Plot the 200-day SMA

Add a title, x-axis label, and y-axis label to the plot.Add a legend to identify each line on the chart.Display the plot.
