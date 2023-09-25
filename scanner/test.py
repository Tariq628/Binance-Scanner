from binance.client import Client
import pandas as pd
import pyti.relative_strength_index as rsi
from ta.trend import ADXIndicator
import ta.trend as tr
import numpy as np
import ta.volatility as vl
import warnings
from scipy.stats import linregress
from datetime import datetime
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

# Replace YOUR_API_KEY and YOUR_API_SECRET with your actual Binance API key and secret
client = Client('UMLne9tvM0WDHOMaUFTspKjqvYP0PHTkZxpyNFW4jdflIlZ76mm8ASK9VrHqG9Tk', 'YxSNGmO66BFCCDVovRG4pjkeyUtUQROG30948AbiJX8oikojbdFde3zh6V5LRJBo')

# Define a method to get the historical data from Binance
def get_historical_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

# Define a method to calculate the RSI
def calculate_rsi(data, period):
    data['RSI'] = rsi.relative_strength_index(data['Close'].values, period)
    return data

# Define a method to calculate the ADX
def calculate_adx(data, period):
    adxI = ADXIndicator(data['High'], data['Low'], data['Close'], period, fillna=True)
    data['ADX'] = adxI.adx()
    return data

# Define a method to calculate the SMA
def calculate_sma(data, period, column_name):
    data[column_name] = data['Close'].rolling(window=period).mean()
    return data

# Define a method to calculate the EMA
def calculate_ema(data, period, column_name):
    data[column_name] = data['Close'].ewm(span=period, adjust=False).mean()
    return data

# Define a method to calculate the Rate of Change (ROC)
def calculate_roc(data, period):
    data['ROC'] = (data['Close'] - data['Close'].shift(period)) / data['Close'].shift(period) * 100
    return data
def get_btc_price():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1) # get data for the last day

    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, start_time.strftime("%d %b %Y %H:%M:%S"), end_time.strftime("%d %b %Y %H:%M:%S"))

    btc_price = [float(kline[4]) for kline in klines] # extract the closing price from each kline

    return btc_price

def calculate_trend(data):
    n = len(data)
    x = np.array(range(n))
    y = np.array(data)

    slope, intercept, r_value, _, std_err = linregress(x, y)
    
    r_squared = r_value ** 2
    std_dev = np.std(y)

    slope_percentage = slope * 100 / np.mean(y)
    std_dev_percentage = std_dev * 100 / np.mean(y)

    return slope_percentage, intercept, r_squared, std_dev_percentage

btc_price = get_btc_price()

slope, intercept, r_squared, std_dev = calculate_trend(btc_price)

# Define a method to calculate Beta
def calculate_beta(data, period):
    data['Log_Ret'] = data['Close'].pct_change()
    data['Log_Index'] = data['Close'].pct_change().rolling(window=period).cov(data['Close'].pct_change()) / data['Close'].pct_change().rolling(window=period).var()
    data['Beta'] = data['Log_Index'] / data['Log_Ret'].var()
    data.drop(['Log_Ret', 'Log_Index'], axis=1, inplace=True)
    return data

# Define a method to calculate the Super Trend
def calculate_super_trend(data, period):
    data['atr'] = vl.average_true_range(data['High'], data['Low'], data['Close'], period)
    data['upperband'] = data['High'] - (period * data['atr'])
    data['lowerband'] = data['Low'] + (period * data['atr'])
    data['in_uptrend'] = True

    for current in range(1, len(data.index)):
        previous = current - 1

        if data['Close'][current] > data['upperband'][previous]:
            data['in_uptrend'][current] = True
            data['lowerband'][current] = min(data['lowerband'][current], data['lowerband'][previous])
        else:
            data['in_uptrend'][current] = False
            data['upperband'][current] = max(data['upperband'][current], data['upperband'][previous])

    data['Super_Trend'] = data.apply(lambda row: row['lowerband'] if row['in_uptrend'] else row['upperband'], axis=1)
    data.drop(['atr', 'upperband', 'lowerband', 'in_uptrend'], axis=1, inplace=True)
    return data

with open('details.txt', 'r') as f:
    lst = []
    lst.extend(f.readlines(0))

symb = str(lst[0]).replace('\n', '')
dur = str(lst[1])

# Get the historical data
df = get_historical_data(symb, dur, '500')

# Calculate the RSI
df = calculate_rsi(df, 14)

# Calculate the ADX
df = calculate_adx(df, 14)

# Calculate the SMAs
df = calculate_sma(df, 10, 'SMA_10')
df = calculate_sma(df, 20, 'SMA_20')

# Calculate the EMA
df = calculate_ema(df, 10, 'EMA_10')

# Calculate the ROC
df = calculate_roc(df, 12)

# Calculate Beta
df = calculate_beta(df, 20)

# Calculate Super Trend
df = calculate_super_trend(df, 7)

# Get the latest RSI, ADX, Volume, Closing Price, EMA, ROC, Beta, SMA latest 20 points, and Super Trend
latest_rsi = df['RSI'].iloc[-1]
latest_adx = df['ADX'].iloc[-1]
latest_volume = df['Volume'].iloc[-1]
latest_close = df['Close'].iloc[-1]
latest_ema_10 = df['EMA_10'].iloc[-1]
latest_roc = df['ROC'].iloc[-1]
latest_beta = df['Beta'].iloc[-1]
latest_sma_20 = df['SMA_20'].iloc[-1]
latest_super_trend = df['Super_Trend'].iloc[-1]

print('Latest RSI: {:.2f}%'.format(latest_rsi))
print('Latest ADX (trend strength): {:.2f}'.format(latest_adx))
print('Latest Volume: {:.2f}'.format(latest_volume))
print('Latest Close Price: {:.2f}'.format(latest_close))
print('Latest EMA (10 period): {:.2f}'.format(latest_ema_10))
print('Latest ROC: {:.2f}%'.format(latest_roc))
print('Latest Beta: {:.2f}'.format(latest_beta))
print('Latest 20-point SMA: {:.2f}'.format(latest_sma_20))
print('Latest Super Trend: {:.2f}'.format(latest_super_trend))
print("Current BTC price: ", btc_price[-1])
print("Trend (Slope in %): ", slope)
print("Intercept: ", intercept)
print("R-Squared: ", r_squared)
print("Standard Deviation (in %): ", std_dev)
# Determine the latest momentum and trend
latest_sma_10 = df['SMA_10'].iloc[-1]
if latest_close > latest_ema_10:
    print('Closing price is above the EMA')
elif latest_close < latest_ema_10:
    print('Closing price is below the EMA')
else:
    print('Closing price is exactly at the EMA')
