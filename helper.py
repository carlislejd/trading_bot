import pandas as pd


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


def long_short(df):
    if (df['EMA9'] > df['EMA55']) and (df['rsi'] >= 51) and (df['macdhist'] >= 0):
        return 'Long'
    if (df['EMA9'] < df['EMA55']) and (df['rsi'] <= 49) and (df['macdhist'] <= 0):
        return 'Short'