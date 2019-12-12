from webscraper.index_historical import IndexHistoricalOptions
from tasks import NSEIndiaTradedToDelivered, RediffMoneyTradedToDelivered
from util.log import Logger
from datetime import datetime


# TODO: Complete this and move to tasks module
###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())


Logger.info('=====================Job Starting at: ' + str(datetime.now()))
t1 = NSEIndiaTradedToDelivered(push_output_to_slack=True)
t1.run()
# t2 = RediffMoneyTradedToDelivered(number_of_instruments=10, push_output_to_slack=True)
# t2.run()
t1.start()
t1.join()
# t2.start()
# t2.join()
Logger.info('Complete!')
Logger.info('=====================Job Completed at: ' + str(datetime.now()))
