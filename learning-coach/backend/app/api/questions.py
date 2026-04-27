from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.mcp.orchestrator import orchestrator
from app.mcp.tool1_knowledge_graph import knowledge_graph

router = APIRouter()

class QuestionRequest(BaseModel):
    user_id: str
    topic: str
    difficulty: Optional[int] = None

@router.post("/generate-question")
async def generate_question(req: QuestionRequest):
    return await orchestrator.get_next_question(req.user_id, req.topic)

@router.get("/topics")
async def get_topics():
    return {"topics": knowledge_graph.get_all_topics()}

@router.get("/topic/{topic}")
async def get_topic_info(topic: str):
    return knowledge_graph.get_topic_info(topic) or {"error": "Topic not found"}
