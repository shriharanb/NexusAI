# rag/Document_loader.py

import fitz


def load_document(file_path: str) -> str:

    text = ""

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        return text

    except Exception as e:
        raise Exception(
            f"Failed to load document: {e}"
        )