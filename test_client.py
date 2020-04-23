import pytest

common_dir = "/Users/tong/Documents/bme547/final-project-tongshen9095/images/"
fpath1 = common_dir + "acl1.jpg"
fpath2 = common_dir + "esophagus2.jpg"
fpath3 = common_dir +  "synpic50411.jpg"


@pytest.mark.parametrize("fpath, expt", [
    (fpath1, "acl.1.jpg"),
    (fpath2, "esophagus2.jpg"),
    (fpath3, "synpic50411.jpg")
])
def test_parseName(fpath, expt):
    from client import parseName
    fname = parseName(fpath)
    assert fname == expt
