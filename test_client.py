import pytest


common_dir = "./images/"

fname1 = "acl1.jpg"
fname2 = "esophagus2.jpg"
fname3 = "synpic50411.jpg"

fpath1 = common_dir + fname1
fpath2 = common_dir + fname2
fpath3 = common_dir + fname3

img_size1 = "512x512"
img_size2 = "1024x1245"
img_size3 = "228x369"

img_size_adjust1 = (500, 500)
img_size_adjust2 = (411, 500)
img_size_adjust3 = (228, 369)


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, fname1),
    (fpath2, fname2),
    (fpath3, fname3)
])
def test_parseName(fpath, expt):
    from client import parseName
    fname = parseName(fpath)
    assert fname == expt


@pytest.mark.parametrize("img_size, dw, expt", [
    (img_size1, 500, img_size_adjust1),
    (img_size2, 500, img_size_adjust2),
    (img_size3, 500, img_size_adjust3)
])
def test_imgResize(img_size, dw, expt):
    from client import imgResize
    ans = imgResize(img_size, dw)
    assert ans == expt
