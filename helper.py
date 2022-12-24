import requests
import pandas as pd
from os import getenv
from dotenv import load_dotenv

load_dotenv()

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
    

def current_position():
    with open('current_position.txt', 'r') as f:
        for current_position in f:
            return current_position
        

def telegram_notification(message):
    token = getenv('TELEGRAM')
    chat_id = getenv('TELEGRAM_CHAT_ID')
    message = message

    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'

    print(requests.get(url).json())