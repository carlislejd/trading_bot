import numpy as np
import pandas as pd 

from config import price_collection


start = pd.to_datetime('2019-01-01')
end = pd.to_datetime('now')
search = {'_id': 0, 'date': 1, 'open': 1, 'high': 1, 'low': 1, 'close': 1, 'volume': 1}

historical = price_collection()
prices = historical.find({'blockchain': 'ethereum', 'symbol': 'weth', 'date': {'$lt': end, '$gte': start}}, search)
df = pd.DataFrame(list(prices))
df.to_parquet(f'data/eth_data.parquet')