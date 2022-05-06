Blabel
======

.. image:: https://github.com/Edinburgh-Genome-Foundry/blabel/actions/workflows/build.yml/badge.svg
    :target: https://github.com/Edinburgh-Genome-Foundry/blabel/actions/workflows/build.yml
    :alt: GitHub CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/blabel/badge.svg?branch=master
    :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/blabel?branch=master

.. raw:: html

    <p align="center">
    <img alt="Blabel Logo" title="Blabel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/docs/_static/images/title.png" width="400">
    <br /><br />
    </p>

Blabel is a Python package to generate labels (typically for printing stickers)
with barcodes and other niceties.

**Some features:**

- Generates PDF files where each page is a label (that's the way most label printers want it).
- Label layout is defined by HTML (Jinja) templates and CSS. Supports any page dimensions and margins.
- Builtin support for various barcodes, QR-codes, datamatrix, and more (wraps other libraries).
- Labels data can be provided as list of dicts (easy to generate from spreadsheets).
- Possibility to print several items per sticker.

.. raw:: html
    
    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/docs/_static/images/demo_screenshot.png" width="715">
    <br /><br />
    </p>


Example
-------

To generate labels with Blabel you first need a HTML/Jinja template, and
optionally a style sheet, to define how your labels will look like.

.. raw:: html

    <br/><br/>

**HTML item template** (``item_template.html``)

Notice the use of ``label_tools`` (Blabel's builtin features). The variables
``sample_name`` and ``sample_id`` will be defined at label creation time.

.. code:: html

    <img src="{{label_tools.qr_code(sample_id)}}"/>
    <span class='label'>
        {{ sample_name }} <br/>
        Made with blabel <br/>
        {{ label_tools.now() }}
    </span>

.. raw:: html

    <br/><br/>

**CSS stylesheet** (``style.css``)

Notice the CSS ``@page`` attributes which allows you to adjust the page format
to the dimensions of your sticker.
Also notice the ``pixelated`` image rendering. If your printer is black/white
only with no greyscale support, this option will ensure crisp-looking barcodes,
qr codes, etc.

.. code:: css

    @page {
        width: 27mm;
        height: 7mm;
        padding: 0.5mm;
    }
    img {
        height: 6.4mm;
        display: inline-block;
        vertical-align: middle;
        image-rendering: pixelated;
    }
    .label {
        font-family: Verdana;
        font-weight: bold;
        vertical-align: middle;
        display: inline-block;
        font-size: 7px;
    }

.. raw:: html

    <br/><br/>

**Python code**

In your Python script, create a ``LabelWriter`` linked to the two files above,
and feed it a list of of dicts ("records"), one for each label to print:


.. code:: python

    from blabel import LabelWriter

    label_writer = LabelWriter("item_template.html",
                               default_stylesheets=("style.css",))
    records= [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2")
    ]

    label_writer.write_labels(records, target='qrcode_and_label.pdf')

.. raw:: html

    <br/><br/>

**Result:**

.. raw:: html

    <p align="center">
    <img alt="Blabel Logo" title="Labels" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/examples/qrcode_and_date/screenshot.png" width="300">
    <br /><br />
    </p>


Other examples
--------------

- `Example with a barcode and a dynamically generated picture <https://github.com/Edinburgh-Genome-Foundry/blabel/tree/master/examples/barcode_and_dynamic_picture>`_
- `Ugly example with a logo and a datamatrix <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/logo_and_datamatrix>`_
- `Example with date and QR code (sources of the example above) <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/qrcode_and_date>`_
- `Example where the label data is read from spreadsheets <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/labels_from_spreadsheet>`_
- `Example where several items are printed on each page/sticker <https://github.com/Edinburgh-Genome-Foundry/blabel/tree/master/examples/several_items_per_page>`_


Installation
-------------

You can install Blabel via PIP:

.. code::

    pip install blabel

Alternatively, you can unzip the sources in a folder and type

.. code::

    python setup.py install


**Note:** the package depends on the WeasyPrint Python package. If there are any issues, see installation instructions in the `WeasyPrint documentation <https://doc.courtbouillon.org/weasyprint/stable/first_steps.html>`_. The version is `fixed to <=52 <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/setup.py>`_ as not all GNU/Linux distributions have the latest Pango that is required by the latest WeasyPrint.

**Note: on macOS**, you may need to first install pango with ``brew install pango``.

**Note: on some Debian systems** you may need to first install libffi-dev (``apt install libffi-dev``).
The package name may be libffi-devel on some systems.


License = MIT
-------------

DnaChisel is an open-source software originally written at the `Edinburgh Genome Foundry
<https://edinburgh-genome-foundry.github.io/home.html>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/blabel>`_ under the MIT licence (Copyright 2018 Edinburgh Genome Foundry). Everyone is welcome to contribute!


More biology software
---------------------

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Edinburgh-Genome-Foundry.github.io/master/static/imgs/logos/egf-codon-horizontal.png
  :target: https://edinburgh-genome-foundry.github.io/

Blabel was originally written to print labels for biological samples and is part of the `EGF Codons <https://edinburgh-genome-foundry.github.io/>`_
synthetic biology software suite for DNA design, manufacturing and validation.
