from datetime import datetime
from django.utils import timezone

from .models import CoinData, CoinStatsCalculated, CoinStatsRange, CoinStatsHistorical, Trade

from datetime import datetime, timedelta
import pytz
import csv
import os
import warnings
import math

from ta.trend import ADXIndicator
import pyti.relative_strength_index as rsi
import ta.volatility as vl
import numpy as np
import pandas as pd
from scipy.stats import linregress

warnings.filterwarnings('ignore')


def convert_timestamp_to_utc(timestamp):
    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
    return utc_datetime


def get_ohlcv_from_db(coin, num_of_candles=15, timeframe=5):
    try:
        last_ohlcv = CoinData.objects.filter(coin=coin).order_by('-time').first()
        last_combined_candle = {
            'open': last_ohlcv.open,
            'high': last_ohlcv.high,
            'low': last_ohlcv.low,
            'close': last_ohlcv.close,
            'volume': last_ohlcv.volume
        }
    except Exception as e:
        print(e)
        return []

    current_dt = datetime.now().replace(second=0, microsecond=0).astimezone(pytz.utc)
    current_dt -= timedelta(minutes=current_dt.minute % timeframe)

    data = []
    for _ in range(num_of_candles):
        end_dt = current_dt
        start_dt = end_dt - timedelta(minutes=timeframe)

        # Calculate the OHLCV for the custom timeframe
        ohlcv_data = CoinData.objects.filter(
            coin=coin,
            time__gte=start_dt,
            time__lt=end_dt
        )

        if ohlcv_data:
            open_price = ohlcv_data.first().open
            close_price = ohlcv_data.last().close
            high_price = max(ohlcv.high for ohlcv in ohlcv_data)
            low_price = min(ohlcv.low for ohlcv in ohlcv_data)
            volume = sum(ohlcv.volume for ohlcv in ohlcv_data)
        else:
            open_price = last_combined_candle['open']
            close_price = last_combined_candle['close']
            high_price = last_combined_candle['high']
            low_price = last_combined_candle['low']
            volume = last_combined_candle['volume']

        combined_candle = {
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        }
        data.insert(0, combined_candle)
        last_combined_candle = combined_candle

        current_dt -= timedelta(minutes=timeframe)

    return data


def make_pandas_df(data):
    opens = pd.Series([float(row['open']) for row in data], name='open')
    highs = pd.Series([float(row['high']) for row in data], name='high')
    lows = pd.Series([float(row['low']) for row in data], name='low')
    closes = pd.Series([float(row['close']) for row in data], name='close')
    volume = pd.Series([float(row['volume']) for row in data], name='volume')

    opens = opens.fillna(0)
    highs = highs.fillna(0)
    lows = lows.fillna(0)
    closes = closes.fillna(0)
    volume = volume.fillna(0)

    df = pd.concat([opens, highs, lows, closes, volume], axis=1)

    return df


def calculate_rsi(data, period):
    data['RSI'] = rsi.relative_strength_index(data['close'].values, period)
    return round(data['RSI'].iloc[-1], 2)


def calculate_adx(data):
    adx_i = ADXIndicator(data['high'], data['low'], data['close'], window=14, fillna=True)
    data['adx'] = adx_i.adx()

    return round(data['adx'].iloc[-1], 2)


def get_latest_volume(coin):
    return CoinData.objects.filter(coin=coin).order_by('-time').first().volume


def get_latest_close_price(coin):
    return CoinData.objects.filter(coin=coin).order_by('-time').first().close


def calculate_sma(data, period, column_name):
    data[column_name] = data['close'].rolling(window=period).mean()
    return round(data[column_name].iloc[-1], 2)


def calculate_ema(data, period, column_name):
    data[column_name] = data['close'].ewm(span=period, adjust=False).mean()
    return round(data[column_name].iloc[-1], 2)


def calculate_roc(data, period):
    data['ROC'] = (data['close'] - data['close'].shift(period)) / data['close'].shift(period) * 100
    return round(data['ROC'].iloc[-1], 2)


def calculate_beta(data, period):
    data['Log_Ret'] = data['close'].pct_change()
    data['Log_Index'] = data['close'].pct_change().rolling(window=period).cov(data['close'].pct_change()) / data[
        'close'].pct_change().rolling(window=period).var()
    data['Beta'] = data['Log_Index'] / data['Log_Ret'].var()
    data.drop(['Log_Ret', 'Log_Index'], axis=1, inplace=True)
    return round(data['Beta'].iloc[-1], 2)


def calculate_super_trend(data, period):
    data['atr'] = vl.average_true_range(data['high'], data['low'], data['close'], period)
    data['upperband'] = data['high'] - (period * data['atr'])
    data['lowerband'] = data['low'] + (period * data['atr'])
    data['in_uptrend'] = True

    for current in range(1, len(data.index)):
        previous = current - 1

        if data['close'][current] > data['upperband'][previous]:
            data['in_uptrend'][current] = True
            data['lowerband'][current] = min(data['lowerband'][current], data['lowerband'][previous])
        else:
            data['in_uptrend'][current] = False
            data['upperband'][current] = max(data['upperband'][current], data['upperband'][previous])

    data['Super_Trend'] = data.apply(lambda row: row['lowerband'] if row['in_uptrend'] else row['upperband'], axis=1)
    data.drop(['atr', 'upperband', 'lowerband', 'in_uptrend'], axis=1, inplace=True)
    return round(data['Super_Trend'].iloc[-1], 2)


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


def perform_new_calculations(coin, timeframe=5):
    data = get_ohlcv_from_db(coin, 50, timeframe=timeframe)
    df = make_pandas_df(data)

    rsi = calculate_rsi(df, 14)
    adx = calculate_adx(df)

    sma_20 = calculate_sma(df, 20, 'sma_20')
    ema = calculate_ema(df, 10, 'ema_10')

    roc = calculate_roc(df, 12)
    beta = calculate_beta(df, 20)
    super_trend = calculate_super_trend(df, 7)

    slope, intercept, r_squared, std_dev = calculate_trend(df['close'].tolist())

    stats = {
            'latest_rsi': rsi,
            'adx': adx,
            'volume': get_latest_volume(coin),
            'closing_price': get_latest_close_price(coin),
            'sma_20': sma_20,
            'ema': ema,
            'roc': roc,
            'beta': beta,
            'super_trend': super_trend,
            'slope_percent': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'std_deviation': std_dev
    }
    for key, value in stats.items():
        if math.isnan(value) or math.isinf(value):
            stats[key] = None

    coin_stats_calculated, created = CoinStatsCalculated.objects.update_or_create(
        coin=coin,
        timeframe=timeframe,
        defaults=stats
    )


def write_coin_stats_to_csv(coin_stats_calculated):
    fname = f'{coin_stats_calculated.coin.name}_{coin_stats_calculated.timeframe}.csv'
    if not os.path.exists(fname):
        with open(fname, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'rsi', 'adx',
                             'volume', 'closing_price',
                             'sma_20', 'ema', 'roc', 'beta',
                             'super_trend', 'slope_percent', 'intercept',
                             'r_squared', 'std_deviation'])

    with open(fname, 'a', newline='') as f:
        writer = csv.writer(f)
        time = coin_stats_calculated.time.strftime("%m-%d-%Y %H:%M:%S")

        writer.writerow([time, coin_stats_calculated.latest_rsi,
                         coin_stats_calculated.adx, coin_stats_calculated.volume,
                         coin_stats_calculated.closing_price, coin_stats_calculated.sma_20,
                         coin_stats_calculated.ema, coin_stats_calculated.roc, coin_stats_calculated.beta,
                         coin_stats_calculated.super_trend, coin_stats_calculated.slope_percent,
                         coin_stats_calculated.intercept, coin_stats_calculated.r_squared,
                         coin_stats_calculated.std_deviation])


def write_coin_stats_to_db(coin_stats_calculated):
    CoinStatsHistorical.objects.create(
        coin=coin_stats_calculated.coin,
        timeframe=coin_stats_calculated.timeframe,
        latest_rsi=coin_stats_calculated.latest_rsi,
        adx=coin_stats_calculated.adx,
        volume=coin_stats_calculated.volume,
        ema=coin_stats_calculated.ema,
        roc=coin_stats_calculated.roc,
        beta=coin_stats_calculated.beta,
        sma_20=coin_stats_calculated.sma_20,
        super_trend=coin_stats_calculated.super_trend,
        slope_percent=coin_stats_calculated.slope_percent,
        intercept=coin_stats_calculated.intercept,
        r_squared=coin_stats_calculated.r_squared,
        std_deviation=coin_stats_calculated.std_deviation,
        closing_price=coin_stats_calculated.closing_price
    )

def check_coin_stats_in_range(coin_stats_calculated):
    coin_stats_range = CoinStatsRange.objects.get(coin=coin_stats_calculated.coin,
                                                  timeframe=coin_stats_calculated.timeframe)
    values_to_check = [
        'latest_rsi', 'adx', 'volume', 'closing_price', 'sma_20', 'ema', 'roc', 'beta',
        'super_trend', 'slope_percent', 'intercept', 'r_squared', 'std_deviation'
    ]

    # If all the attributes are none then there's no need to check if parameters are in range
    all_are_none = True
    for value in values_to_check:
        if (getattr(coin_stats_range, f'lower_{value}') is not None and
                getattr(coin_stats_range, f'upper_{value}') is not None):
            all_are_none = False
            break

    if all_are_none:
        return False

    for value in values_to_check:
        if (getattr(coin_stats_range, f'lower_{value}') is None or
                getattr(coin_stats_range, f'upper_{value}') is None or
                getattr(coin_stats_calculated, value) is None):
            continue

        if getattr(coin_stats_range, f'lower_{value}') <= getattr(coin_stats_calculated, value) <= getattr(
                coin_stats_range, f'upper_{value}'):
            pass
        else:
            return False

    return True


def generate_buy_signal(coin_stats_calculated):
    Trade.objects.create(
        coin=coin_stats_calculated.coin,
        price=coin_stats_calculated.closing_price,
        action='buy'
    )
