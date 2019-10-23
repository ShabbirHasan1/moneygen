from index_historical_options import IndexHistoricalOptions

index_historical_options = IndexHistoricalOptions('BANKNIFTY')
expiries = index_historical_options.get_expiries()
print(expiries)