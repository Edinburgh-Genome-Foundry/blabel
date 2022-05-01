def list_chunks(mylist, n):
    """Yield successive n-sized chunks from mylist."""
    return [mylist[i : i + n] for i in range(0, len(mylist), n)]


class JupyterPDF(object):
    """Class to display PDFs in a Jupyter / IPython notebook.
    Just write this at the end of a code Cell to get in-browser PDF preview:
    >>> from pdf_reports import JupyterPDF
    >>> JupyterPDF("path_to_some.pdf")
    Credits to StackOverflow's Jakob: https://stackoverflow.com/a/19470377
    """

    def __init__(self, url, width=600, height=800):
        self.url = url
        self.width = width
        self.height = height

    def _repr_html_(self):
        return """
            <center>
                <iframe src={self.url} width={self.width} height={self.height}>
                </iframe>
            </center>
        """.format(
            self=self
        )

