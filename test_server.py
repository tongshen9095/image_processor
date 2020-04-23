import pytest

sample_dict = {"name": str, "b64str": str}
in_dict1 = {"imgname": "apple.jpg", "b64str": 123}
expt1 =  (False, "name key not found")
in_dict2 = {"name": "apple.jpg", "b64str": 123}
expt2 = (False, "b64str value not correct type")
in_dict3 = {"name": "apple.jpg", "b64str": "123"}
expt3 = (True, "")


@pytest.mark.parametrize("in_dict, sample_dict, expt", [
    (in_dict1, sample_dict, expt1),
    (in_dict2, sample_dict, expt2),
    (in_dict3, sample_dict, expt3)
])
def test_verifyInfo(in_dict, sample_dict, expt):
    from server import verifyInfo
    ans = verifyInfo(in_dict, sample_dict)
    assert ans == expt
