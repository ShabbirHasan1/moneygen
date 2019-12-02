# from webscraper.index_historical.index_historical_options import IndexHistoricalOptions
from util.log.logger import Logger
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())

from webscraper.gainer_loser_info.nse_india_gl_scraper import NSEIndiaGLScraper
from webscraper.equity.equity_scraper import EquityScraper

gainers_info = NSEIndiaGLScraper(info_type='Gainers', view_type='All Securities')
gainers_list = gainers_info.get_instruments(complete_info=False)
equity_scraper = EquityScraper()
Logger.info(str(equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')), push_to_slack=True)
Logger.info(str(equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')), push_to_slack=True)
# Logger.info(str(equity_scraper.get_info_specfic('GAMMNINFRA')), push_to_slack=True)
