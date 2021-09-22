import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open("blabel/version.py").read())  # loads __version__

setup(
    name="blabel",
    version=__version__,
    author="Zulko",
    description="Generate multi-page, multi-label pdfs in Python.",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    url="https://github.com/Edinburgh-Genome-Foundry/blabel",
    keywords="label barcode pdf generator",
    packages=find_packages(exclude="docs"),
    include_package_data=True,
    install_requires=[
        "jinja2",
        "qrcode",
        "pystrich",
        "python-barcode",
        "pillow",
        "weasyprint<=52",
    ],
)
