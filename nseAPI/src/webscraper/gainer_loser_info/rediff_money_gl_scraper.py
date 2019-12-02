from webscraper.gainer_loser_info.base_gl_scraper import BaseGLScraper


class RediffMoneyGLScraper(BaseGLScraper):
    '''Creates instance to scrape Gainers/Losers information from RediffMoney
    Parameters:
    view_type (str): Can only be 'All' or 'Nifty 50'
    '''
    def __init__(self):
        super().__init__()
    

    def get_instruments(self, complete_info=False):
        pass

    def get_instrument_info(self):
        pass