from db.models import KiteSimulatorStateModel, GainerLoserInfoModel
from datetime import datetime, date


class SimulationSetup:
    def __init__(self, funds=10000):
        self.class_name = SimulationSetup.__name__
        mongo_adapter = MongoAdapter()
        kite_state
        gl_object = get_stored_gainer_loser_info_from_db()[0]
        self.get_and_store_company_list(gl_object.listOfCompanies)
        self.get_and_store_funds(funds)
        self.get_and_store_previous_close_price(gl_object.previousClosePrice)
        self.calc_and_store_number_of_stocks_per_company()
        self.calc_and_store_number_of_stocks_per_company()
        self.calc_and_store_profit_slab_for_stocks()
        



    def get_and_store_company_list(self, listOfCompanies):
        pass

    def get_and_store_funds(self):
        pass

    def get_and_store_previous_close_price(self):
        pass

    def calc_and_store_funds_per_company(self):
        pass

    def calc_and_store_number_of_stocks_per_company(self):
        pass

    def calc_and_store_profit_slab_for_stocks(self):
        pass


    def get_stored_gainer_loser_info_from_db(self):
        ''' Gets securities stored on same day
        '''
        gl_objects = GainerLoserInfoModel.objects.raw(
                {
                'createdBy': self.class_name,
                'createdDate': str(date.today())
                }
            )
        return gl_objects
