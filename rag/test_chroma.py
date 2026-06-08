from pdf_loader import load_pdf
from chunker import split_text
from embedder import get_embeddings
from vector_store import store_chunks

text = load_pdf("data/Brown_Eyes.pdf")

chunks = split_text(text)

embeddings = get_embeddings(chunks)

store_chunks(chunks, embeddings)