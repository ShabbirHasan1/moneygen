import time
from selenium_dispatcher import SeleniumDispatcher
from selenium.webdriver.support.select import Select
from index_derivative_historical import IndexDerivativeHistorical
from config import Config


class IndexDerivativeHistoricalOptions(IndexDerivativeHistorical):
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
    def __init__(self, symbol_name: str):
        super().__init__(symbol_name)

        # Get filtering information for OPTIONS
        # Select instrument specified in method params
        instrument_types_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-instrumentType']/select"
            )
        # print(instrument_types_select_element.text)
        instrument_types_selector = Select(instrument_types_select_element)
        instrument_types_selector.select_by_visible_text(
                self.instrument_types['OPTIONS']
            )
        time.sleep(Config.SLEEP_DURATION)
        print('Instrument type selected: ', self.instrument_types['OPTIONS'])

        # Dictonary to store year, expiry date of each year,
        # and strike prices for each option (call, put) wrt each expiry date
        self.year_expiry_type_strike_dict = dict()

    def get_available_years(self):
        # Get all available years for OPTIONS contracts
        date_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-year']/select"
            )
        self.options_years = date_select_element.text.split('\n')[1:]
        print('Available years fetch complete')

    def get_available_expiry_dates(self):
        # Get all available 'Expiry Dates' for OPTIONS contracts
        self.options_expiry_dates = dict()
        date_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-year']/select"
            )
        for year in self.options_years:
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            self.options_expiry_dates[year] = self.driver. \
                find_element_by_xpath(
                    "//div[@id='eq-derivatives-historical-expiryDate']/select"
                ).text.split('\n')[1:]
        print('Available expiry dates fetch for each year complete')

    def get_available_strike_prices(self, option_type: str):
        # Get all available strike prices for CALL OPTIONS
        date_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-year']/select"
            )
        self.year_expiry_type_strike_dict[option_type] = dict()
        for year in self.options_expiry_dates.keys():
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            self.year_expiry_type_strike_dict[option_type][year] = dict()
            for expiry_date in self.options_expiry_dates[year]:
                expiry_date_select_element = self.driver.\
                    find_element_by_xpath(
                        "//div[@id='eq-derivatives-historical-expiryDate']/"
                        + "select"
                    )
                Select(expiry_date_select_element).select_by_visible_text(
                    expiry_date)
                time.sleep(Config.SLEEP_DURATION)
                option_type_select_element = self.driver.find_element_by_xpath(
                    "//div[@id='eq-derivatives-historical-optionType']/select"
                    )
                Select(option_type_select_element).select_by_visible_text(
                    option_type
                    )
                time.sleep(Config.SLEEP_DURATION)
                strike_price_select_element = self.driver.\
                    find_element_by_xpath(
                        "//div[@id='eq-derivatives-historical-strikePrice']/"
                        + "select"
                    )
                self.year_expiry_type_strike_dict[option_type][year][expiry_date] = \
                    strike_price_select_element.text.split('\n')[2:]
        print('Strike prices fetch for "', option_type, '" option complete')

    def download_data_for_each_strike_price(self):
        print(self.year_expiry_type_strike_dict)
        self.driver.find_element_by_xpath('//a[@data_val="1Y"]').click()
        instrument_types_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-instrumentType']/select"
            )
        # print(instrument_types_select_element.text)
        instrument_types_selector = Select(instrument_types_select_element)
        instrument_types_selector.select_by_visible_text(
                self.instrument_types['OPTIONS']
            )
        time.sleep(Config.SLEEP_DURATION)
        date_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-year']/select"
            )
        self.driver.find_element_by_xpath("//a[@data-val='1Y']").click()
        for year in self.year_expiry_type_strike_dict[option_type].keys():
            Select(date_select_element).select_by_visible_text(year)
            time.sleep(Config.SLEEP_DURATION)
            for expiry_date in self.year_expiry_type_strike_dict[option_type][year].keys():
                expiry_date_select_element = self.driver.\
                    find_element_by_xpath(
                        "//div[@id='eq-derivatives-historical-expiryDate']/"
                        + "select"
                    )
                Select(expiry_date_select_element).select_by_visible_text(
                    expiry_date)
                time.sleep(Config.SLEEP_DURATION)
                option_type_select_element = self.driver.find_element_by_xpath(
                    "//div[@id='eq-derivatives-historical-optionType']/select"
                    )
                Select(option_type_select_element).select_by_visible_text(
                    option_type
                    )
                time.sleep(Config.SLEEP_DURATION)
                strike_price_select_element = self.driver.\
                    find_element_by_xpath(
                        "//div[@id='eq-derivatives-historical-strikePrice']/"
                        + "select"
                    )
                Select(strike_price_select_element).select_by_visible_text(self.year_expiry_type_strike_dict[option_type][year])
                self.driver.find_elements_by_xpath("//div[@class='xlsdownload']/a").click()



    def __del__(self):
        self.driver.close()
