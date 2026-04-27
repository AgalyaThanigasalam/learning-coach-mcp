"""
MCP Tool 2: Learner Profiling Agent
Tracks user performance, accuracy, response time, and maintains user state.
"""
from typing import Dict, List, Optional
from datetime import datetime
import json, os

_profiles: Dict[str, dict] = {}

DEFAULT_PROFILE = {
    "user_id": "",
    "name": "Learner",
    "current_topic": "Computer Science",
    "current_difficulty": 2,
    "completed_topics": [],
    "weak_topics": [],
    "strong_topics": [],
    "topic_stats": {},
    "total_questions": 0,
    "total_correct": 0,
    "streak": 0,
    "last_active": None,
    "session_start": None,
    "xp": 0,
    "level": 1,
}

class LearnerProfilingAgent:
    def get_profile(self, user_id: str) -> dict:
        if user_id not in _profiles:
            profile = DEFAULT_PROFILE.copy()
            profile["user_id"] = user_id
            profile["session_start"] = datetime.utcnow().isoformat()
            _profiles[user_id] = profile
        return _profiles[user_id]

    def update_performance(self, user_id: str, topic: str, is_correct: bool, response_time: float, difficulty: int) -> dict:
        profile = self.get_profile(user_id)
        if topic not in profile["topic_stats"]:
            profile["topic_stats"][topic] = {"attempts": 0, "correct": 0, "avg_time": 0.0, "difficulty_history": []}
        stats = profile["topic_stats"][topic]
        stats["attempts"] += 1
        if is_correct:
            stats["correct"] += 1
        stats["avg_time"] = (stats["avg_time"] * (stats["attempts"] - 1) + response_time) / stats["attempts"]
        stats["difficulty_history"].append(difficulty)
        profile["total_questions"] += 1
        if is_correct:
            profile["total_correct"] += 1
            profile["streak"] += 1
            profile["xp"] += difficulty * 10
        else:
            profile["streak"] = 0
        profile["last_active"] = datetime.utcnow().isoformat()
        profile["level"] = max(1, profile["xp"] // 100 + 1)
        self._update_weak_strong(profile, topic)
        _profiles[user_id] = profile
        return profile

    def _update_weak_strong(self, profile: dict, topic: str):
        stats = profile["topic_stats"].get(topic, {})
        if stats.get("attempts", 0) < 2:
            return
        accuracy = stats["correct"] / stats["attempts"]
        if accuracy < 0.5 and topic not in profile["weak_topics"]:
            profile["weak_topics"].append(topic)
            if topic in profile["strong_topics"]:
                profile["strong_topics"].remove(topic)
        elif accuracy >= 0.8 and topic not in profile["strong_topics"]:
            profile["strong_topics"].append(topic)
            if topic in profile["weak_topics"]:
                profile["weak_topics"].remove(topic)

    def get_weak_topics(self, user_id: str) -> List[str]:
        return self.get_profile(user_id).get("weak_topics", [])

    def set_current_topic(self, user_id: str, topic: str):
        profile = self.get_profile(user_id)
        profile["current_topic"] = topic
        _profiles[user_id] = profile

    def complete_topic(self, user_id: str, topic: str):
        profile = self.get_profile(user_id)
        if topic not in profile["completed_topics"]:
            profile["completed_topics"].append(topic)
        _profiles[user_id] = profile

    def get_accuracy(self, user_id: str, topic: Optional[str] = None) -> float:
        profile = self.get_profile(user_id)
        if topic:
            stats = profile["topic_stats"].get(topic, {})
            if stats.get("attempts", 0) == 0:
                return 0.0
            return stats["correct"] / stats["attempts"]
        if profile["total_questions"] == 0:
            return 0.0
        return profile["total_correct"] / profile["total_questions"]

learner_profiler = LearnerProfilingAgent()
