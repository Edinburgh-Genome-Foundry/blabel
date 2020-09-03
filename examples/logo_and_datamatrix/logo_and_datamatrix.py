from blabel import LabelWriter

label_writer = LabelWriter("item_template.html", default_stylesheets=("style.css",))
records = [
    dict(sample_id="s01", sample_name="Sample 1"),
    dict(sample_id="s02", sample_name="Sample 2"),
]

label_writer.write_labels(records, target="logo_and_datamatrix.pdf", base_url=".")
