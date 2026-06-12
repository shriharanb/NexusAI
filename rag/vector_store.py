# rag/vector_store.py

import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(
    chunks,
    embeddings,
    source_file
):

    ids = [
        f"{source_file}_{i}"
        for i in range(len(chunks))
    ]

    metadata = [
        {
            "source": source_file,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )