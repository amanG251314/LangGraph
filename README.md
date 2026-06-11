# LangGraph Learning

A hands-on repository for learning LangGraph concepts and best practices, from fundamentals to production-ready applications.

## Structure

```
LangGraph/
├── basics/                        # Core LangGraph concepts (notebooks)
│   ├── basic-01.ipynb             # Graphs, nodes, edges
│   ├── basic-02.ipynb             # State management
│   ├── basic-conditional-routing.ipynb   # Conditional edges & routing
│   ├── basic-tool-calling.ipynb   # Tool use with LLM
│   ├── basic-tool-calling-2.ipynb # Advanced tool calling
│   └── Memory/
│       ├── basic-memory.ipynb     # Conversation memory basics
│       └── basic-memory-2.ipynb   # Memory with checkpointers
│
└── chatbot/                       # Production-ready chatbot app
    └── README.md                  # Setup & API docs
```

## Concepts Covered

| Topic | Location |
|-------|----------|
| Graphs, nodes, edges | `basics/basic-01.ipynb` |
| State management | `basics/basic-02.ipynb` |
| Conditional routing | `basics/basic-conditional-routing.ipynb` |
| Tool calling | `basics/basic-tool-calling.ipynb` |
| Memory & checkpointing | `basics/Memory/` |
| Full app with FastAPI + PostgreSQL | `chatbot/` |

## Getting Started

```bash
pip install langgraph
jupyter notebook
```

Open any notebook under `basics/` to start learning, or head to [`chatbot/`](chatbot/README.md) to run the full application.
