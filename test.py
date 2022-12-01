from config import ccxt_connect

exchange = ccxt_connect()
exchange.load_markets()