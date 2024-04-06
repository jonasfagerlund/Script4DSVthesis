import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
import os


def search_in_pdf(file_path, keywords):
    # Open the PDF file
    doc = fitz.open(file_path)
    matches = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        for keyword in keywords:
            if keyword in text:
                matches.append((keyword, page_num + 1))

    doc.close()
    return matches


def create_summary_pdf(output_path, results):
    c = canvas.Canvas(output_path)
    y_position = 800  # Starting Y position for drawing text

    for file_path, matches in results.items():
        c.drawString(100, y_position, f"File: {file_path}")
        y_position -= 20
        for match in matches:
            keyword, page = match
            c.drawString(120, y_position, f"Keyword: {keyword}, Page: {page}")
            y_position -= 20
            if y_position < 100:  # Add a new page if there's not much space left
                c.showPage()
                y_position = 800

    c.save()


# List of keywords to search for
keywords = ["example", "keyword"]

# Path to the directory containing PDFs
pdf_directory = "path/to/your/pdfs"
pdf_files = [
    os.path.join(pdf_directory, f)
    for f in os.listdir(pdf_directory)
    if f.endswith(".pdf")
]

results = {}
for file_path in pdf_files:
    matches = search_in_pdf(file_path, keywords)
    if matches:
        results[file_path] = matches

create_summary_pdf("summary_of_matches.pdf", results)
