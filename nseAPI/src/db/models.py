from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from config import Config



class GainerLoserInfoModel(MongoModel):
    listOfCompanies = fields.ListField()
    createdBy = fields.CharField()
    createdDate = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = Config.CONNECTION_ALIAS