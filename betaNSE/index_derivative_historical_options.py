import time
from selenium_dispatcher import SeleniumDispatcher
from selenium.webdriver.support.select import Select
from index_derivative_historical import IndexDerivativeHistorical
from config import Config

class IndexDerivativeHistoricalOptions():
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
        IndexDerivativeHistorical.__init__(self, symbol_name)

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
        print('Available years fetch complete')

        # Get all available 'Expiry Dates' for OPTIONS contracts
        self.options_expiry_dates = dict()
        for year in self.options_years:
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            self.options_expiry_dates[year] = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-expiryDate']/select").text.split('\n')[1:]
        print('Available expiry dates fetch for each year complete')

        # Get all available strike prices for CALL OPTIONS
        self.year_expiry_type_strike_dict = dict()
        for year in self.options_expiry_dates.keys():
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            for expiry_date in self.options_expiry_dates[year]:
                self.year_expiry_type_strike_dict[year] = dict()
                expiry_date_select_element = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-expiryDate']/select")
                Select(expiry_date_select_element).select_by_visible_text(expiry_date)
                option_type_select_element = self.driver.find_element_by_xpath("//div[@id='eq-derivatives-historical-optionType']/select")
                Select(option_type_select_element).select_by_visible_text('Call')
                



        # Get all available strike prices for PUT OPTIONS

        
        self.options_strike_prices = 4


    def get_available_years(self):
        pass


™   def get_available_expiry_dates(self):
        pass

    def get_available_strike_prices(self, option_type: str):
        pass

    def get_data_for_each_strike_price(self):
        pass

    def __del__(self):
        self.driver.close()

