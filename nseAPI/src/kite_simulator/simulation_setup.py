from db.models import KiteSimulatorStateModel, GainerLoserInfoModel
from datetime import datetime, date
from config import Config
import numpy as np


class SimulationSetup:
    def __init__(self, funds=Config.KITE_FUNDS):
        self.class_name = SimulationSetup.__name__
        mongo_adapter = MongoAdapter()
        self.kite_state = KiteSimulatorStateModel(createdDate=str(date.today()), createdBy=self.class_name)
        self.funds = funds
        gl_object = get_stored_gainer_loser_info_from_db()[0]
        self.get_and_store_company_list(gl_object.listOfCompanies)
        self.get_and_store_funds()
        self.get_and_store_previous_close_price(gl_object.previousClosePrice)
        self.calc_and_store_number_of_stocks_per_company()
        self.calc_and_store_funds_per_company()
        self.calc_and_store_profit_slab_for_stocks()


    def get_and_store_company_list(self, listOfCompanies):
        self.kite_state.companies = listOfCompanies
        self.kite_state.save()

    def get_and_store_funds(self):
        self.kite_state.funds = self.funds
        self.kite_state.save()

    def get_and_store_previous_close_price(self, previousClosePrice):
        self.kite_state.previousClosePrice = previousClosePrice
        self.kite_state.save()

    def calc_and_store_funds_per_company(self):
        number_of_companies = len(self.kite_state.companies)
        self.funds_per_company = self.funds/number_of_companies
        self.kite_state.fundsPerCompany = self.funds_per_company
        self.kite_state.save()

    def calc_and_store_number_of_stocks_per_company(self):
        previous_close_price_float_array = np.array(self.kite_state.previousClosePrice).astype(np.float)
        self.kite_state.numberOfStocksPerCompany = np.floor(self.funds_per_company/previous_close_price_float_array - 1).tolist()
        self.kite_state.save()


    def calc_and_store_profit_slab_for_stocks(self):
        profit_slab = dict()
        for price in self.kite_state.previousClosePrice:
            if price <= 1:
                profit_slab[price] = 0.05
            elif price > 1 and price <= 10:
                profit_slab[price] = 0.5
            elif price > 10 and price <=100:
                profit_slab[price] = 1
            elif price > 100 and price <= 200:
                profit_slab[price] = 2
            elif price > 200 and price <=500:
                profit_slab[price] = 5
            else:
                profit_slab[price] = 10
        self.kite_state.profitSlab = profit_slab
        self.kite_state.save()
        self.kite_state.profitDifference = profit_slab.values()
        self.kite_state.save()


    def get_stored_gainer_loser_info_from_db(self):
        ''' Gets securities stored on same day
        '''
        gl_objects = GainerLoserInfoModel.objects.raw(
                {
                'createdDate': str(date.today())
                }
            )
        return gl_objects
