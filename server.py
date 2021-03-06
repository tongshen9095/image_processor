from flask import Flask, jsonify, request
import logging
import db
import transimg

app = Flask(__name__)


@app.route("/api/new_img", methods=["POST"])
def postImg():
    """Post request from server to add image to database.

    returns:
        (tuple): tuple containing:
        str: Status message.
        str: Status code.
    """
    sample_dict = {"name": str,
                   "b64str": str,
                   "imgsize": str,
                   "processed": bool,
                   "timestamp": str}
    in_dict = request.get_json()
    isValid, msg = verifyInfo(in_dict, sample_dict)
    if not isValid:
        return msg, 400
    logging.info("post a new image: {}".format(in_dict["name"]))
    db.addImg(in_dict)
    return "image added", 200


@app.route("/api/all_imgs", methods=["GET"])
def getNames():
    """Get the list of image names.

    Returns:
        list: A list of image names.
    """
    ans = db.getNames()
    return jsonify(ans)


@app.route("/api/img/<img_name>", methods=["GET"])
def getImg(img_name):
    """Get the information of an image.

    Args:
        img_name (str): Name of the image.
    Returns:
        dict: An dictionary contains image information.
    """
    in_dict = db.getImg(img_name)
    return jsonify(in_dict)


@app.route("/api/process_img/<img_name>", methods=["GET"])
def processImg(img_name):
    """Invert the image and add the image to database.

    Args:
        img_name (str): Name of the image.
    """
    in_dict = db.getImg(img_name)
    inv_b64_str = transimg.invertImg(in_dict["b64str"])
    fname = img_name.split(".")[0] + "_proecessed" + ".jpg"
    inv_in_dict = transimg.makeDict(fname, inv_b64_str,
                                    in_dict["imgsize"], True)
    db.addImg(inv_in_dict)
    return "Success: process the image"


@app.route("/api/all_imgs/<processed>")
def getSelectedNames(processed):
    """Get the list of names of selected images.

    Args:
        processed (str): "1" processed image, "0" unprocessed image
    Returns:
        list: A list of image names.
    """
    ans = db.getSelectedNames(processed)
    return jsonify(ans)


@app.route("/api/del/<img_name>")
def delImg(img_name):
    db.delImg(img_name)
    return "Success: delete the image"


def verifyInfo(in_dict, sample_dict):
    """Verify whether the input dictionary is valid.
    An input dictionary is valid when 1) all the keys in the sample dictionary
    can be found in the input dictionary; 2) values in the input dictionary
    should have the same datatype as what in the smaple dictionary

    Args:
        in_dict (dict): An input dictionary.
        sample_dict (dict): An sample dictionary.
    Returns:
        (tuple): tuple containing:
            bool: True if the input dictionary is valid else False.
            str: Detialed message about the checking status.
    """
    for key, ddtype in sample_dict.items():
        if key not in in_dict:
            msg = "{} key not found".format(key)
            return False, msg
        if type(in_dict[key]) is not ddtype:
            msg = "{} value not correct type".format(key)
            return False, msg
    return True, ""


if __name__ == "__main__":
    log_fpath = "develop.log"
    logging.basicConfig(filename=log_fpath, level=logging.INFO)
    db.initDb("medicalimage")
    app.run()
