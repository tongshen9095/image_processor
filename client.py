from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

def designWindow():
    root = Tk()

    # Add upload button
    upload_btn = ttk.Button(root, text="Upload", command=uploadBtnCmd)
    upload_btn.grid(column=0, row=0)

    root.mainloop()
    return


def uploadBtnCmd():
    fpath = selectImg()
    fname = parseName(fpath)
    print(fname)

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


if __name__ == "__main__":
    designWindow()
