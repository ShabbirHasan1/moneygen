# from index_historical.index_historical_options import IndexHistoricalOptions
from log_util.logger import Logger
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())

from util.gainers_losers_info import GainersLosersInfo

gl_info = GainersLosersInfo(info_type='Losers', view_type='All Securities')
Logger.log(gl_info.get_instruments())

