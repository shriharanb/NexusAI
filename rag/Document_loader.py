import fitz

def load_document(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text
text= load_document("data/Brown_Eyes.pdf")