"""
Leaderboard Module — MCP-based scoring using existing tools.
Score = 0.4*Mastery + 0.3*Accuracy + 0.2*Streak + 0.1*AvgDifficulty
"""
from typing import List, Dict
from app.mcp.tool2_learner_profiling import learner_profiler
from app.mcp.tool7_progress_analytics import progress_analytics

# In-memory leaderboard store: user_id -> {username, stats}
_leaderboard: Dict[str, Dict] = {}

BADGES = [
    (90, "🏆 Legend"),
    (75, "⭐ Expert"),
    (55, "🔥 Advanced"),
    (35, "📈 Intermediate"),
    (0,  "🌱 Beginner"),
]

def get_badge(score: float) -> str:
    for threshold, badge in BADGES:
        if score >= threshold:
            return badge
    return "🌱 Beginner"

def register_user(user_id: str, username: str = None):
    if user_id not in _leaderboard:
        _leaderboard[user_id] = {"username": username or f"Learner_{user_id[-4:]}"}

def compute_score(user_id: str) -> Dict:
    profile = learner_profiler.get_profile(user_id)
    analytics = progress_analytics.get_full_analytics(user_id)

    mastery = analytics.get("overall_mastery", 0)
    accuracy = (profile.get("total_correct", 0) / max(profile.get("total_questions", 1), 1)) * 100
    streak = min(profile.get("streak", 0), 30)  # cap at 30 for scoring
    streak_score = (streak / 30) * 100

    # Average difficulty from topic stats
    topic_stats = profile.get("topic_stats", {})
    if topic_stats:
        all_diffs = []
        for stats in topic_stats.values():
            all_diffs.extend(stats.get("difficulty_history", []))
        avg_diff = (sum(all_diffs) / len(all_diffs) * 20) if all_diffs else 20  # scale to 0-100
    else:
        avg_diff = 20

    final_score = round(
        0.4 * mastery +
        0.3 * accuracy +
        0.2 * streak_score +
        0.1 * avg_diff,
        1
    )

    username = _leaderboard.get(user_id, {}).get("username", f"Learner_{user_id[-4:]}")
    return {
        "user_id": user_id,
        "username": username,
        "score": final_score,
        "mastery": round(mastery, 1),
        "accuracy": round(accuracy, 1),
        "streak": profile.get("streak", 0),
        "total_questions": profile.get("total_questions", 0),
        "level": profile.get("level", 1),
        "badge": get_badge(final_score),
        "xp": profile.get("xp", 0),
    }

def get_leaderboard(limit: int = 20) -> List[Dict]:
    # Include all known users from profiler + leaderboard store
    from app.mcp.tool2_learner_profiling import _profiles
    all_users = set(list(_profiles.keys()) + list(_leaderboard.keys()))

    entries = []
    for uid in all_users:
        try:
            entry = compute_score(uid)
            if entry["total_questions"] > 0:  # only show active users
                entries.append(entry)
        except Exception:
            continue

    entries.sort(key=lambda x: x["score"], reverse=True)
    for i, entry in enumerate(entries[:limit]):
        entry["rank"] = i + 1
        if i == 0:
            entry["rank_badge"] = "🥇"
        elif i == 1:
            entry["rank_badge"] = "🥈"
        elif i == 2:
            entry["rank_badge"] = "🥉"
        else:
            entry["rank_badge"] = f"#{i+1}"
    return entries[:limit]
