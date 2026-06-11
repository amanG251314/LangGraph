# LangGraph Chatbot

A conversational chatbot built with LangGraph and FastAPI. Supports persistent multi-turn conversations using PostgreSQL as the checkpoint store.

## Features

- Multi-turn conversation with memory per session
- PostgreSQL-backed checkpointing via LangGraph
- REST API with user-scoped session management
- Powered by OpenAI GPT models

## Project Structure

```
chatbot/
├── app/
│   ├── config/
│   │   └── settings.py        # Environment config
│   ├── database/
│   │   └── checkpoint.py      # PostgreSQL checkpointer setup
│   ├── graph/
│   │   ├── builder.py         # LangGraph graph definition
│   │   ├── nodes.py           # Chatbot node (LLM call)
│   │   └── state.py           # Graph state schema
│   ├── services/
│   │   └── chat_service.py    # Graph invocation logic
│   ├── main.py                # FastAPI app factory
│   ├── router.py              # API routes
│   └── schemas.py             # Pydantic request/response models
├── app.py                     # Entry point
├── docker-compose.yaml        # PostgreSQL service
├── requirements.txt
└── .env.example
```

## Prerequisites

- Python 3.11+
- Docker (for PostgreSQL)
- OpenAI API key

## Setup

**1. Clone and enter the directory**

```bash
cd chatbot
```

**2. Create and activate a conda environment**

```bash
conda create -n langgraph python=3.11
conda activate langgraph
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=langgraph
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

**5. Start PostgreSQL**

```bash
docker compose up -d
```

**6. Run the server**

```bash
python app.py
```

Server starts at `http://localhost:8000`.

## API Reference

Interactive docs available at `http://localhost:8000/docs`.

### Chat

```
POST /api/v1/users/{user_id}/sessions/{session_id}/chat
```

**Body:**
```json
{
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "I'm doing well! How can I help you?",
  "session_id": "session_001"
}
```

### Get History

```
GET /api/v1/users/{user_id}/sessions/{session_id}/history
```

**Response:**
```json
{
  "user_id": "aman",
  "session_id": "session_001",
  "messages": [
    { "role": "human", "content": "Hello" },
    { "role": "ai", "content": "Hi! How can I help you?" }
  ]
}
```

### Clear Session

```
DELETE /api/v1/users/{user_id}/sessions/{session_id}
```

**Response:**
```json
{
  "detail": "Session session_001 for user aman cleared"
}
```
