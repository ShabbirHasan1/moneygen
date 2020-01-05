from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from config import Config



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