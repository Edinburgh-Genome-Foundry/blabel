"""Utilities for label generation.
"""
import base64
from io import BytesIO
import datetime
import textwrap

import qrcode
import barcode as python_barcode
from pystrich.datamatrix import DataMatrixEncoder
from PIL import Image, ImageOps


def now(fmt="%Y-%m-%d %H:%M"):
    """Display the current time.

    Default format is "year-month-day hour:minute" but another format can be
    provided (see ``datetime`` docs for date formatting).
    """
    now = datetime.datetime.now()
    if fmt is not None:
        now = now.strftime(fmt)
    return now


def pil_to_html_imgdata(img, fmt="PNG"):
    """Convert a PIL image into HTML-displayable data.
    
    The result is a string ``data:image/FMT;base64,xxxxxxxxx`` which you
    can provide as a "src" parameter to a ``<img/>`` tag.

    Examples:
    ---------

    >>> data = pil_to_html_imgdata(my_pil_img)
    >>> html_data = '<img src="%s"/>' % data
    """
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    img_str = base64.b64encode(buffered.getvalue())
    prefix = "data:image/%s;charset=utf-8;base64," % fmt.lower()
    return prefix + img_str.decode()


def wrap(text, col_width):
    """Breaks the text into lines with at maximum 'col_width' characters."""
    return "\n".join(textwrap.wrap(text, col_width))


def hiro_square(width="100%"):
    """Return a <svg/> string of a Hiro square to be included in HTML."""
    svg = """
      <svg height="%s" width="%s" version="1.1" viewBox="0 0 4 4"
        xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="4" height="4" fill="#000" stroke-width="0"/>
        <rect x="1" y="1" width="2" height="2" fill="#fff" stroke-width="0"/>
      </svg>
    """ % (
        width,
        width,
    )
    prefix = "data:image/svg+xml;charset=utf-8;base64,"
    return prefix + base64.b64encode(svg.encode()).decode()


def qr_code(
    data, optimize=20, fill_color="black", back_color="white", **qr_code_params
):
    """Return a QR code's image data.

    Powered by the Python library ``qrcode``. See this library's documentation
    for more details.

    Parameters
    ----------
    data
      Data to be encoded in the QR code.
    
    optimize
      Chunk length optimization setting.
    
    fill_color, back_color
      Colors to use for QRcode and its background.
    
    **qr_code_params
      Parameters of the ``qrcode.QRCode`` constructor, such as ``version``,
      ``error_correction``, ``box_size``, ``border``.

    Returns
    -------
    image_base64_data
      A string ``data:image/png;base64,xxxxxxxxx`` which you can provide as a
      "src" parameter to a ``<img/>`` tag.

    Examples:
    ---------

    >>> data = qr_code('egf45728')
    >>> html_data = '<img src="%s"/>' % data
    """
    params = dict(box_size=5, border=0)
    params.update(qr_code_params)
    qr = qrcode.QRCode(**params)
    qr.add_data(data, optimize=20)
    qri = qr.make_image(fill_color=fill_color, back_color=back_color)
    return pil_to_html_imgdata(qri.get_image())


def datamatrix(data, cellsize=2, with_border=False):
    """Return a datamatrix's image data.

    Powered by the Python library ``pyStrich``. See this library's documentation
    for more details.

    Parameters
    ----------
    data
      Data to be encoded in the datamatrix.

    cellsize
      size of the picture in inches (?).
    
    with_border
      If false, there will be no border or margin to the datamatrix image.

    Returns
    -------
    image_base64_data
      A string ``data:image/png;base64,xxxxxxxxx`` which you can provide as a
      "src" parameter to a ``<img/>`` tag.

    Examples:
    ---------

    >>> data = datamatrix('EGF')
    >>> html_data = '<img src="%s"/>' % data
    """
    encoder = DataMatrixEncoder(data)
    img_data = encoder.get_imagedata(cellsize=cellsize)
    img = Image.open(BytesIO(img_data))
    if not with_border:
        img = img.crop(ImageOps.invert(img).getbbox())
    return pil_to_html_imgdata(img)


def barcode(
    data, barcode_class="code128", fmt="png", add_checksum=True, **writer_options
):
    """Return a barcode's image data.

    Powered by the Python library ``python-barcode``. See this library's
    documentation for more details.

    Parameters
    ----------
    data
      Data to be encoded in the datamatrix.

    barcode_class
      Class/standard to use to encode the data. Different standards have
      different constraints.
    
    writer_options
      Various options for the writer to tune the appearance of the barcode
      (see python-barcode documentation).

    Returns
    -------
    image_base64_data
      A string ``data:image/png;base64,xxxxxxxxx`` which you can provide as a
      "src" parameter to a ``<img/>`` tag.

    Examples:
    ---------

    >>> data = barcode('EGF12134', barcode_class='code128')
    >>> html_data = '<img src="%s"/>' % data

    Examples of writer options:

    >>> { 'background': 'white',
    >>>   'font_size': 10,
    >>>   'foreground': 'black',
    >>>   'module_height': 15.0,
    >>>   'module_width': 0.2,
    >>>   'quiet_zone': 6.5,
    >>>   'text': '',
    >>>   'text_distance': 5.0,
    >>>   'write_text': True
    >>> }
    """
    constructor = python_barcode.get_barcode_class(barcode_class)
    data = str(data).zfill(constructor.digits)
    writer = {
        "svg": python_barcode.writer.SVGWriter,
        "png": python_barcode.writer.ImageWriter,
    }[fmt]
    if "add_checksum" in getattr(constructor, "__init__").__code__.co_varnames:
        barcode_img = constructor(data, writer=writer(), add_checksum=add_checksum)
    else:
        barcode_img = constructor(data, writer=writer())
    img = barcode_img.render(writer_options=writer_options)
    if fmt == "png":
        return pil_to_html_imgdata(img, fmt="PNG")
    else:
        prefix = "data:image/svg+xml;charset=utf-8;base64,"
        return prefix + base64.b64encode(img).decode()
