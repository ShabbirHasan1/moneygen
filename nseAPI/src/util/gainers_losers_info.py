import requests

class GainersLosersInfo(object):
    '''Creates instance to scrape Gainers/Losers information from NSEIndia
    Parameters:
    info_type (str): Can only be either 'Gainers' or 'Losers'
    view_type (str): Can only be:
                    - 'Nifty 50'
                    - 'Nifty Next 50'
                    - 'Securities > Rs.20'
                    - 'Securities < Rs.20'
                    - 'F&O Securities'
                    - 'All Securities'
    '''
    def __init__(self, info_type: str, view_type: str):
        self.info_type = info_type
        self.view_type_map = {
            'Nifty 50': 'nifty' + self.info_type + '1',
            'Nifty Next 50': 'jrNifty' + self.info_type + '1',
            'Securities > Rs.20': 'secGt20' + self.info_type + '1',
            'Securities < Rs.20': 'secLt20' + self.info_type + '1',
            'F&O Securities': 'fno' + self.info_type + '1',
            'All Securities': 'allTop' + self.info_type + '1',
        }
        self.view_type = self.view_type_map[view_type]

    def get_instruments(self):
        res = requests.get(
                'https://www.nseindia.com/live_market/dynaContent/live_analysis/'
                + self.info_type.lower()
                + '/'
                + self.view_type
                + '.json'
            )
        data = res.json()
        symbol_info_list = data['data']
        symbols = list()
        for symbol_info in symbol_info_list:
            # Currently considering EQUITY series only
            if symbol_info['series'] == 'EQ':
                symbols.append(symbol_info['symbol'])
                
        return symbols