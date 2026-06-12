# rag/embedder.py

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


def get_embeddings(texts):

    return model.encode(
        texts,
        normalize_embeddings=True
    )