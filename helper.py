import pandas as pd
from config import binance_client


def vwap(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates volume-weighted average price (VWAP) for a 5 minute chart.

    Parameters:
    data (pd.DataFrame): Dataframe containing 'timestamp', 'open', 'high', 'low', 'close', and 'volume' columns.

    Returns:
    pd.DataFrame: Dataframe containing 'timestamp', 'vwap' columns.
    """
    # Create a new dataframe to store the VWAP values
    vwap_data = pd.DataFrame(columns=['date', 'vwap'])
    
    # Iterate through each row in the data
    for index, row in data.iterrows():
        # Calculate the VWAP for the current row
        vwap = (row['close'] * row['vol'] + row['open'] * row['vol']) / (2 * row['vol'])
        
        # Append the timestamp and VWAP value to the vwap_data dataframe
        vwap_data = vwap_data.append({'date': row['date'], 'vwap': vwap}, ignore_index=True)
        
    return vwap_data
    

def check_decimals(symbol):
    client = binance_client()
    info = client.get_symbol_info(symbol)
    val = info['filters'][2]['stepSize']
    decimal = 0
    is_dec = False
    for c in val:
        if is_dec is True:
            decimal += 1
        if c == '1':
            break
        if c == '.':
            is_dec = True
    return decimal


def current_position():
    with open('current_position.txt', 'r') as f:
        for current_position in f:
            return current_position