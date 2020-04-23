from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import base64
import requests
from PIL import Image

server_name = "http://127.0.0.1:5000"

def designWindow():
    root = Tk()

    # Add upload button
    upload_btn = ttk.Button(root, text="Upload", command=uploadBtnCmd)
    upload_btn.grid(column=0, row=0)

    root.mainloop()
    return


def uploadBtnCmd():
    """Command for upload botton."""
    fpath = selectImg()
    fname = parseName(fpath)
    b64_str = img2b64(fpath)
    img_size = getImgSize(fpath)
    print(img_size)
    #in_dict = makeDict(fname, fpath, b64_str)
    #print(in_dict)
    #cpostImg(in_dict)
    return


def selectImg():
    """Select an image from file browser.
    
    Returns:
        str: File path of the selected image.
    """
    fpath = filedialog.askopenfilename()
    return fpath


def parseName(fpath):
    """Extract the file name from the file path.

    Args:
        fpath (str): File path.
    Returns:
        str: File name.
    """
    return os.path.basename(fpath)


def img2b64(fpath):
    """Convert image file to base64 string.
    
    Args:
        fpath (str): File path.
    Return:
        str: base64 representation of the image file.
    """
    with open(fpath, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_str = str(b64_bytes, encoding='utf-8')
    return b64_str


def getImgSize(fpath):
    """Compute the image size.

    Args:
        fpath (str): File path.
    Returns:
        img_size (str): width x height
    """
    im = Image.open(fpath)
    w, h = im.size
    img_size = str(w) + " x " + str(h)
    return img_size


def makeDict(fname, fpath, b64_str):
    """Create the input dictionary.
    
    Args:
        fname (str): File name.
        fpath (str): File path.
        b64_str (str): Base64 representation of the image file.
    Returns:
        dict: An dictionary.
    """
    in_dict = {"name": fname, "dir": fpath, "b64str": b64_str}
    return in_dict


def cpostImg(in_dict):
    """Post requet from client site to upload image.

    Args:
        in_dict (dict): An input dictionary.
    """
    r = requests.post(server_name + "/api/new_img", json=in_dict)
    if r.status_code == 200:
        msg = "Success: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg, title="upload")
    else:
        msg = "Error: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg, title="upload", icon="error")
    return


if __name__ == "__main__":
    designWindow()
