from index_historical_options import IndexHistoricalOptions

index_historical_options = IndexHistoricalOptions('BANKNIFTY', 'CE')
print(index_historical_options.download_data_all())