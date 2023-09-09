import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Replace 'YOUR_STOCK_TICKER' and 'START_DATE' and 'END_DATE' with the stock symbol and date range you want.
# You can use a library like yfinance to fetch historical stock data.
# For example, you can install yfinance with 'pip install yfinance'.

import yfinance as yf

stock_symbols = ['SE', 'AAPL', 'TSLA', 'GOOGL', 'AMZN']
start_date = '2022-08-08'
end_date = '2023-09-09'



for stock_symbol in stock_symbols:
    print(f"\n\nAnalyzing {stock_symbol}")
    # Download historical stock data
    data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Calculate the rolling mean and standard deviation
    window = 20  # Adjust the window size as needed
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    data['Upper'] = data['SMA'] + (data['STD'] * 2)
    data['Lower'] = data['SMA'] - (data['STD'] * 2)

    action = "buy"
    invested = 0
    total_profit = 0
    highestBuy = 0
    for row in data.to_dict('records'):
        if action == "buy":
            if row['Close'] <= row['Lower']:
                invested = 100 * row['Close']
                if invested > highestBuy:
                    highestBuy = invested
                print(f'Buy 100 stocks at {row["Close"]} | {invested}')
                action = "sell"
        else:
            if row['Close'] >= 0.90 * row['High']:
                profit = 100 * row['High'] - invested
                if profit > 0:
                    invested = 0
                    total_profit += profit
                    sold = 100 * row['High']
                    action = "buy"
                    print(f'Sold 100 stocks at {row["High"]} | {sold} | Profit: {profit}')
    try:
        print(f"Cumulative Profit : {total_profit} | Percentage Returns: {(total_profit/highestBuy)*100}")
    except:
        pass

    # Create a plot of the stock price and Bollinger Bands
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=stock_symbol + ' Close Price', color='blue')
    plt.plot(data.index, data['SMA'], label='SMA (' + str(window) + ' days)', color='black')
    plt.plot(data.index, data['Upper'], label='Upper Bollinger Band', color='red', linestyle='--')
    plt.plot(data.index, data['Lower'], label='Lower Bollinger Band', color='green', linestyle='--')

    plt.title('Bollinger Bands for ' + stock_symbol)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
