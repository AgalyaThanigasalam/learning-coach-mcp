"""
MCP Tool 3: Adaptive Difficulty Engine
Dynamically adjusts question difficulty based on user performance.
"""
from typing import Dict
from app.mcp.tool2_learner_profiling import learner_profiler

DIFFICULTY_LABELS = {1: "Beginner", 2: "Easy", 3: "Intermediate", 4: "Hard", 5: "Advanced", 6: "Expert"}
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 6

class AdaptiveDifficultyEngine:
    def __init__(self):
        self.window_size = 5  # look at last N answers
        self.increase_threshold = 0.8  # 80% correct → increase
        self.decrease_threshold = 0.4  # below 40% → decrease

    def get_next_difficulty(self, user_id: str, topic: str) -> int:
        profile = learner_profiler.get_profile(user_id)
        current_difficulty = profile.get("current_difficulty", 2)
        stats = profile.get("topic_stats", {}).get(topic, {})
        attempts = stats.get("attempts", 0)
        if attempts < 2:
            return current_difficulty
        correct = stats.get("correct", 0)
        recent_accuracy = correct / attempts
        history = stats.get("difficulty_history", [])[-self.window_size:]
        avg_difficulty = sum(history) / len(history) if history else current_difficulty
        if recent_accuracy >= self.increase_threshold:
            new_difficulty = min(int(avg_difficulty) + 1, MAX_DIFFICULTY)
        elif recent_accuracy <= self.decrease_threshold:
            new_difficulty = max(int(avg_difficulty) - 1, MIN_DIFFICULTY)
        else:
            new_difficulty = int(avg_difficulty)
        profile["current_difficulty"] = new_difficulty
        return new_difficulty

    def get_difficulty_label(self, level: int) -> str:
        return DIFFICULTY_LABELS.get(level, "Intermediate")

    def get_difficulty_for_topic(self, user_id: str, topic: str) -> Dict:
        level = self.get_next_difficulty(user_id, topic)
        return {"level": level, "label": self.get_difficulty_label(level), "topic": topic}

    def reset_difficulty(self, user_id: str):
        profile = learner_profiler.get_profile(user_id)
        profile["current_difficulty"] = 2

adaptive_difficulty = AdaptiveDifficultyEngine()
