from retriever import retrieve

query = "Where does Paul Stewart live?"

results = retrieve(query, n_results=10)

print("\nRetrieved Chunks:\n")

for i, chunk in enumerate(results, 1):
    print(f"\nChunk {i}:")
    print(chunk)