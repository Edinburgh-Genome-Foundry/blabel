import os
import tempfile
from io import BytesIO

import jinja2
from weasyprint import HTML
from . import label_tools
from . import tools

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(THIS_PATH, 'data', 'print_template.html'), 'r') as f:
    PRINT_TEMPLATE = jinja2.Template(f.read())

GLOBALS = {
    'list': list,
    'len': len,
    'enumerate': enumerate,
    'label_tools': label_tools,
    'str': str
}

def write_pdf(html, target=None, base_url=None, extra_stylesheets=()):
    """Write the provided HTML in a PDF file.

    Parameters
    ----------
    html
      A HTML string
    target
      A PDF file path or file-like object, or None for returning the raw bytes
      of the PDF.
    base_url
      The base path from which relative paths in the HTML template start.
    use_default_styling
      Setting this parameter to False, your PDF will have no styling at all by
      default. This means no Semantic UI, which can speed up the rendering.
    extra_stylesheets
      List of paths to other ".css" files used to define new styles or
      overwrite default styles.
    """
    weasy_html = HTML(string=html, base_url=base_url)
    if target in [None, "@memory"]:
        with BytesIO() as buffer:
            weasy_html.write_pdf(buffer, stylesheets=extra_stylesheets)
            pdf_data = buffer.getvalue()
        return pdf_data
    else:
        weasy_html.write_pdf(target, stylesheets=extra_stylesheets)

class LabelWriter:
    """Class to write labels
    """

    def __init__(self, item_template_path=None, item_template=None,
                 default_stylesheets=(),
                 use_default_styling=True, default_base_url=None,
                 items_per_page=1, **default_context):
        if item_template_path is not None:
            with open(item_template_path, 'r') as f:
                item_template = f.read()
        if isinstance(item_template, str):
            item_template = jinja2.Template(item_template)
        self.default_context = default_context if default_context else {}
        self.default_stylesheets = default_stylesheets
        self.use_default_styling = use_default_styling
        self.default_base_url = default_base_url
        self.item_template = item_template
        self.items_per_page = items_per_page


    def record_to_html(self, record):
        context = dict(GLOBALS.items())
        context.update(self.default_context)
        context.update(record)
        return self.item_template.render(**context)
    
    def records_to_html(self, records, target=None):
        items_htmls = [self.record_to_html(record) for record in records]
        items_chunks = tools.list_chunks(items_htmls, self.items_per_page)
        html = PRINT_TEMPLATE.render(items_chunks=items_chunks)
        if target is not None:
            with open(target, 'w') as f:
                f.write(html)
        else:
            return html



    def write_labels(self, records, target=None, extra_stylesheets=(),
                     base_url=None):
        return write_pdf(
            self.records_to_html(records),
            target=target,
            extra_stylesheets=self.default_stylesheets + extra_stylesheets,
            base_url=base_url if base_url else self.default_base_url,
        )