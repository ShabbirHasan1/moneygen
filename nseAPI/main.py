from index_historical_options import IndexHistoricalOptions

index_historical_options = IndexHistoricalOptions('BANKNIFTY', 'CE')
print(index_historical_options.get_expiry_strike_price_map_for_all())