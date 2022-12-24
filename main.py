import time
import talib
import sched
import pandas as pd
from time import time, sleep

from datetime import datetime
from strategy import long_short
from config import binance_client, prices_collection
from helper import check_decimals, current_position, telegram_notification





def run():
    client = binance_client()
    prices = prices_collection()

    last_date = prices.find().sort('date', -1).limit(1).next()['date']
    print(f'Finding the last record in our DB')

    new_data_query = client.get_historical_klines('ETHUSDT', '5m', str(last_date), limit=100)
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

    print('Calculating signals')
    df['signal'] = df.apply(long_short, axis=1)

    symbol = 'ETHUSD'
    decimal = check_decimals(symbol)

    signal = df['signal'].iloc[-1]
    price = df['close'].iloc[-1]
    position = current_position()
    print(f'Current signal: {signal}, current position: {position}')

    if signal == position or signal == None:
        print('No change in position, sleep for 5min and rescan')
        
    else:
        with open('current_position.txt', 'w') as f:
            f.write(str(signal))

        if signal == 'BUY':
            print(f'Signal went from: {position} to {signal}, flipping to long at {price}')
            balance = client.get_asset_balance(asset='USD')
            usd_balance = float(balance['free']) * .95
            print(f'USD Balance: {usd_balance}')
            quantity = round((usd_balance / price), decimal)
            print(f'ETH price: {price}')
            print(f'Taking 95% of USD balance: {usd_balance * .95} and getting ETH quantity we can buy with it: {quantity}{symbol}')
            order = client.create_order(symbol=symbol, side=signal, type='MARKET', quantity=quantity)
            telegram_notification(f"{order['symbol']} {order['side']} {order['executedQty']} at {order['fills'][0]['price']}")
            print(order)

        if signal == 'SELL':
            print(f'Signal went from: {position} to {signal}, flipping to short at {price}')
            balance = client.get_asset_balance(asset='ETH')
            eth_balance = float(balance['free']) * .95
            print(f'ETH Balance: {eth_balance}')
            quantity = round(eth_balance, decimal)
            print(f'Selling {quantity} {symbol}')
            order = client.create_order(symbol=symbol, side=signal, type='MARKET', quantity=quantity)
            telegram_notification(f"{order['symbol']} {order['side']} {order['executedQty']} at {order['fills'][0]['price']}")
            print(order)


if __name__ == '__main__':
    starttime = time()
    while True:
        run()
        sleep(300 - ((time() - starttime) % 300))