from Document_loader import load_document
from chunker import split_text
from embedder import get_embeddings
from vector_store import store_chunks


def ingest_document(file_path):

    text = load_document(file_path)

    chunks = split_text(text)

    embeddings = get_embeddings(chunks)

    store_chunks(
        chunks,
        embeddings,
        file_path
    )

    return len(chunks)