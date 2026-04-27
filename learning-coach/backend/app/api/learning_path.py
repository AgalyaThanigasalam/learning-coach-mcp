from fastapi import APIRouter
from pydantic import BaseModel
from app.mcp.tool1_knowledge_graph import knowledge_graph
from app.mcp.tool2_learner_profiling import learner_profiler

router = APIRouter()

class PathRequest(BaseModel):
    user_id: str
    target_topic: str

@router.post("/learning-path")
async def get_path(req: PathRequest):
    profile = learner_profiler.get_profile(req.user_id)
    known = profile.get("completed_topics", [])
    return {
        "target_topic": req.target_topic,
        "learning_path": knowledge_graph.get_learning_path(req.target_topic, known),
        "next_recommended": knowledge_graph.get_next_topics(known),
        "topic_info": knowledge_graph.get_topic_info(req.target_topic),
    }

@router.get("/learning-path/{user_id}")
async def get_user_path(user_id: str):
    profile = learner_profiler.get_profile(user_id)
    known = profile.get("completed_topics", [])
    current = profile.get("current_topic", "Machine Learning")
    return {
        "current_topic": current,
        "learning_path": knowledge_graph.get_learning_path(current, known),
        "next_recommended": knowledge_graph.get_next_topics(known),
        "all_topics": knowledge_graph.get_all_topics(),
    }
