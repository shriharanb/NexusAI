from pdf_loader import load_pdf
from chunker import split_text

text = load_pdf("data/Brown_Eyes.pdf")

chunks = split_text(text)

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0])