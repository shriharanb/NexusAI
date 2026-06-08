import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="books"
)


def store_chunks(chunks, embeddings):

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    print("Stored Successfully")