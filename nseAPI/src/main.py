# from index_historical.index_historical_options import IndexHistoricalOptions
from log_util.logger import Logger
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())

from util.gainers_losers_info import GainersLosersInfo
from equity.equity_scraper import EquityScraper

gainers_info = GainersLosersInfo(info_type='Gainers', view_type='All Securities')
gainers_list = gainers_info.get_instruments(complete_info=False)
print(gainers_list)
equity_scraper = EquityScraper()
print(equity_scraper.get_info_all(gainers_list))

