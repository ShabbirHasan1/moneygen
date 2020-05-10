import requests
import pandas as pd
from io import StringIO

class AvailableSecurities:
    def __init__(self):
        pass

    def get_available_securities(self, columns=None, series='All'):
        res = requests.get('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
        df = pd.read_csv(StringIO(res.content.decode('utf-8')))
        if series != 'All':
            df = pd[df[' SERIES'] == series]
        
        if columns is None:
            return df.values.tolist()
        else:
            return df[columns].values.tolist()