import blabel
import os

SAMPLES_DIR = os.path.join('tests', 'data', 'samples')

def get_template_and_style(folder_name):
    folder = os.path.join(SAMPLES_DIR, folder_name)
    template = os.path.join(folder, 'item_template.html')
    style = os.path.join(folder, 'style.css')
    return template, style


def test_qrcode_and_date(tmpdir):
    template, style = get_template_and_style('qrcode_and_date')

    label_writer = blabel.LabelWriter(template,
                            default_stylesheets=(style,))
    records= [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2")
    ]
    target = os.path.join(str(tmpdir), 'target.pdf')
    label_writer.write_labels(records, target=target)