from os import getenv
from dotenv import load_dotenv

from config import ccxt_connect

load_dotenv()


exchange = ccxt_connect()


symbol = 'ETH/BTC'
type = 'market'  
side = 'sell'  
amount = 1.0
price = 0.060154 