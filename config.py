from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from pybit import inverse_perpetual


load_dotenv()

def bybit_client():
    client = inverse_perpetual.HTTP(endpoint='https://api.bytick.com', api_key=getenv('BYBIT_API_KEY'), api_secret=getenv('BYBIT_SECRET_KEY'))
    return client

def prices_collection():
    """Returns a collection from the MongoDB database."""
    client = MongoClient(getenv('MONGO'))
    db = client.tradebot
    return db.historical_prices