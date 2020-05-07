import pytest
import db

db.initDb()

in_dict1 = {"name": "test_img1",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "120X123",
            "processed": False,
            "timestamp": "2020-05-07"}

in_dict2 = {"name": "test_img2",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "280X322",
            "processed": True,
            "timestamp": "2020-05-02"}

in_dict3 = {"name": "test_img3",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "194X322",
            "processed": False,
            "timestamp": "2020-05-02"}


@pytest.mark.parametrize("in_dict", [
    (in_dict1),
    (in_dict2),
    (in_dict3)
])
def test_addImg(in_dict):
    from db import addImg
    name = addImg(in_dict)
    db.delImg(name)
    assert name == in_dict["name"]
