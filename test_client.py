import pytest

common_dir = "/Users/tong/Documents/bme547/final-project-tongshen9095/images/"
fpath1 = common_dir + "acl1.jpg"
fpath2 = common_dir + "esophagus2.jpg"
fpath3 = common_dir +  "synpic50411.jpg"


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
    (fpath1, "/9j/4AAQSkZJRgABAgAA"),
    (fpath2, "/9j/4AAQSkZJRgABAgAA"),
    (fpath3, "/9j/4AAQSkZJRgABAgAA")
])
def test_img2b64(fpath, expt):
    from client import img2b64
    b64_str = img2b64(fpath)
    assert b64_str[0:20] == expt

