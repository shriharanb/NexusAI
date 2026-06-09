from Document_loader import load_document
from chunker import split_text

text = load_document("data/Brown_Eyes.pdf")

chunks = split_text(text)

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0])