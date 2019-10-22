import time
from config import Config
from selenium_dispatcher import SeleniumDispatcher


class IndexDerivativeHistorical:
    def __init__(self, symbol_name: str):
        self.driver = SeleniumDispatcher(download_path='/Users/mayank.gupta/Moneygen/betaNSE/downloads').get_driver()
        self.driver.get(
                Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper()
            )
        time.sleep(Config.SLEEP_DURATION)
        # Click on 'All Historical Data'
        self.driver.find_element_by_link_text('All Historical Data').click()

        # Get instrument types from config
        time.sleep(Config.SLEEP_DURATION + 8)
