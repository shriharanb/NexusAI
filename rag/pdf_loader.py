import fitz

def load_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text
text= load_pdf("data/Brown_Eyes.pdf")
