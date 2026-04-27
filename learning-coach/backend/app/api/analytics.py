from fastapi import APIRouter
from app.mcp.orchestrator import orchestrator

router = APIRouter()

@router.get("/analytics/{user_id}")
async def get_analytics(user_id: str):
    return orchestrator.get_analytics(user_id)
