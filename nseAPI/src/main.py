from webscraper.index_historical import IndexHistoricalOptions
from tasks.traded_to_percent_delivered import TradedToPercentDelivered, TradedToPercentDeliveredReport
from util.log import Logger
from datetime import datetime
from dateutil.tz import *


# TODO: Complete this and move to tasks module
###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())



Logger.info('=====================Job Starting at: ' + str(datetime.now()))

now = datetime.now().astimezone(tzlocal())
end = now.replace(hour=15, minute=31)

if now > end:
    t1 = TradedToPercentDeliveredReport()
    t1.start()
    t1.join()
else:
    t1 = TradedToPercentDelivered()
    t1.start()
    t1.join()

Logger.info('Complete!')
Logger.info('=====================Job Completed at: ' + str(datetime.now()))
