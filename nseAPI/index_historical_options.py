from index_historical import IndexHistorical
import requests


class IndexHistoricalOptions(IndexHistorical):
    def __init__(self, symbol_name: str, option_type: str):
        super().__init__(symbol_name)
        self.derivative_type = 'OPTIONS'
        self.derivative_type_val = 'OPTIDX'
        self.derivative_type_display_val = 'Index Options'
        self.option_type = option_type

    def get_expiries(self):
        url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteDataTest.jsp?i='\
                + self.derivative_type\
                + '&u='\
                + self.symbol_name\
                + '&e=&o=&k='
        res = requests.get(url)
        self.expiries = res.json()['expiries']
        return self.expiries


    def get_strike_prices(self, expiries: list):
        expiry_strike_price_map = dict()
        for expiry in expiries:
            url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteDataTest.jsp?i='\
                    + self.derivative_type_val\
                    + '&u='\
                    + self.symbol_name\
                    + '&e='\
                    + expiry\
                    + '&o='\
                    + self.option_type\
                    + '&k='\
                    + self.option_type
            res = requests.get(url)
            expiry_strike_price_map[expiry] = res.json()['strikePrices']
        return expiry_strike_price_map

    def get_expiry_strike_price_map_for_all(self):
        try:
            self.expiry_strike_price_map = self.get_strike_prices(self.expiries)
            return self.expiry_strike_price_map
        except Exception:
            self.get_expiries()
            self.expiry_strike_price_map = self.get_strike_prices(self.expiries)
            return self.expiry_strike_price_map

    def fetch_all_infos(self, expiry: str, strike_price: str):
        pass

    def download_data(self, expiry: str, strike_price: str, option_type: str):
        pass