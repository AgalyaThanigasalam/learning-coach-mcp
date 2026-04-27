"""
Revision Mode API — MCP flow:
Learner Profiling → Identify weak topics → Question Generator → Return targeted questions
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.mcp.tool2_learner_profiling import learner_profiler
from app.mcp.tool3_adaptive_difficulty import adaptive_difficulty
from app.mcp.tool4_question_generator import question_generator

router = APIRouter()

class RevisionRequest(BaseModel):
    user_id: str
    num_questions: int = 5

@router.post("/revision-mode")
async def revision_mode(req: RevisionRequest):
    # Step 1: Learner Profiling — get weak topics
    profile = learner_profiler.get_profile(req.user_id)
    weak_topics = profile.get("weak_topics", [])

    # If no weak topics yet, use current topic at easy difficulty
    if not weak_topics:
        current = profile.get("current_topic", "Machine Learning")
        weak_topics = [current]
        message = f"No weak areas detected yet. Practicing {current} to build your baseline."
    else:
        message = f"Focusing on your {len(weak_topics)} weak area(s): {', '.join(weak_topics[:3])}"

    # Step 2: Generate questions from weak topics
    questions = []
    for i in range(req.num_questions):
        topic = weak_topics[i % len(weak_topics)]
        # Use easy-medium difficulty for revision
        diff_info = adaptive_difficulty.get_difficulty_for_topic(req.user_id, topic)
        revision_diff = max(1, diff_info["level"] - 1)  # one level easier for revision
        q = await question_generator.generate(topic, revision_diff, req.user_id)
        questions.append({**q, "revision_topic": topic})

    return {
        "message": message,
        "weak_topics": weak_topics,
        "questions": questions,
        "mode": "revision",
        "total": len(questions),
    }

@router.get("/revision-mode/{user_id}")
async def get_revision_question(user_id: str):
    """Get a single revision question for the user's weakest topic."""
    profile = learner_profiler.get_profile(user_id)
    weak_topics = profile.get("weak_topics", [])
    topic = weak_topics[0] if weak_topics else profile.get("current_topic", "Machine Learning")
    diff_info = adaptive_difficulty.get_difficulty_for_topic(user_id, topic)
    revision_diff = max(1, diff_info["level"] - 1)
    q = await question_generator.generate(topic, revision_diff, user_id)
    return {
        "question": q,
        "revision_topic": topic,
        "weak_topics": weak_topics,
        "difficulty_info": {"level": revision_diff, "label": adaptive_difficulty.get_difficulty_label(revision_diff)},
    }
