from RagEngine import rag_sys
def ingest_document(docs):
    Scraper=rag_sys()
    text = Scraper.load_document(docs)
    chunks = Scraper.split_text(text)
    embeddings = Scraper.get_embeddings(chunks)
    Scraper.store_chunks(chunks,embeddings,docs)
    return len(chunks)
ans=ingest_document("data/Brown_Eyes.pdf")
