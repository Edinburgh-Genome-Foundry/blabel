.. raw:: html

    <p align="center">
    <img alt="Blabel Logo" title="DNA Chisel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/docs/_static/images/title.png" width="400">
    <br /><br />
    </p>

Blabel
======

.. image:: https://travis-ci.org/Edinburgh-Genome-Foundry/blabel.svg?branch=master
    :target: https://travis-ci.org/Edinburgh-Genome-Foundry/blabel

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/blabel/badge.svg?branch=master
    :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/blabel?branch=master

Blabel is a python library to generate labels (typically for printing stickers)
with barcodes and other niceties

**Some features:**

- Generates PDF files where each page is a label (compatible with most label printers).
- Label layout defined by HTML (Jinja) templates and CSS. Supports any paper/margin format !
- Builtin support for various barcodes, QR-codes, datamatrix, and more (wraps other libraries).
- Labels data can be provided as list of dicts (easy to generate from spreadsheets).
- Possibility to print several items per sticker.

.. raw:: html
    
    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/docs/_static/images/demo_screenshot.png" width="715">
    <br /><br />
    </p>

Example
--------

To generate labels with Blabel you first need a HTML/Jinja template, and optionally a style sheet, to define how your labels will look like.

**HTML item template** (``item_template.html``)

Notice the use of ``label_tools`` (Blabel's builtin features). The variables ``sample_name`` and ``sample_id`` will be defined at label creation time.

.. code:: html

    <img src="{{label_tools.qr_code(sample_id)}}"/>
    <span class='label'>
        {{ sample_name }} <br/>
        Made with ❤ @ EGF <br/>
        🗓 {{ label_tools.now() }}
    </span>

**CSS stylesheet** (``style.css``)

Notice the CSS ``@page`` attributes which allows you to adjust the page format to the dimensions of your sticker.

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

**Python code**

In your Python script, create a ``LabelWriter`` linked to the two files above,
and feed it a list of of dicts ("records"), one for each label to print :


.. code:: python

    from blabel import LabelWriter

    label_writer = LabelWriter("item_template.html",
                               default_stylesheets=("style.css",))
    records= [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2")
    ]

    label_writer.write_labels(records, target='qrcode_and_label.pdf')

And voila !

.. raw:: html

    <p align="center">
    <img alt="Blabel Logo" title="DNA Chisel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/blabel/master/examples/qrcode_and_date/screenshot.png" width="300">
    <br /><br />
    </p>

Other examples
--------------

- `Example with a barcode and a dynamically generated picture <https://github.com/Edinburgh-Genome-Foundry/blabel/tree/master/examples/barcode_and_dynamic_picture>`_
- `Ugly example with a logo and a datamatrix <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/logo_and_datamatrix>`_
- `Example with date and QR code (sources of the example above) <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/qrcode_and_date>`_
- `Example where the label data is read from spreadsheets <https://github.com/Edinburgh-Genome-Foundry/blabel/blob/master/examples/labels_from_spreadsheet>`_
- `Example where several items are printed on each page/sticker <https://github.com/Edinburgh-Genome-Foundry/blabel/tree/master/examples/several_items_per_page>`_

Documentation
-------------

In progress. See examples and source code in the mean time.

License = MIT
--------------

DnaChisel is an open-source software originally written at the `Edinburgh Genome Foundry
<https://edinburgh-genome-foundry.github.io/home.html>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/blabel>`_ under the MIT licence (¢ Edinburg Genome Foundry). Everyone is welcome to contribute !

More biology software
-----------------------

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Edinburgh-Genome-Foundry.github.io/master/static/imgs/logos/egf-codon-horizontal.png
  :target: https://edinburgh-genome-foundry.github.io/

Blabel was originally written to print labels for biological samples and is part of the `EGF Codons <https://edinburgh-genome-foundry.github.io/>`_
synthetic biology software suite for DNA design, manufacturing and validation.


.. raw:: html
    
     <a href="https://twitter.com/share" class="twitter-share-button"
     data-text="Blabel - Python library to create labels/stickers from HTML templates" data-size="large" data-hashtags="Python PDF">Tweet
     </a>
     <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
     if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';
     fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
     </script>
     <iframe src="http://ghbtns.com/github-btn.html?user=Edinburgh-Genome-Foundry&repo=blabel&type=watch&count=true&size=large"
     allowtransparency="true" frameborder="0" scrolling="0" width="152px" height="30px" margin-bottom="30px"></iframe>

.. raw:: html
  
    <a href="https://github.com/Edinburgh-Genome-Foundry/blabel" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>



.. toctree::
    :hidden:
    :maxdepth: 3

    self


.. toctree::
   :hidden:
   :caption: Reference
   :maxdepth: 3

   ref


.. _Github: https://github.com/EdinburghGenomeFoundry/dnachisel
.. _PYPI: https://pypi.python.org/pypi/dnachisel

