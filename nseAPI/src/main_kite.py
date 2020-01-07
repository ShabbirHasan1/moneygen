from webscraper.index_historical import IndexHistoricalOptions
from tasks.traded_to_percent_delivered import TradedToPercentDelivered, TradedToPercentDeliveredReport
from kite_simulator import SimulationSetup
from util.log import Logger
from datetime import datetime
from dateutil.tz import *



Logger.info('=====================Kite Job Starting at: ' + str(datetime.now()))

now = datetime.now().astimezone(tzlocal())
market_open = now.replace(hour=9, minute=15)
market_close = now.replace(hour=15, minute=30)
market_preopen_open = now.replace(hour=9, minute=0)
market_preopen_close = market_open


if now >= market_preopen_open and now <= market_open:
    kite_sim_setup = SimulationSetup()

if now >= market_open and now <= market_close:
    ## Run the ticker simulation here
    pass

Logger.info('Complete!')
Logger.info('=====================Kite Job Completed at: ' + str(datetime.now()))
