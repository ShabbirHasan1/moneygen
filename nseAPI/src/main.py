from webscraper.index_historical.index_historical_options import IndexHistoricalOptions
from util.log.logger import Logger
from webscraper.gainer_loser_info.nse_india_gl_scraper import NSEIndiaGLScraper
from webscraper.equity.equity_scraper import EquityScraper
from webscraper.gainer_loser_info.rediff_money_gl_scraper import RediffMoneyGLScraper


###### OPTIONS #######
# index_historical_options_call = IndexHistoricalOptions('BANKNIFTY', 'CE')
# index_historical_options_call.get_info_all()
# # index_historical_options_put = IndexHistoricalOptions('BANKNIFTY', 'PE')
# # print(index_historical_options_put.download_data_all())





# TODO: Implement multi threading to execute all scrapers parallely
# TODO: Write util methods to format slack messages
##### NSEIndia ######
def nse_india():
    gainers_info = NSEIndiaGLScraper(info_type='Gainers', view_type='All Securities')
    gainers_list = gainers_info.get_instruments(complete_info=False)
    equity_scraper = EquityScraper()
    percent_delivered = equity_scraper.get_info_all(gainers_list, specific_info_key='deliveryToTradedQuantity')
    last_price = equity_scraper.get_info_all(gainers_list, specific_info_key='lastPrice')

    ## Formatting output ##
    percent_delivered_str = '---------NSEIndia-------\ndeliveryToTradedQuantity--------\n'
    for item in percent_delivered:
        percent_delivered_str = percent_delivered_str + '{} - {}\n'.format(item, percent_delivered[item])


    last_price_str = 'lastPrice--------\n'
    for item in last_price:
        last_price_str = last_price_str + '{} - {}\n'.format(item, last_price[item])

    final_output = percent_delivered_str + '\n' + last_price_str
    ### ------- ###

    Logger.info(final_output, push_to_slack=True)


##### Rediff money ######
def rediff_money():
    gainers_info = RediffMoneyGLScraper(view_type='All')
    gainers_list = gainers_info.get_instruments(limit_number_of_instruments=3)
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




nse_india()
rediff_money()