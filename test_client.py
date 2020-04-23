import pytest

common_dir = "/Users/tong/Documents/bme547/final-project-tongshen9095/images/"
fname1 = "acl1.jpg"
fname2 = "esophagus2.jpg"
fname3 = "synpic50411.jpg"
fpath1 = common_dir + fname1
fpath2 = common_dir + fname2
fpath3 = common_dir + fname3
b64_str1 = "/9j/4AAQSkZJRgABAgAA"
b64_str2 = "/9j/4AAQSkZJRgABAgAA"
b64_str3 = "/9j/4AAQSkZJRgABAgAA"


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, "acl1.jpg"),
    (fpath2, "esophagus2.jpg"),
    (fpath3, "synpic50411.jpg")
])
def test_parseName(fpath, expt):
    from client import parseName
    fname = parseName(fpath)
    assert fname == expt


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, b64_str1),
    (fpath2, b64_str2),
    (fpath3, b64_str3)
])
def test_img2b64(fpath, expt):
    from client import img2b64
    b64_str = img2b64(fpath)
    assert b64_str[0:20] == expt

"""
expt_dict1 = {"name": "acl1.jpg", "b64str": b64_str}

def test_makeDict(fname, b64_str, expt):
    from client import makeDict
    in_dict = makeDict(fname, b64_str)
    assert in_dict == expt
"""
