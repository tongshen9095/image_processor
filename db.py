from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors


class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    b64str = fields.CharField()
    imgsize = fields.CharField()
    processed = fields.BooleanField()
    timestamp = fields.CharField()


def initDb(db_name):
    """Connect to database."""
    print("Connecting to database...")
    connect("mongodb+srv://db_access:9095@bme547-tla9o.mongodb.net/"
            "{}?retryWrites=true&w=majority".format(db_name))
    print("Connected to database")
    return


def addImg(in_dict):
    """Add image to database.

    Args:
        in_dict (dict): An dictionary.
    Returns:
        str: name of the saved image.
    """
    img = Image(name=in_dict["name"],
                b64str=in_dict["b64str"],
                imgsize=in_dict["imgsize"],
                processed=in_dict["processed"],
                timestamp=in_dict["timestamp"])
    ans = img.save()
    return ans.name


def getNames():
    """Get a list of image names.

    Returns:
        list: a list of image names.
    """
    imgs = Image.objects.raw({})
    ans = []
    for img in imgs:
        ans.append(img.name)
    ans.sort()
    return ans


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


def getSelectedNames(processed):
    """Returns a list of names of processed / unprocessed images.

    Args:
        processed (str): "1" processed image, "0" unprocessed image
    Return:
        list: a list of selected image names.
    """
    if processed == "1":
        status = True
    else:
        status = False
    imgs = Image.objects.raw({"processed": status})
    ans = []
    for img in imgs:
        ans.append(img.name)
    ans.sort()
    return ans


def delImg(img_name):
    """Delete an image from the database.

    Args:
        img_name (str): Name of the image
    Returns:
        str: name of the deleted image.
    """
    img = Image.objects.raw({"_id": img_name}).first()
    img.delete()
    return


def hasImg(img_name):
    """Check whether the database has the image.

    Args:
        name (str): img_name
    Returns:
        True if the database contains the image, False if not.
    """
    try:
        Image.objects.raw({"_id": img_name}).first()
        return True
    except pymodm_errors.DoesNotExist:
        return False
