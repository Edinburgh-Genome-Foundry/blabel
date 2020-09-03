from blabel import LabelWriter

import pydenticon
import base64


def generate_identicon(sample_id):
    identicon_generator = pydenticon.Generator(
        6, 6, foreground=["red", "blue", "green", "purple"]
    )
    img = identicon_generator.generate(sample_id, 60, 60)
    return "data:image/png;base64,%s" % (base64.b64encode(img).decode())


label_writer = LabelWriter(
    "item_template.html",
    default_stylesheets=("style.css",),
    generate_identicon=generate_identicon,
)
records = [
    dict(sample_id="s01", sample_name="Sample 1"),
    dict(sample_id="s02", sample_name="Sample 2"),
    dict(sample_id="s03", sample_name="Sample 3"),
]

label_writer.write_labels(records, target="barcode_and_dynamic_picture.pdf")
