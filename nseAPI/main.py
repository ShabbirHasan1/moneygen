from index_historical_options import IndexHistoricalOptions

index_historical_options = IndexHistoricalOptions('BANKNIFTY', 'CE')
expiries = index_historical_options.get_expiries()
print(expiries)
print(index_historical_options.get_strike_prices(expiries))