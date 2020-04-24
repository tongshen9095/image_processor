from flask import Flask, jsonify, request
import logging
import db

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
    db.initDb()
    app.run()
