from fastapi import APIRouter
from app.mcp.orchestrator import orchestrator
from app.mcp.tool2_learner_profiling import learner_profiler

router = APIRouter()

@router.get("/progress/{user_id}")
async def get_progress(user_id: str):
    return orchestrator.get_analytics(user_id)

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    return learner_profiler.get_profile(user_id)
