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
    def __init__(self, thread_id=None, thread_name=None, slack=False, sendgrid=False, number_of_rediff_instruments=10):
        threading.Thread.__init__(self)
        self.class_name = TradedToPercentDelivered.__name__
        self.number_of_rediff_instruments = number_of_rediff_instruments
        self.local_datetime = datetime.now().astimezone(tzlocal())
        self.local_time = str(self.local_datetime).split(' ')[1].split('.')[0]
        self.equity_scraper = EquityScraper()
        self.slack_notif = slack
        self.sendgrid_notif = sendgrid
        

    def run(self):
        
        # Check if we have the list in DB
        gl_objects_list = list(self.get_stored_securities_from_db())
        if len(gl_objects_list) == 0:
            gainers_info_nse = NSEIndiaGLScraper(info_type='Gainers', view_type='All Securities')
            gainers_list_nse = gainers_info_nse.get_instruments(complete_info=False)
            gainers_info_rediff = RediffMoneyGLScraper(view_type='All')
            gainers_list_rediff = gainers_info_rediff.get_instruments(limit_number_of_instruments=self.number_of_rediff_instruments)
            gainers_list = list(set(gainers_list_nse).union(set(gainers_list_rediff)))
            percent_delivered_dict = self.equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')
            percent_delivered = list(percent_delivered_dict.values())
            previous_close_prices = list(self.equity_scraper.get_info_all(gainers_list, specific_info_key='previousClose').values())
            # Storing the list for future use
            self.store_securities_in_db(gainers_list)
            self.store_percent_delivered_in_db(percent_delivered)
            self.store_previous_close_price_in_db(previous_close_prices)
        else:
            # Getting only the first object
            percent_delivered = gl_objects_list[0].percentDelivered
            gainers_list = gl_objects_list[0].listOfCompanies

        last_price = self.equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')
        self.store_last_price_in_db(list(last_price.values()))

        table = PrettyTable(['Security', 'TradedToDelivered', 'LastPrice'])

        for security, percent_delivered in zip(gainers_list, percent_delivered):
            table.add_row([security, percent_delivered, last_price[security]])

        Logger.info(message=table.get_string(), push_to_slack=self.slack_notif)
        Logger.info(message=table.get_html_string(), push_to_sendgrid=self.sendgrid_notif, sendgrid_subject=self.class_name)



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

    def store_previous_close_price_in_db(self, previous_close_prices: list):
        gl_object = list(self.get_stored_securities_from_db())[0]
        gl_object.previousClosePrice = previous_close_prices
        gl_object.save()

