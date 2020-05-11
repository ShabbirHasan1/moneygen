from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from config import Config
from db.mongo import MongoAdapter
from pymodm.connection import connect


# PyMODM connection
connect(MongoAdapter().get_connection_string(), alias=Config.CONNECTION_ALIAS)



class GainerLoserInfoModel(MongoModel):
    # TODO: add modifiedDate, modifiedBy in GainerLoserInfoModel
    listOfCompanies = fields.ListField()
    percentDelivered = fields.ListField()
    lastPrice = fields.DictField()
    openPrice = fields.ListField()
    highPrice = fields.ListField()
    lowPrice = fields.ListField()
    closePrice = fields.ListField()
    previousClosePrice = fields.ListField()
    createdBy = fields.CharField()
    createdDate = fields.CharField()
    createdTime = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = Config.CONNECTION_ALIAS


class KiteSimulatorStateModel(MongoModel):
    funds = fields.IntegerField()
    companies = fields.ListField()
    companyTokens = fields.ListField()
    previousClosePrice = fields.ListField()
    lowPrice = fields.ListField()
    fundsPerCompany = fields.IntegerField()
    numberOfStocksPerCompany = fields.ListField()
    buyPrice = fields.ListField()
    profitSlab = fields.ListField()
    profitablePrice = fields.ListField()
    profitDifference = fields.ListField()
    sellPrice = fields.ListField()
    pnl = fields.FloatField()
    pnlPerCompany = fields.ListField()
    createdBy = fields.CharField()
    createdDate = fields.CharField()
    simulationInitSuccessful = fields.BooleanField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = Config.CONNECTION_ALIAS