from vector_store import collection
from embedder import get_embeddings

def retrieve(query, n_results=3):

    query_embedding = get_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    print("\nDEBUG RESULTS:")
    print(results)

    return results["documents"][0]