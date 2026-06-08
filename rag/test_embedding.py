from pdf_loader import load_pdf
from chunker import split_text
from embedder import get_embeddings

text = load_pdf("data/Brown_Eyes.pdf")

chunks = split_text(text)

embeddings = get_embeddings(chunks)

print("Number of chunks:", len(chunks))

print("Embedding dimension:", len(embeddings[0]))