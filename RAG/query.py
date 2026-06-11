import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pickle

from app.config.settings import settings
from app.embedding.embedding_factory import get_embeddings
from app.retreival.bm25_store import BM25Store
from app.retreival.faiss_store import FaissStore
from app.retreival.hybrid_retreiver import HybridRetriever
from app.graph.graph import build_graph
from app.memory.postgres import get_checkpointer
from app.services.rag_service import RAGService

with open(f"{settings.cache_dir}/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

embeddings = get_embeddings()
faiss_store = FaissStore.load(embeddings, chunks, f"{settings.cache_dir}/faiss.index")
bm25 = BM25Store.load(f"{settings.cache_dir}/bm25.pkl")

retriever = HybridRetriever(bm25, faiss_store, chunks)
graph = build_graph(retriever, get_checkpointer())
service = RAGService(graph)

while True:
    query = input("User: ")
    answer = service.chat(query=query, thread_id="aman")
    print(answer)
