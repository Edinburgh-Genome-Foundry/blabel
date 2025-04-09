from blabel import LabelWriter

label_writer = LabelWriter(
    "item_template.html", items_per_page=1, default_stylesheets=("style.css",)
)
records = list()

for k in range(1, 10):
    string_sampleid = "s0" + str(k)
    string_heading = "Heading " + str(k)
    string_sample = "Sample" + str(k)
    records.append(
        dict(sample_id=string_sampleid, heading=string_heading, sample=string_sample)
    )

label_writer.write_labels(records, target="labels_on_a4_paper.pdf", base_url=".")
