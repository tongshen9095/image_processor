from pymodm import connect, MongoModel, fields


class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    b64str = fields.CharField()
    imgsize = fields.CharField()
    processed = fields.BooleanField()
    timestamp = fields.CharField()


def initDb():
    """Connect to database."""
    print("Connecting to database...")
    connect("mongodb+srv://db_access:9095@bme547-tla9o.mongodb.net/"
            "medicalimage?retryWrites=true&w=majority")
    print("Connected to database")
    return


def addImg(in_dict):
    """Add image to database.

    Args:
         in_dict (dict): An dictionary.
    """
    img = Image(name=in_dict["name"],
                b64str=in_dict["b64str"],
                imgsize=in_dict["imgsize"],
                processed=in_dict["processed"],
                timestamp=in_dict["timestamp"])
    img.save()
    return


def getNames():
    """Get a list of image names.

    Returns:
        list: a list of image names.
    """
    imgs = Image.objects.raw({})
    ans = []
    for img in imgs:
        ans.append(img.name)
    return ans

