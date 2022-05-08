import os
import base64

import pydenticon
import pandas

import blabel

SAMPLES_DIR = os.path.join("tests", "data", "samples")


def get_template_and_style(folder_name):
    folder = os.path.join(SAMPLES_DIR, folder_name)
    template = os.path.join(folder, "item_template.html")
    style = os.path.join(folder, "style.css")
    return template, style


def test_qrcode_and_date(tmpdir):
    template, style = get_template_and_style("qrcode_and_date")

    label_writer = blabel.LabelWriter(template, default_stylesheets=(style,))
    records = [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2"),
    ]
    target = os.path.join(str(tmpdir), "target.pdf")
    label_writer.write_labels(records, target=target)
    target = os.path.join(str(tmpdir), "target.html")
    label_writer.records_to_html(records, target=target)
    data = label_writer.write_labels(records, target=None)
    assert 10_000 < len(data) < 20_000


def test_barcode_and_dynamic_picture():
    def generate_identicon(sample_id):
        identicon_generator = pydenticon.Generator(
            6, 6, foreground=["red", "blue", "green", "purple"]
        )
        img = identicon_generator.generate(sample_id, 60, 60)
        return "data:image/png;base64,%s" % (base64.b64encode(img).decode())

    template, style = get_template_and_style("barcode_and_dynamic_picture")
    label_writer = blabel.LabelWriter(
        template, default_stylesheets=(style,), generate_identicon=generate_identicon,
    )
    records = [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2"),
        dict(sample_id="s03", sample_name="Sample 3"),
    ]

    data = label_writer.write_labels(records, target=None)
    assert 40_000 > len(data) > 22_000


def test_labels_from_spreadsheet():
    dataframe = pandas.read_csv(
        os.path.join(SAMPLES_DIR, "labels_from_spreadsheet", "records.csv")
    )
    records = dataframe.to_dict(orient="record")
    template, style = get_template_and_style("labels_from_spreadsheet")
    label_writer = blabel.LabelWriter(template, default_stylesheets=(style,))
    data = label_writer.write_labels(records, target=None)
    assert 18_000 > len(data) > 11_000


def test_logo_and_datamatrix():
    records = [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2"),
    ]
    template, style = get_template_and_style("logo_and_datamatrix")
    label_writer = blabel.LabelWriter(template, default_stylesheets=(style,))
    data = label_writer.write_labels(
        records, target=None, base_url=os.path.join(SAMPLES_DIR, "logo_and_datamatrix"),
    )
    assert 55_000 > len(data) > 19_500


def test_several_items_per_page():
    records = [
        dict(name="Scott", sex="M"),
        dict(name="Laura", sex="F"),
        dict(name="Jane", sex="F"),
        dict(name="Valentin", sex="M"),
        dict(name="Hille", sex="F"),
    ]
    template, style = get_template_and_style("several_items_per_page")
    label_writer = blabel.LabelWriter(template, default_stylesheets=(style,))
    data = label_writer.write_labels(
        records,
        target=None,
        base_url=os.path.join(SAMPLES_DIR, "several_items_per_page"),
    )
    assert 28_000 > len(data) > 15_000
