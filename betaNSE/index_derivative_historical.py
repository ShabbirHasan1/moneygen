class IndexDerivativeHistorical:
    def __init__(self):
        self.driver = SeleniumDispatcher().get_driver()
        self.driver.get(Config.HISTORICAL_DERIVATIVE_DATA_URL + symbol_name.upper())
        time.sleep(Config.SLEEP_DURATION)