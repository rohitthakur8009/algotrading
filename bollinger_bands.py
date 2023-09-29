import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


def download_stock_data(stock_symbol, start_date, end_date):
    # Download historical stock data
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data


def calculate_bollinger_bands(data, window=20):
    # Calculate the rolling mean and standard deviation
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    data['Upper'] = data['SMA'] + (data['STD'] * 2)
    data['Lower'] = data['SMA'] - (data['STD'] * 2)
    return data


def simulate_trading(data):
    action = "buy"
    invested = 0
    total_profit = 0
    highest_buy = 0

    for _, row in data.iterrows():
        if action == "buy":
            if row['Close'] <= row['Lower']:
                invested = 100 * row['Close']
                if invested > highest_buy:
                    highest_buy = invested
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

    return total_profit, highest_buy


def plot_bollinger_bands(data, stock_symbol, window):
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


def calculate_bollinger_bands_with_rsi(data, window=20, rsi_window=14):
    # Calculate the rolling mean and standard deviation
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    data['Upper'] = data['SMA'] + (data['STD'] * 2)
    data['Lower'] = data['SMA'] - (data['STD'] * 2)

    # Calculate RSI
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=rsi_window).mean()
    avg_loss = loss.rolling(window=rsi_window).mean()

    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


def simulate_advanced_trading(data, short_window=10, long_window=50):
    action = "buy"
    invested = 0
    total_profit = 0

    short_ma = data['Close'].rolling(window=short_window).mean()
    long_ma = data['Close'].rolling(window=long_window).mean()

    for _, row in data.iterrows():
        if action == "buy":
            if row['RSI'] < 30 and short_ma[row.name] > long_ma[row.name]:
                invested = 100 * row['Close']
                print(f'Buy 100 stocks at {row["Close"]} | {invested}')
                action = "sell"
        else:
            if row['RSI'] > 70 or short_ma[row.name] < long_ma[row.name]:
                profit = 100 * row['Close'] - invested
                if profit > 0:
                    invested = 0
                    total_profit += profit
                    print(f'Sold 100 stocks at {row["Close"]} | Profit: {profit}')
                    action = "buy"

    return total_profit


def main():
    stock_symbols = ['SE', 'TSLA']
    start_date = '2022-08-08'
    end_date = '2023-09-09'
    window = 20

    for stock_symbol in stock_symbols:
        print(f"\n\nAnalyzing {stock_symbol}")
        data = download_stock_data(stock_symbol, start_date, end_date)
        data = calculate_bollinger_bands_with_rsi(data, window)
        total_profit = simulate_advanced_trading(data)

        try:
            print(f"Cumulative Profit : {total_profit}")
        except ZeroDivisionError:
            print("No purchases were made.")

        plot_bollinger_bands(data, stock_symbol, window)


if __name__ == "__main__":
    main()
