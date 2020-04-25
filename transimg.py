import base64
import io
import matplotlib.image as mpimg
from skimage.io import imsave
from PIL import Image, ImageTk
import datetime
from skimage import util


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


def ndarray2img(img_ndarray, x, y):
    """Convert ndarray to tk image.

    Args:
        img_ndarray: An ndarray containing image data.
        x: width of the new size
        y: height of the new size
    Returns:
        tk_image object
    """
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img).resize((x, y))
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image


def b64_to_img(b64_str, fpath):
    """Convert b64 string to image file.

    Args:
        b64_str (str): Base64 representation of an image file.
    """
    img_bytes = base64.b64decode(b64_str)
    with open(fpath, "wb") as out_file:
        out_file.write(img_bytes)
    return


def ndarray2b64(img_ndarray):
    """Convert ndarray to base64 string.

    Args:
        img_ndarray (ndarray): An ndarray contains image data.
    Returns
        (str): Base64 representation of an image.
    """
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_str = str(y, encoding='utf-8')
    return b64_str


def makeDict(fname, b64_str, img_size, processed_status):
    """Create the input dictionary.

    Args:
        fname (str): File name.
        b64_str (str): Base64 representation of the image file.
        img_size (str): Image size.
        processed_status (bool): Whether the image is processed.
    Returns:
        dict: An dictionary.
    """
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    in_dict = {"name": fname,
               "b64str": b64_str,
               "imgsize": img_size,
               "processed": processed_status,
               "timestamp": curr_time_str}
    return in_dict


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


def invertImg(b64_str):
    """Invert image.
    
    Args:
        b64_str (str): Base64 representation of the original image.
    Returns:
        str: Base64 representation of the inversed image.
    """
    img_ndarray = b64_to_ndarray(b64_str)
    inv_ndarray = util.invert(img_ndarray)
    inv_b64_str = ndarray2b64(inv_ndarray)
    return inv_b64_str