from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.mcp.leaderboard import get_leaderboard, compute_score, register_user

router = APIRouter()

class RegisterRequest(BaseModel):
    user_id: str
    username: Optional[str] = None

@router.get("/leaderboard")
async def leaderboard(limit: int = 20):
    return {"leaderboard": get_leaderboard(limit), "total_users": limit}

@router.get("/leaderboard/user/{user_id}")
async def user_rank(user_id: str):
    board = get_leaderboard(100)
    user_entry = next((e for e in board if e["user_id"] == user_id), None)
    if not user_entry:
        score = compute_score(user_id)
        score["rank"] = len(board) + 1
        score["rank_badge"] = f"#{score['rank']}"
        return score
    return user_entry

@router.post("/leaderboard/register")
async def register(req: RegisterRequest):
    register_user(req.user_id, req.username)
    return {"message": "Registered", "user_id": req.user_id, "username": req.username}
