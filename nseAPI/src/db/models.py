from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from config import Config
from db import MongoAdapter
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


class OrderModel(MongoModel):
    # TODO: Add fields for OrderModel
    orderId = fields.CharField()
    exchangeOrderId = fields.CharField()
    placedBy = fields.CharField()
    statuses = fields.ListField()
    statusMessages = fields.ListField()
    tradingSymbol = fields.ListField()
    symbolExchangeToken = fields.IntegerField()
    exchange = fields.CharField()
    orderType = fields.CharField()
    transactionType = fields.CharField()
    validity = fields.CharField()
    product = fields.CharField()
    averagePrice = fields.FloatField()
    price = fields.FloatField()
    quantity = fields.IntegerField()
    filledQuantity = fields.IntegerField()
    unfilledQuantity = fields.IntegerField()
    triggerPrice = fields.FloatField()
    userId = fields.CharField()
    orderTimestamp = fields.DateTimeField()
    exchangeTimestamp = fields.DateTimeField()
    lastChecksum = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = Config.CONNECTION_ALIAS