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
import transimg

server_name = "http://127.0.0.1:5000"


def mainWindow():
    root = Tk()

    # Add a upload button
    upload_btn = ttk.Button(root, text="Upload", command=uploadBtnCmd)
    upload_btn.grid(column=0, row=0)

    # Add a main display buttun
    def popDisplayWindow():
        dw = 500
        dh = 750
        windowsize = str(dw) + "x" + str(dh)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select label
        select_label = ttk.Label(window, text="Select an image")
        xp, yp = 15, 2
        select_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)
        img_choice_box["values"] = cgetNames()

        # Put a blank image
        img_obj = Image.open("./images/blank.png").resize((dw, dw))
        tk_img = ImageTk.PhotoImage(img_obj)
        img_label = ttk.Label(window, image=tk_img)
        img_label.image = tk_img
        xp, yp = 0, 8
        img_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a text box
        h, w = 4, 300
        text_box = Text(window, height=h, width=w)
        yp = 85
        text_box.place(x=(dw-w)//2, y=dh*yp//100)

        # Add an Info button
        def infoBtnCmd():
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            in_dict = cgetImg(img_name)
            line1 = "timestamp: {}".format(in_dict["timestamp"])
            line2 = "image size: {} pixels".format(in_dict["imgsize"])
            text_box.delete("1.0", "end")
            text_box.insert(END, line1+"\n"+line2)
            return
        info_btn = ttk.Button(window, text="Info", command=infoBtnCmd)
        xp, yp = 60, 95
        info_btn.place(x=dw*xp//100, y=dh*yp//100)

        # Add a display button
        def displayBtnCmd():
            # Put a blank image
            img_obj = Image.open("./images/blank.png").resize((dw, dw))
            tk_img = ImageTk.PhotoImage(img_obj)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            xp, yp = 0, 8
            img_label.place(x=dw*xp//100, y=dh*yp//100)

            # Put medical image on top of the blank image
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            in_dict = cgetImg(img_name)
            x, y = imgResize(in_dict["imgsize"], dw)
            tk_img = getTkImg(in_dict["b64str"], x, y)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            img_label.place(x=(dw-x)//2, y=(dw-y)//2+dh*yp//100)
            return

        display_btn = ttk.Button(window, text="Display", command=displayBtnCmd)
        xp, yp = 20, 95
        display_btn.place(x=dw*xp//100, y=dh*yp//100)
        return

    main_display_btn = ttk.Button(root, text="Display",
                                  command=popDisplayWindow)
    main_display_btn.grid(column=1, row=0)

    # Add a main download button     
    def popDownloadWindow():
        dw = 500
        dh = 300
        windowsize = str(dw) + "x" + str(dh)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select label
        select_label = ttk.Label(window, text="Select an image")
        xp, yp = 15, 2
        select_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)
        img_choice_box["values"] = cgetNames()

        # Add a download button
        def downloadBtnCmd():
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            in_dict = cgetImg(img_name)
            fpath = filedialog.asksaveasfilename()
            if not fpath:
                msg = "Please select an directory to save your image."
                messagebox.showerror(message=msg, icon="error")
                return
            transimg.b64_to_img(in_dict["b64str"], fpath)
            msg = "Success: Download the image."
            messagebox.showinfo(message=msg)
            return
        download_btn = ttk.Button(window, text="Dowdload",
                                  command=downloadBtnCmd)
        xp, yp = 40, 80
        download_btn.place(x=dw*xp//100, y=dh*yp//100)
        return

    main_download_btn = ttk.Button(root, text="Download",
                                   command=popDownloadWindow)
    main_download_btn.grid(column=2, row=0)

    # Add a main process buttom
    def popProcessWindow():
        dw = 500
        dh = 300
        windowsize = str(dw) + "x" + str(dh)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select label
        select_label = ttk.Label(window, text="Select an image")
        xp, yp = 15, 2
        select_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)
        img_choice_box["values"] = cgetNames()

        # Add a process button
        def processBtnCmd():
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            cprocessImg(img_name)
            msg = "Success: Process the image."
            messagebox.showinfo(message=msg)
            return
        process_btn = ttk.Button(window, text="Process",
                                  command=processBtnCmd)
        xp, yp = 40, 80
        process_btn.place(x=dw*xp//100, y=dh*yp//100)
        return

    main_process_btn = ttk.Button(root, text="Process",
                                   command=popProcessWindow)
    main_process_btn.grid(column=3, row=0)

    root.mainloop()
    return


# function wrappers
def uploadBtnCmd():
    """Command for upload botton."""
    fpath = filedialog.askopenfilename()
    if not fpath:
        msg = "Please select an image first."
        messagebox.showinfo(message=msg, icon="error")
        return
    fname = parseName(fpath)
    b64_str = transimg.img2b64(fpath)
    img_size = transimg.getImgSize(fpath)
    in_dict = transimg.makeDict(fname, b64_str, img_size, False)
    cpostImg(in_dict)
    return


def getTkImg(b64_str, x, y):
    """Get tk image with the name of the image.
    Args:
        b64 (str): Base64 representation of the image.
    Returns:
        tk image object
    """
    img_ndarray = transimg.b64_to_ndarray(b64_str)
    tk_img = transimg.ndarray2img(img_ndarray, x, y)
    return tk_img


# Requests
def cpostImg(in_dict):
    """Post requet from client site to upload image.

    Args:
        in_dict (dict): An input dictionary.
    """
    r = requests.post(server_name + "/api/new_img", json=in_dict)
    if r.status_code == 200:
        msg = "Success: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg)
    else:
        msg = "Error: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg, icon="error")
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


def cprocessImg(img_name):
    """Get request from client site to initialize image processing.
    
    Args:
        img_name (str): Name of an image.
    """
    r = requests.get(server_name + "/api/process_img/{}".format(img_name))
    if r.staus != 200:
        msg = "Error: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg, icon="error")
        return
    return


def imgResize(img_size, dw):
    """Resize the image based on the default window width.

    Args:
        img_size (str): Original image size.
        dw (int): Default window width.
    Returns:
        tuple: Adjusted image size.
    """
    img_size = img_size.split("x")
    x, y = img_size
    x, y = int(x), int(y)
    if x > y:
        new_x = min(x, dw)
        new_y = y * new_x // x
    else:
        new_y = min(y, dw)
        new_x = x * new_y // y
    return new_x, new_y


def parseName(fpath):
    """Extract the file name from the file path.

    Args:
        fpath (str): File path.
    Returns:
        str: File name.
    """
    return os.path.basename(fpath)


if __name__ == "__main__":
    mainWindow()
