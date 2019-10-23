import time
from selenium_dispatcher import SeleniumDispatcher
from selenium.webdriver.support.select import Select
from index_derivative_historical import IndexDerivativeHistorical
from config import Config
import wget
from datetime import datetime
from datetime import timedelta
import os


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
        print('Initialising IndexDerivativeHistoricalOptions')
        super().__init__(symbol_name)
        self.instrument_type = Config.INSTRUMENT_TYPES['OPTIONS']
        self.instrument_type_value = Config.INSTRUMENT_TYPES_VALUES[self.instrument_type]
        self.symbol_name = symbol_name
        # Get filtering information for OPTIONS
        # Select instrument specified in method params
        instrument_types_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-instrumentType']/select"
            )
        # print(instrument_types_select_element.text)
        instrument_types_selector = Select(instrument_types_select_element)
        instrument_types_selector.select_by_visible_text(
                self.instrument_type
            )
        time.sleep(Config.SLEEP_DURATION)
        print('Instrument type selected: ', self.instrument_type)

        # Dictonary to store year, expiry date of each year,
        # and strike prices for each option (call, put) wrt each expiry date
        self.year_expiry_type_strike_dict = dict()
        print('IndexDerivativeHistoricalOptions initialised!')

    def get_available_years(self):
        print('Fetching available years')
        # Get all available years for OPTIONS contracts
        date_select_element = self.driver.find_element_by_xpath(
                "//div[@id='eq-derivatives-historical-year']/select"
            )
        self.options_years = date_select_element.text.split('\n')[1:]
        print('Total option years:', date_select_element.text)
        print('COMPLETE')

    def get_available_expiry_dates(self):
        print('Fetching available expiry dates for each year')
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
        print('COMPLETE!')

    def get_available_strike_prices(self, option_type: str):
        print('Getting available strike prices')
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
        print('COMPLETE!')

    def __download_data_for_each_strike_price(self, option_type):
        print('Downoading data for each strike price')
        # print(self.year_expiry_type_strike_dict['Put'])
        self.driver.find_element_by_xpath('//a[@data-val="1Y"]').click()
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
                try:
                    for strike_price in self.year_expiry_type_strike_dict[option_type][year][expiry_date]:
                        print('Selected strike price, expiry, option:', strike_price, expiry_date, option_type)
                        Select(strike_price_select_element).select_by_visible_text(strike_price)
                        time.sleep(1)
                        self.driver.find_element_by_xpath("//div[@class='xlsdownload']/a").click()
                except Exception:
                    print('Error occured, trying from last checkpoint')
                    self.download_data_for_each_strike_price(option_type)
        print('COMPLETE')

    def download_data_for_each_strike_price(self, option_type):
        option_type_val = Config.OPTIONS_TYPES[option_type]
        now_time = datetime.now()
        to_date_string = now_time.strftime("%d-%m-%Y")
        year_back_time = now_time - timedelta(days=365)
        from_date_string = year_back_time.strftime("%d-%m-%Y")
        for year in self.year_expiry_type_strike_dict[option_type].keys():
            for expiry_date in self.year_expiry_type_strike_dict[option_type][year].keys():
                for strike_price in self.year_expiry_type_strike_dict[option_type][year][expiry_date]:
                    if strike_price == '-':
                        strike_price = '0'
                    url = 'https://beta.nseindia.com/api/historical/fo/derivatives?&from=' + \
                        from_date_string + \
                        '&to=' + \
                        to_date_string + \
                        '&optionType=' + \
                        option_type_val + \
                        '&strikePrice=' + \
                        strike_price.split('.')[0] + \
                        '&expiryDate=' + \
                        expiry_date + \
                        '&instrumentType=' + \
                        self.instrument_type_value + \
                        '&symbol=' + \
                        self.symbol_name + \
                        '&csv=true'
                    print(url)
                    wget.download(
                        url=url,
                        out=os.path.join(
                                Config.DOWNLOAD_LOCATION,
                                expiry_date + '_' + strike_price + '_' + option_type + '.csv'
                            )
                    )

    def __del__(self):
        self.driver.close()
