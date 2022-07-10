from blabel import LabelWriter

label_writer = LabelWriter(
    "item_template.html", items_per_page=1, default_stylesheets=("style.css",)
)
records = list();
records.append(dict(sample_id="s01",heading="Heading 1",sample="Sample 1"));
records.append(dict(sample_id="s02",heading="Heading 2",sample="Sample 2"));
records.append(dict(sample_id="s03",heading="Heading 3",sample="Sample 3"));
records.append(dict(sample_id="s04",heading="Heading 4",sample="Sample 4"));
records.append(dict(sample_id="s05",heading="Heading 5",sample="Sample 5"));
records.append(dict(sample_id="s06",heading="Heading 6",sample="Sample 6"));
records.append(dict(sample_id="s07",heading="Heading 7",sample="Sample 7"));
records.append(dict(sample_id="s08",heading="Heading 8",sample="Sample 8"));
records.append(dict(sample_id="s09",heading="Heading 9",sample="Sample 9"));


label_writer.write_labels(records, target="labels_on_a4_paper.pdf", base_url=".")
