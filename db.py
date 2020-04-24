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

def hasImg(img_name):
    """Check wheter an image is in the database.

    Args:
        img_name (str): Name of the image.
    Returns:
        (bool): True if the image is in the database else False.
    """
    try:
        Image.objects.raw({"_id": img_name}).first()
        return True
    except:
        return False

def getImg(img_name):
    """Get an image form the database.

    Args:
        img_name (str): Name of the image.
    Returns:
        dict: An dictionary of the image info.
    """
    img = Image.objects.raw({"_id": img_name}).first()
    in_dict = {}
    in_dict["name"] = img.name
    in_dict["b64str"] = img.b64str
    in_dict["imgsize"] = img.imgsize
    in_dict["processed"] = img.processed
    in_dict["timestamp"] = img.timestamp
    return in_dict

