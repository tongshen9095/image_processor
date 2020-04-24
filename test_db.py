import pytest
import db

db.initDb()

@pytest.mark.parametrize("img_name, expt", [
    ('esophagus2.jpg', True),
    ("acl2.jpg", True),
    ("abc.jpg", False)

])
def test_hasImg(img_name, expt):
    from db import hasImg
    ans = hasImg(img_name)
    assert ans == expt
