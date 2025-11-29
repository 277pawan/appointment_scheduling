import os
import chromadb
from chromadb.config import Settings

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vectordb")

client = chromadb.Client(
    Settings(persist_directory=VECTOR_DB_PATH)
)

COLLECTION_NAME = "clinic_faq"

def get_collection():
    return client.get_or_create_collection(name=COLLECTION_NAME)

def add_documents(docs):
    col = get_collection()
    col.add(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d["meta"] for d in docs],
    )

def query_collection(query: str, n_results: int = 3):
    col = get_collection()
    res = col.query(query_texts=[query], n_results=n_results)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return list(zip(docs, metas))

