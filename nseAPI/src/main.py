from index_historical_options import IndexHistoricalOptions

index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
index_historical_options_call.get_info_all()
# index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# print(index_historical_options_put.download_data_all())