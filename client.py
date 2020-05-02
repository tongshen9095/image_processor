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
    """Design a main Graphical User Interface."""
    root = Tk()

    # Add a main upload button
    upload_btn = ttk.Button(root, text="Upload", command=uploadBtnCmd)
    upload_btn.grid(column=0, row=0)

    # Add a main display buttun
    def popDisplayWindow():
        """Pop a window to display the images."""
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
        def updateChoice():
            """Update the values of the combobox."""
            status, img_names = cgetNames()
            if status:
                img_choice_box["values"] = img_names
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice,
                                      postcommand=updateChoice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Put a blank image
        img_obj = Image.open("./images/blank.png").resize((dw, dw))
        tk_img = ImageTk.PhotoImage(img_obj)
        img_label = ttk.Label(window, image=tk_img)
        img_label.image = tk_img
        xp, yp = 0, 8
        img_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a text box
        text_box = Text(window)
        xp, yp = 24, 82
        text_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add an Info button
        def infoBtnCmd():
            """Display image infomation."""
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, line1, line2 = infoHelper(img_name)
            if not status:
                return
            text_box.delete("1.0", "end")
            content = "name: {}".format(img_name) + "\n" + line1 + "\n" + line2
            text_box.insert(END, content)
            return
        info_btn = ttk.Button(window, text="Info", command=infoBtnCmd)
        xp, yp = 60, 95
        info_btn.place(x=dw*xp//100, y=dh*yp//100)

        # Add a display button
        def displayBtnCmd():
            """Display the image."""
            # Put a blank image
            img_obj = Image.open("./images/blank.png").resize((dw, dw))
            tk_img = ImageTk.PhotoImage(img_obj)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            xp, yp = 0, 8
            img_label.place(x=dw*xp//100, y=dh*yp//100)

            # Put a medical image on top of the blank image
            img_name = img_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, in_dict = cgetImg(img_name)
            if not status:
                return
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
        """Pop an window to download the image."""
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
        def updateChoice():
            """Update the values of the combobox."""
            status, img_names = cgetNames()
            if status:
                img_choice_box["values"] = img_names
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice,
                                      postcommand=updateChoice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add a download button
        def downloadBtnCmd():
            """Download the image."""
            img_name = img_choice.get()
            downloadHelper(img_name)
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
        """Pop an window to process the image."""
        dw = 500
        dh = 300
        windowsize = str(dw) + "x" + str(dh)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select label
        select_label = ttk.Label(window, text="Select an image")
        xp, yp = 15, 2
        select_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box for original images
        def updateChoice():
            """Update the values of the combobox."""
            status, img_names = cgetSelectedNames("0")
            if status:
                org_choice_box["values"] = img_names
        org_choice = StringVar()
        org_choice_box = ttk.Combobox(window, textvariable=org_choice,
                                      postcommand=updateChoice)
        xp, yp = 55, 2
        org_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add a process button
        def processBtnCmd():
            """Process the image."""
            img_name = org_choice.get()
            if not img_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            if not cprocessImg(img_name):
                return
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

    # Add a main compare button
    def popCompareWindow():
        """Pop an window to compare two images."""
        dw0 = 500
        dw = 1100
        dh = 750
        windowsize = str(dw) + "x" + str(dh)
        window = Toplevel(root)
        window.geometry(windowsize)

        # Add a select an orginal image label
        org_label = ttk.Label(window, text="Select an original image")
        xp, yp = 5, 2
        org_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a select a processed image label
        pro_label = ttk.Label(window, text="Select an processed image")
        xp, yp = 58, 2
        pro_label.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box for orginal images
        def updateOrgChoice():
            """Update the values of the combobox."""
            status, img_names = cgetSelectedNames("0")
            if status:
                org_choice_box["values"] = img_names
        org_choice = StringVar()
        org_choice_box = ttk.Combobox(window, textvariable=org_choice,
                                      postcommand=updateOrgChoice)
        xp, yp = 25, 2
        org_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add a choice box for processed images
        def updateProChoice():
            """Update the values of the combobox."""
            status, img_names = cgetSelectedNames("1")
            if status:
                pro_choice_box["values"] = img_names
        pro_choice = StringVar()
        pro_choice_box = ttk.Combobox(window, textvariable=pro_choice,
                                      postcommand=updateProChoice)
        xp, yp = 78, 2
        pro_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Put a blank image for display orginal images
        img_obj = Image.open("./images/blank.png").resize((dw, dw))
        tk_img = ImageTk.PhotoImage(img_obj)
        org_img_label = ttk.Label(window, image=tk_img)
        org_img_label.image = tk_img
        xp, yp = 0, 8
        org_img_label.place(x=dw*xp//100, y=dh*yp//100)

        # Put a blank image for display processed images
        pro_img_label = ttk.Label(window, image=tk_img)
        pro_img_label.image = tk_img
        yp = 8
        pro_img_label.place(x=600, y=dh*yp//100)

        # Add a text box for orginal image
        org_text_box = Text(window, width=50)
        xp, yp = 12, 82
        org_text_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add a text box for processed image
        pro_text_box = Text(window, width=50)
        xp, yp = 65, 82
        pro_text_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add an Info button for originl images
        def orgInfoBtnCmd():
            """Display the information of the original image."""
            org_name = org_choice.get()
            if not org_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, line1, line2 = infoHelper(org_name)
            if not status:
                return
            org_text_box.delete("1.0", "end")
            content = "name: {}".format(org_name) + "\n" + line1 + "\n" + line2
            org_text_box.insert(END, content)
            return
        org_info_btn = ttk.Button(window, text="Info", command=orgInfoBtnCmd)
        xp, yp = 30, 95
        org_info_btn.place(x=dw*xp//100, y=dh*yp//100)

        # Add an Info button for processed images
        def proInfoBtnCmd():
            """Display the image of the processed image."""
            pro_name = pro_choice.get()
            if not pro_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, line1, line2 = infoHelper(pro_name)
            if not status:
                return
            pro_text_box.delete("1.0", "end")
            content = "name: {}".format(pro_name) + "\n" + line1 + "\n" + line2
            pro_text_box.insert(END, content)
            return
        pro_info_btn = ttk.Button(window, text="Info", command=proInfoBtnCmd)
        xp, yp = 82, 95
        pro_info_btn.place(x=dw*xp//100, y=dh*yp//100)

        # Add an display button for original images
        def orgDisplayBtnCmd():
            """Display the original image."""
            # Put a blank image
            img_obj = Image.open("./images/blank.png").resize((dw0, dw0))
            tk_img = ImageTk.PhotoImage(img_obj)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            xp, yp = 0, 8
            img_label.place(x=dw*xp//100, y=dh*yp//100)

            # Put an original image on top of the blank image
            org_name = org_choice.get()
            if not org_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, in_dict = cgetImg(org_name)
            if not status:
                return
            x, y = imgResize(in_dict["imgsize"], dw0)
            tk_img = getTkImg(in_dict["b64str"], x, y)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            img_label.place(x=(dw0-x)//2, y=(dw0-y)//2+dh*yp//100)
            return

        org_display_btn = ttk.Button(window, text="Display",
                                     command=orgDisplayBtnCmd)
        xp, yp = 10, 95
        org_display_btn.place(x=dw*xp//100, y=dh*yp//100)

        # Add an display button for processed images
        def proDisplayBtnCmd():
            """Display the processed image."""
            # Put a blank image
            img_obj = Image.open("./images/blank.png").resize((dw0, dw0))
            tk_img = ImageTk.PhotoImage(img_obj)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            yp = 8
            img_label.place(x=600, y=dh*yp//100)

            # Put a processed image on top of the blank image
            pro_name = pro_choice.get()
            if not pro_name:
                msg = "Please select an image first."
                messagebox.showinfo(message=msg, icon="error")
                return
            status, in_dict = cgetImg(pro_name)
            if not status:
                return
            x, y = imgResize(in_dict["imgsize"], dw0)
            tk_img = getTkImg(in_dict["b64str"], x, y)
            img_label = ttk.Label(window, image=tk_img)
            img_label.image = tk_img
            img_label.place(x=(dw0-x)//2+600, y=(dw0-y)//2+dh*yp//100)
            return

        pro_display_btn = ttk.Button(window, text="Display",
                                     command=proDisplayBtnCmd)
        xp, yp = 62, 95
        pro_display_btn.place(x=dw*xp//100, y=dh*yp//100)
        return

    compare_btn = ttk.Button(root, text="Compare",
                             command=popCompareWindow)
    compare_btn.grid(column=4, row=0)

    # Add an main delete buttun
    def popDelWindow():
        """Pop a window to delete the image."""
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
        def updateChoice():
            """Update the values of the combobox."""
            status, img_names = cgetNames()
            if status:
                img_choice_box["values"] = img_names
        img_choice = StringVar()
        img_choice_box = ttk.Combobox(window, textvariable=img_choice,
                                      postcommand=updateChoice)
        xp, yp = 55, 2
        img_choice_box.place(x=dw*xp//100, y=dh*yp//100)

        # Add a delete button
        def delBtnCmd():
            """Delete the image."""
            img_name = img_choice.get()
            delHelper(img_name)
            return
        del_btn = ttk.Button(window, text="Delete", command=delBtnCmd)
        xp, yp = 40, 80
        del_btn.place(x=dw*xp//100, y=dh*yp//100)
        return
    main_del_btn = ttk.Button(root, text="Delete", command=popDelWindow)
    main_del_btn.grid(column=5, row=0)

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


def infoHelper(img_name):
    """Help fill the function of info button.

    Args:
        img_name: Name of the selected image.
    Returns:
        (tuple): tuple containing:
            bool: True if the requests succeed else False.
            str: Image timestamp.
            str: Image size.
    """
    if not img_name:
        msg = "Please select an image first."
        messagebox.showinfo(message=msg, icon="error")
        return False, "", ""
    status, in_dict = cgetImg(img_name)
    if not status:
        return False, "", ""
    line1 = "timestamp: {}".format(in_dict["timestamp"])
    line2 = "image size: {} pixels".format(in_dict["imgsize"])
    return True, line1, line2


def downloadHelper(img_name):
    """Help fulfill the function of download button.

    Args:
        img_name: Name of the selected image.
    """
    if not img_name:
        msg = "Please select an image first."
        messagebox.showinfo(message=msg, icon="error")
        return
    status, in_dict = cgetImg(img_name)
    if not status:
        return
    fpath = filedialog.asksaveasfilename()
    if not fpath:
        msg = "Please select an directory to save your image."
        messagebox.showerror(message=msg, icon="error")
        return
    transimg.b64_to_img(in_dict["b64str"], fpath)
    msg = "Success: Download the image."
    messagebox.showinfo(message=msg)
    return


def delHelper(img_name):
    """Help fulfill the function of delete button.

    Args:
        img_name: Name of the selected image.
    """
    if not img_name:
        msg = "Please select an image first."
        messagebox.showinfo(message=msg, icon="error")
        return
    status = cdelImg(img_name)
    if not status:
        return
    msg = "Success: Delete the image."
    messagebox.showinfo(message=msg)
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
        msg = "Success: {}".format(r.text)
        messagebox.showinfo(message=msg)
    else:
        msg = "Error: {} - {}".format(r.status_code, r.text)
        messagebox.showinfo(message=msg, icon="error")
    return


def cgetNames():
    """Get request from client site to get a list of image names.

    Returns:
        (tuple): tuple containing:
            bool: True if the requests succeed else False.
            list: A list of image names.
    """
    r = requests.get(server_name + "/api/all_imgs")
    if r.status_code != 200:
        msg = "Error: {} - {}".format(r.status_code, "unknown error")
        messagebox.showinfo(message=msg, icon="error")
        return False, []
    ans = json.loads(r.text)
    ans = tuple(ans)
    return True, ans


def cgetImg(img_name):
    """Get request from client site to get the information of an image.

    Args:
        img_name (str): Name of an image.
    Returns:
        (tuple): tuple containing:
            bool: True if the requests succeed else False.
            dict: An dictionary of image information.
    """
    r = requests.get(server_name + "/api/img/{}".format(img_name))
    if r.status_code != 200:
        msg = "Error: {} - {}".format(r.status_code, "unknown error")
        messagebox.showinfo(message=msg, icon="error")
        return False, {}
    return True, json.loads(r.text)


def cprocessImg(img_name):
    """Get request from client site to initialize image processing.

    Args:
        bool: True if the requests succeed else False.
    """
    r = requests.get(server_name + "/api/process_img/{}".format(img_name))
    if r.status_code != 200:
        msg = "Error: {} - {}".format(r.status_code, "unknown error")
        messagebox.showinfo(message=msg, icon="error")
        return False
    return True


def cgetSelectedNames(processed):
    """Get request from client site to get the names of selected image.

    Args:
        processed (str): "1" processed image, "0" unprocessed image.
    Returns:
        (tuple): tuple containing:
            bool: True if the requests succeed else False.
            list: An list of names of selected images.
    """
    r = requests.get(server_name + "/api/all_imgs/" + processed)
    if r.status_code != 200:
        msg = "Error: {} - {}".format(r.status_code, "unknown error")
        messagebox.showinfo(message=msg, icon="error")
        return False, []
    ans = json.loads(r.text)
    ans = tuple(ans)
    return True, ans


def cdelImg(img_name):
    """Get request from client site to delete an image.

    Arg:
        img_name: name of the image.
        bool: True if the requests succeed else False.
    """
    r = requests.get(server_name + "/api/del/{}".format(img_name))
    if r.status_code != 200:
        msg = "Error: {} - {}".format(r.status_code, "unknown error")
        messagebox.showinfo(message=msg, icon="error")
        return False
    return True


def imgResize(img_size, dw):
    """Resize the image based on the default window width.

    Args:
        img_size (str): org image size.
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
