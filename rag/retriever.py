# rag/retriever.py

from vector_store import collection
from embedder import get_embeddings


def retrieve(
    query,
    n_results=5 #top 5 closest match
):

    query_embedding = get_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results 
    )

    return {
        "context":
        "\n\n".join(
            results["documents"][0]
        ),

        "documents":
        results["documents"][0],

        "metadata":
        results["metadatas"][0]
    }
ans=retrieve("What is the real reason Stephen Griggs pretends to be Peter Reed in Brown Eyes?")
print(ans)