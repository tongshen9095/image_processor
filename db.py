from pymodm import connect, MongoModel, fields

class Image(MongoModel):
    name = fields.CharField()
    b64str = fields.CharField()
    timestamp = fields.CharField()
    imgsize = fields.CharField()

def init_db():
    """Connect to database."""
    print("Connecting to database...")
    connect("mongodb+srv://db_access:9095@bme547-tla9o.mongodb.net/"
            "img?retryWrites=true&w=majority")
    print("Connected to database")
