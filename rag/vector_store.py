# rag/vector_store.py

import chromadb
from pathlib import Path
DB_PATH= Path(__file__).resolve().parent.parent / "vector_db"

client = chromadb.PersistentClient(
    path= str(DB_PATH)
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

    # Remove old chunks if they already exist
    try:
        collection.delete(ids=ids)
    except:
        pass

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )