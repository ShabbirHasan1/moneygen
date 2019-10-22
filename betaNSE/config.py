import sys
import os


class Config(object):
    SELENIUM_DRIVER_BASE_PATH = 'chromedriver'
    SELENIUM_DRIVER_EXEC_PATH = \
        os.path.join(SELENIUM_DRIVER_BASE_PATH, sys.platform)
    HISTORICAL_DERIVATIVE_DATA_URL = \
        'https://beta.nseindia.com/get-quotes/derivatives?symbol='
    SLEEP_DURATION = 2
    INSTRUMENT_TYPES = {'OPTIONS': 'Index Options', 'FUTURES': 'Index Futures'}
    DOWNLOAD_LOCATION = '/Users/mayank.gupta/Moneygen/betaNSE/downloads'
    OPTIONS_TYPES = {'Call': 'CE', 'Put': 'PE'}
    DOWNLOAD_DATE_RANGE_FORMAT = 'DD-MM-YYYY'
    EXPIRY_DATE_FORMAT = 'DD-MMM-YYYY'
    INSTRUMENT_TYPES_VALUES = {'Index Options': 'OPTIDX', 'Index Futures': 'FUTIDX'}
