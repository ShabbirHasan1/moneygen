import time
from selenium_dispatcher import SeleniumDispatcher
from selenium.webdriver.support.select import Select
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
        self.driver = SeleniumDispatcher().get_driver()
        self.driver.get(Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper())
        time.sleep(Config.SLEEP_DURATION)

        # Click on 'All Historical Data'
        self.driver.find_element_by_link_text('All Historical Data').click()

        # Get instrument types from config
        self.instrument_types = Config.INSTRUMENT_TYPES

        ### Get filtering information for OPTIONS
        # Select instrument specified in method params
        time.sleep(Config.SLEEP_DURATION + 4)
        instrument_types_select_element = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-instrumentType']/select")
        # print(instrument_types_select_element.text)
        instrument_types_selector = Select(instrument_types_select_element)
        instrument_types_selector.select_by_visible_text(self.instrument_types['OPTIONS'])
        time.sleep(Config.SLEEP_DURATION)
        print('Instrument type selected: ', self.instrument_types['OPTIONS'])

        

        # Get all available years for OPTIONS contracts
        date_select_element = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-year']/select")
        self.options_years = date_select_element.text.split('\n')[1:]

        # Get all available 'Expiry Dates' for OPTIONS contracts
        self.options_expiry_dates = dict()
        for year in self.options_years:
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            self.options_expiry_dates[year] = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-expiryDate']/select").text.split('\n')[1:]
        print(self.options_expiry_dates)
        
        self.options_years = 1
        self.options_expiry_dates = 3
        self.options_strike_prices = 4


    def get_futures_data(self, expiry_date: str, current_year: bool = False):
        pass

    def get_options_data(self, expiry_date: str, option_type: str, strike_price: str, current_year: bool = False):
        pass


    def __del__(self):
        self.driver.close()

