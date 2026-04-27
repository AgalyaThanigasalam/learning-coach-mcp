"""
MCP Orchestrator — ALL logic flows through here.
No direct LLM calls from API routes.
No direct dataset calls from API routes.
Every user action goes through this pipeline.
"""
from typing import Dict, Optional
from app.mcp.tool1_knowledge_graph import knowledge_graph
from app.mcp.tool2_learner_profiling import learner_profiler
from app.mcp.tool3_adaptive_difficulty import adaptive_difficulty
from app.mcp.tool4_question_generator import question_generator
from app.mcp.tool5_explanation_generator import explanation_generator
from app.mcp.tool6_vector_memory import vector_memory
from app.mcp.tool7_progress_analytics import progress_analytics

class MCPOrchestrator:
    """
    Central orchestrator. All 7 MCP tools are coordinated here.
    Pipeline: Profile → Difficulty → Generate → Store → Analytics
    """

    async def get_next_question(self, user_id: str, topic: str) -> Dict:
        # 1. Update learner profile with current topic
        learner_profiler.set_current_topic(user_id, topic)
        # 2. Adaptive difficulty decides level
        diff_info = adaptive_difficulty.get_difficulty_for_topic(user_id, topic)
        # 3. Question generator (LLM first, dataset fallback)
        question = await question_generator.generate(topic, diff_info["level"], user_id)
        # 4. Knowledge graph suggests next topics
        profile = learner_profiler.get_profile(user_id)
        next_topics = knowledge_graph.get_next_topics(profile.get("completed_topics", []))
        # 5. Store in vector memory
        vector_memory.store(user_id, f"Question served: {question['question']}", {"type": "question_served", "topic": topic})
        return {
            "question": question,
            "difficulty_info": diff_info,
            "next_topics": next_topics[:3],
            "user_level": profile.get("level", 1),
            "user_xp": profile.get("xp", 0),
        }

    async def process_answer(self, user_id: str, topic: str, question: str,
                              user_answer: str, correct_answer: str,
                              difficulty: int, response_time: float) -> Dict:
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        # 1. Update learner profile
        profile = learner_profiler.update_performance(user_id, topic, is_correct, response_time, difficulty)
        # 2. Adaptive difficulty recalculates
        next_diff = adaptive_difficulty.get_next_difficulty(user_id, topic)
        # 3. Explanation generator (LLM) if wrong
        explanation = None
        if not is_correct:
            explanation = await explanation_generator.explain(
                question, "intermediate", user_answer, correct_answer
            )
        # 4. Vector memory stores result
        vector_memory.store_question_result(user_id, question, user_answer, is_correct, topic)
        # 5. Progress analytics update
        analytics = progress_analytics.get_full_analytics(user_id)
        # 6. Knowledge graph — mark topic progress
        if analytics["overall_mastery"] > 70 and topic not in profile.get("completed_topics", []):
            learner_profiler.complete_topic(user_id, topic)
        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "next_difficulty": {"level": next_diff, "label": adaptive_difficulty.get_difficulty_label(next_diff)},
            "streak": profile.get("streak", 0),
            "xp_gained": difficulty * 10 if is_correct else 0,
            "total_xp": profile.get("xp", 0),
            "mastery": analytics["overall_mastery"],
            "weak_topics": profile.get("weak_topics", []),
        }

    async def chat(self, user_id: str, message: str, topic: str, mode: str) -> Dict:
        # 1. Get learner context
        profile = learner_profiler.get_profile(user_id)
        weak = profile.get("weak_topics", [])
        context = vector_memory.get_context_summary(user_id)
        # 2. Store user message
        vector_memory.store_chat(user_id, "user", message, topic)
        # 3. Route through MCP tools based on intent
        actions = []
        response_text = None
        msg = message.lower()

        if any(k in msg for k in ["question", "quiz", "practice", "test me", "give me"]):
            result = await self.get_next_question(user_id, topic)
            actions.append({"type": "question", "data": result["question"]})
            response_text = f"Here's a {result['difficulty_info']['label']} question on **{topic}**!"

        elif any(k in msg for k in ["explain", "why", "how", "what is", "help", "simple", "basics", "teach", "correct answer", "wrong"]):
            level = "beginner" if any(k in msg for k in ["simple", "basics", "easy", "beginner"]) else "intermediate"
            # Pass the full message as the concept so LLM gets full context
            exp = await explanation_generator.explain(message, level)
            actions.append({"type": "explanation", "data": exp})
            response_text = exp

        elif any(k in msg for k in ["weak", "improve", "revise", "revision"]):
            if weak:
                result = await self.get_next_question(user_id, weak[0])
                actions.append({"type": "question", "data": result["question"]})
                response_text = f"Let's work on your weak area: **{weak[0]}**. Here's a question!"
            else:
                response_text = "You're doing great — no weak topics detected yet! Keep going."

        if not response_text:
            response_text = await explanation_generator.chat_response(message, topic, weak, context)

        # 4. Store assistant response
        vector_memory.store_chat(user_id, "assistant", response_text, topic)
        history = vector_memory.get_chat_history(user_id, limit=12)
        return {
            "response": response_text,
            "actions": actions,
            "mode": mode,
            "topic": topic,
            "chat_history": [{"role": h["metadata"]["role"], "content": h["content"]} for h in history],
        }

    def get_analytics(self, user_id: str) -> Dict:
        analytics = progress_analytics.get_full_analytics(user_id)
        profile = learner_profiler.get_profile(user_id)
        path = knowledge_graph.get_learning_path(
            profile.get("current_topic", "Machine Learning"),
            profile.get("completed_topics", [])
        )
        analytics["learning_path"] = path
        analytics["next_topics"] = knowledge_graph.get_next_topics(profile.get("completed_topics", []))
        return analytics

orchestrator = MCPOrchestrator()
