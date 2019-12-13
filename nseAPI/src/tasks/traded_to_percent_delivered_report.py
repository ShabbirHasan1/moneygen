from tasks import TradedToPercentDelivered

class TradedToPercentDeliveredReport(TradedToPercentDelivered):
    def __init__(self, thread_id=None, thread_name=None, push_output_to_slack=False):
        super().__init__(thread_id, thread_name, push_output_to_slack)
        self.gl_object = list(super().get_stored_securities_from_db())[0]
    

    def run(self):
        
        open_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='open')
        high_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='dayHigh')
        low_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='dayLow')
        close_price = self.equity_scraper.get_info_all(self.gl_object.listOfCompanies, specific_info_key='closePrice')

        self.store_open_price_in_db(list(open_price.values()))
        self.store_high_price_in_db(list(high_price.values()))
        self.store_low_price_in_db(list(low_price.values()))
        self.store_close_price_in_db(list(close_price.values()))


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