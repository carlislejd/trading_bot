def long_short(df):
    if (df['EMA9'] > df['EMA55']) and (df['rsi'] >= 51) and (df['macdhist'] >= 0):
        return 2
    if (df['EMA9'] < df['EMA55']) and (df['rsi'] <= 49) and (df['macdhist'] <= 0):
        return 1
    else:
        return 0
    
def create_signal(df):
    if (df['signal'] != 0.0) and (df['cross'] == 2):
        return 'Buy'
    if (df['signal'] != 0.0) and (df['cross'] == 1):
        return 'Sell'