from webscraper.index_historical import IndexHistoricalOptions
from tasks import NSEIndiaTradedToDelivered, RediffMoneyTradedToDelivered



###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())





t1 = RediffMoneyTradedToDelivered()
t1.start()