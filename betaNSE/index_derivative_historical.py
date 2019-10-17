from selenium_dispatcher import SeleniumDispatcher
from config import Config

class IndexDerivativeHistorical:
    """
    Manages historical data for Index derivates as per NSE.
    Currently it supports:
    - Nifty 50 (NIFTY)
    - Nifty Bank (BANKNIFTY)
    - Nifty IT (NIFTYIT)
    Parameters
    ----------
    symbol_name : str
        Symbol of the index.
    """
    def __init__(self, symbol_name : str):
        self.driver = SeleniumDispatcher().get_driver();
        self.driver.get(Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper())
        index_select = self.driver.find_element_by_id("eq-derivatives-historical-instrumentType")

        #####self.futures_years =###
        
        self.options_years = ###
        self.futures_expiry_dates = ###
        self.options_expiry_dates = #####
        self.options_strike_prices = 


    def get_futures_data(self, expiry_date: str, current_year: bool = False):
        pass

    def get_options_data(self, expiry_date: str, option_type: str, strike_price: str, current_year: bool = False)
        pass


    def __del__(self):
        self.driver.close()

