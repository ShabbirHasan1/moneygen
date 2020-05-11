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
import sys
import traceback


class HistoricalData:
    def __init__(self):
        # TODO: Make date range configurable
        self.date_range = '24month' # Value in dropdown in target URL
        # TODO: Make series configurable
        self.series = 'ALL' # Value in dropdown on target URL
        self.engine = create_engine(Config.POSTGRES_CONNECTION_STRING)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_data_for_security(self, security_symbol: str) -> pd.DataFrame:
        url = f"https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={security_symbol}&segmentLink=3&symbolCount=2&series={self.series}&dateRange={self.date_range}&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE"
        res = requests.get(url, headers=Config.NSE_HEADERS)
        soup = BeautifulSoup(res.content, 'html.parser')
        try:
            data_stream = StringIO(soup.find(id='csvContentDiv').get_text())
        except BaseException as ex:
            Logger.err('Problem occured: '+ str(ex), push_to_slack=True)
            traceback.print_exc(3, file=sys.stdout)
            sys.exit()

        df = pd.read_csv(data_stream, lineterminator=':')
        return df

    
    def create_table_for_securities(self, symbols: list):
        
        for symbol in symbols:
            try:
                meta = MetaData()
                table = Table(
                    symbol, meta, 
                    Column('id', Integer, primary_key = True), 
                    Column('Symbol', String), 
                    Column('Series', String), 
                    Column('Date', String), 
                    Column('Prev Close', String), 
                    Column('Open Price', String), 
                    Column('High Price', String), 
                    Column('Low Price', String),
                    Column('Last Price', String),
                    Column('Close Price', String),
                    Column('Average Price', String),
                    Column('Total Traded Quantity', String),
                    Column('Turnover', String),
                    Column('No. of Trades', String),
                    Column('Deliverable Qty', String),
                    # using 'Pct' instead of '%' since Postgres doesn't allow that
                    Column('Pct Dly Qt to Traded Qty', String)
                )
                meta.create_all(self.engine)
            except IntegrityError:
                Logger.err('Table exists: ', symbol)
            
    # TODO: Make it add only the new data when run on daily basis
    def upsert_data(self, data: pd.DataFrame, symbol: str):
        base = declarative_base()
        # using 'Pct' instead of '%' since Postgres doesn't allow that
        df = data.rename(columns={'% Dly Qt to Traded Qty':'Pct Dly Qt to Traded Qty'})
        # df.to_sql(symbol, self.engine, index=False)
        attr_dict = {		
                '__tablename__': symbol,
                'id': Column(Integer, primary_key = True), 
                'Symbol': Column(String), 
                'Series': Column(String), 
                'Date': Column(String), 
                'Prev Close': Column(String), 
                'Open Price': Column(String), 
                'High Price': Column(String), 
                'Low Price': Column(String),
                'Last Price': Column(String),
                'Close Price': Column(String),
                'Average Price': Column(String),
                'Total Traded Quantity': Column(String),
                'Turnover': Column(String),
                'No. of Trades': Column(String),
                'Deliverable Qty': Column(String),
                # using 'Pct' instead of '%' since Postgres doesn't allow that
                'Pct Dly Qt to Traded Qty': Column(String)
            }
        try:
            TableInstance = type(symbol, (base,), attr_dict)
        except InvalidRequestError:
            Logger.err('Table instance already in memory: ', symbol)

        all_data = [TableInstance(**row_dict) for row_dict in df.to_dict(orient='rows')]
        try:
            self.session.bulk_save_objects(all_data)
            self.session.commit()
        except ProgrammingError:
            self.create_table_for_securities([symbol])
            self.session.bulk_save_objects(all_data)
            self.session.commit()
        