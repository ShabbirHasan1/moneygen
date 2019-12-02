from webscraper.gainer_loser_info.base_gl_scraper import BaseGLScraper
from bs4 import BeautifulSoup
import requests


class RediffMoneyGLScraper(BaseGLScraper):
    '''Creates instance to scrape Gainers/Losers information from RediffMoney
    Parameters:
    view_type (str): Can only be 'All' or 'Nifty 50'
    '''
    def __init__(self, view_type: str):
        super().__init__()
        view_type_map = {
            'All':'groupall',
            'Nifty 50':'nifty'
        }
        self.view_type = view_type_map[view_type]
    

    def get_instruments(self, complete_info=False):
        url = 'https://money.rediff.com/gainers/nse/daily/' + self.view_type
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.findAll("table", attrs={"class": "dataTable"})[0]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            link = row.find_all('td')[0].find_all('a')[0]['href']
            cols = [ele.text.strip() for ele in cols]
            cols.append('https:'+link)
            data.append([ele for ele in cols if ele])
        # TODO: Return Symbols instead of names of instruments and check for complete data flag
        return data

    def get_instrument_info(self):
        pass