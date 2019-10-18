import time
from config import Config
from selenium_dispatcher import SeleniumDispatcher

class IndexDerivativeHistorical:
    def __init__(self, symbol_name: str):
        self.driver = SeleniumDispatcher().get_driver()
        self.driver.get(Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper())
        time.sleep(Config.SLEEP_DURATION)