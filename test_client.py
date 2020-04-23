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

img_size1 = "512 x 512"
img_size2 = "1024 x 1245"
img_size3 = "228 x 369"

expt_dict1 = {"name": fname1, "b64str": b64_str1, "imgsize": img_size1}
expt_dict2 = {"name": fname2, "b64str": b64_str2, "imgsize": img_size2}
expt_dict3 = {"name": fname3, "b64str": b64_str3, "imgsize": img_size3}

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


@pytest.mark.parametrize("fname, b64_str, img_size, expt", [
    (fname1, b64_str1, img_size1, expt_dict1),
    (fname2, b64_str2, img_size2, expt_dict2),
    (fname3, b64_str3, img_size3, expt_dict3),
])
def test_makeDict(fname, b64_str, img_size, expt):
    from client import makeDict
    in_dict = makeDict(fname, b64_str, img_size)
    expt["timestamp"] = in_dict["timestamp"]
    assert in_dict == expt
