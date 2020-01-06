from webscraper.index_historical import IndexHistoricalOptions
from tasks.traded_to_percent_delivered import TradedToPercentDelivered, TradedToPercentDeliveredReport
from kite_simulator import SimulationSetup
from util.log import Logger
from datetime import datetime
from dateutil.tz import *


# TODO: Complete this and move to tasks module
###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())



Logger.info('=====================Main Job Starting at: ' + str(datetime.now()))

now = datetime.now().astimezone(tzlocal())
market_open = now.replace(hour=9, minute=15)
market_close = now.replace(hour=15, minute=30)
market_preopen_open = now.replace(hour=9, minute=0)
market_preopen_close = market_open

if now > market_close:
    t1 = TradedToPercentDeliveredReport(slack=True, sendgrid=True)
    t1.start()
    t1.join()


if now >= market_preopen_open and now <= market_close:
    t1 = TradedToPercentDelivered(slack=True, sendgrid=True)
    t1.start()
    t1.join()





Logger.info('Complete!')
Logger.info('=====================Main Job Completed at: ' + str(datetime.now()))
