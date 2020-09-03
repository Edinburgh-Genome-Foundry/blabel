from blabel import LabelWriter

label_writer = LabelWriter(
    "item_template.html", items_per_page=3, default_stylesheets=("style.css",)
)
records = [
    dict(name="Scott", sex="M"),
    dict(name="Laura", sex="F"),
    dict(name="Jane", sex="F"),
    dict(name="Valentin", sex="M"),
    dict(name="Hille", sex="F"),
]

label_writer.write_labels(records, target="several_items_per_page.pdf", base_url=".")
