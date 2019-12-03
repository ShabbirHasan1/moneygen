from webscraper.gainer_loser_info import BaseGLScraper
from bs4 import BeautifulSoup
import requests


class RediffMoneyGLScraper(BaseGLScraper):
    '''Creates instance to scrape Gainers/Losers information from RediffMoney
    Parameters:
    view_type (str): Can only be 'All' or 'Nifty 50'
    '''
    # TODO: Add support for info_type (to switch between gainers and losers) as well
    def __init__(self, view_type: str):
        super().__init__()
        view_type_map = {
            'All':'groupall',
            'Nifty 50':'nifty'
        }
        self.view_type = view_type_map[view_type]
    

    def get_instruments(self, limit_number_of_instruments=-1, complete_info=False,):
        '''Get instruments

        Parameters:

        limit_number_of_instruments (int): Number of instruments for view_type='All'
        can go beyond 500 which can take time. Limit for fewer<->faster results.

        complete_info (bool): Specifies if complete info of instrument is needed,
        returns just symbol name otherwise.
        '''

        url = 'https://money.rediff.com/gainers/nse/daily/' + self.view_type
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.findAll("table", attrs={"class": "dataTable"})[0]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        # Get data of parent page (only tabular data)
        ## Going to instrument specific page will be required to get symbol name
        table_data = []

        if limit_number_of_instruments != -1:
            rows = rows[:limit_number_of_instruments]

        
        for row in rows:
            cols = row.find_all('td')
            link = row.find_all('td')[0].find_all('a')[0]['href']
            cols = [ele.text.strip() for ele in cols]
            cols.append('https:'+link)
            table_data.append([ele for ele in cols if ele])

        # Getting information related to each specific instrument
        instruments_data = dict()
        for instrument_data in table_data:
            instrument_name = instrument_data[0]
            child_data = self.__get_instrument_info(instrument_data, complete_info=complete_info)
            if complete_info:
                # Complete info will be a dict
                instruments_data[child_data['symbol']] = child_data
            else:
                # Solo info will just be symbol name for instrument
                instruments_data[child_data] = instrument_name

        # TODO: Remove multiple checks for `complete_info` flag
        return {True: instruments_data, False: list(instruments_data.keys())} [complete_info]


    def __get_instrument_info(self, instrument_data: list, complete_info=False):     
        instrument_url = instrument_data[4]
        res = requests.get(instrument_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        symbol = soup.findAll("input", attrs={"name": "nseCompanyCode"})[0]['value']
        if complete_info:
            complete_data_url = 'https://money.rediff.com/money1/currentstatus.php?companycode=' + symbol
            complete_data = requests.get(complete_data_url).json()
            complete_data['symbol'] = symbol
            return complete_data
        return symbol
