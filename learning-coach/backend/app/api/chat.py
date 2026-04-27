from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.mcp.orchestrator import orchestrator
from app.mcp.tool6_vector_memory import vector_memory

router = APIRouter()

class ChatMessage(BaseModel):
    user_id: str
    message: str
    mode: str = "tutor"
    current_topic: Optional[str] = None

@router.post("/chat")
async def chat(req: ChatMessage):
    topic = req.current_topic or "Machine Learning"
    return await orchestrator.chat(req.user_id, req.message, topic, req.mode)

@router.get("/chat/history/{user_id}")
async def get_history(user_id: str):
    history = vector_memory.get_chat_history(user_id, limit=50)
    return {"history": [
        {"role": h["metadata"]["role"], "content": h["content"], "timestamp": h["timestamp"]}
        for h in history
    ]}
