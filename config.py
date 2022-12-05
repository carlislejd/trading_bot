import ccxt
import pymongo
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def price_collection(): 
    """NONFUNGIBLE HISTORICAL, READ ONLY""" 
    client = pymongo.MongoClient(getenv('MONGO'), readPreference='secondary') 
    db = client.nonfungible 
    return db.historicalusds

def ccxt_connect():
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = ccxt.binance()
    exchange = exchange_class({'apiKey': getenv('BINANCE_API '), 'secret': getenv('BINANCE_SECRET'), 'enableRateLimit': True})
    return exchange