from fastapi import APIRouter
from pydantic import BaseModel
from app.mcp.orchestrator import orchestrator
from app.mcp.tool5_explanation_generator import explanation_generator

router = APIRouter()

class AnswerRequest(BaseModel):
    user_id: str
    topic: str
    question: str
    user_answer: str
    correct_answer: str
    difficulty: int = 2
    response_time: float = 10.0

@router.post("/submit-answer")
async def submit_answer(req: AnswerRequest):
    return await orchestrator.process_answer(
        req.user_id, req.topic, req.question,
        req.user_answer, req.correct_answer,
        req.difficulty, req.response_time
    )

@router.get("/explanation")
async def get_explanation(topic: str, level: str = "intermediate"):
    exp = await explanation_generator.explain(topic, level)
    return {"topic": topic, "level": level, "explanation": exp}
