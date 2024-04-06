import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
import os


def highlight_keyword(page, text):
    """Highlight all occurrences of `text` in `page`."""
    text_instances = page.search_for(text)
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.update()  # Apply the highlighting


def search_and_highlight_pdf(file_path, keywords):
    doc = fitz.open(file_path)
    matches = []
    any_keyword_found = False  # Indicator if any keyword is found
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        for keyword in keywords:
            if keyword in text:
                any_keyword_found = True  # Set to True if keyword found
                highlight_keyword(page, keyword)
                text_instances = page.search_for(keyword)
                for inst in text_instances:
                    matches.append((keyword, page_num + 1))
    if any_keyword_found:
        # Save the annotated document only if at least one keyword was found
        doc.save(f"annotated_{os.path.basename(file_path)}")
    doc.close()
    return matches


def create_summary_pdf(output_path, results):
    c = canvas.Canvas(output_path)
    y_position = 800  # Starting Y position for drawing text

    for file_path, matches in results.items():
        c.drawString(100, y_position, f"File: {os.path.basename(file_path)}")
        y_position -= 20
        for match in matches:
            keyword, page = match
            c.drawString(120, y_position, f"Keyword: {keyword}, Page: {page}")
            y_position -= 20
            if y_position < 100:  # Add a new page if there's not much space left
                c.showPage()
                y_position = 800

    c.save()


def process_pdfs(pdf_directory, keywords):
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]
    results = {}
    for filename in pdf_files:
        file_path = os.path.join(pdf_directory, filename)
        matches = search_and_highlight_pdf(file_path, keywords)
        if matches:
            results[file_path] = matches
    return results


# Define your keywords and directory containing PDFs
keywords = ["centralisering", "decentraliserade"]
pdf_directory = "/Users/jonasfagerlund/Desktop/documents 4 thesis"

# Process PDFs and create summary
results = process_pdfs(pdf_directory, keywords)
create_summary_pdf("summary_of_matches.pdf", results)
