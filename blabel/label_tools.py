"""Utilities for label generation.
"""
import base64
from io import BytesIO
import datetime
import textwrap

import qrcode
from barcode import get_barcode_class
from pystrich.datamatrix import DataMatrixEncoder
from PIL import Image, ImageOps

def now(fmt="%Y-%m-%d %H:%M"):
    now = datetime.datetime.now()
    if fmt is not None:
        now = now.strftime(fmt)
    return now

def pil_to_html_imgdata(img, fmt='PNG'):
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    img_str = base64.b64encode(buffered.getvalue())
    prefix = 'data:image/%s;charset=utf-8;base64,' % fmt.lower()
    return  prefix + img_str.decode()

def figure_data(fig, size=None, fmt='png', bbox_inches='tight', **kwargs):
    """Return a HTML-embeddable string of the figure data.
    The string can be embedded in an image tag as ``<img src="{DATA}"/>``.
    Parameters
    ----------
    fig
      A Matplotlib figure. A Matplotlib "ax" can also be provided, at which
      case the whole ``ax.figure`` will be displayed (i.e. all axes in the
      same figure).
    size
      Size or resolution (width, height) of the final figure image, in inches.
    fmt
      Image format, for instance "png", "svg", "jpeg". SVG is vectorial (non
      pixelated) but sometimes more difficult to work with inside HTML/PDF
      documents.
    bbox_inches
      Keeping this option to "tight" will ensure that your plot's delimitation
      is optimal.
    **kwargs
      Any other option of Matplotlib's figure.savefig() method.
    """
    if "AxesSubplot" in str(fig.__class__):
        # A matplotlib axis was provided: take its containing figure.
        fig = fig.figure
    output = BytesIO()
    original_size = fig.get_size_inches()
    if size is not None:
        fig.set_size_inches((int(size[0]), int(size[1])))
    fig.savefig(output, format=fmt, bbox_inches=bbox_inches, **kwargs)
    fig.set_size_inches(original_size)
    data = output.getvalue()
    if fmt == "svg":
        svg_txt = data.decode()
        svg_txt = "\n".join(svg_txt.split("\n")[4:])
        svg_txt = "".join(svg_txt.split("\n"))
        content = base64.b64encode(svg_txt.encode("ascii"))
    else:
        content = base64.b64encode(data)
    result = b"data:image/%s+xml;base64,%s" % (fmt.encode('utf-8'), content)
    return result.decode("utf-8")

def wrap(text, col_width):
    return "\n".join(textwrap.wrap(text, col_width))

def hiro_square(width='100%'):
    svg= """
      <svg height="%s" width="%s" version="1.1" viewBox="0 0 4 4"
        xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="4" height="4" fill="#000" stroke-width="0"/>
        <rect x="1" y="1" width="2" height="2" fill="#fff" stroke-width="0"/>
      </svg>
    """ % (width, width)
    prefix = "data:image/svg+xml;charset=utf-8;base64,"
    return  prefix + base64.b64encode(svg.encode()).decode()

def qr_code(data, optimize=20, fill_color="black", back_color="white",
            **qr_code_params):
    params = dict(box_size=5, border=0)
    params.update(qr_code_params)
    qr = qrcode.QRCode(**params)
    qr.add_data(data, optimize=20)
    qri = qr.make_image(fill_color=fill_color, back_color=back_color)
    return pil_to_html_imgdata(qri.get_image())


def datamatrix(data, cellsize=2, with_border=False):
    encoder = DataMatrixEncoder(data)
    img_data = encoder.get_imagedata(cellsize=cellsize)
    img = Image.open(BytesIO(img_data))
    if not with_border:
        img = img.crop(ImageOps.invert(img).getbbox())
    return pil_to_html_imgdata(img)

def barcode(data, barcode_class='code128', **writer_options):
    constructor = get_barcode_class(barcode_class)
    data = str(data).zfill(constructor.digits)
    barcode_img = constructor(data)
    svg = barcode_img.render(writer_options=writer_options)
    prefix = "data:image/svg+xml;charset=utf-8;base64,"
    return prefix + base64.b64encode(svg).decode()