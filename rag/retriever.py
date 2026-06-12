# rag/retriever.py

from vector_store import collection
from embedder import get_embeddings


def retrieve(
    query,
    n_results=5
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