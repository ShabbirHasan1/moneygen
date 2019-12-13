from webscraper.equity import EquityScraperBase
from bs4 import BeautifulSoup
import requests
import json
from util import SeleniumDispatcher
from nsetools import Nse
from config import Config


class EquityScraper(EquityScraperBase):
    def __init__(self):
        self.nse = Nse()


    # TODO: modify to accept multiple keys for info dict to return data
    def get_info_specfic(self, instrument_symbol: str):
        url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' \
                + instrument_symbol

        # res = SeleniumDispatcher(headless=False, selenium_wire=True).get_response(url)
        res = requests.get(url, headers=Config.NSE_HEADERS)
        soup = BeautifulSoup(res.content, 'html.parser')
        # Get data inside html element with id='responseDiv'
        res_json = soup.find(id='responseDiv').get_text()
        res_dict = json.loads(res_json)
        return res_dict['data'][0]


    # TODO: modify to accept multiple keys for info dict to return data
    def get_info_all(self, instruments: list, specific_info_key: str=None):
        instrument_infos = dict()
        for instrument in instruments:
            if specific_info_key is None:
                instrument_infos[instrument] = self.get_info_specfic(instrument)
            else:
                instrument_infos[instrument] = self.get_info_specfic(instrument)[specific_info_key]
        return instrument_infos

