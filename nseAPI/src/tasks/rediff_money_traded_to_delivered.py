import threading
from util.log import Logger
from webscraper.gainer_loser_info import RediffMoneyGLScraper
from webscraper.equity import EquityScraper
from config import Config
from db.mongo_adapter import MongoAdapter
from db.models import GainerLoserInfoModel
from datetime import datetime


class RediffMoneyTradedToDelivered(threading.Thread):
    # TODO: thread_id, thread_name to be used in task manager
    def __init__(self, thread_id=None, thread_name=None, push_output_to_slack=False, number_of_instruments=10):
        threading.Thread.__init__(self)
        self.class_name = RediffMoneyTradedToDelivered.__name__
        self.slack_output=push_output_to_slack
        self.number_of_instruments = number_of_instruments

    def run(self):
        # Check if we have the list in DB
        gainers_list = list(self.get_stored_securities_from_db())
        if len(gainers_list) == 0:
            gainers_info = RediffMoneyGLScraper(view_type='All')
            gainers_list = gainers_info.get_instruments(limit_number_of_instruments=self.number_of_instruments)
            # Storing the list for future use
            self.store_securities_in_db(gainers_list)
        else:
            # Getting only the first object
            gainers_list = gainers_list[0].listOfCompanies

        equity_scraper = EquityScraper()
        percent_delivered = equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')
        last_price = equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')

        ## Formatting output ##
        # TODO: Use python text tables to make it look good
        percent_delivered_str = '---------Rediff Money--------\ndeliveryToTradedQuantity-----\n'
        for item in percent_delivered:
            percent_delivered_str = percent_delivered_str + '{} - {}\n'.format(item, percent_delivered[item])


        last_price_str = 'lastPrice-----\n'
        for item in last_price:
            last_price_str = last_price_str + '{} - {}\n'.format(item, last_price[item])

        final_output = percent_delivered_str + '\n' + last_price_str
        ## --------- ##

        Logger.info(final_output, push_to_slack=self.slack_output)

    def get_stored_securities_from_db(self):
        ''' Gets securities stored on same day
        '''
        mongo_adapter = MongoAdapter()
        gl_objects = GainerLoserInfoModel.objects.raw(
                {
                'createdBy': self.class_name,
                'createdDate': datetime.now().strftime(Config.DATE_FORMAT)
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
                createdDate=datetime.now().strftime(Config.DATE_FORMAT)
            ).save()