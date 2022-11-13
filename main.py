from PyPDF2 import PdfReader, PdfWriter

fname = "1.pdf"
in_path = "res/" + fname
out_path = "res/out/" + fname
reader = PdfReader(in_path)
writer = PdfWriter()

number_of_pages = len(reader.pages)
print(number_of_pages)

page = reader.pages[0]
writer.add_page(page)

with open(out_path, "wb") as fp:
    writer.write(fp)
