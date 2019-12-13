from tasks import TradedToPercentDelivered
from prettytable import PrettyTable
from util.log import Logger


class TradedToPercentDeliveredReport(TradedToPercentDelivered):
    def __init__(self, thread_id=None, thread_name=None, push_output_to_slack=False):
        super().__init__(thread_id, thread_name, push_output_to_slack)
        self.gl_object = list(super().get_stored_securities_from_db())[0]
        self.class_name = TradedToPercentDeliveredReport.__name__
    

    def run(self):
        
        open_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='open')
        high_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='dayHigh')
        low_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='dayLow')
        close_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='closePrice')

        self.store_open_price_in_db(list(open_price.values()))
        self.store_high_price_in_db(list(high_price.values()))
        self.store_low_price_in_db(list(low_price.values()))
        self.store_close_price_in_db(list(close_price.values()))

        report = self.generate_report()

        Logger.info(report.get_string(),push_to_slack=True)
        Logger.info(report.get_html_string(), push_to_slack=False, push_to_sendgrid=True, self.class_name)

    def generate_report(self):
        # Creating table headers
        table_headers = ['Security', 'TradedToDeliverd', 'Open', 'High', 'Low', 'Close']
        table = PrettyTable(table_headers)
        for security, percent, o, h, l, c in zip(
            self.gl_object.listOfCompanies, 
            self.gl_object.percentDelivered,
            self.gl_object.openPrice,
            self.gl_object.highPrice,
            self.gl_object.lowPrice,
            self.gl_object.closePrice,
            ):
            table.add_row([security, percent, o, h, l, c])
        
        for time in self.gl_object.lastPrice.keys():
            table.add_column(time, self.gl_object.lastPrice[time])

        return table
        


    def store_open_price_in_db(self, open_price: list):
        self.gl_object.openPrice = open_price
        self.gl_object.save()

    def store_high_price_in_db(self, high_price: list):
        self.gl_object.highPrice = high_price
        self.gl_object.save()

    def store_low_price_in_db(self, low_price: list):
        self.gl_object.lowPrice = low_price
        self.gl_object.save()
    
    def store_close_price_in_db(self, close_price: list):
        self.gl_object.closePrice = close_price
        self.gl_object.save()