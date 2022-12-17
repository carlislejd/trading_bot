import talib
import pandas as pd

from config import ccxt_connect
from helper import long_short



exchange = ccxt_connect()


data = pd.read_parquet('data/eth_data.parquet')

last_date = int(round(data['date'].iloc[-1].timestamp() * 1000)) + 1

new_data_query = exchange.fetch_ohlcv('ETH/USDT', '5m', limit=250, since=last_date)

new_data = pd.DataFrame(new_data_query[:-1], columns=['at', 'open', 'high', 'low', 'close', 'vol'])
new_data['date'] = pd.to_datetime(new_data['at'], unit='ms')
new_data.drop('at', axis=1, inplace=True)

if len(new_data) > 0:
    data = pd.concat([data, new_data])
    data.reset_index()
    data.to_parquet('data/eth_data.parquet')

data = pd.read_parquet('data/eth_data.parquet')

df = data.copy()
df.set_index('date', inplace=True)
close = df['close'].values
df['rsi'] = talib.RSI(close, timeperiod=14)
df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
df['EMA9'] = talib.EMA(df.close, 9)
df['EMA55'] = talib.EMA(df.close, 55)
df['EMA200'] = talib.EMA(df.close, 200)

df['date'] = df.index
df.reset_index(drop=True, inplace=True)
df.fillna(method='ffill', inplace=True)
df = df.iloc[-200:][['date', 'close', 'rsi', 'macdhist', 'EMA9', 'EMA55', 'EMA200']]

df['signal'] = df.apply(long_short, axis=1)