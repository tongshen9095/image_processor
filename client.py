from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def designWindow():
    root = Tk()

    # Add upload button
    upload_btn = ttk.Button(root, text="Upload")
    upload_btn.grid(column=0, row=0)

    root.mainloop()
    return


def selectImg():
    fpath = filedialog.askopenfilename()
    return fpath

if __name__ == "__main__":
    print(selectImg())
