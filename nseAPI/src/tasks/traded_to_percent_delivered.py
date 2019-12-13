import threading
from util.log import Logger
from webscraper.gainer_loser_info import NSEIndiaGLScraper, RediffMoneyGLScraper
from webscraper.equity import EquityScraper
from db import MongoAdapter
from db.models import GainerLoserInfoModel
from datetime import datetime, date
from config import Config
from prettytable import PrettyTable
from dateutil.tz import *


class TradedToPercentDelivered(threading.Thread):
    # TODO: thread_id, thread_name to be used in task manager
    def __init__(self, thread_id=None, thread_name=None, push_output_to_slack=False, number_of_rediff_instruments=10):
        threading.Thread.__init__(self)
        self.class_name = TradedToPercentDelivered.__name__
        self.slack_output=push_output_to_slack
        self.number_of_rediff_instruments = number_of_rediff_instruments
        self.local_datetime = datetime.now().astimezone(tzlocal())
        self.local_time = str(self.local_datetime).split(' ')[1].split('.')[0]
        self.equity_scraper = EquityScraper()
        

    def run(self):
        
        # Check if we have the list in DB
        gainers_list = list(self.get_stored_securities_from_db())
        if len(gainers_list) == 0:
            gainers_info_nse = NSEIndiaGLScraper(info_type='Gainers', view_type='All Securities')
            gainers_list_nse = gainers_info_nse.get_instruments(complete_info=False)
            gainers_info_rediff = RediffMoneyGLScraper(view_type='All')
            gainers_list_rediff = gainers_info_rediff.get_instruments(limit_number_of_instruments=self.number_of_rediff_instruments)
            gainers_list = list(set(gainers_list_nse).union(set(gainers_list_rediff)))
            percent_delivered = self.equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')
            # Storing the list for future use
            self.store_securities_in_db(gainers_list)
            self.store_percent_delivered_in_db(list(percent_delivered.values()))
        else:
            # Getting only the first object
            gainers_list = gainers_list[0].listOfCompanies

        last_price = self.equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')
        self.store_last_price_in_db(list(last_price.values()))

        table = PrettyTable(['Security', 'TradedToDelivered', 'LastPrice'])

        for security in gainers_list:
            table.add_row([security, percent_delivered[security], last_price[security]])

        Logger.info(message=table.get_html_string())
        Logger.info(message=table.get_string())



    def get_stored_securities_from_db(self):
        ''' Gets securities stored on same day
        '''
        mongo_adapter = MongoAdapter()
        gl_objects = GainerLoserInfoModel.objects.raw(
                {
                'createdBy': self.class_name,
                'createdDate': str(date.today())
                }
            )
        return gl_objects


    def store_securities_in_db(self, securities: list):
        ''' Stores securities with date and jobname
        '''
        mongo_adapter = MongoAdapter()
        GainerLoserInfoModel(
                listOfCompanies=securities, 
                createdBy=self.class_name,
                createdDate=str(date.today()),
                createdTime=self.local_datetime
            ).save()

    def store_percent_delivered_in_db(self, percent_delivered: list):
        gl_object = list(self.get_stored_securities_from_db())[0]
        gl_object.percentDelivered = percent_delivered
        gl_object.save()

    def store_last_price_in_db(self, last_price: list):
        gl_object = list(self.get_stored_securities_from_db())[0]
        gl_object.lastPrice[self.local_time] = last_price
        gl_object.save()

