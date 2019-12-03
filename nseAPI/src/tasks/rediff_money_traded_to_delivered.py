import threading
from util.log.logger import Logger
from webscraper.gainer_loser_info import RediffMoneyGLScraper
from webscraper.equity import EquityScraper


class RediffMoneyTradedToDelivered(threading.Thread):
    # TODO: thread_id, thread_name to be used in task manager
    def __init__(self, thread_id=None, thread_name=None):
        threading.Thread.__init__(self)

    def run(self):
        gainers_info = RediffMoneyGLScraper(view_type='All')
        gainers_list = gainers_info.get_instruments(limit_number_of_instruments=10)
        equity_scraper = EquityScraper()
        percent_delivered = equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')
        last_price = equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')

        ## Formatting output ##
        percent_delivered_str = '---------Rediff Money--------\ndeliveryToTradedQuantity-----\n'
        for item in percent_delivered:
            percent_delivered_str = percent_delivered_str + '{} - {}\n'.format(item, percent_delivered[item])


        last_price_str = 'lastPrice-----\n'
        for item in last_price:
            last_price_str = last_price_str + '{} - {}\n'.format(item, last_price[item])

        final_output = percent_delivered_str + '\n' + last_price_str
        ## --------- ##

        Logger.info(final_output, push_to_slack=True)