from index_historical import IndexHistorical
import requests
import wget
from config import Config
import os


class IndexHistoricalOptions(IndexHistorical):
    def __init__(self, symbol_name: str, option_type: str):
        super().__init__(symbol_name)
        self.derivative_type = 'OPTIONS'
        self.derivative_type_val = 'OPTIDX'
        self.derivative_type_display_val = 'Index Options'
        self.option_type = option_type
        self.expiries = None
        self.expiry_strike_price_map = None

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
        if self.expiries is None:
            self.get_expiries()
        self.expiry_strike_price_map = self.get_strike_prices(self.expiries)
        return self.expiry_strike_price_map

    def get_info_specfic(self, expiry: str, strike_price: str):
        pass

    def get_info_all(self):
        pass

    def download_data_specific(self, expiry: str, strike_price: str):
        url = "https://nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp"\
                + "?underlying=" + self.symbol_name\
                + '&instrument=' + self.derivative_type_val\
                + '&expiry=' + expiry\
                + '&type=' + self.option_type\
                + '&strike=' + strike_price\
                + "&fromDate=" + 'undefined'\
                + "&toDate=" + 'undefined'\
                + "&datePeriod=" + '3months'\
                + "&fileDnld=" + 'undefined'
        download_dir_path = os.path.join(Config.DOWNLOAD_DIRECTORY,self.derivative_type_val,self.option_type)
        if not os.path.isdir(download_dir_path):
            os.makedirs(download_dir_path)
        download_file_path = os.path.join(download_dir_path, expiry + '_' + strike_price + '.csv')
        # filename = wget.download(url=url, out=download_file_path)
        res = requests.get(url, allow_redirects=True)
        open(download_file_path, 'wb').write(res.content)
        return download_file_path

    def download_data_all(self):
        if self.expiry_strike_price_map is None:
            self.get_expiry_strike_price_map_for_all()
        downloaded_files = list()
        for expiry in self.expiry_strike_price_map.keys():
            for strike_price in self.expiry_strike_price_map[expiry]:
                filepath = self.download_data_specific(expiry, strike_price)
                downloaded_files.append(filepath)
        return filepath