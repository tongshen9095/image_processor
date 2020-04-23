from pymodm import connect, MongoModel, fields

class Image(MongoModel):
    name = fields.CharField()
    b64str = fields.CharField()
    timestamp = fields.CharField()
    imgsize = fields.CharField()
