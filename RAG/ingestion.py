import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pickle

from app.config.settings import settings
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.chunker import Chunker
from app.embedding.embedding_factory import get_embeddings
from app.retreival.bm25_store import BM25Store
from app.retreival.faiss_store import FaissStore

os.makedirs(settings.cache_dir, exist_ok=True)

docs = PDFLoader().load_directory(settings.pdf_dir)
chunks = Chunker().split(docs)

with open(f"{settings.cache_dir}/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

embeddings = get_embeddings()

faiss_store = FaissStore(embeddings, chunks)
faiss_store.save(f"{settings.cache_dir}/faiss.index")

bm25 = BM25Store(chunks)
bm25.save(f"{settings.cache_dir}/bm25.pkl")

print(f"Ingested {len(chunks)} chunks from {len(docs)} pages.")
