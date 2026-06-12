import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

# Wipe out the old "books" shelf completely
try:
    client.delete_collection(name="books")
except:
    pass  # Do nothing if it didn't exist yet

# Create a fresh, empty "books" shelf
collection = client.get_or_create_collection(name="books")

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