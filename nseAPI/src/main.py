from webscraper.index_historical.index_historical_options import IndexHistoricalOptions
from util.log.logger import Logger
from webscraper.gainer_loser_info.nse_india_gl_scraper import NSEIndiaGLScraper
from webscraper.equity.equity_scraper import EquityScraper
from webscraper.gainer_loser_info.rediff_money_gl_scraper import RediffMoneyGLScraper
import threading
from tasks import NSEIndiaTradedToDelivered, RediffMoneyTradedToDelivered



###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())





t1 = RediffMoneyTradedToDelivered()
t1.start()