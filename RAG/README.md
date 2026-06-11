# Enterprise RAG

A production-style Retrieval-Augmented Generation system built with LangGraph. Uses hybrid retrieval (BM25 + FAISS) with cross-encoder reranking and persistent Postgres-backed conversation memory.

## Architecture

```
PDF Documents
     │
     ▼
 PDFLoader → Chunker
                │
                ├──────────────────┐
                ▼                  ▼
           BM25Store          FaissStore
          (sparse)            (dense / OpenAI embeddings)
                │                  │
                └──────┬───────────┘
                       ▼
               HybridRetriever (RRF fusion)
                       │
                       ▼
                  BGEReranker
                       │
                       ▼
              LangGraph StateGraph
           ┌────────────────────────┐
           │  retrieve → build_context → generate │
           └────────────────────────┘
                       │
                 PostgresSaver
              (conversation memory)
```

## Project Structure

```
RAG/
├── ingestion.py              # Run once to build & persist indexes
├── query.py                  # Chat loop (loads persisted indexes)
├── requirements.txt
├── docker-compose.yaml       # Postgres for conversation memory
├── documents/                # Drop PDFs here
├── cache/                    # Auto-created by ingestion.py
│   ├── chunks.pkl
│   ├── faiss.index
│   └── bm25.pkl
└── app/
    ├── config/settings.py    # Pydantic settings (reads .env)
    ├── ingestion/
    │   ├── pdf_loader.py
    │   └── chunker.py
    ├── embedding/
    │   └── embedding_factory.py
    ├── retreival/
    │   ├── faiss_store.py    # Dense vector index (HNSW)
    │   ├── bm25_store.py     # Sparse keyword index
    │   ├── hybrid_retreiver.py  # RRF fusion of both
    │   ├── reranker.py       # BGE cross-encoder reranker
    │   └── rrf.py            # Reciprocal Rank Fusion
    ├── graph/
    │   ├── state.py          # AgentState (LangGraph)
    │   ├── nodes.py          # retrieve / build_context / generate
    │   └── graph.py          # StateGraph builder
    ├── llm/llm_factory.py
    ├── memory/postgres.py    # PostgresSaver checkpointer
    ├── prompts/rag_prompts.py
    └── services/rag_service.py
```

## Prerequisites

- Python 3.11+
- [Docker](https://www.docker.com/) (for Postgres)
- An OpenAI API key

## Setup

**1. Clone and install dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure environment**

Create a `.env` file in the `RAG/` directory:

```env
OPENAI_API_KEY=sk-...

POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/enterprise_rag

EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o

PDF_DIR=documents
```

**3. Start Postgres**

```bash
docker compose up -d
```

**4. Add PDFs**

Drop your PDF files into the `documents/` folder (or whichever directory `PDF_DIR` points to).

## Running

### Step 1 — Ingest (run once, or when documents change)

```bash
python ingestion.py
```

This loads PDFs, chunks them, embeds via OpenAI, and saves the FAISS index and BM25 model to `cache/`. Re-run only when your document set changes.

### Step 2 — Query

```bash
python query.py
```

Loads the persisted indexes (no API calls during startup), builds the LangGraph pipeline, and starts an interactive chat loop. Conversation history is stored in Postgres per `thread_id`, so context is preserved across sessions.

## How It Works

| Step | Component | Detail |
|------|-----------|--------|
| Chunking | `RecursiveCharacterTextSplitter` | 1000 tokens, 200 overlap |
| Dense retrieval | `FaissStore` (HNSW) | OpenAI `text-embedding-3-small` |
| Sparse retrieval | `BM25Store` | BM25Okapi on token splits |
| Fusion | `reciprocal_rank_fusion` | Top-20 from each, merged via RRF |
| Reranking | `BGEReranker` | `BAAI/bge-reranker-large` cross-encoder |
| Generation | `ChatOpenAI` | `gpt-4o`, temperature 0 |
| Memory | `PostgresSaver` | Full message history per `thread_id` |
