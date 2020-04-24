from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import base64
import requests
from PIL import Image, ImageTk
import datetime
import json
import io
import matplotlib.image as mpimg
from skimage.io import imsave

server_name = "http://127.0.0.1:5000"


def mainWindow():
    root = Tk()

    # Add a upload button
    upload_btn = ttk.Button(root, text="Upload", command=uploadBtnCmd)
    upload_btn.grid(column=0, row=0)

    # Add a main display buttun
    def popDisplayWindow():
        dw = 500
        ph = 100
        windowsize = str(dw) + "x" + str(dw+ph)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select label
        select_label = ttk.Label(window, text="Select an image")
        select_label.grid(column=0, row=0)

        # Add a choice box
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice)
        img_choice_box.grid(column=1, row=0)
        img_choice_box["values"] = cgetNames()

        # Put a blank image
        img_obj = Image.open("./images/blank.png").resize((dw, dw))
        tk_img = ImageTk.PhotoImage(img_obj, dw)
        img_label = ttk.Label(window, image=tk_img)
        img_label.image = tk_img
        img_label.grid(column=0, row=1, columnspan=2)

        # Add a display button
        def displayBtnCmd():
            img_name = img_choice.get()
            tk_img = getTkImg(img_name)
            img_label.image = tk_img
            img_label.configure(image=tk_img)
            return
        
        display_btn = ttk.Button(window, text="display", command=displayBtnCmd)
        display_btn.grid(column=0, row=2, columnspan=2)
        return
    
    main_display_btn = ttk.Button(root, text="Display",
                                  command=popDisplayWindow)
    main_display_btn.grid(column=1, row=0)

    root.mainloop()
    return


def uploadBtnCmd():
    """Command for upload botton."""
    fpath = selectImg()
    fname = parseName(fpath)
    b64_str = img2b64(fpath)
    img_size = getImgSize(fpath)
    in_dict = makeDict(fname, b64_str, img_size)
    cpostImg(in_dict)
    return


def getTkImg(img_name, dw):
    """Get tk image with the name of the image.
    Args:
        img_name (str): Name of the image.
    Returns:
        tk image object
    """
    in_dict = cgetImg(img_name)
    b64_str = in_dict["b64str"]
    img_size = in_dict["imgsize"]
    img_size_adjust = imgResize(img_size, dw)
    img_ndarray = b64_to_ndarray(b64_str)
    tk_img = ndarray2img(img_ndarray, img_size_adjust)
    return tk_img


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
    img_size = str(w) + "x" + str(h)
    return img_size


def makeDict(fname, b64_str, img_size):
    """Create the input dictionary.

    Args:
        fname (str): File name.
        b64_str (str): Base64 representation of the image file.
        img_size (str): Image size.
    Returns:
        dict: An dictionary.
    """
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    in_dict = {"name": fname,
               "b64str": b64_str,
               "imgsize": img_size,
               "processed": False,
               "timestamp": curr_time_str}
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


def cgetNames():
    """Get request from client site to get a list of image names.

    Returns:
        list: A list of image names.
    """
    r = requests.get(server_name + "/api/all_imgs")
    ans = json.loads(r.text)
    ans = tuple(ans)
    return ans


def cgetImg(img_name):
    """Get request from client site to get the information of an image.

    Args:
        img_name (str): Name of an image.
    Returns:
        dict: An dictionary of image information.
    """
    r = requests.get(server_name + "/api/img/{}".format(img_name))
    return json.loads(r.text)


def b64_to_ndarray(b64_str):
    """Convert base64 string to ndarray.

    Args:
        b64_str (str): base64 string.
    Returns:
        ndarray: An ndarray containing image data.
    """
    img_bytes = base64.b64decode(b64_str)
    img_buf = io.BytesIO(img_bytes)
    img_ndarray = mpimg.imread(img_buf, format='JPG')
    return img_ndarray


def ndarray2img(img_ndarray, img_size_adjust):
    """Convert ndarray to tk image.

    Args:
        img_ndarray: An ndarray containing image data.
    Returns:
        tk_image object
    """
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img).resize(img_size_adjust)
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image

def imgResize(img_size, dw):
    """Resize the image based on the default window width.
    
    Args:
        img_size (str): Original image size.
        dw (int): Default window width.
    Returns:
        tuple: Adjusted image size.
    """
    x, y = float(img_size[0])


if __name__ == "__main__":
    mainWindow()
