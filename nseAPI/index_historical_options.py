from index_historical import IndexHistorical
import requests


class IndexHistoricalOptions(IndexHistorical):
    def __init__(self, symbol_name: str):
        super().__init__(symbol_name)
        self.option_type = 'OPTIONS'
        self.option_type_val = 'OPTIDX'
        self.option_type_display_val = 'Index Options'

    def get_expiries(self):
        res = requests.get(
            'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteDataTest.jsp?i='\
            + self.option_type\
            + '&u='\
            + self.symbol_name\
            + '&e=&o=&k='
        )
        self.expiries = res.json()['expiries']
        return self.expiries


    def get_strike_prices(self, expiries: list, option_type: str):
        pass

    def get_expiry_strike_price_map(self, expiries: list):
        pass

    def fetch_all_infos(self, expiry: str, strike_price: str):
        pass

    def download_data(self, expiry: str, strike_price: str, option_type: str):
        pass