from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from binance import Client


load_dotenv()


def binance_client():
    client = Client(getenv('BINANCE_API'), getenv('BINANCE_SECRET'), tld='us')
    return client


def prices_collection():
    """Returns a collection from the MongoDB database."""
    client = MongoClient(getenv('MONGO'))
    db = client.tradebot
    return db.historical_prices