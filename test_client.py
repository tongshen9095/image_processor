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

expt_dict1 = {"name": fname1, "dir": fpath1, "b64str": b64_str1}
expt_dict2 = {"name": fname2, "dir": fpath2, "b64str": b64_str2}
expt_dict3 = {"name": fname3, "dir": fpath3, "b64str": b64_str3}

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


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, "512 x 512"),
    (fpath2, "1024 x 1245"),
    (fpath3, "228 x 369")
])
def test_getImgSize(fpath, expt):
    from client import getImgSize
    img_size = getImgSize(fpath)
    assert img_size == expt


@pytest.mark.parametrize("fname, fpath, b64_str, expt", [
    (fname1, fpath1, b64_str1, expt_dict1),
    (fname2, fpath2, b64_str2, expt_dict2),
    (fname3, fpath3, b64_str3, expt_dict3),
])
def test_makeDict(fname, fpath, b64_str, expt):
    from client import makeDict
    in_dict = makeDict(fname, fpath, b64_str)
    assert in_dict == expt

