from blabel import LabelWriter
import pandas

dataframe = pandas.read_csv("records.csv")
records = dataframe.to_dict(orient="record")

label_writer = LabelWriter("item_template.html", default_stylesheets=("style.css",))

label_writer.write_labels(records, target="labels_from_spreadsheet.pdf")
