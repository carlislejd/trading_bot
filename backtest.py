def backtest(df, initial_capital=1000, taker_fee=0.0006, leverage=5):
    
    # Initialize the portfolio with an initial capital of 100
    portfolio = initial_capital
    
    # Initialize the position to None
    position = None

    # Set the taker fee to 0.06%
    taker_fee = taker_fee

    # Set the leverage to 5x
    leverage = leverage
    
    # Iterate through each row in the DataFrame
    for i, row in df.iterrows():
      # Check the value of the signal column
      if row['action'] == 'Buy':
        # If the signal is 1 and the position is None, buy the asset at the current price
        if position is None:
          investment = (portfolio * leverage) * (1 - taker_fee)
          # Update the portfolio value
          portfolio += investment * (row['close'] / investment)
          position = 'long'
        # If the signal is 1 and the position is short, close the short position and buy the asset at the current price
        elif position == 'short':
          investment = (portfolio * leverage) * (1 - taker_fee)
          # Update the portfolio value
          portfolio += 2 * investment * (row['close'] / investment)
          position = 'long'
      elif row['action'] == 'Sell':
        # If the signal is -1 and the position is None, short the asset at the current price
        if position is None:
          investment = (portfolio * leverage) * (1 - taker_fee)
          # Update the portfolio value
          portfolio -= investment * (row['close'] / investment)
          position = 'short'
        # If the signal is -1 and the position is long, sell the asset at the current price and short the asset at the current price
        elif position == 'long':
          investment = (portfolio * leverage) * (1 - taker_fee)
          # Update the portfolio value
          portfolio -= 2 * investment * (row['close'] / investment)
          position = 'short'
        
    # Return the final value of the portfolio
    return portfolio