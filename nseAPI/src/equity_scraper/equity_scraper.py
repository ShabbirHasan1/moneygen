from equity_scraper_base import EquityScraperBase
from util.gainers_losers_info import GainersLosersInfo
from bs4 import BeautifulSoup
import requests
import json


class EquityScraper(EquityScraperBase):
    def __init__(self, instrument_symbol: str):
        super().__init__(instrument_symbol=instrument_symbol)


    def get_info_specfic(self, instrument_symbol: str):
        url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' \
                + instrument_symbol

        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        # Get data inside html element with id='responseDiv'
        res_json = soup.find(id='responseDiv').get_text()
        res_dict = json.loads(res_json)
        return res_dict



    def get_info_all(self, instruments: list):
        instrument_infos = dict()
        for instrument in instruments:
            instrument_info = self.get_info_specfic(instrument)
            instrument_infos[instrument] = instrument_info
        return instrument_infos

