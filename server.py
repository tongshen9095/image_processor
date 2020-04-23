from flask import Flask, jsonify, request

"""
app = Flask(__name__)

@app.route("/api/new_img", method=["POST"])
def postImg():
    sample_dict = {"name": str, "b64str": str}
    in_dict = request.get_json()
    isValid, msg = verifyInfo(in_dict, sample_dict)
    if not isValid:
        return msg, 400
"""


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
