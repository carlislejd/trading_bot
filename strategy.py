def long_short(df):
    if (df['EMA9'] > df['EMA55']) and (df['rsi'] >= 51) and (df['macdhist'] >= 0):
        return 'BUY'
    if (df['EMA9'] < df['EMA55']) and (df['rsi'] <= 49) and (df['macdhist'] <= 0):
        return 'SELL'