from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.checkpoint import (
    CheckpointManager
)

from app.graph.builder import (
    GraphBuilder
)

from app.services.chat_service import (
    ChatService
)

from app.router import router, init_router


def create_chat_service() -> ChatService:

    checkpointer = (
        CheckpointManager.initialize()
    )

    graph = GraphBuilder.build(
        checkpointer
    )

    return ChatService(graph)


@asynccontextmanager
async def lifespan(app: FastAPI):
    chat_service = create_chat_service()
    init_router(chat_service)
    yield


def create_app() -> FastAPI:

    app = FastAPI(
        title="LangGraph Chatbot",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )