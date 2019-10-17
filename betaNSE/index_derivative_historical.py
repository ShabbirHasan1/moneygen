from selenium_dispatcher import SeleniumDispatcher

# Go to URL https://beta.nseindia.com/get-quotes/derivatives?symbol=<SYMBOLNAME>

class IndexDerivativeHistorical:
    def __init__(symbol_name: str):
        driver = SeleniumDispatcher().get_driver();
    
