from pymodm import connect, MongoModel, fields

class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    b64str = fields.CharField()
    imgsize = fields.CharField()
    timestamp = fields.CharField()
    

def initDb():
    """Connect to database."""
    print("Connecting to database...")
    connect("mongodb+srv://db_access:9095@bme547-tla9o.mongodb.net/"
            "img?retryWrites=true&w=majority")
    print("Connected to database")


def addImg(in_dict):
    """Add image to database.

    Args:
         in_dict (dict): An dictionary.
    """
    img = Image(name=in_dict["name"],
                b64str=in_dict["b64str"],
                imgsize = in_dict["imgsize"],
                timestamp=in_dict["timestamp"])
    img.save()
                