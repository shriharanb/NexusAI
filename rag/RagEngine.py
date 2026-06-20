import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
class rag_sys():
    def load_document(slef,docs: str) -> str:
        text = ""
        try:
            doc = fitz.open(docs)

            for page in doc:
               text += page.get_text()

            doc.close()

            return text
        except Exception as e:
            raise Exception(
            f"Failed to load document: {e}"
        )   
    def split_text(slef,text: str,chunk_size: int = 500,chunk_overlap: int = 100):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        return splitter.split_text(text)
    def get_embeddings(slef,texts):
        MODEL_NAME = "BAAI/bge-small-en-v1.5"
        model = SentenceTransformer(MODEL_NAME)
        return model.encode(texts,normalize_embeddings=True)#normalize is convert the number b/w -1 to 1
    def store_chunks(slef,chunks,embeddings,source_file):
        DB_PATH= Path(__file__).resolve().parent.parent / "vector_db"
        client = chromadb.PersistentClient(path= str(DB_PATH))
        collection = client.get_or_create_collection(name="documents")
        ids = [f"{source_file}_{i}"for i in range(len(chunks))]
        metadata = [{"source": source_file,"chunk_id": i}for i in range(len(chunks))]
        try:
            collection.delete(ids=ids)
        except:
            pass
        finally:
            collection.add(ids=ids,
                           documents=chunks,
                           embeddings=embeddings.tolist(), 
                           metadatas=metadata)
            #Need to mention stored successfully in UI

def retrieve(query,n_results=5 ): #top 5 closest match
    Collector=rag_sys()
    query_embedding = Collector.get_embeddings([query])[0]
    DB_PATH= Path(__file__).resolve().parent.parent / "vector_db"
    client = chromadb.PersistentClient(path= str(DB_PATH))
    collection = client.get_or_create_collection(name="documents")
    results = collection.query(query_embeddings=[query_embedding.tolist()],n_results=n_results ) #collection is variable
    return {
    "context":
    "\n\n".join(
    results["documents"][0]
    ),
    "documents":
    results["documents"][0],
    "metadata":
    results["metadatas"][0]
    }#dictionary format
    




    