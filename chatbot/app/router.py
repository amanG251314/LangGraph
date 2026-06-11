from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

_chat_service: ChatService | None = None


def init_router(chat_service: ChatService):
    global _chat_service
    _chat_service = chat_service


def get_service() -> ChatService:
    if _chat_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return _chat_service


@router.post("/users/{user_id}/sessions/{session_id}/chat", response_model=ChatResponse)
def chat(user_id: str, session_id: str, request: ChatRequest):
    service = get_service()
    response = service.chat(
        user_id=user_id,
        session_id=session_id,
        message=request.message,
    )
    return ChatResponse(response=response, session_id=session_id)


@router.get("/users/{user_id}/sessions/{session_id}/history")
def get_history(user_id: str, session_id: str):
    service = get_service()
    history = service.get_history(session_id)
    messages = history.get("messages", [])
    return {
        "user_id": user_id,
        "session_id": session_id,
        "messages": [
            {"role": m.type, "content": m.content}
            for m in messages
        ],
    }


@router.delete("/users/{user_id}/sessions/{session_id}")
def clear_session(user_id: str, session_id: str):
    service = get_service()
    service.clear_thread(session_id)
    return {"detail": f"Session {session_id} for user {user_id} cleared"}
