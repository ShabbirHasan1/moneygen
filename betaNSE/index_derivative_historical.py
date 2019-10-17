from selenium_dispatcher import SeleniumDispatcher
from config import Config

class IndexDerivativeHistorical:
    """
    Manages historical data for Index derivates as per NSE.
    Currently it supports:
    - Nifty 50 (NIFTY)
    - Nifty Bank (BANKNIFTY)
    - Nifty IT (NIFTYIT)
    """
    def __init__(self, symbol_name: str, derivative_type: str, expiry_date: str,option_type: str=None ,strike_price: str=None):
        """
        Parameters
        ----------
        symbol_name: str
            Symbol of the index.
        derivative_type: str
            Can only be either "OPTIONS" or "FUTURES"
        option_type: str
            Can only be either "PUT" or "CALL".
            Required if the "derivative_type"="OPTIONS"
        expiry_date: str
            Should be in format "DD-MMM-YYYY"
        strike_price: str
            The strike price for contract.
            Required if the "derivative_type"="OPTIONS"
        """
        self.driver = SeleniumDispatcher().get_driver();
        self.driver.get(Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper())

    def __del__(self):
        self.driver.close()

