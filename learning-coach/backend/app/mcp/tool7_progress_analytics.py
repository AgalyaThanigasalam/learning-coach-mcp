"""
MCP Tool 7: Progress Analytics Engine
Computes mastery %, engagement score, topic completion, and performance insights.
"""
from typing import Dict, List
from datetime import datetime, timedelta
from app.mcp.tool2_learner_profiling import learner_profiler

class ProgressAnalyticsEngine:
    def get_full_analytics(self, user_id: str) -> Dict:
        profile = learner_profiler.get_profile(user_id)
        return {
            "user_id": user_id,
            "overall_mastery": self.compute_mastery(user_id),
            "engagement_score": self.compute_engagement(user_id),
            "topic_completion": self.get_topic_completion(user_id),
            "topic_performance": self.get_topic_performance(user_id),
            "streak": profile.get("streak", 0),
            "xp": profile.get("xp", 0),
            "level": profile.get("level", 1),
            "total_questions": profile.get("total_questions", 0),
            "total_correct": profile.get("total_correct", 0),
            "weak_topics": profile.get("weak_topics", []),
            "strong_topics": profile.get("strong_topics", []),
            "history_timeline": self.get_history_timeline(user_id),
            "recommendations": self.get_recommendations(user_id),
        }

    def compute_mastery(self, user_id: str) -> float:
        profile = learner_profiler.get_profile(user_id)
        total = profile.get("total_questions", 0)
        correct = profile.get("total_correct", 0)
        if total == 0:
            return 0.0
        base = (correct / total) * 100
        topic_stats = profile.get("topic_stats", {})
        if not topic_stats:
            return round(base, 1)
        topic_mastery = []
        for topic, stats in topic_stats.items():
            if stats["attempts"] > 0:
                topic_mastery.append(stats["correct"] / stats["attempts"])
        avg_topic = (sum(topic_mastery) / len(topic_mastery) * 100) if topic_mastery else base
        return round((base + avg_topic) / 2, 1)

    def compute_engagement(self, user_id: str) -> float:
        profile = learner_profiler.get_profile(user_id)
        score = 0.0
        total = profile.get("total_questions", 0)
        score += min(total * 2, 40)
        streak = profile.get("streak", 0)
        score += min(streak * 5, 30)
        topics_studied = len(profile.get("topic_stats", {}))
        score += min(topics_studied * 5, 30)
        return round(min(score, 100), 1)

    def get_topic_completion(self, user_id: str) -> Dict:
        profile = learner_profiler.get_profile(user_id)
        completed = profile.get("completed_topics", [])
        studied = list(profile.get("topic_stats", {}).keys())
        return {
            "completed": completed,
            "in_progress": [t for t in studied if t not in completed],
            "completion_rate": round(len(completed) / max(len(studied), 1) * 100, 1),
        }

    def get_topic_performance(self, user_id: str) -> List[Dict]:
        profile = learner_profiler.get_profile(user_id)
        result = []
        for topic, stats in profile.get("topic_stats", {}).items():
            accuracy = round(stats["correct"] / max(stats["attempts"], 1) * 100, 1)
            result.append({
                "topic": topic,
                "attempts": stats["attempts"],
                "correct": stats["correct"],
                "accuracy": accuracy,
                "avg_time": round(stats.get("avg_time", 0), 2),
                "status": "strong" if accuracy >= 80 else ("weak" if accuracy < 50 else "average"),
            })
        return sorted(result, key=lambda x: x["accuracy"], reverse=True)

    def get_history_timeline(self, user_id: str) -> List[Dict]:
        profile = learner_profiler.get_profile(user_id)
        timeline = []
        for topic, stats in profile.get("topic_stats", {}).items():
            timeline.append({"topic": topic, "attempts": stats["attempts"], "accuracy": round(stats["correct"] / max(stats["attempts"], 1) * 100, 1)})
        return timeline

    def get_recommendations(self, user_id: str) -> List[str]:
        profile = learner_profiler.get_profile(user_id)
        recs = []
        weak = profile.get("weak_topics", [])
        if weak:
            recs.append(f"Focus on weak topics: {', '.join(weak[:3])}")
        if profile.get("streak", 0) == 0:
            recs.append("Start a learning streak — answer at least one question daily!")
        if profile.get("total_questions", 0) < 10:
            recs.append("Complete more questions to unlock personalized insights.")
        if not recs:
            recs.append("Great progress! Try advancing to harder difficulty levels.")
        return recs

progress_analytics = ProgressAnalyticsEngine()
