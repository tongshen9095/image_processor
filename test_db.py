import pytest
import db

db.initDb("med_img_test")

in_dict1 = {"name": "test_img1.jpeg",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "120X123",
            "processed": False,
            "timestamp": "2020-05-07"}

in_dict2 = {"name": "test_img2.png",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "280X322",
            "processed": True,
            "timestamp": "2020-05-02"}

in_dict3 = {"name": "test_img3.jpg",
            "b64str": "/9j/4AAQSkZJRgABAgAA",
            "imgsize": "194X322",
            "processed": False,
            "timestamp": "2020-05-02"}

img_name1 = "test_img1.jpeg"
img_name2 = "test_img2.png"
img_name3 = "test_img3.jpg"


@pytest.mark.parametrize("in_dict", [
    (in_dict1),
    (in_dict2),
    (in_dict3)
])
def test_addImg(in_dict):
    name = db.addImg(in_dict)
    db.delImg(name)
    assert db.hasImg(name) == False


@pytest.mark.parametrize("img_name, expt", [
    (img_name1, True),
    (img_name2, True),
    (img_name3, False)
])
def test_hasImg(img_name, expt):
    db.addImg(in_dict1)
    db.addImg(in_dict2)
    ans = db.hasImg(img_name)
    assert ans == expt
    

