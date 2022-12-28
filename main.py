import time
import talib
import sched
import pandas as pd
from time import time, sleep

from datetime import datetime
from strategy import long_short, create_signal
from config import ccxt_connect, prices_collection, binance_client
from helper import current_position, telegram_notification


client = ccxt_connect()
binance = binance_client()
prices = prices_collection()


def run():
    print('Starting the bot')
    print(f"Current time: {datetime.utcnow().strftime('%m-%d-%y-%H:%M:%S')}")

    last_date = prices.find().sort('date', -1).limit(1).next()['date']
    print(f"Finding the last record in our DB: \n{last_date.strftime('%m-%d-%y-%H:%M:%S')}")

    print(f'Querying data from binance to make current')
    new_data_query = binance.get_klines(symbol='ETHUSDT', interval=binance.KLINE_INTERVAL_5MINUTE, endTime=int(last_date.timestamp() * 1000))
    print('Getting new data from Binance API (5m interval)')

    new_data = pd.DataFrame(new_data_query[:-1], columns=['Open time', 'open', 'high', 'low', 'close', 'vol', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    new_data['date'] = pd.to_datetime(new_data['Close time'], unit='ms')
    cols_to_drop = ['Open time', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    new_data.drop(cols_to_drop, axis=1, inplace=True)

    cols = ['open', 'high', 'low', 'close', 'vol']
    new_data[cols] = new_data[cols].apply(pd.to_numeric, errors='ignore', axis=1)

    if len(new_data) > 0:
        print(f'Inserting new data into DB')
        prices_collection().insert_many(new_data.to_dict('records'))

    df = pd.DataFrame(list(prices.find().sort('date', -1).limit(300)))
    df.sort_values('date', inplace=True)

    df.set_index('date', inplace=True)
    close = df['close'].values
    df['rsi'] = talib.RSI(close, timeperiod=14)
    macd, macdsignal, df['macdhist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['EMA9'] = talib.EMA(df.close, 9)
    df['EMA55'] = talib.EMA(df.close, 55)
    df['EMA200'] = talib.EMA(df.close, 200)

    df['date'] = df.index
    df.reset_index(drop=True, inplace=True)
    df.fillna(method='ffill', inplace=True)

    df.drop_duplicates(subset='date', keep='last', inplace=True)

    print('Calculating signals')
    df['cross'] = df.apply(long_short, axis=1)

    df['signal'] = df[df['cross'] != 0]['cross'].diff()
    df['signal'].fillna(0, inplace=True)

    df['action'] = df.apply(create_signal, axis=1)

    symbol = 'ETHUSD'

    date = df['date'].iloc[-1]
    signal = df['action'].iloc[-1]
    price = df['close'].iloc[-1]
    print(f'New last record: {date}, Current signal: {signal}, Current price: {price}')

    if signal == None:
        print('No change in position, sleep for 5min and rescan')
        
    else:
        if signal == 'Buy':
            print(f'Flipping to long at {price}')
            balance = client.fetch_balance()
            last_order = client.fetch_closed_orders(symbol)
            if last_order[-1]['info']['side'] == 'Sell':
                close = client.create_order(
                        symbol = 'ETHUSD',
                        type = 'market',
                        side = 'buy',
                        amount = int(last_order[-1]['info']['qty']),               
                        params = {'reduce_only': True})
            sleep(2)
            balance = client.fetch_balance()
            print(balance['ETH'])
            quantity = round((float(balance['ETH']['total']) * .95), 3)
            order = client.create_order(
                    symbol = 'ETHUSD',
                    type = 'market',
                    side = 'buy',
                    amount = (price * quantity) * 5,
                    params = {'leverage': 5})
            telegram_notification(order)
            print(order)

        if signal == 'Sell':
            print(f'Flipping to short at {price}')
            balance = client.fetch_balance()
            last_order = client.fetch_closed_orders(symbol)
            if last_order[-1]['info']['side'] == 'Buy':
                close = client.create_order(
                        symbol = 'ETHUSD',
                        type = 'market',
                        side = 'sell',
                        amount = int(last_order[-1]['info']['qty']),
                        params = {'reduce_only': True})
            sleep(2)
            balance = client.fetch_balance()
            print(balance['ETH'])
            quantity = round((float(balance['ETH']['total']) * .95), 3)
            order = client.create_order(
                    symbol = 'ETHUSD',
                    type = 'market',
                    side = 'sell',
                    amount = (price * quantity) * 5,
                    params = {'leverage': 5})
            telegram_notification(order)
            print(order)


starttime = time()
while True:
    run()
    sleep(300 - ((time() - starttime) % 300))