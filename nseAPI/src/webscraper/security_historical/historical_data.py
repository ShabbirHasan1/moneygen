import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from config import Config
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import *
from util.log import Logger


class HistoricalData:
    def __init__(self):
        # TODO: Make date range configurable
        self.date_range = '24months' # Value in dropdown in target URL
        # TODO: Make series configurable
        self.series = 'All'

    def get_data_for_security(self, security_symbol: str) -> pd.DataFrame:
        url = f"https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={security_symbol}&segmentLink=3&symbolCount=2&series={self.series}&dateRange={self.data_range}&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE"
        res = requests.get(url, headers=Config.NSE_HEADERS)
        soup = BeautifulSoup(res.content, 'html.parser')
        data_stream = StringIO(soup.find(id='csvContentDiv').get_text())
        df = pd.read_csv(data_stream, lineterminator=':')
        return df

    # TODO: Make it add only the new data when run on daily basis
    def create_table(self, symbols: list):
        engine = create_engine(Config.POSTGRES_CONNECTION_STRING)
        meta = MetaData()
        for symbol in symbols:
            try:
                table = Table(
                    symbol, meta, 
                    Column('id', Integer, primary_key = True), 
                    Column('Symbol', String), 
                    Column('Series', String), 
                    Column('Date', String), 
                    Column('Prev Close', Float), 
                    Column('Open Price', Float), 
                    Column('High Price', Float), 
                    Column('Low Price', Float),
                    Column('Last Price', Float),
                    Column('Close Price', Float),
                    Column('Average Price', Float),
                    Column('Total Traded Quantity', Float),
                    Column('Turnover', Float),
                    Column('No. of Trades', Float),
                    Column('Deliverable Qty', Float),
                    Column('% Dly Qt to Traded Qty', Float),
                )
            except IntegrityError:
                Logger.err('Table exists: ', symbol)
            
        meta.create_all(engine)

        