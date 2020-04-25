import pytest
import os
import filecmp

common_dir = "./images/"

fname1 = "acl1.jpg"
fname2 = "esophagus2.jpg"
fname3 = "synpic50411.jpg"

fpath1 = common_dir + fname1
fpath2 = common_dir + fname2
fpath3 = common_dir + fname3

b64_str1 = "/9j/4AAQSkZJRgABAgAA"
b64_str2 = "/9j/4AAQSkZJRgABAgAA"
b64_str3 = "/9j/4AAQSkZJRgABAgAA"

img_size1 = "512x512"
img_size2 = "1024x1245"
img_size3 = "228x369"

expt_dict1 = {"name": fname1,
              "b64str": b64_str1,
              "imgsize": img_size1,
              "processed": False}
expt_dict2 = {"name": fname2,
              "b64str": b64_str2,
              "imgsize": img_size2,
              "processed": False}
expt_dict3 = {"name": fname3,
              "b64str": b64_str3,
              "imgsize": img_size3,
              "processed": True}

img_ndarray1 = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
img_ndarray2 = [[205, 205, 205],
                [205, 205, 205],
                [205, 205, 205],
                [205, 205, 205],
                [205, 205, 205]]
img_ndarray3 = [[3, 3, 3],
                [2, 2, 2],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]

inv_b64_str1 = 'iVBORw0KGgoAAAANSUhE'
inv_b64_str2 = 'iVBORw0KGgoAAAANSUhE'
inv_b64_str3 = 'iVBORw0KGgoAAAANSUhE'


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, b64_str1),
    (fpath2, b64_str2),
    (fpath3, b64_str3)
])
def test_img2b64(fpath, expt):
    from transimg import img2b64
    b64_str = img2b64(fpath)
    assert b64_str[0:20] == expt


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, img_size1),
    (fpath2, img_size2),
    (fpath3, img_size3)
])
def test_getImgSize(fpath, expt):
    from transimg import getImgSize
    img_size = getImgSize(fpath)
    assert img_size == expt


@pytest.mark.parametrize("fname, b64_str, img_size, processed_status, expt", [
    (fname1, b64_str1, img_size1, False, expt_dict1),
    (fname2, b64_str2, img_size2, False, expt_dict2),
    (fname3, b64_str3, img_size3, True, expt_dict3),
])
def test_makeDict(fname, b64_str, img_size, processed_status, expt):
    from transimg import makeDict
    in_dict = makeDict(fname, b64_str, img_size, processed_status)
    expt["timestamp"] = in_dict["timestamp"]
    assert in_dict == expt


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, img_ndarray1),
    (fpath2, img_ndarray2),
    (fpath3, img_ndarray3)
])
def test_b64_to_ndarray(fpath, expt):
    from transimg import b64_to_ndarray, img2b64
    b64_str = img2b64(fpath)
    ans = b64_to_ndarray(b64_str)
    assert (ans[0][0:5] == expt).all


@pytest.mark.parametrize("fpath", [
    (fpath1),
    (fpath2),
    (fpath3)
])
def test_b64_to_img(fpath):
    from transimg import img2b64, b64_to_img
    b64_str = img2b64(fpath)
    out_fpath = "test_img.jpg"
    b64_to_img(b64_str, out_fpath)
    ans = filecmp.cmp(fpath, out_fpath)
    os.remove(out_fpath)
    assert ans


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, inv_b64_str1),
    (fpath2, inv_b64_str2),
    (fpath3, inv_b64_str3)
])
def test_invertImg(fpath, expt):
    from transimg import img2b64, invertImg
    b64_str1 = img2b64(fpath)
    inv_b64_str = invertImg(b64_str1)
    ans = inv_b64_str[:20]
    assert ans == expt
