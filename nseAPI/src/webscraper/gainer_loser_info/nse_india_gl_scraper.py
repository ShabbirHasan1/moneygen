import requests
from util.log import Logger
from webscraper.gainer_loser_info import BaseGLScraper
from util import SeleniumDispatcher
import json


class NSEIndiaGLScraper(BaseGLScraper):
    '''Creates instance to scrape Gainers/Losers information from NSEIndia
    Parameters:
    info_type (str): Can only be either 'Gainers' or 'Losers'
    view_type (str): Can only be:
                    - 'Nifty 50'
                    - 'Nifty Next 50'
                    - 'Securities > Rs.20'
                    - 'Securities < Rs.20'
                    - 'F&O Securities'
                    - 'All Securities'
    '''
    def __init__(self, info_type: str, view_type: str):
        super().__init__()
        self.info_type = info_type
        self.view_type_map = {
            'Nifty 50': 'nifty' + self.info_type + '1',
            'Nifty Next 50': 'jrNifty' + self.info_type + '1',
            'Securities > Rs.20': 'secGt20' + self.info_type + '1',
            'Securities < Rs.20': 'secLt20' + self.info_type + '1',
            'F&O Securities': 'fno' + self.info_type + '1',
            'All Securities': 'allTop' + self.info_type + '1',
        }
        self.view_type = self.view_type_map[view_type]

    def get_instruments(self, complete_info=False):
        url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/'\
                + self.info_type.lower()\
                + '/'\
                + self.view_type\
                + '.json'
        Logger.info(url)
        # try:
        res = SeleniumDispatcher(headless=True, selenium_wire=True).get_response(url)
        # except BaseException as ex:
        #     Logger.info('Exception occured while getting gainer/loser info: '+ str(ex))
        #     Logger.info('Retrying...')
        #     driver = SeleniumDispatcher(selenium_wire=False, headless=True).get_driver()
        #     driver.get(url)
        #     driver.close()
        #     res = requests.get(url)
        data = json.loads(res)
        symbol_info_list = data['data']
        symbols = list()
        for symbol_info in symbol_info_list:
            # Currently considering EQUITY series only
            if symbol_info['series'] == 'EQ':
                symbols.append(symbol_info['symbol'])
        
        return {True: symbol_info_list, False: symbols} [complete_info]


    # TODO: Setting complete info flag in `get_instruments` method should call below method for each instrument to get info
    def get_instrument_info(self):
        pass