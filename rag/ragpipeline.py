from rag.RagEngine import rag_sys
from pathlib import Path
import chromadb

def ingest_document(docs):
    Scraper = rag_sys()
    text = Scraper.load_document(docs)
    chunks = Scraper.split_text(text)
    embeddings = Scraper.get_embeddings(chunks)
    Scraper.store_chunks(chunks, embeddings, docs)
    return len(chunks)

def delete_document(docs):
    """
    🎯 Purges all chunks, embeddings, IDs, and metadata associated 
    with the selected document from ChromaDB using a metadata filter.
    """
    DB_PATH = Path(__file__).resolve().parent.parent / "vector_db"
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(name="documents")
    
    # ChromaDB supports deleting entries using a 'where' metadata filter
    collection.delete(where={"source": docs})